"""Validate the distributed client without service access; optionally build a candidate."""

import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile

PACKAGE_FILES = (
    ".codex-plugin/README.md", ".codex-plugin/plugin.json", ".mcp.json",
    "CHANGELOG.md", "LICENSE-NOTICE.md", "README.md", "SECURITY.md",
    "assets/README.md", "assets/icon.png", "assets/icon.svg", "skills/README.md",
    "skills/prdb-actions/README.md", "skills/prdb-actions/SKILL.md",
    "skills/prdb-reading/README.md", "skills/prdb-reading/SKILL.md",
    "skills/prdb-reading/scripts/README.md",
    "skills/prdb-reading/scripts/selected_files.py",
    "skills/prdb-reading/scripts/upload_pdf.py",
    "skills/prdb-setup/README.md", "skills/prdb-setup/SKILL.md",
    "skills/prdb-setup/scripts/README.md", "skills/prdb-setup/scripts/onboard.py",
)
SCOPES = frozenset({
    "documents:read", "documents:upload", "resources:write", "reader:read",
    "annotations:write", "notes:read", "notes:write", "notes:delete",
    "reviews:draft", "reviews:publish", "library:read", "library:write",
    "community:read", "community:write", "notifications:read",
    "notifications:write", "profile:read", "profile:write", "requests:read",
    "requests:write", "documents:delete",
})


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_object(path):
    value = json.loads(path.read_text())
    require(isinstance(value, dict), f"Expected JSON object: {path.name}")
    return value


def validate(root):
    root = Path(root)
    package = root / "plugins/prdb"
    require(not package.is_symlink(), "Package directory must not be a symlink")
    require(package.is_dir(), "Missing plugins/prdb directory")
    found = set()
    for path in package.rglob("*"):
        require(not path.is_symlink(), "Package symlinks are forbidden")
        if path.is_file():
            found.add(path.relative_to(package).as_posix())
    require(found == set(PACKAGE_FILES), "Package files differ from the reviewed allowlist")
    manifest = load_object(package / ".codex-plugin/plugin.json")
    version = manifest.get("version", "")
    require(isinstance(version, str) and re.fullmatch(r"\d+\.\d+\.\d+", version), "Invalid package version")
    require(manifest.get("name") == "prdb", "Plugin identity must stay prdb")
    require(manifest.get("skills") == "./skills/", "Unexpected skills directory")
    require(manifest.get("mcpServers") == "./.mcp.json", "Unexpected MCP manifest path")
    interface = manifest.get("interface", {})
    require(isinstance(interface, dict) and interface.get("displayName") == "PRDB", "Invalid interface")
    for key in ("composerIcon", "logo"):
        require(interface.get(key) == "./assets/icon.png", "Unexpected plugin icon")
    mcp = load_object(package / ".mcp.json")
    servers = mcp.get("mcpServers")
    require(isinstance(servers, dict) and set(servers) == {"prdb-reading"}, "Unexpected MCP servers")
    server = servers["prdb-reading"]
    require(isinstance(server, dict) and set(server) == {"url", "scopes"}, "Unexpected MCP settings or embedded credentials")
    require(server["url"] == "https://prdb.ai/mcp", "Unexpected production MCP endpoint")
    scopes = server["scopes"]
    require(isinstance(scopes, list) and all(isinstance(x, str) for x in scopes), "Invalid scopes")
    require(len(scopes) == len(set(scopes)) and set(scopes) == SCOPES, "Scopes require a reviewed allowlist update")
    marketplace = load_object(root / ".agents/plugins/marketplace.json")
    require(marketplace.get("name") == "prdb", "Marketplace identity must stay prdb")
    entries = marketplace.get("plugins")
    require(isinstance(entries, list) and len(entries) == 1, "Expected one marketplace plugin")
    entry = entries[0]
    require(isinstance(entry, dict) and entry.get("name") == "prdb", "Invalid marketplace entry")
    require(entry.get("source") == {"source": "local", "path": "./plugins/prdb"}, "Unexpected marketplace source")
    require(entry.get("policy") == {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}, "Unexpected authentication policy")
    for name in PACKAGE_FILES:
        path = package / name
        if path.suffix == ".py":
            ast.parse(path.read_text(), filename=name)
        if name.endswith("SKILL.md"):
            text = path.read_text()
            require(text.startswith("---\n") and "\n---\n" in text[4:], f"Missing skill metadata: {name}")
    return version


def build_candidate(root, output, source_sha):
    root, output = Path(root), Path(output)
    version = validate(root)
    require(re.fullmatch(r"[0-9a-f]{40}", source_sha) is not None, "A full source commit SHA is required")
    package = (root / "plugins/prdb").resolve()
    destination = output.resolve()
    require(destination != package and package not in destination.parents, "Candidate output must be outside the payload")
    output.mkdir(parents=True, exist_ok=False)
    archive = output / f"prdb-{version}-codex.zip"
    files = {}
    with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as zf:
        for name in sorted(PACKAGE_FILES):
            data = (package / name).read_bytes()
            files[name] = hashlib.sha256(data).hexdigest()
            info = zipfile.ZipInfo("prdb/" + name, date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, data)
    record = {
        "kind": "unpublished-plugin-candidate", "version": version,
        "source_sha": source_sha, "archive": archive.name, "files": files,
    }
    manifest = output / "manifest.json"
    manifest.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    (output / "SHA256SUMS").write_text("".join(
        f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n"
        for p in (archive, manifest)
    ))
    return archive


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, help="New candidate output directory (never a Release)")
    args = parser.parse_args()
    version = validate(args.root)
    if args.output:
        sha = subprocess.check_output(["git", "-C", str(args.root), "rev-parse", "HEAD"], text=True).strip()
        build_candidate(args.root, args.output, sha)
    print(f"Validated PRDB {version}: {len(PACKAGE_FILES)} reviewed package files; no publication performed.")


if __name__ == "__main__":
    main()
