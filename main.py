import requests
import pandas as pd

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
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        return res.json()
    except Exception as e:
        print(f"Error fetching {scrip}: {e}")
        return {}

def extract_relevant(data):
    results = []

    try:
        for item in data.get("Table", []):
            title = item.get("HEADLINE", "")

            if any(x in title.lower() for x in [
                "analyst", "investor", "conference"
            ]):
                results.append({
                    "title": title,
                    "date": item.get("NEWSSUB"),
                    "link": item.get("ATTACHMENTNAME")
                })
    except Exception as e:
        print(f"Error extracting: {e}")

    return results

def run():
    all_data = []

    for name, code in companies.items():
        print(f"Fetching {name}")

        data = fetch_bse_announcements(code)
        filtered = extract_relevant(data)

        for f in filtered:
            f["company"] = name
            all_data.append(f)

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv("output.csv", index=False)
        print("Data saved to output.csv")
    else:
        print("No data found")

if __name__ == "__main__":
    run()
