import requests
import traceback

urls = [
    "https://www.sarkariexam.com/mobile/",
    "https://www.sarkariexam.com/category/hot-job/",
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

for url in urls:
    print("\n================================")
    print("TEST:", url)
    print("================================")

    try:
        r = requests.get(
            url,
            headers=headers,
            timeout=30,
            allow_redirects=True
        )

        print("STATUS:", r.status_code)
        print("FINAL URL:", r.url)
        print("PAGE SIZE:", len(r.text))

        if r.status_code == 200:
            print("✅ ACCESS OK")
        else:
            print("❌ ACCESS BLOCKED")

    except Exception:
        print("❌ REQUEST ERROR")
        traceback.print_exc()
