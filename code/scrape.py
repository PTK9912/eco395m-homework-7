import os
import json
import csv

from scrape_pages import scrape_all_pages
from scrape_books import scrape_books


def scrape():
    """Scrape everything and return a list of books."""
    result = scrape_all_pages()
    return result


def write_books_to_csv(books, path):
    with open(path, 'w+', newline = "", encoding="utf-8") as out_file:
        field = ['upc', 'title', 'category', 'description', 'price_gbp', 'stock']
        csvwriter = csv.DictWriter(out_file, fieldnames = field)
        csvwriter.writeheader()
        csvwriter.writerows(books)

def write_books_to_jsonl(books, path):

    with open(path, "w") as file:
        for ob in books:
            file.write( json.dumps(ob) + '\n' )



if __name__ == "__main__":

    BASE_DIR = "artifacts"
    CSV_PATH = os.path.join(BASE_DIR, "results.csv")
    JSONL_PATH = os.path.join(BASE_DIR, "results.jsonl")

    os.makedirs(BASE_DIR, exist_ok=True)

    book_urls = scrape_all_pages()
    books = scrape_books(book_urls)
    write_books_to_csv(books, CSV_PATH)
    write_books_to_jsonl(books, JSONL_PATH)
