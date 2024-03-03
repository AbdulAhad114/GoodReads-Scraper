import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import base64

def scrape_goodreads(keyword, num_pages):
    base_url = "https://www.goodreads.com/search"
    data = []

    for page in range(1, num_pages+1):
        params = {
            "q": keyword,
            "page": page
        }
        response = requests.get(base_url, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all("tr", attrs={"itemtype": "http://schema.org/Book", "itemscope": True})
        # print(books)
        for book in books:
            title = book.find("a", {"class": "bookTitle"}).text.strip()
            author = book.find("span", {"itemprop": "name"}).text.strip()
            rating_text = book.find("span", {"class": "minirating"}).text.strip()
            rating = rating_text.split()[0]
            ratings_count = rating_text.split()[-2]
            image_url = book.find("img", {"class": "bookCover"})['src']
            data.append([title, author, rating, ratings_count, image_url])
    return data

def main():
    st.title("Goodreads Scraper")
    keyword = st.text_input("Enter the genre or keyword")
    num_pages = st.slider("Select number of pages to scrape", 1, 10)
    if st.button("Scrape"):
        if keyword:
            st.write(f"Scraping for keyword: {keyword}")
            data = scrape_goodreads(keyword, num_pages)
            df = pd.DataFrame(data, columns=["Book Title", "Author", "Ratings", "Average Score","URL"])
            st.dataframe(df)
            st.markdown(get_table_download_link(df), unsafe_allow_html=True)
        else:
            st.error("Please enter a keyword")

def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="goodreads_data.csv">Download CSV File</a>'
    return href

if __name__ == "__main__":
    main()
