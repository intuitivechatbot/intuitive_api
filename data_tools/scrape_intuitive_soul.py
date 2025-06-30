import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin
import time

def sanitize_filename(title):
    return re.sub(r'[<>:"/\\|?*]', '', title)[:100]

def scrape_posts_on_page(page_url, output_dir, visited_urls):
    """Scrape every post linked from a single blog page."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    try:
        resp = requests.get(page_url, headers=headers)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Error accessing {page_url}: {e}")
        return

    soup = BeautifulSoup(resp.content, 'html.parser')
    post_links = soup.select('h3 a[href*="intuitivesoul.com"]')

    for link in post_links:
        post_url   = urljoin(page_url, link['href'])
        post_title = link.get_text(strip=True)

        if post_url in visited_urls:
            continue
        visited_urls.add(post_url)

        try:
            post_resp = requests.get(post_url, headers=headers)
            post_resp.raise_for_status()
            post_soup = BeautifulSoup(post_resp.content, 'html.parser')

            content_area = (
                post_soup.select_one('article') or
                post_soup.select_one('.post')    or
                post_soup.select_one('main')
            )
            if content_area:
                paras = content_area.find_all('p')
            else:
                h1 = post_soup.select_one('h1')
                paras = h1.find_all_next('p') if h1 else []

            content = "\n".join(p.get_text(strip=True) for p in paras if p.get_text(strip=True))
            if not content:
                content = "No content found"

            if not os.path.isdir(output_dir):
                os.makedirs(output_dir)

            fname = sanitize_filename(post_title) + '.txt'
            fpath = os.path.join(output_dir, fname)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(f"Title: {post_title}\n\n")
                f.write(f"URL: {post_url}\n\n")
                f.write("Content:\n")
                f.write(content)

            print(f"Saved: {fname}")
            time.sleep(1)

        except Exception as e:
            print(f"Error scraping {post_url}: {e}")

if __name__ == "__main__":
    BASE = "https://intuitivesoul.com/blog"
    OUTDIR = "intuitive_soul_posts"
    visited = set()

    for page in range(4, 28):
        page_url = f"{BASE}/page/{page}"
        print(f"\n=== Scraping page {page} ===")
        scrape_posts_on_page(page_url, OUTDIR, visited)