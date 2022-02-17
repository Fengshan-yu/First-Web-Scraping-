from bs4 import BeautifulSoup as bs
import requests

url = "https://en.wikipedia.org/wiki/Tang_Enbo"
data = requests.get(url).text
soup = bs(data, 'html.parser')

tag = soup.find("body")
General_info_list=[]
general_info = {}

info_boxes = tag.find(class_="infobox vcard")
info_rows = info_boxes.find_all("tr")


def get_content_row(row_data):
    if row_data.find("li"):
        return [li.get_text(" ", strip=True).replace("\xa0", " ").replace("†", "（殉国）") for li in
                row_data.find_all("li")]
    else:
        return row.find("td").get_text(" ", strip=True).replace("\xa0", " ").replace("†", "（殉国）")


for index, row in enumerate(info_rows):
    if index == 0:
        general_info["title"] = row.find("div", attrs={"class": "fn"}).get_text()
    elif len(row) == 0:
        continue
    else:
        try:
            dict_key = row.find("th").get_text(" ", strip=True).replace("\xa0", " ")
            dict_value = get_content_row(row.find("td"))
            general_info[dict_key] = dict_value

        except Exception as e:
            print(e)

General_info_list.append(general_info)

import json

def save_data(title, data):
    with open(title, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

save_data("General_info_list.json", General_info_list)

import pandas as pd
df=pd.DataFrame(General_info_list)
df.to_csv("General_info_list_021722.csv")

