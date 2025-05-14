@echo off
title IndiaCode Crawler

C:\Users\Admin\Desktop\python\gigs\india_acts\scripts\venv\Scripts\python.exe main.py ^
--base-url "https://www.indiacode.nic.in/" ^
--max-depth 2 ^
--max-files 100 ^
--batch-size 5 ^
--export-csv "document_links.csv" ^
--download-path "downloads" ^
--failed-log "failed_urls.csv"

pause