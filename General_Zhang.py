from bs4 import BeautifulSoup as bs
import requests

url = "https://en.wikipedia.org/wiki/Zhang_Zizhong"
data = requests.get(url).text
soup = bs(data, 'html.parser')

tag = soup.find("body")
info_boxes = tag.find(class_="infobox vcard")
info_rows = info_boxes.find_all("tr")

General_info = {}

for index, row in enumerate(info_rows):
    if index <= 1:
        continue
    elif index == 2:
        General_info["姓名"] = info_boxes.find("div", attrs={"class": "nickname"}).get_text()

    else:
        dict_key = row.find("th").get_text().replace("\xa0", " ")
        dict_value = row.find("td").get_text(" ", strip=True).replace("\xa0", " ").replace("†", "（殉国）")
        General_info[dict_key] = dict_value


from openpyxl import Workbook, load_workbook

wb = Workbook()
ws = wb.active
ws.title = "general_info"

heading = [k for k in General_info.keys()]

ws.append(heading)
ws.append([v for v in General_info.values()])

wb.save("general_info.xlsx")