"""Build release/tempa-config.zip: the config tree as a package to upload in Tempa.

Only what Tempa reads goes in (tenant.yaml and the asset folders). The zip is reproducible: the same files
give the same bytes, so CI can check that the committed release is up to date.

    python3 scripts/build_release.py                    # release/tempa-config.zip
    python3 scripts/build_release.py --tenant my-org    # with your tenant id, ready to publish
    python3 scripts/build_release.py --check            # fail when the committed zip is out of date
"""

import argparse
import io
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "release" / "tempa-config.zip"
CONFIG_FILES = ["tenant.yaml"]
CONFIG_DIRS = ["nodes", "standards", "skills", "commands", "agents", "mcp", "policies"]
SKIPPED_NAMES = {".DS_Store"}
FIXED_TIME = (1980, 1, 1, 0, 0, 0)
TENANT_ID = re.compile(r"^id: *[^ #\n]+", re.MULTILINE)
VALID_TENANT = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def config_files() -> list[Path]:
    files = [ROOT / name for name in CONFIG_FILES]
    for folder in CONFIG_DIRS:
        files += [p for p in (ROOT / folder).rglob("*") if p.is_file() and p.name not in SKIPPED_NAMES]
    return sorted(files, key=lambda p: p.relative_to(ROOT).as_posix())


def with_tenant(tenant_yaml: bytes, tenant: str) -> bytes:
    text, count = TENANT_ID.subn(f"id: {tenant}", tenant_yaml.decode("utf-8"), count=1)
    if count != 1:
        sys.exit("tenant.yaml has no top-level 'id:' line")
    return text.encode("utf-8")


def build(tenant: str | None) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in config_files():
            name = path.relative_to(ROOT).as_posix()
            data = path.read_bytes()
            if name == "tenant.yaml" and tenant:
                data = with_tenant(data, tenant)
            info = zipfile.ZipInfo(name, FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            mode = 0o755 if path.stat().st_mode & 0o100 else 0o644
            info.external_attr = (0o100000 | mode) << 16
            info.create_system = 3  # Unix, so the mode is read back
            archive.writestr(info, data)
    return buffer.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tenant", help="your Tempa tenant id, written into tenant.yaml in the zip")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="where to write the zip")
    parser.add_argument("--check", action="store_true", help="fail when the zip at --out is out of date")
    args = parser.parse_args()
    if args.tenant and not VALID_TENANT.match(args.tenant):
        sys.exit(f"not a tenant id: {args.tenant!r} (lowercase letters, digits and dashes)")

    data = build(args.tenant)
    if args.check:
        if not args.out.is_file() or args.out.read_bytes() != data:
            sys.exit(f"{args.out} is out of date: run python3 scripts/build_release.py")
        print(f"{args.out} is up to date")
        return
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(data)
    print(f"wrote {args.out} ({len(data)} bytes, {len(config_files())} files)")


if __name__ == "__main__":
    main()
