"""Static checks for the DBE GitHub Pages project home (no external dependencies)."""
from hashlib import sha1
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parents[1]
DIMENSIONS_BLOB = "38868b59145591d978f2412d875ab604a711d884"

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.scripts = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            assert attrs["id"] not in self.ids
            self.ids.add(attrs["id"])
        if tag == "a":
            assert attrs.get("href")
            self.links.append(attrs["href"])
        if tag == "script" and attrs.get("src"):
            self.scripts.append(attrs["src"])

def test_landing_links_and_anchors():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    page = Links()
    page.feed(html)
    assert {"main", "explore", "projects"} <= page.ids
    assert not page.scripts
    for href in page.links:
        p = urlparse(href)
        assert p.scheme in ("", "https"), href
        if p.scheme:
            assert p.netloc == "github.com", href
        elif href.startswith("#"):
            assert href[1:] in page.ids, href
        else:
            target = (ROOT / unquote(p.path)).resolve()
            assert target.is_relative_to(ROOT.resolve()), href
            if target.is_dir():
                target /= "index.html"
            assert target.is_file(), href
    assert "./research/lab.html" in page.links
    assert "./dimensions/" in page.links
    assert not any(x.startswith("./navigator") for x in page.links)
    for branch in ("SDBES", "feature/research-grade-physics", "dimensions-beyond-energy"):
        assert f"https://github.com/pjrny/DBE_V0/blob/{branch}/README.md" in html
    assert "Dimension G" in html
    assert "Web deployment pending" in html

def test_dimensions_mirror_is_original():
    data = (ROOT / "dimensions" / "index.html").read_bytes()
    blob = sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
    assert blob == DIMENSIONS_BLOB
    assert b"Dimensions Beyond Energy" in data

def test_existing_observatory_assets_unchanged_and_present():
    lab = (ROOT / "research" / "lab.html")
    js = (ROOT / "research" / "lab.js")
    assert lab.is_file() and js.is_file()
    assert 'src="lab.js"' in lab.read_text(encoding="utf-8")
    source = js.read_text(encoding="utf-8")
    for name in ("catalog.json", "claims.json", "versions.json", "reviews.json", "ledger.json"):
        assert name in source
        assert (ROOT / "research" / name).is_file()
