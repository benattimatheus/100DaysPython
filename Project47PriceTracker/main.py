import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

MY_EMAIL=os.environ["MY_EMAIL"]
PASSWORD=os.environ["PASSWORD"]

practice_url = "https://appbrewery.github.io/instant_pot/"
live_url = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Google Chrome\";v=\"144\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
}

response = requests.get(live_url, headers=headers)

page = response.content
soup = BeautifulSoup(page, "html.parser")

price = soup.find('span', class_='priceToPay').get_text()
price_number = float(price.split("$")[1])

print(price_number)

target_price = 101.99

product_name = soup.find('span', id='productTitle').get_text().strip()

print(product_name)

email_content = (f"The product {product_name} is now ${price_number}. The target price was set to ${target_price}."
                 f"\n{practice_url}")

if price_number < target_price:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=MY_EMAIL,
                            msg=f"Subject:Amazon Price Alert!\n\n{email_content}".encode("utf-8")
                            )