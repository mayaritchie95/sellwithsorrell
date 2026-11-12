# sellwithsorrell.com: static site

`site/` is the whole website. Upload its contents to the web host's root folder.
`source/` holds the generator. Edit `build.py`, then run `python3 source/build.py` to rebuild every page.

## Before launch
1. **myRealPage embeds**: search the pages for `myRealPage EMBED` and paste the matching embed code over each dashed box
   (home search, My Listings, Office Listings, List/Map IDX Search, Watch List, one predefined search per city page).
2. **Forms**: set `form_endpoint` in build.py (for example a Formspree form ID, or your host's form handler), then rebuild.
3. **Email and Google Maps link**: set `email` and `maps` in build.py, then rebuild.
4. **Review the draft copy**: the About bio, marketing strategy and privacy policy are drafts for Christian to approve.
5. **Redirects**: if any old myRealPage URLs differ from the new ones, add 301 redirects on the host.
6. **Google**: verify the domain in Search Console, submit `https://sellwithsorrell.com/sitemap.xml`,
   and link the site from his Google Business Profile.
