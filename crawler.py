from urllib.parse import urljoin
import random
import requests
import time
import logging
from bs4 import BeautifulSoup
from config import USER_AGENT

def crawl_urls(base_url, max_depth=2, current_depth=0, user_agent=None, visited=None, max_links=None):
    if visited is None:
        visited = set()

    if current_depth > max_depth:
        return set()

    if base_url in visited:
        return set()

    if max_links and len(visited) >= max_links:
        return set()

    logging.info(f"[{len(visited):04d}] Crawling: {base_url} (Depth: {current_depth})")

    try:
        headers = {"User-Agent": random.choice(user_agent) if user_agent else random.choice(USER_AGENT)}
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        logging.error(f"[ERROR] Failed to fetch {base_url}: {e}")
        return set()

    visited.add(base_url)
    soup = BeautifulSoup(response.content, "html.parser")

    document_links = set()

    for link in soup.find_all("a", href=True):
        full_url = urljoin(base_url, link["href"]).split("#")[0]

        # Loguj každý link
        logging.debug(f"Found link: {full_url}")

        # Přidání dokumentů
        if full_url.lower().endswith(('.pdf', '.doc', '.docx', '.xls', '.txt')):
            logging.info(f"Document link found: {full_url}")
            document_links.add(full_url)

        # Povolíme crawl jen v rámci domény indiacode.nic.in
        elif full_url.startswith("https://www.indiacode.nic.in") and full_url not in visited:
            document_links.update(crawl_urls(
                full_url,
                max_depth=max_depth,
                current_depth=current_depth + 1,
                user_agent=user_agent,
                visited=visited,
                max_links=max_links
            ))

    time.sleep(random.uniform(2, 5))
    return document_links


def filter_documents(links):
    logging.info(f"Number of found documents: {len(links)}")
    return [link for link in links if link.lower().endswith(('.pdf', '.doc', '.docx', '.xls', '.txt'))]

__all__ = ["crawl_urls", "filter_documents"]
