import random
import time
import requests
import logging
import os
import csv
import logging
from urllib.parse import urlparse, parse_qs
from config import USER_AGENT
from metadata import save_metadata_to_csv

# Function to try download several times
def download_file_with_retry(url, retries, folder_name, failed_log_file, filename):
    attempt = 0
    while attempt < retries:
        try:
            start_time = time.time()
            response = requests.get(url, headers={"User-Agent": random.choice(USER_AGENT)}, timeout=10)
            response.raise_for_status()

            filepath = os.path.join(folder_name, filename)
            with open(filepath, "wb") as file:
                file.write(response.content)

            logging.info(f"Downloaded {url} to {filepath}")
            download_size = len(response.content)
            download_time = time.time() - start_time
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            return filepath, response.status_code, timestamp, download_size, download_time
        except requests.RequestException as e:
            attempt += 1
            logging.warning(f"Attempt {attempt} - Failed to download {url}: {e}")
            time.sleep(random.uniform(3, 6))

    with open(failed_log_file, "a", encoding="utf-8") as failed_log:
        failed_log.write(f"{url}\n")
    return None, None, None, None, None

# Function to log metadata to a CSV file
def log_metadata(url, filename, filepath, status_code, timestamp, download_size, download_time, metadata_file):
    if not os.path.exists(metadata_file):
        with open(metadata_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["URL", "Filename", "Filepath", "Status Code", "Timestamp", "Download Size (bytes)", "Download Time (seconds)"])

    with open(metadata_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([url, filename, filepath, status_code, timestamp, download_size, download_time])

# Function to download single file
def download_file(url, base_path, failed_log_file):
    try:
        response = requests.get(url, headers={"User-Agent": random.choice(USER_AGENT)}, timeout=10)
        response.raise_for_status()

        file_name = os.path.join(base_path, url.split("/")[-1])

        with open(file_name, "wb") as file:
            file.write(response.content)

        logging.info(f"Downloaded {url} to {file_name}")
    except requests.RequestException as e:
        logging.error(f"Failed to download {url}: {e}")
        with open(failed_log_file, "a") as failed_log:
            failed_log.write(f"{url}\n")

# Function to download all the files
def download_files(doc_urls, base_path, failed_log_file, batch_size, metadata_csv, max_files=None):
    print(f"batch_size type: {type(batch_size)} value: {batch_size}")
    batch_size = int(batch_size)
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    if not os.path.exists(metadata_csv):
        with open(metadata_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["URL", "Filename", "Filepath", "Status Code", "Timestamp", "Download Size (bytes)", "Download Time (seconds)"])

    if max_files:
        doc_urls = doc_urls[:max_files]

    metadata = []

    for i in range(0, len(doc_urls), batch_size):
        batch = doc_urls[i:i + batch_size]
        for url in batch:
            parsed = urlparse(url)
            filename = parse_qs(parsed.query).get("rfilename", [parsed.path.split("/")[-1]])[0]
            folder_name = os.path.join(base_path, parsed.path.strip('/'))
            os.makedirs(folder_name, exist_ok=True)

            filepath = os.path.join(folder_name, filename)
            if os.path.exists(filepath):
                logging.info(f"Skipping {filename}, already downloaded.")
                continue

            start_time = time.time()
            filepath, status_code, timestamp, size, download_time = download_file_with_retry(
                url=url,
                retries=3,
                folder_name=folder_name,
                failed_log_file=failed_log_file,
                filename=filename
            )

            end_time = time.time()
            download_time = end_time - start_time

            if filepath:
                metadata.append({
                    'url': url,
                    'filename': filename,
                    'filepath': filepath,
                    'status_code': status_code,
                    'timestamp': timestamp,
                    'download_size': size,
                    'download_time': download_time
                })

            if metadata:
                save_metadata_to_csv(metadata, metadata_csv)

        logging.info(f"Batch {i // batch_size + 1} finished. Pausing before next batch.")
        time.sleep(random.uniform(5, 10))

# Function to export links to cvs
def export_links_to_csv(links, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["URL"])
        for link in links:
            writer.writerow([link])

    logging.info(f"Exported {len(links)} links to {filename}")