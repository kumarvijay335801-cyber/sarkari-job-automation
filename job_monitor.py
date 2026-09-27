import requests

BASE = "https://www.sarkariexam.com"

urls = [
    BASE + "/feed/",
    BASE + "/feed/rss/",
    BASE + "/rss/",
    BASE + "/wp-json/",
    BASE + "/wp-json/wp/v2/posts",
    BASE + "/wp-json/wp/v2/categories",
    BASE + "/sitemap.xml",
    BASE + "/post-sitemap.xml",
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

for url in urls:
    print("\n======================================")
    print("TEST:", url)
    print("======================================")

    try:
        r = requests.get(
            url,
            headers=headers,
            timeout=30,
            allow_redirects=True
        )

        print("STATUS:", r.status_code)
        print("FINAL URL:", r.url)
        print("CONTENT TYPE:", r.headers.get("content-type"))
        print("PAGE SIZE:", len(r.content))

        if r.status_code == 200:
            print("✅ ACCESS OK")
            print("PREVIEW:")
            print(r.text[:300].replace("\n", " "))

        elif r.status_code == 403:
            print("❌ BLOCKED (403)")

        elif r.status_code == 404:
            print("❌ NOT FOUND (404)")

        else:
            print("⚠️ OTHER STATUS")

    except Exception as e:
        print("❌ ERROR:", type(e).__name__, str(e))
