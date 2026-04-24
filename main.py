import requests
import pandas as pd

# Full company mapping
companies = {
    # PRIMARY
    "ARAPL": "AFFORDABLE",
    "EFC": "EFCIL",
    "EMS": "EMSLIMITED",
    "PTC": "PTC",
    "TAC": "TAC",
    "VSTL": "VSTL",
    "VGIL": "VGINFOTECH",

    # SECONDARY
    "ALPEX": "ALPEXSOLAR",
    "ASIAN": "ASIANTILES",
    "DENTA": "DENTA",
    "DRONACHARYA": "DRONACHARYA",
    "KESAR": "KESARPE",
    "MARKOLINES": "MARKOLINES",
    "SHARAT": "SHINDL",
    "SKM": "SKM"
}

def fetch_bse_announcements(scrip):
    url = f"https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w?pageno=1&strCat=Company%20Update&strPrevDate=&strScrip={scrip}&strSearch=P&strToDate=&strType=C"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        print(f"Status for {scrip}: {res.status_code}")
        return res.json()
    except Exception as e:
        print(f"Error fetching {scrip}: {e}")
        return {}

def extract_relevant(data, company):
    results = []

    try:
        table = data.get("Table", [])
        print(f"{company} → Total announcements fetched: {len(table)}")

        for item in table:
            title = item.get("HEADLINE", "").lower()

            # Expanded keyword matching
            if any(keyword in title for keyword in [
                "analyst",
                "investor meet",
                "investor meeting",
                "conference call",
                "earnings call"
            ]):
                results.append({
                    "company": company,
                    "title": item.get("HEADLINE"),
                    "date": item.get("NEWSSUB"),
                    "link": item.get("ATTACHMENTNAME")
                })

    except Exception as e:
        print(f"Error extracting for {company}: {e}")

    print(f"{company} → Filtered relevant items: {len(results)}")
    return results

def run():
    all_data = []

    for name, code in companies.items():
        print(f"\n🔍 Fetching data for {name}")

        data = fetch_bse_announcements(code)

        print(f"Raw data for {name}: {data}")

        filtered = extract_relevant(data, name)

        print(f"Filtered results for {name}: {filtered}")

        all_data.extend(filtered)

    # Always create file
    df = pd.DataFrame(all_data)

    if df.empty:
        print("\n⚠️ No relevant data found. Creating empty output.csv")
    else:
        print("\n✅ Data found. Writing to output.csv")

    df.to_csv("output.csv", index=False)
    print("📁 output.csv created successfully")

if __name__ == "__main__":
    run()
