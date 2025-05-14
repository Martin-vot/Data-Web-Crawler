import logging
import os
import csv
from config import USER_AGENT

# Load existing metadata from CSV file
def load_existing_metadata(export_csv):
    metadata = []
    if os.path.exists(export_csv):
        with open(export_csv, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                metadata.append(row)
    return metadata

# Save metadata to CSV file
def save_metadata_to_csv(metadata, export_csv):
    file_exists = os.path.exists(export_csv)
    with open(export_csv, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ['url', 'filename', 'filepath', 'status_code', 'timestamp', 'download_size', 'download_time']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for data in metadata:
            writer.writerow(data)

# Read failed URLs from log
def read_failed_urls(failed_log):
    failed_urls = []
    if os.path.exists(failed_log):
        with open(failed_log, mode='r', encoding='utf-8') as file:
            failed_urls = [line.strip() for line in file.readlines()]
    return failed_urls

# Log failed download attempts
def log_failed_download(url, failed_log):
    with open(failed_log, mode='a', encoding='utf-8') as file:
        file.write(url + "\n")
    logging.error(f"Failed to download: {url}")

# Log metadata after download
def log_metadata(url, filename, filepath, status_code, timestamp, download_size=0, download_time=0, metadata_csv=None):
    file_exists = os.path.exists(metadata_csv)
    with open(metadata_csv, mode='a', newline='', encoding='utf-8') as file:
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