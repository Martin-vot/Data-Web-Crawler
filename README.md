# Data Web Crawler

This is a modular and production-ready web crawler for downloading legal documents from [indiacode.nic.in](https://www.indiacode.nic.in/).  
It is written in Python and designed for recursive link exploration, filtering downloadable files (PDF, DOCX, etc.), and saving them with metadata.

## Features

- Recursive crawling with max depth and link limit
- Filtering of downloadable documents
- Batched parallel downloading
- Error logging (failed URLs)
- Export of metadata to CSV
- CLI support via `argparse`

## Folder Structure

```
IndiaCode/
│
├── Scripts/
│   ├── main.py
│   ├── crawler.py
│   ├── downloader.py
│   ├── config.py
│   ├── metadata.py
│   ├── utils.py
│   ├── run.bat
│   └── requirements.txt
│
├── downloads/          # Downloaded files
├── metadata/           # CSV metadata exports
├── logs/               # Logs and errors
└── README.md
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Martin-vot/Data-Web-Crawler.git
   cd Data-Web-Crawler
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r Scripts/requirements.txt
   ```

## Usage

Run the crawler using:

```bash
python Scripts/main.py ^
  --base-url "https://www.indiacode.nic.in/" ^
  --max-depth 2 ^
  --max-files 100 ^
  --batch-size 5 ^
  --export-csv "document_links.csv" ^
  --download-path "downloads" ^
  --failed-log "failed_urls.csv"
```

Or use the prepared batch file:

```bash
Scripts/run.bat
```

## Author

GitHub: [Martin-vot](https://github.com/Martin-vot)
