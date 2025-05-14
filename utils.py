import os
import csv
import logging
import re

def log_metadata(url, filename, filepath, status_code, timestamp, download_size=0, download_time=0, metadata_file="metadata/downloaded_metadata.csv"):
    file_exists = os.path.exists(metadata_file)
    with open(metadata_file, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ['url', 'filename', 'filepath', 'status_code', 'timestamp', 'download_size', 'download_time']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            'url': url,
            'filename': filename,
            'filepath': filepath,
            'status_code': status_code,
            'timestamp': timestamp,
            'download_size': download_size,
            'download_time': download_time
        })

def export_links_to_csv(links, filename="document_links.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["URL"])
        for link in links:
            writer.writerow([link])

    logging.info(f"Exported {len(links)} links to {filename}")

def sanitize_filename(filename):
    # Invalid characters for Windows and Unix-based systems
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def ensure_directory_exists(path):
    os.makedirs(path, exist_ok=True)

__all__ = ["log_metadata", "export_links_to_csv", "sanitize_filename", "ensure_directory_exists"]
