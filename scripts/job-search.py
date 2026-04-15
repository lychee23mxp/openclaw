#!/usr/bin/env python3
"""
Daily job search script for Yuwei Shang
Sources: LinkedIn (public guest API) + Himalayas + Remotive + Crypto RSS
Target: 50 new jobs/day, NYC + Remote, analyst/data/finance roles
"""

import json, os, re, time, feedparser, requests
from datetime import date
from html.parser import HTMLParser

BASE = os.path.dirname(os.path.abspath(__file__))
SEEN_FILE  = os.path.join(BASE, "seen-jobs.json")
REPORT_DIR = os.path.join(BASE, "..", "memory", "job-reports")
TARGET = 50
TODAY  = date.today().isoformat()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

LI_KEYWORDS = [
    "data analyst", "business analyst", "financial analyst",
    "operations analyst", "quantitative analyst", "data scientist",
    "strategy analyst", "product analyst",
]
LI_LOCATIONS = ["New York, NY", "United States"]  # US catches remote too

ANALYST_TERMS = ["analyst", "data scientist", "quant", "intelligence",
                 "scientist", "strategy", "operations"]

H1B_LIST = [
    "google","meta","amazon","microsoft","apple","netflix","uber","airbnb",
    "salesforce","oracle","ibm","intel","nvidia","bloomberg","palantir",
    "jpmorgan","j.p. morgan","goldman sachs","morgan stanley","citadel",
    "two sigma","jane street","blackrock","deloitte","pwc","kpmg","ey ",
    "coinbase","ripple","chainlink","consensys","openai","anthropic",
    "databricks","stripe","robinhood","plaid","accenture","mckinsey",
    "bain","bcg","capgemini","tata consultancy","infosys","cognizant",
    "bybit","binance","kraken","gemini","dydx","alchemy",
    "iheartmedia","walt disney","jpmc",
]

# ── Utils ─────────────────────────────────────────────────────────────────────
def load_seen():
    return set(json.load(open(SEEN_FILE))) if os.path.exists(SEEN_FILE) else set()

def save_seen(s):
    json.dump(list(s), open(SEEN_FILE, "w"))

def h1b(company):
    c = company.lower()
    return "✅ Known sponsor" if any(x in c for x in H1B_LIST) else "❓ Check"

def is_target(title):
    return any(t in title.lower() for t in ANALYST_TERMS)

def dedupe(jobs):
    seen, out = {}, []
    for j in jobs:
        key = f"{j['title'][:45].lower()}|{j['company'][:25].lower()}"
        if key not in seen:
            seen[key] = 1
            out.append(j)
    return out

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_html(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

# ── LinkedIn guest API ────────────────────────────────────────────────────────
def search_linkedin(keyword, location, start=0):
    url = (
        "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
        f"?keywords={requests.utils.quote(keyword)}"
        f"&location={requests.utils.quote(location)}"
        f"&start={start}&sortBy=DD"
    )
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        if r.status_code != 200:
            return []
        html = r.text
        jobs = []
        # Parse job cards from HTML
        cards = re.findall(
            r'data-entity-urn="urn:li:jobPosting:(\d+)".*?'
            r'<h3[^>]*class="base-search-card__title"[^>]*>\s*(.*?)\s*</h3>.*?'
            r'<h4[^>]*class="base-search-card__subtitle"[^>]*>.*?<a[^>]*>\s*(.*?)\s*</a>.*?'
            r'<span[^>]*class="job-search-card__location"[^>]*>\s*(.*?)\s*</span>',
            html, re.DOTALL
        )
        for job_id, title, company, loc in cards:
            title = strip_html(title).strip()
            company = strip_html(company).strip()
            loc = strip_html(loc).strip()
            if not is_target(title):
                continue
            jobs.append({
                "title": title,
                "company": company,
                "location": loc,
                "link": f"https://www.linkedin.com/jobs/view/{job_id}",
                "source": "LinkedIn",
                "id": f"li_{job_id}",
            })
        return jobs
    except Exception as ex:
        print(f"  LinkedIn error ({keyword}, {location}): {ex}")
        return []

# ── Himalayas ─────────────────────────────────────────────────────────────────
def search_himalayas():
    jobs = []
    for kw in LI_KEYWORDS:
        try:
            r = requests.get(
                f"https://himalayas.app/jobs/api?q={requests.utils.quote(kw)}&limit=25",
                timeout=12)
            if r.status_code != 200:
                continue
            for j in r.json().get("jobs", []):
                title = j.get("title", "")
                if not is_target(title):
                    continue
                locs = j.get("locationRestrictions", [])
                if locs and "United States" not in locs:
                    continue
                link = j.get("applicationLink") or j.get("guid", "")
                jobs.append({
                    "title": title,
                    "company": j.get("companyName", "Unknown"),
                    "location": "Remote (US)" if not locs else ", ".join(locs[:2]),
                    "link": link,
                    "source": "Himalayas",
                    "id": link,
                })
            time.sleep(0.3)
        except Exception as ex:
            print(f"  Himalayas error ({kw}): {ex}")
    return jobs

# ── Remotive ──────────────────────────────────────────────────────────────────
def search_remotive():
    jobs = []
    for kw in ["analyst", "data analyst", "financial analyst"]:
        try:
            r = requests.get(
                f"https://remotive.com/api/remote-jobs?search={requests.utils.quote(kw)}&limit=25",
                timeout=12)
            if r.status_code != 200:
                continue
            for j in r.json().get("jobs", []):
                title = j.get("title", "")
                if not is_target(title):
                    continue
                jobs.append({
                    "title": title,
                    "company": j.get("company_name", "Unknown"),
                    "location": "Remote",
                    "link": j.get("url", ""),
                    "source": "Remotive",
                    "id": str(j.get("id", "")),
                })
        except Exception as ex:
            print(f"  Remotive error ({kw}): {ex}")
    return jobs

# ── Crypto/Web3 RSS ───────────────────────────────────────────────────────────
def search_crypto_rss():
    jobs = []
    for name, url in [
        ("Crypto.jobs",   "https://crypto.jobs/jobs.rss"),
        ("Web3.career",   "https://web3.career/rss.xml"),
        ("CryptoJobsList","https://cryptojobslist.com/rss.xml"),
    ]:
        try:
            feed = feedparser.parse(url)
            for e in feed.entries[:50]:
                title = strip_html(e.get("title", "")).strip()
                if not is_target(title):
                    continue
                company = strip_html(getattr(e, "author", "")).strip() or "Unknown"
                link = e.get("link", "")
                jobs.append({
                    "title": title,
                    "company": company,
                    "location": "Remote/Web3",
                    "link": link,
                    "source": name,
                    "id": e.get("id", link),
                })
        except Exception as ex:
            print(f"  {name} error: {ex}")
    return jobs

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    os.makedirs(REPORT_DIR, exist_ok=True)
    seen = load_seen()
    all_jobs = []

    print(f"🔍 Job search — {TODAY}")

    # LinkedIn: 3 keywords × 2 locations = up to 60 results
    for kw in LI_KEYWORDS[:4]:
        for loc in LI_LOCATIONS:
            print(f"  LinkedIn: {kw} @ {loc}")
            all_jobs.extend(search_linkedin(kw, loc))
            time.sleep(0.8)

    print("  Himalayas...")
    all_jobs.extend(search_himalayas())

    print("  Remotive...")
    all_jobs.extend(search_remotive())

    print("  Crypto/Web3 RSS...")
    all_jobs.extend(search_crypto_rss())

    # Filter new + dedupe
    by_id   = {j["id"]: j for j in all_jobs if j["id"]}
    new_jobs = [j for jid, j in by_id.items() if jid not in seen]
    new_jobs = dedupe(new_jobs)
    print(f"  ✓ {len(new_jobs)} new jobs (from {len(all_jobs)} fetched)")

    selected = new_jobs[:TARGET]
    for j in selected:
        seen.add(j["id"])
    save_seen(seen)

    # ── Report ────────────────────────────────────────────────────────────────
    report_path = os.path.join(REPORT_DIR, f"{TODAY}.md")
    lines = [
        f"# 📋 Daily Job Report — {TODAY}",
        f"",
        f"**Found:** {len(new_jobs)} new | **Showing:** {len(selected)} | "
        f"**Profile:** Analyst roles | NYC + Remote | OPT→H-1B 2027",
        f"",
        "---",
        "",
    ]
    by_src = {}
    for j in selected:
        by_src.setdefault(j["source"], []).append(j)

    rank = 1
    for src, items in by_src.items():
        lines.append(f"## {src} ({len(items)})\n")
        for j in items:
            lines += [
                f"### {rank}. {j['title']}",
                f"🏢 **{j['company']}** | 📍 {j['location']} | 🛂 {h1b(j['company'])}",
                f"🔗 {j['link']}",
                "",
            ]
            rank += 1

    if not selected:
        lines.append("_No new jobs today._")

    report = "\n".join(lines)
    with open(report_path, "w") as f:
        f.write(report)
    print(f"✅ Report saved: {report_path}")

    # Telegram summary (top 15)
    print("\n=== SUMMARY ===")
    print(f"📋 求职日报 {TODAY} — {len(new_jobs)} 个新职位\n")
    for i, j in enumerate(selected[:15], 1):
        print(f"{i}. **{j['title']}** @ {j['company']}")
        print(f"   📍 {j['location']} | 🛂 {h1b(j['company'])} | [{j['source']}]")
        print(f"   {j['link']}\n")
    if len(selected) > 15:
        print(f"...还有 {len(selected)-15} 个，见完整报告")

if __name__ == "__main__":
    main()
