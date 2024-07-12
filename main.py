import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sys
import pandas as pd

def is_valid(url):
    """Check if the URL is valid."""
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_website_links(url):
    """Returns all URLs and their links that are found on the given URL."""
    urls = set()
    domain_name = urlparse(url).netloc
    url_count = 0
    data = []
    links = []

    def crawl(url):
        nonlocal url_count
        try:
            response = requests.get(url, timeout=5, allow_redirects=False)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            data.append({"URL": url, "Status Code": response.status_code, "Error": str(http_err)})
            return
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            data.append({"URL": url, "Status Code": "N/A", "Error": str(e)})
            return

        url_count += 1
        print(f"{url_count}. {url} - Status Code: {response.status_code}")
        urls.add(url)
        data.append({"URL": url, "Status Code": response.status_code, "Error": ""})

        if "text/html" not in response.headers.get("Content-Type", ""):
            return

        soup = BeautifulSoup(response.content, "html.parser")

        # Extract meta tags
        title_tag = soup.find("title")
        meta_description = soup.find("meta", attrs={"name": "description"})
        title = title_tag.string.strip() if title_tag else ""
        description = meta_description["content"].strip() if meta_description else ""

        # Extract header tags
        header_tags = [tag.text.strip() for tag in soup.find_all(["h1", "h2", "h3"])]

        # Extract canonical URL
        canonical_tag = soup.find("link", attrs={"rel": "canonical"})
        canonical_url = canonical_tag["href"] if canonical_tag else ""

        # Extract image alt texts
        img_tags = soup.find_all("img")
        alt_texts = [tag.get("alt", "") for tag in img_tags]

        data.append({
            "URL": url,
            "Status Code": response.status_code,
            "Error": "",
            "Title": title,
            "Meta Description": description,
            "Header Tags": ", ".join(header_tags),
            "Canonical URL": canonical_url,
            "Image Alt Text": ", ".join(alt_texts)
        })

        # Extract links
        for a_tag in soup.find_all("a", href=True):
            href = a_tag.attrs["href"]
            if not is_valid(href):
                href = urljoin(url, href)
            parsed_href = urlparse(href)
            if domain_name not in parsed_href.netloc:
                continue
            if href not in urls:
                crawl(href)
            links.append((url, href))

    crawl(url)
    print(f"\nTotal URLs found: {url_count}")
    return data, links

def save_to_excel(data, links, filename):
    df = pd.DataFrame(data)
    df_links = pd.DataFrame(links, columns=['Source', 'Target'])
    with pd.ExcelWriter(filename) as writer:
        df.to_excel(writer, sheet_name='URLs', index=False)
        df_links.to_excel(writer, sheet_name='Links', index=False)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python crawler.py <url>")
        sys.exit(1)

    start_url = sys.argv[1]
    if not is_valid(start_url):
        print("Invalid URL")
        sys.exit(1)

    data, links = get_all_website_links(start_url)
    save_to_excel(data, links, "crawled_data.xlsx")
