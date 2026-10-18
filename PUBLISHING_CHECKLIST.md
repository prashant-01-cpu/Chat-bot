# Before making this GitHub repository public

1. Revoke the old Groq API key that was embedded in `main.py` and create a new key in the Groq Console. Never reuse the old one.
2. Replace your local `main.py`, add `.gitignore`, `.env.example`, `requirements.txt`, and `README.md` from this package. Keep your existing `templates/` and `static/` directories.
3. Run `cp .env.example .env` in the repository, add the **new** API key, and generate your own unique `FLASK_SECRET_KEY`.
4. Confirm `.env` is untracked: `git check-ignore -v .env`. If it was previously tracked, run `git rm --cached .env` (does not delete the local file).
5. Confirm no key remains in the files you intend to commit. Example: `git grep -n -E 'gsk_[A-Za-z0-9]+' -- ':!*.md'` (review output locally and do not paste secrets into issues or chat).
6. Check **Git history**, not only current files. If any real secret was committed, GitHub's official guide explains how to rewrite the affected history with `git-filter-repo`. History rewrites affect collaborators and forks. Rotating the exposed key is essential even after a rewrite.
7. Test locally and verify chat behavior before pushing. Commit only the files that you intend to publish; inspect `git status` and `git diff --cached`.
8. Use GitHub Settings > General > Danger Zone > Change repository visibility only after the secret and history checks are complete.
9. Before hosting the app online, add rate limits and usage protections, a production WSGI server, HTTPS secure session cookies, and an appropriate session store.

Official GitHub guidance: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
