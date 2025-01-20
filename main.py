import requests
from bs4 import BeautifulSoup
import csv
import time

# URL of the website to scrape
URL = "https://example.com/articles"

# Send a GET request to the website
response = requests.get(URL)

# Check if the request was successful
if response.status_code != 200:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
else:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all article containers on the page (assuming the articles are inside <article> tags)
    articles = soup.find_all("article")

    # Prepare to save the data to a CSV file
    with open("articles.csv", "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["Title", "Link", "Published Date"])

        # Loop through all the articles and extract data
        for article in articles:
            try:
                # Extract article title
                title = article.find("h2").get_text(strip=True)
                # Extract the article's link (assuming it's in an <a> tag inside the article)
                link = article.find("a")["href"]
                # Extract the publication date (assuming it's in a <time> tag)
                pub_date = article.find("time").get_text(strip=True)
                
                # Write the data to the CSV file
                writer.writerow([title, link, pub_date])

                # Optional: Print each article's details
                print(f"Title: {title}")
                print(f"Link: {link}")
                print(f"Published Date: {pub_date}")
                print("-" * 40)

            except AttributeError as e:
                print("Error parsing an article. Skipping this one.")
                continue

            # Optional: Delay between requests to avoid overwhelming the server
            time.sleep(1)

    print("Scraping complete! Data has been saved to 'articles.csv'.")
