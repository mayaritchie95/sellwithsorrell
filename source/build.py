#!/usr/bin/env python3
"""Static site generator for sellwithsorrell.com.
Run:  python3 build.py   -> writes every page into ../sellwithsorrell/
Edit SITE below for contact details, then rebuild."""
import json, os, datetime, html

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')
HERE = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.date.today().isoformat()

SITE = {
    'domain': 'https://sellwithsorrell.com',
    'name': 'Christian Sorrell',
    'brokerage': 'RE/MAX Niagara Realty Ltd., Brokerage',
    'phone': '905-931-0583',
    'phone_intl': '+1-905-931-0583',
    'email': '',  # TODO: add Christian's email, e.g. 'christian@sellwithsorrell.com'
    'street': '261 Martindale Rd., Unit 14C',
    'city': 'St. Catharines', 'region': 'ON', 'postal': 'L2W 1A2', 'country': 'CA',
    'maps': '',  # TODO: Google Business Profile link
    'form_endpoint': 'https://formspree.io/f/YOUR_FORM_ID',  # TODO: form backend
    'social': {
        'Instagram': 'https://www.instagram.com/sellwithsorrell',
        'YouTube': 'https://www.youtube.com/@sellwithsorrell',
        'TikTok': 'https://www.tiktok.com/@sellwithsorrell',
        'LinkedIn': 'https://www.linkedin.com/in/christian-sorrell-00900523b',
    },
}
D = SITE['domain']

CITIES = [
    ('st-catharines', 'St. Catharines', 'staircase', [
        "St. Catharines is the largest city in the Niagara region and the place I call home base. Known as the Garden City, it blends established tree-lined neighbourhoods with a revitalized downtown, a lively arts scene anchored by the FirstOntario Performing Arts Centre, and easy access to the QEW and GO train service toward Toronto.",
        "Buyers here have real choice: lakeside living and historic charm in Port Dalhousie, character homes near downtown, family-friendly streets in the north end and Merritton, and a steady rental market driven by Brock University and Niagara's growing workforce. That variety is exactly why pricing a home correctly in St. Catharines takes local, street-level knowledge."],
        ['Port Dalhousie: waterfront, beaches and the Lakeside Park carousel', 'Downtown: lofts, condos and walkable restaurants and venues', 'North End and Grantham: established family neighbourhoods near the lake', 'Merritton: heritage homes and quick highway access', 'Near Brock University: popular with investors and student rentals']),
    ('niagara-falls', 'Niagara Falls', 'kitchen', [
        "Beyond the famous falls and the tourist core, Niagara Falls is a city of quiet residential neighbourhoods, newer subdivisions and good value compared with markets closer to Toronto. Many buyers are surprised by how much home their budget gets them here.",
        "Tourism supports a strong local economy and an active rental market, which makes Niagara Falls a frequent pick for investors, while families are drawn to areas like Chippawa and the newer communities on the city's south and west sides. QEW access keeps commutes across the region simple."],
        ['Chippawa: small-village feel along the Welland River', 'Newer south-end and west-end subdivisions for growing families', 'Established central neighbourhoods with affordable detached homes', 'Income properties near the tourist and hospitality corridor']),
    ('thorold', 'Thorold', 'living-green', [
        "Thorold sits right between St. Catharines and Welland with the Welland Canal running through its heart. It has a close-knit, small-city feel, a historic downtown and quick access to Brock University and Highway 406.",
        "New subdivisions have made Thorold one of Niagara's growth areas, giving buyers modern homes at prices that often undercut neighbouring cities. Its location near Brock also keeps rental demand steady, which appeals to investors."],
        ['Historic downtown along the canal', 'Newer family subdivisions with modern builds', 'Close to Brock University for rental investment', 'Watch the ships at the Lock 7 viewing area']),
    ('welland', 'Welland', 'card-buyers', [
        "Welland combines affordability with lifestyle. The old Welland Canal is now a recreational waterway used for paddling, rowing and waterfront trails, and the city is home to Niagara College's Welland campus.",
        "For first-time buyers and investors, Welland is often one of the best values in the region, with solid detached homes, a growing number of new builds and easy access to Highway 406 for commuting to St. Catharines and beyond."],
        ['Homes along the recreational waterway and trail network', 'Affordable starter homes and semi-detached options', 'Rental demand near Niagara College', 'New construction communities on the city\'s edges']),
    ('port-colborne', 'Port Colborne', 'card-sellers', [
        "Port Colborne sits on the north shore of Lake Erie at the southern end of the Welland Canal. Its sandy beaches, marina and relaxed pace make it a favourite for retirees, remote workers and anyone dreaming of lake life.",
        "Compared with many Ontario waterfront towns, Port Colborne still offers attainable prices, from in-town bungalows to lakeside cottages and year-round waterfront homes."],
        ['Lake Erie beaches and waterfront homes', 'Charming downtown along the canal near Lock 8', 'Cottage and recreational properties', 'Quiet, affordable in-town bungalows']),
    ('fort-erie', 'Fort Erie', 'card-search', [
        "Fort Erie sits on the Niagara River across from Buffalo, with the Peace Bridge making cross-border travel easy. It offers a mix of riverfront living, beach communities and small-town neighbourhoods.",
        "Crystal Beach's sandy shoreline and Ridgeway's village charm draw buyers looking for a relaxed lifestyle, while prices remain approachable compared with much of the Golden Horseshoe."],
        ['Crystal Beach: beach town with cottages and year-round homes', 'Ridgeway: village shops and community events', 'Riverfront homes along the Niagara Parkway', 'Easy access to the U.S. via the Peace Bridge']),
    ('pelham', 'Pelham', 'hero', [
        "Pelham, including the communities of Fonthill and Fenwick, is one of Niagara's most sought-after places to live. Rolling hills, orchards and the trails of Short Hills Provincial Park give it a countryside feel just minutes from St. Catharines and Welland.",
        "Pelham attracts families and move-up buyers who want larger lots, highly regarded schools and a strong sense of community. Homes here tend to hold their value well, so preparation and pricing strategy matter when you buy or sell."],
        ['Fonthill: boutique shops, dining and family neighbourhoods', 'Fenwick: small-village living surrounded by farmland', 'Estate homes and larger lots', 'Short Hills Provincial Park trails on your doorstep']),
    ('hamilton', 'Hamilton', 'living-green', [
        "Hamilton has become one of Ontario's most dynamic real estate markets. Known as the City of Waterfalls, it sits along the Niagara Escarpment with McMaster University, major hospitals, GO train service and a thriving arts and food scene.",
        "From character homes in the lower city to suburban communities on the Mountain and in Stoney Creek, Ancaster and Dundas, Hamilton offers options for first-time buyers, families and investors alike."],
        ['Lower city: character homes near Locke Street and James Street North', 'The Mountain: suburban family neighbourhoods', 'Stoney Creek: close to Niagara with lake and escarpment views', 'Ancaster and Dundas: upscale, established communities']),
    ('grimsby', 'Grimsby', 'kitchen', [
        "Grimsby sits between Lake Ontario and the Niagara Escarpment at the gateway to Niagara. Its location right on the QEW makes it a favourite for commuters heading toward Hamilton, Burlington and the GTA.",
        "Buyers love the lakefront condos, the colourful cottages of Grimsby Beach and established family neighbourhoods below and atop the escarpment."],
        ['Lakefront condos and townhomes', 'Historic Grimsby Beach cottages', 'Family neighbourhoods near downtown', 'Escarpment homes with views and trail access']),
    ('lincoln', 'Lincoln', 'card-buyers', [
        "The Town of Lincoln, home to Beamsville, Vineland and Jordan, is the heart of Niagara's wine country. Vineyards, the Twenty Valley and the Bruce Trail give it a relaxed, scenic lifestyle with quick QEW access.",
        "Lincoln suits buyers looking for small-town living, newer subdivisions in Beamsville, or country and rural properties among the vineyards. Ball's Falls and Jordan Village add to its appeal."],
        ['Beamsville: newer family subdivisions and amenities', 'Vineland: rural properties and wineries', 'Jordan Village: boutique shops and heritage charm', 'Country homes along the Niagara Escarpment']),
]

NAV = [
    ('Home', 'index.html', []),
    ('Properties', None, [('Featured Listings', 'mylistings.html'), ('Office Listings', 'office-listings.html'),
                          ('Search Listings', 'recip.html'), ('Map Search', 'map-search.html'), ('Watch List', 'watch-list.html')]),
    ('Buy', None, [('Buying Resources', 'buying.html'), ('Home Finder', 'home-finder.html'), ('Mortgage Calculator', 'mortgage-calculator.html')]),
    ('Sell', None, [('Selling Resources', 'selling.html'), ('Home Evaluation', 'home-evaluation.html'),
                    ('What Your Neighbour Sold For', 'neighbour-sold.html'), ('Marketing Strategy', 'marketing-strategy.html')]),
    ('Investing', 'investing.html', []),
    ('Areas', None, [(c[1], f'homes-for-sale-{c[0]}.html') for c in CITIES]),
    ('About', None, [('About Me', 'about.html'), ('Testimonials', 'testimonials.html')]),
    ('Blog', 'blog.html', []),
    ('Contact', 'contact.html', []),
]

ICONS = {
 'Instagram': '<path d="M12 7a5 5 0 100 10 5 5 0 000-10zm0 8.2a3.2 3.2 0 110-6.4 3.2 3.2 0 010 6.4zM17.3 5.5a1.2 1.2 0 100 2.4 1.2 1.2 0 000-2.4z"/><path d="M16 2H8a6 6 0 00-6 6v8a6 6 0 006 6h8a6 6 0 006-6V8a6 6 0 00-6-6zm4.2 14A4.2 4.2 0 0116 20.2H8A4.2 4.2 0 013.8 16V8A4.2 4.2 0 018 3.8h8A4.2 4.2 0 0120.2 8z"/>',
 'YouTube': '<path d="M23 7.2a3 3 0 00-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 001 7.2 31 31 0 00.5 12a31 31 0 00.5 4.8 3 3 0 002.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 002.1-2.1 31 31 0 00.5-4.8 31 31 0 00-.5-4.8zM9.7 15V9l5.8 3-5.8 3z"/>',
 'TikTok': '<path d="M16.6 2h-3.3v13.4a2.9 2.9 0 11-2.9-2.9c.3 0 .6 0 .8.1V9.2a6.2 6.2 0 105.4 6.2V8.6a7.9 7.9 0 004.5 1.4V6.7a4.6 4.6 0 01-4.5-4.7z"/>',
 'LinkedIn': '<path d="M4.98 3.5a2.5 2.5 0 110 5 2.5 2.5 0 010-5zM3 9.75h4v11H3zM9.5 9.75h3.8v1.5h.1c.5-1 1.8-2 3.8-2 4 0 4.8 2.6 4.8 6v5.5h-4v-4.9c0-1.2 0-2.7-1.6-2.7s-1.9 1.3-1.9 2.6v5H9.5z"/>',
}

def socials_html():
    return '<div class="socials">' + ''.join(
        f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}"><svg viewBox="0 0 24 24">{ICONS[n]}</svg></a>'
        for n, u in SITE['social'].items()) + '</div>'

# ---------------------------------------------------------------- schema
AGENT_ID = D + '/#agent'
PERSON_ID = D + '/#christian'

def base_graph():
    agent = {
        '@type': 'RealEstateAgent', '@id': AGENT_ID,
        'name': 'Christian Sorrell, RE/MAX Niagara Realty Ltd.',
        'url': D + '/', 'logo': D + '/images/logo-cs.png', 'image': D + '/images/christian-headshot.jpg',
        'telephone': SITE['phone_intl'],
        'address': {'@type': 'PostalAddress', 'streetAddress': SITE['street'], 'addressLocality': SITE['city'],
                    'addressRegion': SITE['region'], 'postalCode': SITE['postal'], 'addressCountry': SITE['country']},
        'areaServed': [{'@type': 'City', 'name': c[1] + ', ON'} for c in CITIES] + [{'@type': 'AdministrativeArea', 'name': 'Niagara Region, Ontario'}],
        'sameAs': list(SITE['social'].values()) + ([SITE['maps']] if SITE['maps'] else []),
        'parentOrganization': {'@type': 'RealEstateAgent', 'name': 'RE/MAX Niagara Realty Ltd., Brokerage'},
        'employee': {'@id': PERSON_ID},
        'knowsAbout': ['Residential real estate', 'Real estate investing', 'Home buying', 'Home selling', 'Rental properties', 'Niagara real estate market'],
    }
    if SITE['email']: agent['email'] = SITE['email']
    person = {'@type': 'Person', '@id': PERSON_ID, 'name': 'Christian Sorrell', 'jobTitle': 'REALTOR®',
              'image': D + '/images/christian-headshot.jpg', 'worksFor': {'@id': AGENT_ID},
              'sameAs': list(SITE['social'].values())}
    site = {'@type': 'WebSite', '@id': D + '/#website', 'url': D + '/', 'name': 'Christian Sorrell | Niagara Real Estate',
            'publisher': {'@id': AGENT_ID}, 'inLanguage': 'en-CA'}
    return [agent, person, site]

# ---------------------------------------------------------------- layout
def header(cur):
    items = []
    for label, href, sub in NAV:
        if sub:
            active = ' class="active"' if any(h == cur for _, h in sub) else ''
            dd = ''.join(f'<li><a href="{h}">{l}</a></li>' for l, h in sub)
            items.append(f'<li class="has-dd"><a href="{sub[0][1]}"{active}>{label}</a><ul class="dd">{dd}</ul></li>')
        else:
            active = ' class="active" aria-current="page"' if href == cur else ''
            items.append(f'<li><a href="{href}"{active}>{label}</a></li>')
    return f'''<a class="skip" href="#main">Skip to content</a>
<header>
  <div class="wrap nav">
    <a href="index.html" class="brand" aria-label="Christian Sorrell, home">
      <img src="images/logo-cs-gold.png" alt="" width="46" height="46">
      <span class="txt"><span class="name">CHRISTIAN SORRELL</span><span class="firm">RE/MAX Niagara Realty Ltd.</span></span>
    </a>
    <button class="burger" aria-label="Open menu" aria-expanded="false"><span></span></button>
    <nav aria-label="Main"><ul>{''.join(items)}</ul></nav>
  </div>
</header>'''

def footer():
    email = f'<br><a href="mailto:{SITE["email"]}">{SITE["email"]}</a>' if SITE['email'] else ''
    areas = ' &middot; '.join(f'<a href="homes-for-sale-{c[0]}.html">{c[1]}</a>' for c in CITIES)
    return f'''<footer>
  <div class="wrap">
    <div class="fgrid">
      <div>
        <img class="remax" src="images/logo-cs-gold.png" alt="Christian Sorrell logo" width="56" height="56">
        <h4>Christian Sorrell</h4>
        <p>REALTOR&reg;<br>{SITE['brokerage']}</p>
        {socials_html()}
      </div>
      <div>
        <h4>Contact</h4>
        <p>Cell: <a href="tel:{SITE['phone_intl']}">{SITE['phone']}</a>{email}</p>
        <p style="margin-top:22px"><a href="contact.html" class="btn">Contact Me</a></p>
      </div>
      <div>
        <h4>Office</h4>
        <address style="font-style:normal">RE/MAX Niagara Realty Ltd.<br>{SITE['street']}<br>{SITE['city']}, {SITE['region']} {SITE['postal']}</address>
        <h4 style="margin-top:26px;font-size:20px">Areas I serve</h4>
        <p style="font-size:13px;line-height:2">{areas}</p>
      </div>
    </div>
    <div class="legal">
      <p>The data relating to real estate on this website comes in part from the MLS&reg; Reciprocity program of PropTx MLS&reg;. Information is deemed reliable but not guaranteed. This data is provided exclusively for consumers' personal, non-commercial use and may not be used for any purpose other than to identify prospective properties consumers may be interested in purchasing.</p>
      <p>The trademarks REALTOR&reg;, REALTORS&reg; and the REALTOR&reg; logo are controlled by The Canadian Real Estate Association (CREA) and identify real estate professionals who are members of CREA. The trademarks MLS&reg;, Multiple Listing Service&reg; and the associated logos identify professional services rendered by REALTOR&reg; members of CREA. Not intended to solicit buyers or sellers already under contract.</p>
      <div class="row">
        <span>&copy; <span id="yr">2026</span> Christian Sorrell. All rights reserved. Each office independently owned and operated.</span>
        <span><a href="privacy.html">Privacy Policy</a> &middot; <a href="sitemap.xml">Sitemap</a></span>
      </div>
    </div>
  </div>
</footer>'''

def page(slug, title, desc, body, crumbs=None, schema=None, og_img='images/christian-headshot.jpg',
         preload=None, noindex=False):
    url = D + '/' + ('' if slug == 'index.html' else slug)
    graph = base_graph()
    wp = {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': title, 'description': desc,
          'isPartOf': {'@id': D + '/#website'}, 'about': {'@id': AGENT_ID}, 'inLanguage': 'en-CA'}
    graph.append(wp)
    if crumbs:
        items = [('Home', D + '/')] + [(n, D + '/' + h) for n, h in crumbs]
        graph.append({'@type': 'BreadcrumbList', '@id': url + '#breadcrumb', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(items)]})
        wp['breadcrumb'] = {'@id': url + '#breadcrumb'}
    graph += schema or []
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1)
    robots = 'noindex, follow' if noindex else 'index, follow, max-image-preview:large'
    pre = f'<link rel="preload" as="image" href="{preload}" fetchpriority="high">\n' if preload else ''
    t = html.escape(title); d = html.escape(desc)
    doc = f'''<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta name="author" content="Christian Sorrell">
<meta name="theme-color" content="#0e0e0e">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_CA">
<meta property="og:site_name" content="Christian Sorrell | Niagara Real Estate">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{D}/{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{D}/{og_img}">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Lato:ital,wght@1,400;1,700&family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/styles.css">
<!-- Google Analytics / Search Console verification: paste tags here -->
<!-- myRealPage: paste any <script> tag(s) from the embed code window here -->
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
{header(slug)}
<main id="main">
{body}
</main>
{footer()}
<script src="assets/main.js" defer></script>
</body>
</html>
'''
    with open(os.path.join(OUT, slug), 'w') as f:
        f.write(doc)
    PAGES.append((slug, noindex))

PAGES = []

# ---------------------------------------------------------------- building blocks
def banner(h1, sub, crumbs, img='hero'):
    cr = '<a href="index.html">Home</a>' + ''.join(
        f'<span>/</span>{"<a href=" + chr(34) + h + chr(34) + ">" + n + "</a>" if i < len(crumbs) - 1 else n}'
        for i, (n, h) in enumerate(crumbs))
    return f'''<section class="page-hero" style="background-image:linear-gradient(90deg,rgba(0,0,0,.82),rgba(0,0,0,.45)),url('images/{img}.webp')">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb">{cr}</nav>
    <h1>{h1}</h1>
    <p>{sub}</p>
  </div>
</section>'''

def sidebar(title='Let\'s talk', text='Have a question or ready to make a move? I\'m happy to help, with no pressure and no obligation.'):
    return f'''<aside class="sidebar">
  <h3>{title}</h3>
  <p>{text}</p>
  <a class="phone" href="tel:{SITE['phone_intl']}">{SITE['phone']}</a>
  <p style="font-size:12px;margin-bottom:22px">Call or text Christian</p>
  <a class="btn" href="contact.html">Send a message</a>
  <a class="btn" href="home-evaluation.html">Free home evaluation</a>
  <a class="btn" href="recip.html">Search listings</a>
</aside>'''

def embed(name, note):
    return f'''<!-- =============================================================
     myRealPage EMBED: {name}
     Replace this .embed-slot div with the embed code from
     myRealPage > Listings > WordPress / Embed > Embeddable.
     ============================================================= -->
<div class="embed-slot"><strong>myRealPage "{name}" embed goes here</strong>{note}</div>'''

def band(h, p, btns):
    b = ''.join(f'<a class="btn" href="{h_}">{l}</a>' for l, h_ in btns)
    return f'<section class="band dark"><div class="wrap"><h2 style="margin-bottom:6px">{h}</h2><p class="lead" style="margin:18px auto 26px">{p}</p>{b}</div></section>'

def steps(items):
    return '<div class="steps">' + ''.join(f'<div class="step"><div><h3>{t}</h3><p>{p}</p></div></div>' for t, p in items) + '</div>'

def faq(items):
    h = '<div class="faq">' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in items) + '</div>'
    s = {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q,
         'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}
    return h, s

def form(fields, button, subject):
    out = [f'<form class="form" action="{SITE["form_endpoint"]}" method="POST">',
           f'<input type="hidden" name="_subject" value="{subject}">',
           '<label class="hp">Leave blank<input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label>']
    for kind, name, label, req, full, *opts in fields:
        r = ' required' if req else ''
        cls = ' class="full"' if full else ''
        fid = 'f-' + name
        if kind == 'select':
            o = ''.join(f'<option>{x}</option>' for x in opts[0])
            ctl = f'<select id="{fid}" name="{name}"{r}><option value="">Select…</option>{o}</select>'
        elif kind == 'textarea':
            ctl = f'<textarea id="{fid}" name="{name}"{r}></textarea>'
        else:
            ac = {'name': 'name', 'email': 'email', 'phone': 'tel', 'address': 'street-address'}.get(name, 'off')
            ctl = f'<input id="{fid}" type="{kind}" name="{name}" autocomplete="{ac}"{r}>'
        out.append(f'<div{cls}><label for="{fid}">{label}{" *" if req else ""}</label>{ctl}</div>')
    out.append(f'<div class="full"><button class="btn btn-gold" type="submit">{button}</button></div>')
    out.append('<p class="note full">Your information is kept private and only used to respond to your request. See the <a href="privacy.html" style="color:var(--gold)">privacy policy</a>.</p></form>')
    return '\n'.join(out)

CONTACT_FIELDS = [('text', 'name', 'Full name', True, False), ('email', 'email', 'Email', True, False),
                  ('tel', 'phone', 'Phone', False, False)]

def two_col(main, side=None):
    return f'<section><div class="wrap two-col"><div class="prose">{main}</div>{side or sidebar()}</div></section>'

# ================================================================ PAGES
CITY_LINKS_TITLE = 'Homes for sale in {c} | Christian Sorrell, REALTOR®'

# ---- Home
home = open(os.path.join(HERE, 'home_body.html')).read()
page('index.html',
     'Christian Sorrell | St. Catharines & Niagara Real Estate Agent | RE/MAX',
     'Christian Sorrell is a St. Catharines REALTOR® with RE/MAX Niagara Realty helping buyers, sellers and investors across Niagara. Search MLS® listings and get a free home evaluation.',
     home, og_img='images/hero.jpg', preload='images/hero.webp')

# ---- About
about_main = '''<h2>Hi, I'm Christian</h2>
<!-- DRAFT: have Christian review / replace with his own wording -->
<p>I'm a REALTOR&reg; with RE/MAX Niagara Realty Ltd., based in St. Catharines and serving buyers, sellers, landlords and investors across the Niagara region and Hamilton.</p>
<p>Buying or selling a home is one of the biggest financial decisions you'll make, and you deserve to understand every step of it. I take the time to explain the process clearly, walk you through what the numbers are really saying and make sure you never feel rushed or left in the dark.</p>
<h2>An investor's perspective</h2>
<p>My background in real estate investing shapes how I look at every property: how it fits your life today, and how it's likely to perform over time. Whether you're buying your first home, upgrading for a growing family or adding a rental to your portfolio, that perspective helps you spot real value, avoid costly surprises and negotiate with confidence.</p>
<h2>What you can expect from me</h2>
<ul>
<li><strong>Clear communication.</strong> Quick replies and straight answers, by phone, text or email.</li>
<li><strong>Honest advice.</strong> Realistic expectations on price, timing and condition, even when it isn't what you want to hear.</li>
<li><strong>Local knowledge.</strong> Street-level insight into St. Catharines, Niagara Falls, Welland, Thorold, Pelham and surrounding communities.</li>
<li><strong>Long-term relationships.</strong> I'm still here after closing day whenever you have a question about the market or your next move.</li>
</ul>
<h2>Backed by RE/MAX</h2>
<p>As part of RE/MAX Niagara Realty Ltd., I combine personal, one-on-one service with the marketing reach and resources of one of the most recognized names in real estate.</p>
<p><a class="btn btn-gold" href="contact.html">Let's connect</a> &nbsp; <a class="btn" href="testimonials.html">Read client reviews</a></p>'''
about_side = f'''<aside class="sidebar"><img src="images/christian-headshot.webp" alt="Christian Sorrell, REALTOR® with RE/MAX Niagara Realty" width="792" height="1188" style="margin:-38px -34px 26px;width:calc(100% + 68px);max-width:none;aspect-ratio:4/5;object-fit:cover;object-position:top">
<h3>Christian Sorrell</h3><p>REALTOR&reg; &middot; RE/MAX Niagara Realty Ltd., Brokerage</p>
<a class="phone" href="tel:{SITE['phone_intl']}">{SITE['phone']}</a><p style="font-size:12px">Call or text</p>
{socials_html()}<a class="btn" href="contact.html">Send a message</a></aside>'''
page('about.html', 'About Christian Sorrell | Niagara REALTOR® | RE/MAX Niagara Realty',
     'Meet Christian Sorrell, a St. Catharines REALTOR® with RE/MAX Niagara Realty. Honest advice, an investor\'s perspective and clear communication for Niagara buyers and sellers.',
     banner('About Christian', 'Your Niagara real estate agent: honest advice, an investor\'s eye and service that continues after closing day.', [('About', 'about.html')], 'living-green')
     + two_col(about_main, about_side), crumbs=[('About', 'about.html')],
     schema=[{'@type': 'AboutPage', 'url': D + '/about.html', 'mainEntity': {'@id': PERSON_ID}}])

# ---- Contact
contact_main = '<h2>Send me a message</h2><p>Whether you\'re thinking about buying, selling or investing, or just have a question about the market, I\'d love to hear from you. I usually reply the same day.</p>' + form(
    CONTACT_FIELDS + [('select', 'interest', 'I\'m interested in', False, False, ['Buying', 'Selling', 'Buying and selling', 'Investing', 'Renting / leasing', 'Something else']),
                      ('textarea', 'message', 'Message', True, True)], 'Send message', 'New website enquiry')
maps_q = 'https://www.google.com/maps?q=261+Martindale+Rd+Unit+14C+St.+Catharines+ON+L2W+1A2&output=embed'
contact_side = f'''<aside class="sidebar"><h3>Get in touch</h3>
<p><strong style="color:#fff">Christian Sorrell</strong><br>REALTOR&reg;, {SITE['brokerage']}</p>
<a class="phone" href="tel:{SITE['phone_intl']}">{SITE['phone']}</a><p style="font-size:12px">Call or text</p>
<p><address style="font-style:normal">{SITE['street']}<br>{SITE['city']}, {SITE['region']} {SITE['postal']}</address></p>
{socials_html()}</aside>'''
page('contact.html', 'Contact Christian Sorrell | St. Catharines REALTOR® | 905-931-0583',
     'Contact Christian Sorrell, REALTOR® with RE/MAX Niagara Realty, 261 Martindale Rd., St. Catharines. Call or text 905-931-0583 for help buying, selling or investing in Niagara.',
     banner('Contact Christian', 'Call, text or send a message. I\'m here to help with your next move.', [('Contact', 'contact.html')], 'kitchen')
     + two_col(contact_main, contact_side)
     + f'<section style="padding:0"><iframe title="Map to RE/MAX Niagara Realty, 261 Martindale Rd., St. Catharines" src="{maps_q}" width="100%" height="420" style="border:0;display:block;filter:grayscale(1)" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></section>',
     crumbs=[('Contact', 'contact.html')], schema=[{'@type': 'ContactPage', 'url': D + '/contact.html'}])

# ---- Buying
buy_faq_h, buy_faq_s = faq([
    ('How much do I need for a down payment in Ontario?', 'The minimum down payment depends on the purchase price, and anything under 20% requires mortgage default insurance. Rules change from time to time, so I recommend confirming current requirements with a mortgage professional. I\'m happy to connect you with trusted local lenders and brokers.'),
    ('Does it cost anything to work with a buyer\'s agent?', 'In most Niagara purchases the buyer agent\'s commission is paid out of the sale proceeds by the seller. We\'ll review exactly how compensation works in our buyer representation agreement before you commit to anything.'),
    ('How long does it take to buy a home?', 'Many buyers find the right home within a few weeks to a few months. Once an offer is accepted, closings are typically set 30 to 90 days out, depending on what works for you and the seller.'),
    ('Should I sell my current home first or buy first?', 'It depends on your finances and the market. Buying first gives you certainty on your next home; selling first gives you certainty on your budget. We\'ll weigh both options, including bridge financing, based on your situation.'),
])
buy_main = '''<h2>Buying a home in Niagara</h2>
<p>Whether it\'s your first home, your forever home or a smart investment, buying in St. Catharines and the Niagara region should feel exciting, not overwhelming. Here\'s how we\'ll work together from first conversation to keys in hand.</p>''' + steps([
    ('Consultation', 'We\'ll talk about what you need, what you want, your timeline and the neighbourhoods that fit your lifestyle.'),
    ('Get pre-approved', 'A mortgage pre-approval sets a clear budget and makes your offer stronger. I can introduce you to trusted local lenders.'),
    ('Search and showings', 'I\'ll set you up with automatic MLS&reg; alerts and book showings, pointing out what matters: condition, layout, location and resale value.'),
    ('Make a winning offer', 'We\'ll review comparable sales, set a strategy and negotiate price and conditions, from inspections to financing.'),
    ('Conditions and closing', 'I\'ll coordinate inspections, appraisals and paperwork with your lawyer and lender so closing day goes smoothly.'),
]) + '''<h2>Buyer tools</h2>
<ul><li><a href="recip.html">Search all Niagara MLS&reg; listings</a></li><li><a href="home-finder.html">Tell me what you\'re looking for with Home Finder</a> and I\'ll send matches</li>
<li><a href="mortgage-calculator.html">Estimate payments with the mortgage calculator</a></li><li><a href="watch-list.html">Create a watch list</a> to get alerts on new listings and price changes</li></ul>
<h2>Frequently asked questions</h2>''' + buy_faq_h
page('buying.html', 'Buying a Home in St. Catharines & Niagara | Christian Sorrell',
     'Thinking of buying a home in St. Catharines or Niagara? Christian Sorrell guides you through pre-approval, showings, offers and closing. Buyer tools, FAQs and MLS® search.',
     banner('Buying a home', 'Clear guidance from pre-approval to closing day, so you buy with confidence.', [('Buy', 'buying.html')], 'card-buyers')
     + two_col(buy_main) + band('Ready to start your search?', 'Get new listings that match your criteria the moment they hit the market.', [('Search listings', 'recip.html'), ('Home Finder', 'home-finder.html')]),
     crumbs=[('Buying Resources', 'buying.html')], schema=[buy_faq_s])

# ---- Home finder
hf_main = '<h2>Let me find it for you</h2><p>Tell me what you\'re looking for and I\'ll send you matching homes, including new listings as soon as they hit the market. Prefer to talk it through? Call or text me any time.</p>' + form(
    CONTACT_FIELDS + [('select', 'areas', 'Preferred area', False, False, [c[1] for c in CITIES] + ['Flexible / not sure']),
                      ('select', 'type', 'Property type', False, False, ['Detached', 'Semi-detached', 'Townhouse', 'Condo', 'Multi-unit / investment', 'Land / rural']),
                      ('select', 'budget', 'Budget', False, False, ['Under $500,000', '$500,000–$750,000', '$750,000–$1,000,000', '$1,000,000+']),
                      ('select', 'beds', 'Bedrooms', False, False, ['1+', '2+', '3+', '4+', '5+']),
                      ('select', 'timeline', 'Timeline', False, False, ['ASAP', '1–3 months', '3–6 months', '6+ months']),
                      ('textarea', 'message', 'Must-haves and nice-to-haves', False, True)], 'Find my home', 'Home Finder request')
page('home-finder.html', 'Home Finder | Get Niagara Listings Matched to You | Christian Sorrell',
     'Tell Christian Sorrell what you\'re looking for and get Niagara and St. Catharines homes matched to your budget, area and must-haves, including new MLS® listings as they come out.',
     banner('Home Finder', 'Tell me what you\'re looking for and I\'ll do the searching.', [('Buy', 'buying.html'), ('Home Finder', 'home-finder.html')], 'staircase')
     + two_col(hf_main), crumbs=[('Buying Resources', 'buying.html'), ('Home Finder', 'home-finder.html')])

# ---- Mortgage calculator
calc = f'''<section><div class="wrap">
<div class="calc">
<form id="calc" class="form" onsubmit="return false" aria-label="Mortgage calculator">
  <div class="full"><label for="c-price">Purchase price ($)</label><input id="c-price" type="number" min="0" step="1000" value="650000"></div>
  <div class="full"><label for="c-down">Down payment ($)</label><input id="c-down" type="number" min="0" step="1000" value="130000"></div>
  <div><label for="c-rate">Interest rate (%)</label><input id="c-rate" type="number" min="0" step="0.01" value="4.5"></div>
  <div><label for="c-amort">Amortization (years)</label><select id="c-amort"><option>15</option><option>20</option><option selected>25</option><option>30</option></select></div>
  <div class="full"><label for="c-freq">Payment frequency</label><select id="c-freq"><option value="monthly">Monthly</option><option value="biweekly">Bi-weekly</option><option value="weekly">Weekly</option></select></div>
  <p class="note full">Calculated using semi-annual compounding, the standard for Canadian fixed-rate mortgages. Estimates only. Confirm with your lender.</p>
</form>
<div class="calc-out" aria-live="polite">
  <div class="lbl" id="o-lbl">Monthly payment</div><div class="big" id="o-pay">$0</div>
  <dl><dt>Mortgage amount</dt><dd id="o-principal"></dd><dt>Down payment</dt><dd id="o-downpct"></dd>
  <dt>Total interest</dt><dd id="o-interest"></dd><dt>Total of payments</dt><dd id="o-total"></dd></dl>
  <p class="warn" id="o-warn" hidden>With less than 20% down, mortgage default insurance is required. The premium is added to your mortgage and isn't included above.</p>
  <p style="margin-top:26px"><a class="btn" style="color:#fff;border-color:var(--gold-lt)" href="contact.html">Talk to Christian</a></p>
</div></div></div></section>'''
page('mortgage-calculator.html', 'Mortgage Calculator (Canada) | Estimate Payments | Christian Sorrell',
     'Free Canadian mortgage calculator. Estimate monthly, bi-weekly or weekly payments for a home in St. Catharines and Niagara using semi-annual compounding.',
     banner('Mortgage calculator', 'Estimate your payments and see what fits your budget.', [('Buy', 'buying.html'), ('Mortgage Calculator', 'mortgage-calculator.html')], 'kitchen')
     + calc, crumbs=[('Buying Resources', 'buying.html'), ('Mortgage Calculator', 'mortgage-calculator.html')],
     schema=[{'@type': 'WebApplication', 'name': 'Mortgage Calculator', 'applicationCategory': 'FinanceApplication', 'operatingSystem': 'Any', 'url': D + '/mortgage-calculator.html', 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'CAD'}}])

# ---- Selling
sell_faq_h, sell_faq_s = faq([
    ('How much is my home worth?', 'Value depends on recent comparable sales, condition, location and current demand. Request a free home evaluation and I\'ll prepare a detailed market analysis for your property.'),
    ('What should I fix before listing?', 'Focus on the inexpensive items that make the biggest impression: decluttering, fresh paint in neutral tones, minor repairs and curb appeal. I\'ll walk through your home and tell you what\'s worth doing and what isn\'t.'),
    ('How long will it take to sell?', 'It depends on price, location and the market at the time. A well-prepared, correctly priced home typically sells much faster than one that starts too high and has to be reduced.'),
    ('What does it cost to sell?', 'Typical costs include real estate commission, legal fees and any mortgage discharge penalties. I\'ll give you a clear estimate of your net proceeds before you list.'),
])
sell_main = '''<h2>Selling your home in Niagara</h2>
<p>Selling isn\'t just about putting a sign on the lawn. It\'s about pricing correctly from day one, presenting your home at its best and putting it in front of the right buyers, then negotiating to protect your bottom line.</p>''' + steps([
    ('Free home evaluation', 'A detailed market analysis using recent comparable sales and current competition to set the right price.'),
    ('Preparation', 'Practical advice on repairs, decluttering and staging so your home photographs and shows beautifully.'),
    ('Professional marketing', 'Professional photography, MLS&reg; exposure, social media and targeted promotion. <a href="marketing-strategy.html">See my marketing strategy</a>.'),
    ('Showings and offers', 'I manage showings, collect feedback and guide you through every offer, including multiple-offer situations.'),
    ('Negotiation to closing', 'I negotiate price and terms and keep everything on track with buyers, agents and lawyers until closing.'),
]) + '<h2>Frequently asked questions</h2>' + sell_faq_h
page('selling.html', 'Selling Your Home in St. Catharines & Niagara | Christian Sorrell',
     'Sell your St. Catharines or Niagara home with confidence. Christian Sorrell offers free home evaluations, professional marketing and expert negotiation with RE/MAX.',
     banner('Selling your home', 'The right price, the right presentation and the right buyers.', [('Sell', 'selling.html')], 'card-sellers')
     + two_col(sell_main) + band('What\'s your home worth?', 'Get a free, no-obligation evaluation based on real comparable sales in your neighbourhood.', [('Free home evaluation', 'home-evaluation.html'), ('What your neighbour sold for', 'neighbour-sold.html')]),
     crumbs=[('Selling Resources', 'selling.html')], schema=[sell_faq_s])

# ---- Home evaluation
he_main = '<h2>Find out what your home is worth</h2><p>Online estimates can be off by tens of thousands of dollars because they can\'t see your upgrades, layout or street. I\'ll prepare a personalized comparative market analysis using recent sales near you, free and with no obligation.</p>' + form(
    CONTACT_FIELDS + [('text', 'address', 'Property address', True, True),
                      ('select', 'type', 'Property type', False, False, ['Detached', 'Semi-detached', 'Townhouse', 'Condo', 'Multi-unit']),
                      ('select', 'beds', 'Bedrooms', False, False, ['1', '2', '3', '4', '5+']),
                      ('select', 'timeline', 'Thinking of selling', False, False, ['Within 3 months', '3–6 months', '6–12 months', 'Just curious']),
                      ('textarea', 'message', 'Upgrades, renovations or anything else I should know', False, True)], 'Get my free evaluation', 'Home evaluation request')
page('home-evaluation.html', 'Free Home Evaluation St. Catharines & Niagara | What\'s My Home Worth?',
     'Get a free, accurate home evaluation for your St. Catharines or Niagara property from Christian Sorrell, RE/MAX Niagara Realty. Based on real comparable sales, not an algorithm.',
     banner('Free home evaluation', 'An accurate value based on real local sales, not an algorithm.', [('Sell', 'selling.html'), ('Home Evaluation', 'home-evaluation.html')], 'hero')
     + two_col(he_main), crumbs=[('Selling Resources', 'selling.html'), ('Home Evaluation', 'home-evaluation.html')])

# ---- Neighbour sold
ns_main = '<h2>Curious what homes on your street sold for?</h2><p>Sold prices tell you far more than asking prices. Send me your address and I\'ll put together a list of recent sales near you, with sale prices, days on market and how they compare to your home.</p>' + form(
    CONTACT_FIELDS + [('text', 'address', 'Your address or street', True, True), ('textarea', 'message', 'Anything specific you want to know?', False, True)],
    'Send me recent sales', 'Neighbour sold request')
page('neighbour-sold.html', 'Niagara Sold Prices: What Did My Neighbour\'s Home Sell For?',
     'Find out what homes near you in St. Catharines and Niagara actually sold for. Request a free list of recent sold prices on your street from Christian Sorrell.',
     banner('What your neighbour sold for', 'Real sold prices near you, delivered to your inbox.', [('Sell', 'selling.html'), ('What Your Neighbour Sold For', 'neighbour-sold.html')], 'card-search')
     + two_col(ns_main), crumbs=[('Selling Resources', 'selling.html'), ('What Your Neighbour Sold For', 'neighbour-sold.html')])

# ---- Marketing strategy
mk_main = '''<h2>How I market your home</h2>
<p>Buyers start their search online, so the first impression of your home happens on a screen. My marketing plan is built to make that impression count and reach as many qualified buyers as possible.</p>
<h3>Pricing strategy</h3><p>Marketing starts with the right price. I analyze comparable sales, active competition and market trends so your home attracts serious buyers from day one.</p>
<h3>Preparation and staging advice</h3><p>A walkthrough with practical, budget-conscious recommendations on repairs, decluttering and staging to help your home show at its best.</p>
<h3>Professional photography and video</h3><p>High-quality photos, and video where it suits the property, that make buyers stop scrolling. <!-- Add: drone, 3D tours, floor plans if offered --></p>
<h3>MLS&reg; and online exposure</h3><p>Your listing goes on the MLS&reg; and syndicates to major real estate websites, plus a dedicated feature on this website.</p>
<h3>Social media</h3><p>Promotion across my <a href="https://www.instagram.com/sellwithsorrell" target="_blank" rel="noopener">Instagram</a>, <a href="https://www.youtube.com/@sellwithsorrell" target="_blank" rel="noopener">YouTube</a> and <a href="https://www.tiktok.com/@sellwithsorrell" target="_blank" rel="noopener">TikTok</a> channels to reach buyers where they spend their time.</p>
<h3>The RE/MAX network</h3><p>Exposure to agents and buyers across the RE/MAX network and the wider Niagara real estate community.</p>
<h3>Clear communication</h3><p>Regular updates on showings, feedback and market activity, so you always know where things stand.</p>
<!-- Edit this list so it exactly matches the services Christian provides -->'''
page('marketing-strategy.html', 'Home Selling Marketing Strategy | Niagara Real Estate | Christian Sorrell',
     'How Christian Sorrell markets Niagara homes: strategic pricing, staging advice, professional photography, MLS® exposure, social media and the RE/MAX network.',
     banner('Marketing strategy', 'A plan built to get your home seen by the right buyers.', [('Sell', 'selling.html'), ('Marketing Strategy', 'marketing-strategy.html')], 'living-green')
     + two_col(mk_main), crumbs=[('Selling Resources', 'selling.html'), ('Marketing Strategy', 'marketing-strategy.html')])

# ---- Investing
inv_faq_h, inv_faq_s = faq([
    ('Is Niagara a good place to invest in real estate?', 'Niagara offers lower entry prices than the GTA, a diverse rental base including students, healthcare and tourism workers, and ongoing infrastructure investment. Every property is different, so we\'ll analyze each deal on its own numbers.'),
    ('What types of investment properties do you help with?', 'Single-family rentals, duplexes and triplexes, homes with secondary suites, student rentals near Brock University and Niagara College, and small multi-unit buildings.'),
    ('Can you help me find tenants?', 'Yes. I can help market your rental and screen prospective tenants, as I\'ve done for landlord clients.'),
])
inv_main = '''<h2>Investing in Niagara real estate</h2>
<p>Real estate investing is personal for me, and it\'s a big part of how I approach every deal. I look past the listing photos to the numbers: rent potential, carrying costs, cash flow and long-term appreciation.</p>
<h3>How I help investors</h3>
<ul><li><strong>Deal analysis:</strong> realistic rent estimates, expenses and cash-flow projections before you make an offer</li>
<li><strong>Finding opportunities:</strong> properties with suite potential, value-add upgrades or strong rental demand</li>
<li><strong>Area insight:</strong> where demand is coming from, including students, commuters and healthcare and tourism workers</li>
<li><strong>Leasing support:</strong> marketing your unit and helping you find qualified tenants</li>
<li><strong>Portfolio strategy:</strong> when to hold, refinance or sell to grow your portfolio</li></ul>
<h3>Popular Niagara investment areas</h3>
<p><a href="homes-for-sale-st-catharines.html">St. Catharines</a> and <a href="homes-for-sale-thorold.html">Thorold</a> near Brock University, <a href="homes-for-sale-welland.html">Welland</a> near Niagara College, and <a href="homes-for-sale-niagara-falls.html">Niagara Falls</a> with its tourism-driven economy each offer different strategies and price points.</p>
<h2>Frequently asked questions</h2>''' + inv_faq_h
page('investing.html', 'Niagara Investment Properties | Real Estate Investing | Christian Sorrell',
     'Buy investment properties in St. Catharines, Thorold, Welland and Niagara with a REALTOR® who invests himself. Deal analysis, rental strategy and tenant placement.',
     banner('Real estate investing', 'Work with an agent who looks at every property like an investor.', [('Investing', 'investing.html')], 'kitchen')
     + two_col(inv_main), crumbs=[('Investing', 'investing.html')], schema=[inv_faq_s])

# ---- Listings / search pages (myRealPage embeds)
LIST_PAGES = [
    ('mylistings.html', 'Featured Listings', 'My Listings', 'Christian Sorrell\'s Featured Listings | Niagara Homes for Sale & Lease',
     'Browse Christian Sorrell\'s current featured listings in St. Catharines, Niagara and Hamilton, including homes for sale and for lease with RE/MAX Niagara Realty.', 'Current homes for sale and lease, listed by Christian.'),
    ('office-listings.html', 'Office Listings', 'Office Listings', 'RE/MAX Niagara Realty Office Listings | Christian Sorrell',
     'Browse current listings from RE/MAX Niagara Realty Ltd. across St. Catharines and the Niagara region.', 'Homes listed by the RE/MAX Niagara Realty team.'),
    ('recip.html', 'Search Listings', 'List IDX Search', 'Search Niagara MLS® Listings | Homes for Sale St. Catharines | Christian Sorrell',
     'Search every MLS® listing in St. Catharines, Niagara Falls, Welland and across Niagara. Filter by price, beds, baths and property type and save your favourites.', 'Search every MLS&reg; listing across Niagara and beyond.'),
    ('map-search.html', 'Map Search', 'Map IDX Search', 'Map Search | Niagara Homes for Sale on a Map | Christian Sorrell',
     'Search Niagara homes for sale on an interactive map. Explore listings by neighbourhood in St. Catharines, Niagara Falls, Welland, Pelham and more.', 'Explore homes for sale neighbourhood by neighbourhood.'),
    ('watch-list.html', 'Watch List', 'VOW / Watch List sign-up', 'Watch List & Listing Alerts | Christian Sorrell',
     'Create a free watch list to get instant email alerts on new Niagara listings, price changes and sold homes that match your search.', 'Get alerts on new listings, price changes and sales.'),
]
for slug, h1, emb, title, desc, sub in LIST_PAGES:
    body = banner(h1, sub, [('Properties', 'recip.html'), (h1, slug)], 'staircase') + \
        f'<section><div class="wrap">{embed(emb, "Live listings from PropTx MLS&reg; load here automatically.")}' \
        f'<div style="margin-top:60px"><h2>Search by community</h2><div class="city-tiles" style="margin-top:28px">' + \
        ''.join(f'<a href="homes-for-sale-{c[0]}.html">{c[1]}</a>' for c in CITIES) + '</div></div></div></section>'
    page(slug, title, desc, body, crumbs=[('Properties', 'recip.html'), (h1, slug)])

# ---- City landing pages (local SEO)
for i, (cs, name, img, paras, hoods) in enumerate(CITIES):
    slug = f'homes-for-sale-{cs}.html'
    others = [c for c in CITIES if c[0] != cs]
    c_faq_h, c_faq_s = faq([
        (f'How do I get alerts for new listings in {name}?', f'Create a free <a href="watch-list.html">watch list</a> or use <a href="home-finder.html">Home Finder</a> and I\'ll set up automatic alerts for {name} homes that match your criteria.'),
        (f'What is my {name} home worth?', f'Request a <a href="home-evaluation.html">free home evaluation</a>. I\'ll compare your property with recent {name} sales and current competition to give you an accurate price range.'),
        (f'Do you work with buyers and sellers in {name}?', f'Yes. I help buyers, sellers and investors throughout {name} and the rest of the Niagara region from my office in St. Catharines.'),
    ])
    main = f'<h2>Living in {name}</h2>' + ''.join(f'<p>{p}</p>' for p in paras) + \
        f'<h3>Popular areas and lifestyle in {name}</h3><ul>' + ''.join(f'<li>{h}</li>' for h in hoods) + '</ul>' + \
        f'<h2>{name} homes for sale</h2>' + embed(f'Predefined Search: {name}', f'Create a predefined search for {name} in myRealPage and paste its embed code here.') + \
        f'<h2>Buying or selling in {name}?</h2><p>Whether you\'re searching for your first home, moving up, downsizing or investing, I\'ll help you understand {name}\'s market and make a confident decision. <a href="contact.html">Get in touch</a> or call <a href="tel:{SITE["phone_intl"]}">{SITE["phone"]}</a>.</p>' + \
        '<h2>Frequently asked questions</h2>' + c_faq_h
    body = banner(f'{name} homes for sale', f'Search {name} real estate and get local insight from Christian Sorrell, RE/MAX Niagara Realty.', [('Areas', 'recip.html'), (name, slug)], img) + \
        two_col(main, sidebar(f'Thinking about {name}?', f'Get local market insight, listing alerts or a free evaluation of your {name} home.')) + \
        '<section class="alt"><div class="wrap"><h2>Explore other communities</h2><div class="city-tiles" style="margin-top:28px">' + \
        ''.join(f'<a href="homes-for-sale-{c[0]}.html">{c[1]}</a>' for c in others) + '</div></div></section>'
    page(slug, f'{name} Homes for Sale | Christian Sorrell, REALTOR®',
         f'Search {name}, ON homes for sale and MLS® listings. Local insight, listing alerts and free home evaluations from Christian Sorrell, RE/MAX Niagara Realty.',
         body, crumbs=[('Areas', 'recip.html'), (name, slug)], og_img='images/hero.jpg',
         schema=[c_faq_s, {'@type': 'Place', 'name': f'{name}, Ontario', 'address': {'@type': 'PostalAddress', 'addressLocality': name, 'addressRegion': 'ON', 'addressCountry': 'CA'}}])

# ---- Testimonials
REVIEWS = [
    ('Shane DeBon', 'Christian was amazing helping my wife and I find our apartment. Answered all of our questions, dealt with my many emails back and forth clarifying anything I had questions about. Was quick to respond and helped make this an easy process in getting our place. Would definitely recommend him for anyone looking for a new place.'),
    ('Alexander Miller', 'Christian was very helpful in helping me with obtaining a new place. Very straightforward, quick to action emails, and friendly guy overall.'),
    ('Michaela Goodfield', 'Working with Christian was a positive experience, he was helpful and answered any and all questions in a respectful and professional manner.'),
    ('Murtaza Mohamedbhai', 'I highly recommend Christian, it was great to work with him, very approachable and communicated effectively with us as well as the potential tenants. He did an amazing job in finding us a tenant, he made sure that we get the perfect tenant and went thoroughly through the process.'),
]
tl = ''.join(f'<figure class="tbox"><div class="mark">&ldquo;</div><blockquote>{q}</blockquote><figcaption><cite>{n}</cite></figcaption></figure>' for n, q in REVIEWS)
page('testimonials.html', 'Client Testimonials & Reviews | Christian Sorrell, Niagara REALTOR®',
     'Read what clients say about working with Christian Sorrell, REALTOR® with RE/MAX Niagara Realty in St. Catharines: responsive, honest and easy to work with.',
     banner('Client testimonials', 'What clients say about working with Christian.', [('About', 'about.html'), ('Testimonials', 'testimonials.html')], 'living-green')
     + f'<section class="alt"><div class="wrap"><div class="tlist">{tl}</div>'
     + '<p class="center" style="margin-top:50px"><!-- Add Google review link --><a class="btn" href="contact.html">Work with Christian</a></p></div></section>',
     crumbs=[('About', 'about.html'), ('Testimonials', 'testimonials.html')])

# ---- Blog (starter posts)
POSTS = [
    ('blog-first-time-buyer-guide-niagara.html', 'First-time home buyer guide for Niagara', 'card-buyers', 'Buying',
     'A step-by-step look at buying your first home in St. Catharines and the Niagara region, from budgeting to closing day.',
     '''<p>Buying your first home is a big step, and in Niagara it\'s one that\'s still within reach for many buyers priced out of the GTA. Here\'s a practical roadmap.</p>
<h2>1. Know your numbers</h2><p>Before you look at a single listing, get a mortgage pre-approval. It tells you what you can borrow, locks in a rate for a period of time and shows sellers you\'re serious. Budget beyond the down payment too: closing costs such as land transfer tax, legal fees, title insurance and moving usually add a few percent of the purchase price.</p>
<h2>2. Look into first-time buyer programs</h2><p>Federal and provincial programs, including land transfer tax rebates and registered savings accounts for home buyers, can make a meaningful difference. Program rules change, so check the current details with your lender, lawyer or accountant.</p>
<h2>3. Choose the right community</h2><p>Niagara is a region of very different towns. <a href="homes-for-sale-st-catharines.html">St. Catharines</a> offers the widest selection and GO train access, <a href="homes-for-sale-welland.html">Welland</a> and <a href="homes-for-sale-port-colborne.html">Port Colborne</a> are known for value, and <a href="homes-for-sale-thorold.html">Thorold</a> has plenty of newer construction.</p>
<h2>4. Make a smart offer</h2><p>Your offer is more than a price: deposit, conditions and closing date all matter. We\'ll review comparable sales together so you don\'t overpay, and protect you with the right conditions such as financing and home inspection.</p>
<h2>5. Close with confidence</h2><p>Once your offer is firm, your lawyer, lender and I coordinate the details. On closing day, you get the keys.</p>
<p>Ready to start? <a href="contact.html">Book a free buyer consultation</a>.</p>'''),
    ('blog-how-to-price-your-home-niagara.html', 'How to price your Niagara home to sell', 'card-sellers', 'Selling',
     'Why pricing is the most important decision you\'ll make as a seller, and how to get it right in today\'s Niagara market.',
     '''<p>Of every decision you make when selling, price has the biggest impact on how fast your home sells and how much you walk away with.</p>
<h2>Why overpricing costs you</h2><p>Buyers and their agents compare every listing against recent sales. A home priced well above the market gets fewer showings, sits longer and often needs price reductions, which can end up selling it for less than if it had been priced right from day one.</p>
<h2>What really determines value</h2><ul><li><strong>Comparable sales:</strong> similar homes nearby that sold recently</li><li><strong>Active competition:</strong> what buyers can choose from right now</li><li><strong>Condition and upgrades:</strong> kitchens, bathrooms, roof, windows and mechanicals</li><li><strong>Location:</strong> street, lot, schools and commute</li></ul>
<h2>Why online estimates miss the mark</h2><p>Automated valuations can\'t see your renovated kitchen or your busy street. A local comparative market analysis accounts for the details that buyers actually pay for.</p>
<p>Want to know where your home stands? <a href="home-evaluation.html">Request a free home evaluation</a>.</p>'''),
    ('blog-investing-in-niagara-rental-properties.html', 'What to know before buying a rental property in Niagara', 'kitchen', 'Investing',
     'An investor\'s checklist for analyzing rental properties in St. Catharines, Thorold, Welland and across Niagara.',
     '''<p>Niagara\'s mix of students, commuters and tourism and healthcare workers creates steady rental demand. But a good investment comes down to the numbers, not the listing photos.</p>
<h2>Run the real numbers</h2><p>Start with a realistic rent estimate based on comparable rentals, not optimistic projections. Then account for mortgage payments, property taxes, insurance, utilities you\'ll cover, maintenance, vacancy and property management if you won\'t self-manage.</p>
<h2>Know your tenant pool</h2><p>Properties near Brock University or Niagara College attract students; family homes in established neighbourhoods attract long-term tenants. Each has different management needs and risks.</p>
<h2>Look for value-add potential</h2><p>Homes with separate entrances, finished basements or zoning that allows additional units can boost income. Always confirm permits and zoning with the municipality.</p>
<h2>Understand Ontario landlord rules</h2><p>Ontario\'s Residential Tenancies Act sets the rules on leases, rent increases and ending tenancies. Learn them before you buy.</p>
<p>Want help analyzing a deal? <a href="investing.html">See how I work with investors</a> or <a href="contact.html">get in touch</a>.</p>'''),
]
for slug, t, img, cat, ex, content in POSTS:
    body = banner(t, ex, [('Blog', 'blog.html'), (t, slug)], img) + two_col(content + '<p style="margin-top:30px;font-size:13px;color:#888">By Christian Sorrell, REALTOR&reg;</p>')
    page(slug, f'{t} | Christian Sorrell', ex, body, crumbs=[('Blog', 'blog.html'), (t, slug)], og_img='images/hero.jpg',
         schema=[{'@type': 'BlogPosting', 'headline': t, 'description': ex, 'image': f'{D}/images/{img}.webp',
                  'datePublished': TODAY, 'dateModified': TODAY, 'author': {'@id': PERSON_ID}, 'publisher': {'@id': AGENT_ID},
                  'mainEntityOfPage': f'{D}/{slug}'}])
cards = ''.join(f'<a class="post" href="{s}"><div class="img" style="background-image:url(\'images/{img}.webp\')"></div><div class="b"><div class="meta">{cat}</div><h3>{t}</h3><p>{ex}</p></div></a>' for s, t, img, cat, ex, _ in POSTS)
page('blog.html', 'Niagara Real Estate Blog | Christian Sorrell, REALTOR®',
     'Real estate tips and Niagara market insight from Christian Sorrell: guides for first-time buyers, sellers and investors in St. Catharines and the Niagara region.',
     banner('Blog', 'Real estate tips and Niagara market insight.', [('Blog', 'blog.html')], 'card-search')
     + f'<section class="alt"><div class="wrap"><!-- Move existing blog posts here as new pages --><div class="posts">{cards}</div></div></section>',
     crumbs=[('Blog', 'blog.html')])

# ---- Privacy
priv = f'''<h2>Privacy policy</h2><p><em>Last updated: {datetime.date.today():%B %-d, %Y}</em></p>
<!-- Template only: have Christian / the brokerage review against RECO and PIPEDA requirements -->
<p>Christian Sorrell, REALTOR&reg; with RE/MAX Niagara Realty Ltd., Brokerage ("we", "us") respects your privacy. This policy explains how we collect, use and protect personal information submitted through this website, in line with Canada\'s Personal Information Protection and Electronic Documents Act (PIPEDA).</p>
<h3>Information we collect</h3><p>We collect information you choose to provide through forms on this site, such as your name, email, phone number, property address and details about your real estate needs. We may also collect anonymous usage data (such as pages visited and browser type) through cookies and analytics tools.</p>
<h3>How we use it</h3><ul><li>To respond to your enquiries and provide real estate services</li><li>To send listing alerts or market updates you request</li><li>To improve this website</li></ul>
<p>We do not sell your personal information. We will only send you commercial electronic messages with your consent, in accordance with Canada\'s Anti-Spam Legislation (CASL), and you can unsubscribe at any time.</p>
<h3>Sharing</h3><p>Information may be shared with our brokerage and with service providers who help operate this website, listing search tools and forms, only as needed to provide services, or where required by law.</p>
<h3>Listing data</h3><p>MLS&reg; listing data displayed on this site is provided through the MLS&reg; Reciprocity program of PropTx MLS&reg; for consumers\' personal, non-commercial use.</p>
<h3>Your rights</h3><p>You may request access to, correction of, or deletion of your personal information by contacting us at {SITE['phone']} or through the <a href="contact.html">contact page</a>.</p>'''
page('privacy.html', 'Privacy Policy | Christian Sorrell, RE/MAX Niagara Realty', 'Privacy policy for sellwithsorrell.com: how Christian Sorrell, RE/MAX Niagara Realty collects, uses and protects your personal information.',
     banner('Privacy policy', 'How your information is collected, used and protected.', [('Privacy Policy', 'privacy.html')], 'staircase') + two_col(priv),
     crumbs=[('Privacy Policy', 'privacy.html')])

# ---- 404
page('404.html', 'Page not found | Christian Sorrell', 'The page you were looking for could not be found.',
     banner('Page not found', 'Sorry, that page doesn\'t exist or has moved.', [('404', '404.html')], 'staircase')
     + '<section><div class="wrap center"><a class="btn btn-gold" href="index.html">Back to home</a> &nbsp; <a class="btn" href="recip.html">Search listings</a></div></section>', noindex=True)

# ---------------------------------------------------------------- sitemap / robots / manifest
pri = lambda s: '1.0' if s == 'index.html' else ('0.9' if s.startswith('homes-for-sale') or s in ('buying.html', 'selling.html', 'home-evaluation.html', 'recip.html') else '0.7')
urls = ''.join(f'<url><loc>{D}/{"" if s == "index.html" else s}</loc><lastmod>{TODAY}</lastmod><priority>{pri(s)}</priority></url>\n'
               for s, ni in PAGES if not ni)
open(os.path.join(OUT, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {D}/sitemap.xml\n')
open(os.path.join(OUT, 'site.webmanifest'), 'w').write(json.dumps({
    'name': 'Christian Sorrell | Niagara Real Estate', 'short_name': 'Sell with Sorrell', 'start_url': '/',
    'display': 'standalone', 'background_color': '#ffffff', 'theme_color': '#0e0e0e',
    'icons': [{'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]}, indent=1))
print(f'Built {len(PAGES)} pages')
