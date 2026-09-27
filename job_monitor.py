import requests
import json
import hashlib
import xml.etree.ElementTree as ET
from html import unescape
import re

FEED_URL = "https://www.sarkariexam.com/feed/"
SEEN_FILE = "seen_jobs.json"

HEADERS = {
    "User-Agent": "SarkariJobMonitor/1.0"
}


def clean_text(text):
    if not text:
        return ""

    text = unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def load_seen():
    try:
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except Exception:
        return set()


def save_seen(seen):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen), f, ensure_ascii=False, indent=2)


def make_id(link, title):
    value = link or title
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def main():

    print("======================================")
    print("SARKARI EXAM RSS MONITOR")
    print("======================================")

    print("Feed:", FEED_URL)

    response = requests.get(
        FEED_URL,
        headers=HEADERS,
        timeout=30
    )

    print("STATUS:", response.status_code)

    response.raise_for_status()

    print("CONTENT TYPE:", response.headers.get("content-type"))
    print("FEED SIZE:", len(response.content))

    root = ET.fromstring(response.content)

    channel = root.find("channel")

    if channel is None:
        print("❌ RSS channel not found")
        return

    items = channel.findall("item")

    print("TOTAL RSS ITEMS:", len(items))

    seen = load_seen()

    new_jobs = []

    for item in items:

        title_element = item.find("title")
        link_element = item.find("link")
        description_element = item.find("description")
        date_element = item.find("pubDate")

        title = clean_text(
            title_element.text if title_element is not None else ""
        )

        link = (
            link_element.text.strip()
            if link_element is not None and link_element.text
            else ""
        )

        description = clean_text(
            description_element.text
            if description_element is not None
            else ""
        )

        pub_date = (
            date_element.text.strip()
            if date_element is not None and date_element.text
            else ""
        )

        job_id = make_id(link, title)

        if job_id in seen:
            continue

        new_jobs.append({
            "id": job_id,
            "title": title,
            "link": link,
            "description": description,
            "date": pub_date
        })

        seen.add(job_id)

    print("NEW JOBS:", len(new_jobs))

    if new_jobs:

        print("\n========== NEW JOBS ==========\n")

        for job in new_jobs:

            message = f"""
📢 नई सरकारी नौकरी अपडेट

🔹 {job['title']}

📅 तारीख: {job['date']}

🔗 लिंक:
{job['link']}

ℹ️ Sarkari Exam Update
"""

            print(message)

    else:
        print("ℹ️ कोई नई job नहीं मिली।")

    save_seen(seen)

    print("\n✅ Monitor completed successfully.")


if __name__ == "__main__":
    main()
