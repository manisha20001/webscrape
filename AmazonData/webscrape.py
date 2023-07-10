import requests
import csv
from bs4 import BeautifulSoup

base_url = 'https://www.amazon.in/s'
search_params = {
    'k': 'bags',
    'crid': '2M096C61O4MLT',
    'qid': '1653308124',
    'sprefix': 'ba',
    'ref': 'sr_pg_'
}

# Open a CSV file in write mode
with open('amazon_bags.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['URL', 'Rating', 'Price', 'Product Name'])  # Write header row

    product_count = 0
    page_num = 1

    while product_count < 440:
        search_params['ref'] = f'sr_pg_{page_num}'
        response = requests.get(base_url, params=search_params)
        html_content = response.content

        soup = BeautifulSoup(html_content, 'html.parser')

        products = soup.find_all('div', {'data-component-type': 's-search-result'})
        for product in products:
            # Extract URL
            url = product.find('a', class_='a-link-normal')['href']
            # Extract rating
            rating = product.find('span', class_='a-icon-alt').text.strip()
            # Extract price
            price = product.find('span', class_='a-price-whole').text
            # Extract product name
            product_name = product.find('span', class_='a-size-medium').text

            # Write data to CSV file
            writer.writerow([url, rating, price, product_name])

            product_count += 1
            if product_count == 440:
                break

        page_num += 1

print("Data saved to amazon_bags.csv file.")
