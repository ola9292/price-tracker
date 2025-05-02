import requests
import os
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from fake_useragent import UserAgent
ua = UserAgent()

load_dotenv()
my_email = os.getenv('EMAIL_ADDRESS') or os.environ.get('EMAIL_ADDRESS')
password = os.getenv('EMAIL_PASSWORD') or os.environ.get('EMAIL_PASSWORD')
smtp_address = os.getenv('SMTP_ADDRESS') or os.environ.get('SMTP_ADDRESS')
# print(my_email)
import requests
target_price = 100
URL = "https://www.amazon.com/Armaf-Urban-Elixir-Parfum-Spray/dp/B0CFVF94SN?crid=2YJT2QT0IGTUR&dib=eyJ2IjoiMSJ9.niL_u3g8oQnj9HkeLIEoW5DPTolAj2F9yGUfRylzZlrXwxicTV1QPkxF3fcI95TqiKn-7NfgBCEZRj0yrqv_6uMwtQ8iP9HzBaiO7PG0glrdPaSNMraBHhO9xpInI0a7rLME10DTsdc-N4DP-wH6a_5sr-1rxhkSb_Ijiz71mhs4f08M6x6rbw44n7UMnKhksE64LuetwRGYcqwZ1RD9HDF604AvI0v4rFKyZEVhRzMQ9nlzag_Yale_3O1m5Hw0zpk0arbPUBzVcKYECwRnVvq8Y2LciOpPKwhuEQvlUqQ.DQXFLuxAuiVGrtiI-n8w0xQft47j1cUTHGKvTmdPwkM&dib_tag=se&keywords=club%2Bde%2Bnuit%2Bintense%2Bman&qid=1746141177&sprefix=club%2Bde%2Caps%2C375&sr=8-2&th=1"

# Full headers would look something like this
header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,de;q=0.8,fr;q=0.6,en;q=0.4,ja;q=0.2",
    "Dnt": "1",
    "Priority": "u=1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": ua.random,
    #"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
}

response = requests.get(url=URL, headers=header)
response.raise_for_status()

amazon_webpage = response.text
print(f"Page length: {len(amazon_webpage)}")  # Log HTML size
if "captcha" in amazon_webpage.lower():
    print("CAPTCHA detected")
    exit(1)
soup = BeautifulSoup(amazon_webpage, 'html.parser')

# price_whole = soup.find(name="span", class_="aok-offscreen").getText()
# print(price_whole.split('$')[1])
product_title = soup.find(name="span", class_="product-title-word-break").getText()
# print(product_title)

whole_price = soup.find(name="span", class_="a-price-whole").getText()
fraction_price = soup.find(name="span", class_="a-price-fraction").getText()
price = float(f"{whole_price}{fraction_price}")
# print(type(price))
# print(whole_price)
# print(fraction_price)
if price < target_price:
        message = MIMEMultipart()
        message['From'] = my_email
        message['To'] = "olamide.kazeem@yahoo.com"
        message['Subject'] = "Price Drop Alert!"

        body = f"{product_title.strip()} has dropped to {price}, Hurry and buy now! \n{URL}"
        
        message.attach(MIMEText(body, 'plain'))
        
        # Send email
        connection = smtplib.SMTP(smtp_address)
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email, 
            to_addrs="olamide.kazeem@yahoo.com", 
            msg=message.as_string()
        )
        connection.close()
        
