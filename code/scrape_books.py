from unittest import result
from common import get_soup


def extract_price(price_str):
    """Extracts the price form the string in the product description as a float."""
    ind = price_str.find('£')
    return float(price_str[ind+1:])


def extract_stock(stock_str):
    """Extracts the count form the string in the product description as an int."""
    ind1 = stock_str.find('(')
    ind2 = stock_str.find(' available')
    return int(stock_str[ind1+1:ind2])


def get_category(soup):
    """Extracts the category from the BeautifulSoup instance representing a book page as a string."""

    breadcrumb_tag = soup.find_all("ul", class_="breadcrumb")[0]
    a_tags = breadcrumb_tag.find_all("a")

    return a_tags[2].get_text()



def get_title(soup):
    """Extracts the title from the BeautifulSoup instance representing a book page as a string."""
    title = soup.find('title')
    title_text = title.get_text()
    ind1 = title_text.index(' | Books to Scrape - Sandbox')
    return (title_text[5:ind1])
            
    

def get_description(soup):
    """Extracts the description from the BeautifulSoup instance representing a book page as a string."""
    desc_head = soup.findAll('head')[0]
    desc = desc_head.find('meta', attrs={'name': 'description'})
    description = desc.get('content').strip()
    if description == "":
        description = None
    return description



def get_product_information(soup):
    """Extracts the product information from the BeautifulSoup instance representing a book page as a dict."""
    table = soup.find("table", {"class":"table table-striped"})
    result = {}
    keys = ["upc", "price_gbp", "stock"]
    rows = table.findAll("tr")
    
    for row in rows:
        header = row.find('th').getText()
        if header == 'UPC':
            result['upc'] = row.find('td').getText()
        if header == 'Price (incl. tax)':
            result['price_gbp'] = extract_price(row.find('td').getText())
        if header == 'Availability':
            result['stock'] = extract_stock(row.find('td').getText())
        
    return result


def scrape_book(book_url):
    """Extracts all information from a book page and returns a dict."""
    soup = get_soup(book_url)
    results = get_product_information(soup)
    results['title']=get_title(soup)
    results['category']=get_category(soup)
    results['description']=get_description(soup)
    return results


def scrape_books(book_urls):
    """Extracts all information from a list of book page and returns a list of dicts."""
    results_books = []
    for urls in book_urls:
        results_books.append(scrape_book(urls))
        
    return results_books

if __name__ == "__main__":

    # code for testing

    # set up fixtures for testing

    book_url = "http://books.toscrape.com/catalogue/the-secret-of-dreadwillow-carse_944/index.html"
    book_url_no_description = "http://books.toscrape.com/catalogue/the-bridge-to-consciousness-im-writing-the-bridge-between-science-and-our-old-and-new-beliefs_840/index.html"

    soup = get_soup(book_url)
    soup_no_description = get_soup(book_url_no_description)

    # test extract_price

    assert extract_price("£56.13") == 56.13

    # test extract_stock

    assert extract_stock("In stock (16 available)") == 16

    # test get_category

    assert get_category(soup) == "Childrens"

    # test get_title

    assert get_title(soup) == "The Secret of Dreadwillow Carse"

    # test get_description

    assert get_description(soup) is not None
    assert get_description(soup_no_description) is None

    # test get_product_information

    product_information = get_product_information(soup)

    assert set(product_information.keys()) == {"upc", "price_gbp", "stock"}

    assert product_information == {
        "upc": "b5ea0b5dabed25a8",
        "price_gbp": 56.13,
        "stock": 16,
    }

    # test scrape_book

    book = scrape_book(book_url)
    book_no_description = scrape_book(book_url_no_description)

    expected_keys = {"title", "category", "description", "upc", "price_gbp", "stock"}

    assert set(book.keys()) == expected_keys
    assert set(book_no_description.keys()) == expected_keys
