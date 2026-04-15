#!/usr/bin/env python3
"""
Auto-generate cover letters for all jobs in today's report.
Uses GPT-4o-mini (fast + cheap) to write tailored cover letters.
Output: memory/job-reports/YYYY-MM-DD-coverletters.md
"""

import os, json, re, time
from datetime import date
from openai import OpenAI

BASE       = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.join(BASE, "..", "memory", "job-reports")
TODAY      = date.today().isoformat()
SEEN_FILE  = os.path.join(BASE, "seen-jobs.json")

OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "")
client     = OpenAI(api_key=OPENAI_KEY)

# ── Yuwei's resume summary (condensed for prompt) ────────────────────────────
RESUME = """
Name: Yuwei Shang
Contact: New York | 949-508-8714 | ys3848@nyu.edu
Education: NYU, MS Econometrics (Sep 2023 – May 2025)
Skills: Python, SAS, SQL, R, Tableau, Excel, Adobe After Effects, Photoshop
Publication: "The Interest Hike of Fed: How Will It Influence China and The World Economy?" (EMFRM 2022)
Independent Music Producer & DJ: 50+ original tracks, 20M+ streams; DJ performances across China and U.S.

Experience:
- CHC Group USA | Operations Analyst | Feb 2026–Present (NYC)
  • Performance tracking for 7 fashion brands, 200–500+ SKUs via TikTok Shop
  • Analyzed livestream/sales metrics: engagement, conversion, campaign performance
  • Audience & market analysis; negotiated promotional pricing with brand partners

- AIYA Technology Consulting | Financial Analyst | Mar–Jun 2025 (NYC)
  • Analyzed 10 F&B accounts, generated 25% qualified leads, drove $1.2M revenue
  • Customized offerings for C-suite clients; improved ROI across $2M+ capital
  • Built budget-payback simulation tools in Excel; saved $250K misallocated spend
  • Created business documentation (Confluence/Excel); reduced onboarding time 40%

- Overseas Students Services Corp. | Business Analyst & Accounting Intern | Jan–Mar 2025 (NYC)
  • Reduced AR discrepancies 30%, recovered $180K; improved payment reconciliation
  • Automated financial reporting workflows; saved 120 hrs/quarter, $15K labor cost
  • Built compliance dashboards contributing to $300K in revenue gains

- PFPA Financial Consulting | Financial Analyst | Sep–Dec 2024 (Atlanta)
  • KMV/TIC credit rating model evaluation, backtesting, and stress-testing
  • Improved model credibility 15%; reduced losses $400K/year
  • Identified $200K+ portfolio reallocation opportunities for institutional clients

- Flywire (Global Payments SaaS) | Financial Analyst Intern | May–Aug 2024 (Shanghai)
  • Implemented project tracking system; improved execution efficiency 20%, saved $60K
  • Ran A/B testing on 10+ campaigns; raised CTR 5%, improved ROI $80K

- ICBC Wuhan Branch | Financial Analyst Intern | Jun–Aug 2023 (Hubei)
  • Reduced credit document processing time 25%; digitized client records
  • Tiered client risk profiles; unlocked $3.5M wealth management opportunities

- PricewaterhouseCoopers | Equity Research Intern | May–Jun 2022 (Beijing)
  • Data analysis and statistical testing (Excel, Stata) for healthcare equity research
  • Enabled $500K capital reallocation via trend forecasting
"""

SYSTEM_PROMPT = """You are an expert career coach and cover letter writer.
Write professional, concise, and highly personalized cover letters.
Guidelines:
- 3 paragraphs, ~250 words total
- Opening: mention the specific role and company; show genuine interest
- Middle: pick 2-3 most relevant experiences from resume that match this job; be specific with numbers/impact
- Closing: confident call to action, mention visa status naturally (on OPT, eligible for H-1B sponsorship)
- Tone: professional but not stiff; confident, direct
- Do NOT use generic phrases like "I am writing to express my interest" — be creative
- Do NOT include date, address headers — just the letter body starting with "Dear Hiring Manager,"
"""

def load_jobs_from_report():
    """Parse today's markdown report to extract job list."""
    report_path = os.path.join(REPORT_DIR, f"{TODAY}.md")
    if not os.path.exists(report_path):
        print(f"❌ No report found at {report_path}")
        print("   Run job-search.py first!")
        return []

    jobs = []
    with open(report_path) as f:
        content = f.read()

    # Parse job blocks: ### N. Title\n🏢 **Company** | 📍 Location ...\n🔗 link
    blocks = re.findall(
        r'###\s+\d+\.\s+(.+?)\n'
        r'🏢\s+\*\*(.+?)\*\*\s+\|[^|\n]+\|\s+🛂[^\n]+\n'
        r'🔗\s+(\S+)',
        content
    )
    for title, company, link in blocks:
        jobs.append({
            "title": title.strip(),
            "company": company.strip(),
            "link": link.strip(),
        })

    print(f"  Parsed {len(jobs)} jobs from today's report")
    return jobs

def fetch_job_description(link: str) -> str:
    """Try to fetch a short job description snippet from LinkedIn."""
    if "linkedin.com" not in link:
        return ""
    try:
        import requests
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }
        job_id = link.rstrip("/").split("/")[-1]
        api_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
        r = requests.get(api_url, headers=headers, timeout=10)
        if r.status_code == 200:
            # Strip HTML tags
            text = re.sub(r'<[^>]+>', ' ', r.text)
            text = re.sub(r'\s+', ' ', text).strip()
            return text[:1500]  # First 1500 chars
    except Exception:
        pass
    return ""

def generate_cover_letter(job: dict, jd_snippet: str = "") -> str:
    """Call GPT-4o-mini to generate a cover letter."""
    jd_context = f"\nJob Description excerpt:\n{jd_snippet}" if jd_snippet else ""

    user_prompt = f"""Write a cover letter for this job application:

Role: {job['title']}
Company: {job['company']}
{jd_context}

Applicant Resume:
{RESUME}

Write the cover letter body (starting with "Dear Hiring Manager,"):"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_prompt},
            ],
            max_tokens=500,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as ex:
        return f"[Error generating cover letter: {ex}]"

def main():
    print(f"✍️  Cover letter generator — {TODAY}")
    print(f"   Using: gpt-4o-mini\n")

    jobs = load_jobs_from_report()
    if not jobs:
        return

    output_path = os.path.join(REPORT_DIR, f"{TODAY}-coverletters.md")
    lines = [
        f"# ✍️ Cover Letters — {TODAY}",
        f"",
        f"**Generated for:** {len(jobs)} jobs | **Model:** gpt-4o-mini",
        f"",
        "---",
        "",
    ]

    for i, job in enumerate(jobs, 1):
        print(f"  [{i}/{len(jobs)}] {job['title']} @ {job['company']}")

        # Try to fetch JD for better personalization
        jd = fetch_job_description(job["link"])
        if jd:
            print(f"    ✓ Got JD snippet ({len(jd)} chars)")

        letter = generate_cover_letter(job, jd)

        lines += [
            f"## {i}. {job['title']} @ {job['company']}",
            f"🔗 {job['link']}",
            f"",
            letter,
            "",
            "---",
            "",
        ]

        # Save incrementally every 5 jobs
        if i % 5 == 0:
            with open(output_path, "w") as f:
                f.write("\n".join(lines))
            print(f"    💾 Saved progress ({i}/{len(jobs)})")

        time.sleep(0.5)  # gentle rate limit

    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    print(f"\n✅ All cover letters saved: {output_path}")
    print(f"   Total: {len(jobs)} letters generated")

if __name__ == "__main__":
    main()
