# Research website

The repository is the source of truth. The viewer reads README.md by default, indexes tracked research files, resolves relative links, opens notebooks in Colab, and displays CSV files with search, sorting and pagination.

## GitHub Pages setup (one time)

1. Open Settings → Pages in this repository.
2. Under Build and deployment, select GitHub Actions as Source.
3. Open Actions → Research website → Run workflow (main).

Every subsequent push to main builds and deploys the site automatically. No manual index editing is needed. Existing research files are not changed by the build.

The Pages artifact includes only recognized research formats, excluding hidden paths and website internals. Notebooks, archives and binary data are linked to GitHub/Colab rather than duplicated. Files over 25 MiB are fetched from the source repository when viewed. The repository is public; do not commit secrets or confidential files. Add exclusions in website/build.py if needed.

Local preview: run `python3 website/build.py` from a committed checkout, then `python3 -m http.server 8000 --directory _site`. The root page also supports GitHub API fallback for a branch-based deployment; it requires GitHub API availability and is subject to rate limits.
