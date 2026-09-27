import sys
import traceback

print("====================================")
print("Sarkari Job Monitor - TEST")
print("====================================")

try:
    import requests
    from bs4 import BeautifulSoup

    print("✅ Python OK")
    print("✅ requests OK")
    print("✅ BeautifulSoup OK")

    url = "https://www.sarkariexam.com/category/hot-job/"

    print("🌐 Website checking...")
    print(url)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    print("HTTP Status:", response.status_code)
    print("Page size:", len(response.text))

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a", href=True)

    print("Links found:", len(links))

    print("====================================")
    print("TEST SUCCESSFUL")
    print("====================================")

except Exception as e:
    print("====================================")
    print("❌ ACTUAL ERROR")
    print("====================================")

    print("Error type:", type(e).__name__)
    print("Error:", str(e))

    print("")
    print("FULL TRACEBACK:")
    traceback.print_exc()

    sys.exit(1)
