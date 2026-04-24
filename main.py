import requests
from bs4 import BeautifulSoup
import pandas as pd

companies = {
    "EMS": "EMSLIMITED",
    "VSTL": "VSTL",
    "PTC": "PTC"
}

def fetch_bse_html(scrip):
    url = f"https://www.bseindia.com/corporates/ann.html?scode={scrip}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        return res.text
    except Exception as e:
        print(f"Error fetching HTML for {scrip}: {e}")
        return ""

def extract_from_html(html, company):
    results = []

    soup = BeautifulSoup(html, "html.parser")

    rows = soup.find_all("tr")

    for row in rows:
        text = row.get_text().lower()

        if any(keyword in text for keyword in [
            "analyst", "investor", "conference call"
        ]):
            link_tag = row.find("a")
            link = ""

            if link_tag and link_tag.get("href"):
                link = "https://www.bseindia.com" + link_tag.get("href")

            results.append({
                "company": company,
                "text": row.get_text(strip=True),
                "link": link
            })

    return results

def run():
    all_data = []

    for name, code in companies.items():
        print(f"\nFetching {name}")

        html = fetch_bse_html(code)

        if not html:
            continue

        extracted = extract_from_html(html, name)

        print(f"{name} → Found {len(extracted)} relevant rows")

        all_data.extend(extracted)

    df = pd.DataFrame(all_data)

    if df.empty:
        print("No data found")
    else:
        print("Data found")

    df.to_csv("output.csv", index=False)
    print("output.csv created")

if __name__ == "__main__":
    run()
