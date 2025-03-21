from scrap_gmt_links import run as run_scrap_gmt_links
from scrap_internet_archive_links import run as run_scrap_internet_archive_links

print("Fetching links from Internet Archive...")
run_scrap_internet_archive_links()

print("Scraping GMT Games...")
run_scrap_gmt_links()
