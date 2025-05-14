import os
import logging
import argparse
from crawler import crawl_urls, filter_documents
from downloader import download_files, export_links_to_csv
from config import USER_AGENT

# Setup folders
os.makedirs("downloads", exist_ok=True)
os.makedirs("logs", exist_ok=True)
os.makedirs("metadata", exist_ok=True)

# Logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

info_handler = logging.FileHandler("logs/scraper.log")
info_handler.setLevel(logging.INFO)
info_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
info_handler.setFormatter(info_formatter)

error_handler = logging.FileHandler("logs/scraper_errors.log")
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
error_handler.setFormatter(error_formatter)

logger.addHandler(info_handler)
logger.addHandler(error_handler)

def main(base_url, max_depth, max_links, max_files, batch_size, export_csv, base_path, failed_log_file):
    logging.info(f"Started crawling from base URL: {base_url}")

    document_links = crawl_urls(
        base_url, 
        max_depth, 
        max_links=max_links, 
        user_agent=USER_AGENT
    )

    filtered = filter_documents(document_links)

    if filtered:
        logging.info(f"Found {len(filtered)} documents to download.")
        metadata_csv = os.path.join("metadata", "metadata.csv")
        download_files(
    filtered,
    base_path=base_path,
    failed_log_file=failed_log_file,
    batch_size=int(batch_size),
    metadata_csv=metadata_csv,
    max_files=max_files
)
    else:
        logging.info("No documents to download!")

    if export_csv:
        export_links_to_csv(filtered, filename=export_csv)

    print(f"Found {len(document_links)} links before filtering")
    print(f"Found {len(filtered)} document links after filtering")
    logging.info(f"Completed scraping and downloading for {base_url}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawl the website and download documents.")
    parser.add_argument('--base-url', type=str, required=True, help="Base URL to start crawling.")
    parser.add_argument('--max-depth', type=int, default=2, help="Maximum depth for crawling.")
    parser.add_argument('--max-links', type=int, default=500, help="Maximum number of unique URLs to visit.")
    parser.add_argument('--max-files', type=int, default=100, help="Maximum number of files to download.")
    parser.add_argument('--batch-size', type=int, default=5, help="Batch size for downloads.")
    parser.add_argument('--export-csv', type=str, required=True, help="CSV file to export the links.")
    parser.add_argument('--download-path', type=str, required=True, help="Path to save downloaded files.")
    parser.add_argument('--failed-log', type=str, required=True, help="CSV file to log failed URLs.")

    args = parser.parse_args()

    logging.info(f"Starting the crawl with base URL: {args.base_url}")

    main(
        base_url=args.base_url,
        max_depth=args.max_depth,
        max_links=args.max_links,
        max_files=args.max_files,
        batch_size=args.batch_size,
        export_csv=args.export_csv,
        base_path=args.download_path,
        failed_log_file=args.failed_log
    )
