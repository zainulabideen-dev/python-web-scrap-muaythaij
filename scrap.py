import json
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from colour import Color

col_prd_name = []
col_brand = []
col_cat = []
col_price = []
col_color = []
col_size = []
col_prod_img = []
col_prod_url = []

def getDataFromPage(url):
    print("Scrapping "+ url)
    r = requests.get(url)
    soup = bs(r.content, "html.parser")

    prod_ul = soup.find("ul", {"id": "product-grid"})
    prod_li = prod_ul.find_all("li")

    print("total prod in this page is :"+ str(len(prod_li)))

    meta_script = ""
    for each in soup.find_all("script"):
        if("var meta =" in each.getText()):
            meta_script = each.getText()

    data_str = (meta_script.split("var meta = "))[1].split(',"page":')[0]+"}"
    data_json = json.loads(data_str)

    for each in prod_li:
        prod_img = each.find("img", {"class": "motion-reduce"})["src"]
        prod_img_url = "https:"+prod_img

        prod_url = each.find("a", {"class": "full-unstyled-link"})
        prod_url_http = "https://muaythaij.com/"+prod_url["href"]
        prod_name = prod_url.getText().strip()

        prod_brand = each.find("div", {"class": "caption-with-letter-spacing light"}).getText()
        prod_price = each.find("span", {"class": "price-item price-item--regular"}).getText().strip()

        uid_split = prod_url["id"].split("-")
        uid = uid_split[len(uid_split)-1]

        prod_type = ""
        prod_color = []
        prod_size = []

        for val in data_json["products"]:
            if(str(val["id"])==str(uid)):
                prod_type = val["type"]
                for variant in val["variants"]:
                    try:
                        pub_title = variant["public_title"].split("/")
                        
                        for item in pub_title:
                            try:
                                Color(str(item).strip())
                                if str(item).strip() not in prod_color:
                                    prod_color.append(str(item).strip())
                            except:
                                if str(item).strip() not in prod_size:
                                    prod_size.append(str(item).strip())
                    except:
                        print("-> pass")


        
        col_prd_name.append(prod_name)
        col_brand.append(prod_brand)
        col_cat.append(prod_type)
        col_price.append(prod_price)
        col_color.append(",".join(prod_color))
        col_size.append(",".join(prod_size))
        col_prod_img.append(prod_img_url)
        col_prod_url.append(prod_url_http)


    col_name_dict = {
        "Name": col_prd_name,
        "Brand": col_brand,
        "Type": col_cat,
        "Price": col_price,
        "Color": col_color,
        "Size": col_size,
        "ProductImage": col_prod_img,
        "ProductURL": col_prod_url,
    }

    df = pd.DataFrame(col_name_dict)
    df.to_csv('output.csv')
    print('csv created / updated ...')
        


def createPages():
    for i in range(17):
        getDataFromPage("https://muaythaij.com/collections/all?page="+str(i+1)+"&sort_by=best-selling")


createPages()
