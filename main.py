import requests
import pandas as pd
from datetime import datetime

# Your companies mapping
companies = {
    "EMS": "EMSLIMITED",
    "VSTL": "VSTL",
    "PTC": "PTC"
}

def fetch_bse_announcements(scrip):
    url = f"https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w?pageno=1&strCat=Company%20Update&strPrevDate=&strScrip={scrip}&strSearch=P&strToDate=&strType=C"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    res = requests.get(url, headers=headers)
    return res.json()

def extract_relevant(data):
    results = []
    
    for item in data.get("Table", []):
        title = item.get("HEADLINE", "")
        
        if any(x in title.lower() for x in [
            "analyst", "investor meet", "conference call"
        ]):
            results.append({
                "title": title,
                "date": item.get("NEWSSUB"),
                "link": item.get("ATTACHMENTNAME")
            })
    
    return results

def run():
    all_data = []
    
    for name, code in companies.items():
        data = fetch_bse_announcements(code)
        filtered = extract_relevant(data)
        
        for f in filtered:
            f["company"] = name
            all_data.append(f)
    
    df = pd.DataFrame(all_data)
    df.to_csv("output.csv", index=False)

if __name__ == "__main__":
    run()
