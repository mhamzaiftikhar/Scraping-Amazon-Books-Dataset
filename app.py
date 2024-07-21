import requests
from bs4 import BeautifulSoup
import pandas as pd

# Main Url with out pagination
# url = 'https://www.amazon.in/gp/bestsellers/books/'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
# Pagination
base_url = 'https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_2_books?ie=UTF8&pg={}'

Books = []

# Iterate through multiple pages
for page_num in range(1,3): 
    url = base_url.format(page_num)
    print(f"Scraping page {page_num} - URL: {url}")
    r = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(r.content, 'html.parser')
    containers = soup.find_all('div', class_='_cDEzb_iveVideoWrapper_JJ34T')

    for container in containers:
        # Book Title
        title_element = container.find('div', class_='_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y')
        title = title_element.text.strip() if title_element else 'Title Not Found'
        # This Code will Remove author name from title if it's mistakenly included
        author_element = container.find('div', class_='_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y').find_next('div', class_='a-row a-size-small')
        if author_element:
         author = author_element.text.strip()
         title = title.replace(author, '').strip()
        
        
        # Author Name
        author_element = container.find('div', class_='_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y')
        author = author_element.find_next('div', class_='a-row a-size-small').text.strip() if author_element else 'Author Name Not Found'
        
        # Rating
        rating_element = container.find('i', class_='a-icon')
        rating = rating_element.find_next('span', class_='a-icon-alt').text.strip() if rating_element else 'Rating Not Found'
        

        # Review Number
        review_Number = container.find('i', class_= 'a-icon')
        review = review_Number.find_next('span', class_= 'a-size-small').text.strip() if review_Number else 'Review Not Found'

        
        # Price
        price_element = container.find('div',class_='_cDEzb_p13n-sc-price-animation-wrapper_3PzN2')
        price = price_element.find_next('span', class_='_cDEzb_p13n-sc-price_3mJ9Z').text.strip() if price_element else 'Not Found'
        # Converting Price in to Float
        try:
            price = float(price.replace('₹', '').replace(',', ''))
        except ValueError:
            price = None
        
        
        # This is for the Terminal Printing
        # print('Book Title:', title)
        # print('Author Name:', author)
        # print('Rating of Book:', rating)
        # print('Rating Count:', review)
        # print('Price of Book:', price)
        # print('-' * 50)
        
        Books.append({
            'Book Title': title,
            'Author Name': author,
            'Rating': rating,
            'Review Count': review,
            'Price': price
        })


df = pd.DataFrame(Books)
df.to_csv('AmazonBooks.csv', index=False)

print('Scraping and CSV file saved successfully.')
