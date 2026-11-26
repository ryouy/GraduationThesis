"""Build a static research viewer without editing research files."""
from pathlib import Path
import json
import re
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
    # Inline the first-party assets as one HTML response. This avoids a stale
    # stylesheet or script being paired with new markup by browser/CDN caches.
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "website/style.css").read_text(encoding="utf-8")
    js = (ROOT / "website/app.js").read_text(encoding="utf-8")
    css_tag = '<link rel="stylesheet" href="website/style.css">'
    js_tag = '<script defer src="website/app.js"></script>'
    assert html.count(css_tag) == 1 and html.count(js_tag) == 1
    assert "</style" not in css.lower() and "</script" not in js.lower()
    html = html.replace(css_tag, "<style>\n" + css + "\n</style>")
    html = html.replace(js_tag, "<script>\ndocument.addEventListener('DOMContentLoaded', () => {\n" + js + "\n});\n</script>")
    (OUT / "index.html").write_text(html, encoding="utf-8")
    # Keep these paths working for older HTML still in browser caches.
    for name in ("website/style.css", "website/app.js"):
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
            if suffix == "md":
                # GitHub-only content is not included in the published document.
                md = src.read_text(encoding="utf-8")
                md = re.sub(r"<!--\s*github-only:start\s*-->[\s\S]*?<!--\s*github-only:end\s*-->", "", md)
                if name == "README.md":
                    md = re.sub(r"^\s*\[Web ver\.\]\(https://ryouy\.github\.io/GraduationThesis/?\)[ \t]*(?:\r?\n|$)", "", md, flags=re.I | re.M)
                dst.write_text(md, encoding="utf-8")
            else:
                shutil.copyfile(src, dst)
        files.append({"path": name, "size": size, "local": local})
    (OUT / "manifest.json").write_text(json.dumps({"commit": commit, "files": files}, ensure_ascii=False), encoding="utf-8")
    print(f"Indexed {len(files)} files; copied {sum(f['local'] for f in files)} files.")

if __name__ == "__main__":
    main()
