# sellwithsorrell.com

Website for Christian Sorrell, REALTOR® (RE/MAX Niagara Realty Ltd.). Vercel publishes the repository root automatically on every push to `main`.

```
(root)                     the published site (HTML, assets/, images/, sitemap.xml ...)
_build/source/build.py     page content and settings; run it to rebuild the site
_build/posts/              one .json file per blog post
_build/scripts/new_post.py writes a new post with the Claude API
.github/workflows/         weekly blog automation (Thursdays)
```
`_build`, `.github` and this README are excluded from the live site by `.vercelignore`.

## Weekly blog posts
Every Thursday, GitHub Actions asks Claude for a new SEO post on a topic not covered yet, checks it
(length, headings, internal links only, no scripts, no duplicate topic), rebuilds the site and pushes.
Vercel then publishes it.

**One-time setup:** create an API key at console.anthropic.com, then in this repo go to
Settings → Secrets and variables → Actions → New repository secret, name it `ANTHROPIC_API_KEY`.
Test it from Actions → *Weekly blog post* → **Run workflow**.

To remove a post: delete its file in `_build/posts/` and the matching `blog-….html`, then run
`python3 _build/source/build.py` and commit.
