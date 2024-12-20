import requests
from bs4 import BeautifulSoup
import json
import argparse
import os

# Define headers to serve as a browser request from a user
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://montrealgazette.com/'
}

CACHE_FILE = 'cache.json'  # Cache file to store visited URLs and their data

# Load the cache from the makeshift cache file
def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f) # We already have a JSON cache so turn it into its a readable dictionary
    return {} # Make an empty dictionary mapping URLs visited to the JSONs that we got from scraping those articles

# Save the cache that we ended up with this time around as the new cache file
def save_cache(cache): # It will still be a dictionary of URL -> JSON structure
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=4) # write as a to-JSON type

# Function to fetch and parse the Montreal Gazette News page
def fetch_trending_stories_page(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Failed to retrieve the page, status code: {response.status_code}")
        return None

# Function to extract trending story links from the soup
def extract_trending_story_links(soup):
    story_links = []
    articles_data = []

    # Find the trending stories by navigating the carousel under the nav bar
    trending_stories_carousel = soup.find_all('li', {'data-carousel-item': True})

    # We'll find the link within each story section on the page
    for story in trending_stories_carousel:
        article = story.find('article', class_='article-card article-card--image-left article-card--hide-padlock')
        if article:
            content_div = article.find('div', class_='article-card__content')
            if content_div:
                details_div = content_div.find('div', class_='article-card__details')
                if details_div:
                    link_tag = details_div.find('a', class_='article-card__link')
                    if link_tag and 'href' in link_tag.attrs:
                        story_link = link_tag['href']
                        full_story_url = "https://montrealgazette.com" + story_link
                        article_title = link_tag.get('aria-label', 'No title')

                        if full_story_url not in story_links:
                            story_links.append(full_story_url)
                            articles_data.append({
                                "title": article_title,
                                "publication_date": "",  # Placeholder for now
                                "author": "",            # Placeholder for now
                                "blurb": ""              # Placeholder for now
                            })

    return story_links, articles_data

# Function to visit each article page and extract the publication date, author, and blurb
def fetch_article_details(article_url):
    response = requests.get(article_url, headers=headers)
    if response.status_code == 200:
        article_soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the publication date
        pub_date = article_soup.find('span', class_='published-date__since')
        publication_date = pub_date.get_text().replace('Published ', '').strip() if pub_date else ""

        # Extract the author name from either regular or wire-published structures
        author = ""

        # Check for regular published author
        author_section = article_soup.find('span', class_='published-by__author')
        if author_section:
            author_link = author_section.find('a')
            if author_link:
                author = author_link.get_text().strip()

        # Check for wire-published author if regular author was not found
        if not author:
            wire_author_section = article_soup.find('div', class_='wire-published-by__authors')
            if wire_author_section:
                author = wire_author_section.get_text().strip()

        # Extract the blurb (subtitle)
        blurb_section = article_soup.find('p', class_='article-subtitle')
        blurb = blurb_section.get_text().strip() if blurb_section else ""

        return publication_date, author, blurb
    return "", "", ""

# Main function to scrape trending stories and write to the output file
def scrape_trending_stories(url, output_file, cache):
    # Fetch the main page
    soup = fetch_trending_stories_page(url)
    if not soup:
        return

    # Extract trending story links and prepare the article data
    story_links, articles_data = extract_trending_story_links(soup)

    # Visit each story and update the JSON structure with the publication date
    for i, story_link in enumerate(story_links):
        # Check if article URL is in cache, note that having an entire URL as a key though messy, but reasonable here
        if story_link in cache:
            print(f"Using cached data for {story_link}") # Found a match so can reuse our scraped data
            articles_data[i]["publication_date"] = cache[story_link]["publication_date"]
            articles_data[i]["author"] = cache[story_link]["author"]
            articles_data[i]["blurb"] = cache[story_link]["blurb"]
            # This saves unnecessary load on the website, rather than having to scrape this article page
        else: # Actually need to scrape using our helper function
            publication_date, author, blurb = fetch_article_details(story_link)
            articles_data[i]["publication_date"] = publication_date
            articles_data[i]["author"] = author
            articles_data[i]["blurb"] = blurb

            # Cache the result, for which we don't care about the article title, since
            # We would have found that in the main page anyways
            cache[story_link] = {
                "publication_date": publication_date,
                "author": author,
                "blurb": blurb
            }

    # Turn our list of dictionaries into a JSON output
    articles_json = json.dumps(articles_data, ensure_ascii=False, indent=4)

    # Write the JSON output to the specified file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(articles_json)

    print(f"Successfully written to {output_file}")

    # Save cache after scraping this time around
    save_cache(cache)

# Setup argparse to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Scrape trending articles from Montreal Gazette")
    parser.add_argument('-o', '--output', type=str, required=True, help='Output file to save the JSON data')
    
    args = parser.parse_args()

    # Load the cache
    cache = load_cache()
    
    # URL of the Montreal Gazette News page
    news_url = "https://montrealgazette.com/category/news/"
    
    # Scrape the trending stories and write to the specified output file
    scrape_trending_stories(news_url, args.output, cache)

if __name__ == "__main__":
    main()

# Run this script with python3 collect_trending.py -o trending.json