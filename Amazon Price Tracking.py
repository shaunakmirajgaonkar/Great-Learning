import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
from dotenv import load_dotenv
import os

# Load environment variables (Make sure you have a .env file with EMAIL_USER and EMAIL_PASS)
load_dotenv()

def get_amazon_price(product_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15"
    }
    
    # Send request to Amazon page
    try:
        response = requests.get(product_url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error: Unable to fetch page. Status code {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract price using CSS selectors (Amazon structure may vary)
        price = soup.find('span', {'id': 'priceblock_ourprice'}) or soup.find('span', {'id': 'priceblock_dealprice'})

        if price:
            price_text = price.get_text().strip()
            print(f"Price found: {price_text}")
            # Convert price to float after removing non-numeric characters
            return float(price_text.replace('₹', '').replace(',', ''))
        else:
            print("Price not found")
            return None
    except Exception as e:
        print(f"Error fetching price for {product_url}: {e}")
        return None


def store_price_history(product_url, price):
    try:
        # Open CSV in append mode and write data
        with open('price_history.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now(), product_url, price])
            print(f"Price history saved: ₹{price}")
    except Exception as e:
        print(f"Error writing to CSV: {e}")


def send_email_notification(to_email, subject, message):
    from_email = os.getenv("EMAIL_USER")
    from_password = os.getenv("EMAIL_PASS")
    
    if not from_email or not from_password:
        print("Email credentials not set in .env")
        return

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")


def check_price_and_notify():
    try:
        # Replace with your Amazon product URL
        product_url = "https://www.amazon.in/iPhone-16-Pro-Max-256/dp/B0DGHYDZR9/ref=asc_df_B0DGHYDZR9/?tag=googleshopdes-21&linkCode=df0&hvadid=709962856229&hvpos=&hvnetw=g&hvrand=3759905284475149081&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9154203&hvtargid=pla-2375491031519&psc=1&mcid=83d6e60b0a453bcbb2fa274d70c5a591&gad_source=1"
        current_price = get_amazon_price(product_url)
        
        if current_price:
            print(f"Current price: ₹{current_price}")

            # Price threshold condition (adjust as needed)
            if current_price < 100:  # Example: Notify if price is below ₹100
                send_email_notification("recipient_email@gmail.com", 
                                         "Price Drop Alert!", 
                                         f"The price of your tracked product has dropped to ₹{current_price}.")
                store_price_history(product_url, current_price)
        else:
            print(f"Failed to retrieve price for {product_url}")
    except Exception as e:
        print(f"Error in check_price_and_notify: {e}")


# Schedule the price check every 24 hours
schedule.every(24).hours.do(check_price_and_notify)

# Run the scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)
