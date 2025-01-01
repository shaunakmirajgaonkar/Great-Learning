from tkinter import *
from tkinter import messagebox
from bs4 import BeautifulSoup
import requests
import webbrowser

# Headers for HTTP requests
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15"
}

# Global variables to store URLs
urls = {
    "flipkart": "",
    "ebay": "",
    "amazon": "",
    "olx": "",
    "croma": "",
}

# Flipkart Function
def fetch_flipkart(name):
    try:
        name1 = name.replace(" ", "+")
        urls["flipkart"] = f'https://www.flipkart.com/search?q={name1}'
        res = requests.get(urls["flipkart"], headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        product_name = soup.select('._4rR01T')[0].getText().strip()
        product_price = soup.select('._1_WHN1')[0].getText().strip()

        return f"{product_name}\nPrice: {product_price}\n"
    except Exception:
        return "Product Not Found on Flipkart."

# eBay Function
def fetch_ebay(name):
    try:
        name1 = name.replace(" ", "+")
        urls["ebay"] = f'https://www.ebay.com/sch/i.html?_nkw={name1}'
        res = requests.get(urls["ebay"], headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        product_name = soup.select('.s-item__title')[0].getText().strip()
        product_price = soup.select('.s-item__price')[0].getText().strip()

        return f"{product_name}\nPrice: {product_price}\n"
    except Exception:
        return "Product Not Found on eBay."

# Amazon Function
def fetch_amazon(name):
    try:
        name1 = name.replace(" ", "-")
        urls["amazon"] = f'https://www.amazon.in/{name1}/s?k={name1}'
        res = requests.get(urls["amazon"], headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        product_name = soup.select('.a-color-base.a-text-normal')[0].getText().strip()
        product_price = soup.select('.a-price-whole')[0].getText().strip()

        return f"{product_name}\nPrice: ₹{product_price}\n"
    except Exception:
        return "Product Not Found on Amazon."

# OLX Function
def fetch_olx(name):
    try:
        name1 = name.replace(" ", "-")
        urls["olx"] = f'https://www.olx.in/items/q-{name1}'
        res = requests.get(urls["olx"], headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        product_name = soup.select('._2tW1I')[0].getText().strip()
        product_price = soup.select('._89yzn')[0].getText().strip()

        return f"{product_name}\nPrice: {product_price}\n"
    except Exception:
        return "Product Not Found on OLX."

# Croma Function
def fetch_croma(name):
    try:
        name1 = name.replace(" ", "-")
        urls["croma"] = f'https://www.croma.com/search/?text={name1}'
        res = requests.get(urls["croma"], headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        product_name = soup.select('.product-title')[0].getText().strip()
        product_price = soup.select('.pdpPrice')[0].getText().strip()

        return f"{product_name}\nPrice: ₹{product_price}\n"
    except Exception:
        return "Product Not Found on Croma."

# Open URLs Function
def open_url(event):
    selected_site = site_choice.get()
    if selected_site in urls and urls[selected_site]:
        webbrowser.open_new(urls[selected_site])
    else:
        messagebox.showinfo("Info", f"No URL available for {selected_site.capitalize()}.")

# Search Function
def search():
    search_button.place_forget()

    # Clear boxes before displaying results
    box1.delete(1.0, "end")
    box2.delete(1.0, "end")
    box3.delete(1.0, "end")
    box4.delete(1.0, "end")
    box5.delete(1.0, "end")

    # Fetch product data from each site
    box1.insert(1.0, fetch_flipkart(product_name.get()))
    box2.insert(1.0, fetch_ebay(product_name.get()))
    box3.insert(1.0, fetch_amazon(product_name.get()))
    box4.insert(1.0, fetch_olx(product_name.get()))
    box5.insert(1.0, fetch_croma(product_name.get()))

# GUI Setup
window = Tk()
window.wm_title("Price Comparison")
window.minsize(1500, 800)

# Widgets
Label(window, text="Enter Product Name:", font=("Courier", 10)).place(relx=0.2, rely=0.1, anchor="center")
product_name = StringVar()
Entry(window, textvariable=product_name, width=50).place(relx=0.5, rely=0.1, anchor="center")

search_button = Button(window, text="Search", width=12, command=search)
search_button.place(relx=0.5, rely=0.2, anchor="center")

# Result Boxes
box1 = Text(window, height=7, width=50)
box1.place(relx=0.2, rely=0.4, anchor="center")

box2 = Text(window, height=7, width=50)
box2.place(relx=0.5, rely=0.4, anchor="center")

box3 = Text(window, height=7, width=50)
box3.place(relx=0.8, rely=0.4, anchor="center")

box4 = Text(window, height=7, width=50)
box4.place(relx=0.2, rely=0.6, anchor="center")

box5 = Text(window, height=7, width=50)
box5.place(relx=0.5, rely=0.6, anchor="center")

# URL Selector
site_choice = StringVar(value="flipkart")
OptionMenu(window, site_choice, *urls.keys()).place(relx=0.8, rely=0.6, anchor="center")

# URL Open Button
Button(window, text="Open URL", command=lambda: open_url(None)).place(relx=0.8, rely=0.7, anchor="center")

window.mainloop()
