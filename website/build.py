"""Build a static research viewer without editing research files."""
from pathlib import Path
import json
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_site"
LOCAL = set("md csv png jpg jpeg gif webp svg pdf py json jsonl txt log tsv".split())
ALLOWED = LOCAL | set("ipynb zip npz npy parquet xlsx pptx docx".split())
MAX_LOCAL = 25 * 1024 * 1024

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for name in ("index.html", "website/style.css", "website/app.js"):
        dst = OUT / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, dst)
    (OUT / ".nojekyll").touch()
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip()
    files = []
    for name in sorted(filter(None, tracked)):
        rel = Path(name)
        if any(part.startswith(".") for part in rel.parts) or rel.parts[0] == "website":
            continue
        suffix = rel.suffix.lower().lstrip(".")
        src = ROOT / rel
        if suffix not in ALLOWED or not src.is_file() or src.is_symlink():
            continue
        size = src.stat().st_size
        local = suffix in LOCAL and size <= MAX_LOCAL
        if local:
            dst = OUT / "data" / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
        files.append({"path": name, "size": size, "local": local})
    (OUT / "manifest.json").write_text(json.dumps({"commit": commit, "files": files}, ensure_ascii=False), encoding="utf-8")
    print(f"Indexed {len(files)} files; copied {sum(f['local'] for f in files)} files.")

if __name__ == "__main__":
    main()
