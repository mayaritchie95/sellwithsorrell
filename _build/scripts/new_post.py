#!/usr/bin/env python3
"""Write one new SEO blog post for sellwithsorrell.com with the Claude API.

Run by .github/workflows/weekly-blog.yml every week (or by hand):
    ANTHROPIC_API_KEY=sk-... python3 scripts/new_post.py

Saves posts/YYYY-MM-DD-<slug>.json. Then source/build.py turns it into a page,
adds it to the blog index and sitemap. Nothing is published unless the post
passes the checks below.
"""
import datetime, html, json, os, re, sys, urllib.request, urllib.error
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(ROOT, 'posts')
MODEL = os.environ.get('BLOG_MODEL', 'claude-sonnet-5-5')
IMAGES = ['card-buyers', 'card-sellers', 'card-search', 'kitchen-800', 'living-green-800', 'hero-800', 'staircase-420']
CATEGORIES = ['Buying', 'Selling', 'Investing', 'Market insight', 'Living in Niagara']
LINKS = {  # internal pages the writer may link to
    'buying.html': 'Buyer guide', 'selling.html': 'Seller guide', 'investing.html': 'Investing',
    'home-evaluation.html': 'Free home evaluation', 'mortgage-calculator.html': 'Mortgage calculator',
    'home-finder.html': 'Home Finder', 'recip.html': 'Search listings', 'watch-list.html': 'Listing alerts',
    'contact.html': 'Contact Christian', 'neighbour-sold.html': 'What your neighbour sold for',
    'marketing-strategy.html': 'Marketing strategy', 'testimonials.html': 'Client reviews',
    **{f'homes-for-sale-{c}.html': c.replace('-', ' ').title() + ' homes for sale' for c in
       ['st-catharines', 'niagara-falls', 'thorold', 'welland', 'port-colborne', 'fort-erie', 'pelham', 'hamilton', 'grimsby', 'lincoln']},
}
ALLOWED_TAGS = {'p', 'h2', 'h3', 'ul', 'ol', 'li', 'strong', 'em', 'a'}


def existing():
    out = []
    for fn in sorted(os.listdir(POSTS)):
        if fn.endswith('.json'):
            p = json.load(open(os.path.join(POSTS, fn)))
            out.append(p)
    return out


TOPICS = os.path.join(ROOT, 'topics.txt')


def next_topic(prev):
    """First topic in topics.txt that no post has been written for yet (or None)."""
    if not os.path.exists(TOPICS):
        return None
    done = {p.get('topic', '').strip().lower() for p in prev}
    for line in open(TOPICS, encoding='utf-8'):
        t = line.strip()
        if t and not t.startswith('#') and t.lower() not in done:
            return t
    return None


def prompt(prev, topic=None):
    titles = '\n'.join(f'- {p["title"]}' for p in prev)
    links = '\n'.join(f'- {k} ({v})' for k, v in LINKS.items())
    if topic:
        topic_line = (f'Write ONE new evergreen blog post on this topic: "{topic}". Keep the title close to it '
                      '(you may adjust wording for search). Aim it at a local real estate search phrase.')
    else:
        topic_line = ('Write ONE new evergreen blog post that will help the site rank in Google for a local real estate '
                      'search phrase (for example a "how to", checklist, guide or comparison aimed at Niagara buyers, '
                      'sellers, landlords or people moving to the area).')
    return f"""You write blog posts for the website of Christian Sorrell, a REALTOR® with RE/MAX Niagara Realty Ltd. in St. Catharines, Ontario, serving the Niagara region and Hamilton.

{topic_line}

Rules:
- It must be clearly different from these existing posts:
{titles}
- 600-800 words, friendly and professional, written in Christian's first person where natural ("I", "my clients").
- Use the main keyword phrase naturally in the title, first paragraph and one H2. Include "Niagara" or a Niagara city where it fits.
- Structure with <h2> sections (and <h3> if useful), short paragraphs, and at least one list.
- Include 2-4 internal links using ONLY these relative URLs:
{links}
- End with a short call to action linking to contact.html or another relevant page.
- Do NOT invent statistics, prices, interest rates, tax amounts, program limits, dates, laws or quotes. Stay general where details change over time, and suggest confirming specifics with a lender, lawyer or accountant.
- Do NOT name specific businesses, schools, developments or people.
- Allowed HTML tags in content: p, h2, h3, ul, ol, li, strong, em, a (href only). No h1, images, scripts or styles.

Reply with ONLY a JSON object, no other text:
{{"title": "...(max 65 characters)",
  "slug": "blog-lowercase-words-with-hyphens",
  "category": one of {json.dumps(CATEGORIES)},
  "excerpt": "...(meta description, 120-155 characters)",
  "content": "<p>...</p>..."}}"""


def call_claude(text):
    mock = os.environ.get('NEW_POST_MOCK_FILE')
    if mock:
        return open(mock).read()
    key = (os.environ.get('ANTHROPIC_API_KEY') or '').strip()  # ignore stray spaces/newlines from pasting
    if not key:
        sys.exit('ANTHROPIC_API_KEY is not set')
    req = urllib.request.Request('https://api.anthropic.com/v1/messages', method='POST',
        headers={'x-api-key': key, 'anthropic-version': '2023-06-01', 'content-type': 'application/json'},
        data=json.dumps({'model': MODEL, 'max_tokens': 4000,
                         'messages': [{'role': 'user', 'content': text}]}).encode())
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f'Claude API error {e.code}: {e.read().decode(errors="replace")[:300]}')
    return ''.join(b.get('text', '') for b in data['content'])


class Clean(HTMLParser):
    """Keep only allowed tags; drop links that aren't approved internal pages."""
    def __init__(self):
        super().__init__(convert_charrefs=True); self.out = []; self.links = 0; self.skip_a = []
    def handle_starttag(self, tag, attrs):
        if tag not in ALLOWED_TAGS: return
        if tag == 'a':
            href = dict(attrs).get('href', '')
            ok = href in LINKS
            self.skip_a.append(not ok)
            if not ok: return
            self.links += 1
            self.out.append(f'<a href="{href}">'); return
        self.out.append(f'<{tag}>')
    def handle_endtag(self, tag):
        if tag not in ALLOWED_TAGS: return
        if tag == 'a':
            if self.skip_a and self.skip_a.pop(): return
        self.out.append(f'</{tag}>')
    def handle_data(self, data):
        self.out.append(html.escape(data, quote=False))


def main():
    prev = existing()
    topic = next_topic(prev)
    if topic:
        print(f'Topic from queue: {topic}')
    raw = call_claude(prompt(prev, topic))
    m = re.search(r'\{.*\}', raw, re.S)
    if not m: sys.exit('No JSON in response')
    post = json.loads(m.group(0))

    title = post['title'].strip()
    slug = re.sub(r'[^a-z0-9-]+', '-', post['slug'].lower()).strip('-')
    if not slug.startswith('blog-'): slug = 'blog-' + slug
    slug = slug[:80].rstrip('-') + '.html'
    category = post['category'] if post['category'] in CATEGORIES else 'Market insight'
    excerpt = post['excerpt'].strip()

    c = Clean(); c.feed(post['content']); content = ''.join(c.out)
    words = len(re.sub('<[^>]+>', ' ', content).split())

    problems = []
    if words < 450: problems.append(f'too short ({words} words)')
    if content.count('<h2>') < 2: problems.append('needs at least two H2 sections')
    if c.links < 2: problems.append('needs at least two internal links')
    if any(p['slug'] == slug for p in prev): problems.append('slug already used')
    if any(p['title'].lower() == title.lower() for p in prev): problems.append('title already used')
    if not (60 <= len(excerpt) <= 170): problems.append('excerpt length')
    if problems:
        sys.exit('Post rejected: ' + '; '.join(problems))

    used = [p['image'] for p in prev]
    image = min(IMAGES, key=lambda i: (used.count(i), IMAGES.index(i)))
    date = datetime.date.today().isoformat()
    out = {'topic': topic or '', 'slug': slug, 'title': html.escape(title, quote=False), 'image': image, 'category': category,
           'excerpt': html.escape(excerpt, quote=False), 'date': date,
           'content': content + '<p><em>This article is general information, not legal, tax or financial advice.</em></p>'}
    path = os.path.join(POSTS, f'{date}-{slug[:-5]}.json')
    json.dump(out, open(path, 'w'), indent=1, ensure_ascii=False)
    print(f'New post: {title} ({words} words) -> {os.path.relpath(path, ROOT)}')
    gh = os.environ.get('GITHUB_OUTPUT')
    if gh:
        open(gh, 'a').write(f'title={title}\n')


if __name__ == '__main__':
    main()
