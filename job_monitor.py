job_monitor.py
import json
import os
import re
import hashlib
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

SOURCE_URL = "https://www.sarkariexam.com/category/hot-job/"
DATA_FILE = "seen_jobs.json"


def load_seen():
    if not os.path.exists(DATA_FILE):
        return set()

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except Exception:
        return set()


def save_seen(seen):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(seen), f, ensure_ascii=False, indent=2)


def get_page():
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; JobMonitor/1.0)"
    }

    response = requests.get(
        SOURCE_URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()
    return response.text


def extract_jobs(html):
    soup = BeautifulSoup(html, "html.parser")

    jobs = []

    for link in soup.find_all("a", href=True):
        title = " ".join(link.get_text(" ", strip=True).split())
        url = link.get("href", "").strip()

        if not title or not url:
            continue

        if url.startswith("/"):
            url = "https://www.sarkariexam.com" + url

        if "sarkariexam.com" not in url:
            continue

        # केवल meaningful job/update links
        keywords = [
            "online-form",
            "recruitment",
            "bharti",
            "vacancy",
            "job",
            "result",
            "admit-card",
            "answer-key"
        ]

        if not any(k in url.lower() for k in keywords):
            continue

        job_id = hashlib.sha256(
            url.encode("utf-8")
        ).hexdigest()[:16]

        jobs.append({
            "id": job_id,
            "title": title,
            "url": url
        })

    # Duplicate links हटाएँ
    unique = {}

    for job in jobs:
        unique[job["url"]] = job

    return list(unique.values())


def make_message(job):
    now = datetime.now(timezone.utc).strftime(
        "%d-%m-%Y %H:%M UTC"
    )

    return f"""🚨 नई JOB UPDATE

📌 {job['title']}

🔗 पूरी जानकारी:
{job['url']}

⏰ Detected: {now}

⚠️ आवेदन करने से पहले Official Notification जरूर पढ़ें।

📢 BALAJI EMITRA & CSC CENTER
"""


def main():
    print("SarkariExam monitoring started...")

    html = get_page()
    jobs = extract_jobs(html)

    print(f"Jobs found: {len(jobs)}")

    seen = load_seen()
    new_jobs = []

    for job in jobs:
        if job["id"] not in seen:
            new_jobs.append(job)
            seen.add(job["id"])

    save_seen(seen)

    print(f"New jobs: {len(new_jobs)}")

    for job in new_jobs:
        print("=" * 60)
        print(make_message(job))
        print("=" * 60)


if __name__ == "__main__":
    main()
