import pandas as pd
import requests
from bs4 import BeautifulSoup
import os


categories = [
    'mobiles', 'tablets', 'smart-watches', 'wireless-earbuds', 'mobiles-accessories'
]
range_o = [range(1, 11), range(0, 1), range(1, 9), range(1, 14), range(1, 2)]

data = []

for category, page_range in zip(categories, range_o):
    for i in page_range:
        url = f'https://priceoye.pk/{category}?page={str(i)}'
        web = BeautifulSoup(requests.get(url).content, "html.parser")
        products = web.find_all('div', class_='productBox b-productBox')

        for product in products:
            name_element = product.find('div', class_='p-title')
            price_element = product.find('div', class_='price-box')
            persentage_element = product.find('div', class_='price-diff-saving')

            if name_element is not None and price_element is not None:
                name = name_element.text.strip()
                price = price_element.text.strip()
                percentage_off = persentage_element.text.strip() if persentage_element else "NONE"

                if 'Rs.' in price:
                    price = price.replace('Rs.', '').strip()

                data.append({'Name': name, 'Price': price, 'Percentage Off': percentage_off})

df = pd.DataFrame(data)
print(df)
file_path = 'producttt.csv'
if os.path.isfile(file_path):
    df.to_csv(file_path, mode='a', header=False, index=False)
else:
    df.to_csv(file_path, index=False)

print("CSV file saved successfully.")

