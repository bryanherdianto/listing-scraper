# Web Scraper

A Scrapy-based web scraper that extracts liquidation store listings from [liquidationmap.com](https://www.liquidationmap.com/directory-liquidation/locations/usa/). It crawls the USA directory, follows each state/city page, then visits every individual business listing and extracts contact details.

## Data Extracted

Each scraped listing contains:

| Field      | Description                    |
| ---------- | ------------------------------ |
| `name`     | Business name                  |
| `location` | Street address, state and ZIP  |
| `phone`    | Contact phone number           |
| `email`    | Contact email address          |
| `url`      | URL of the source listing page |

Missing fields are recorded as `"-"`. The current `listing.json` contains 586 listings.

## Project Structure

```
web-scraper/
├── scrapy.cfg                  # Scrapy deployment config
├── listing.json                # Scraped output data
└── listing_scraper/
    ├── __init__.py
    ├── items.py                # Item models
    ├── middlewares.py          # Spider/downloader middlewares
    ├── pipelines.py            # Item pipelines
    ├── settings.py             # Scrapy settings
    └── spiders/
        ├── __init__.py
        └── scraper.py          # The listing spider
```

## How It Works

The spider (`listing_scraper/spiders/scraper.py`) works in three stages:

1. **`parse`** — Starts at the USA directory page and collects all first-level listing links.
2. **`parse_links`** — Follows each link and collects the individual business listing links.
3. **`parse_details`** — Visits each business page and extracts the name, location, phone, email and URL using CSS selectors.

## Requirements

- Python 3.x
- [Scrapy](https://scrapy.org/)

Install Scrapy:

```bash
pip install scrapy
```

## Usage

Run the spider from the project root (where `scrapy.cfg` is located):

```bash
scrapy crawl listing -O listing.json
```

`-O` overwrites the output file. Use `-o` to append to an existing file instead.

To export to other formats, change the file extension:

```bash
scrapy crawl listing -O listing.csv
scrapy crawl listing -O listing.xml
```

## Configuration

Key settings in `listing_scraper/settings.py`:

- `ROBOTSTXT_OBEY = True` — Respects the target site's `robots.txt` rules.
- `LOG_LEVEL = "WARNING"` — Reduces log noise; set to `"INFO"` or `"DEBUG"` for more detail.
- `FEED_EXPORT_ENCODING = "utf-8"` — Ensures output is UTF-8 encoded.

Adjust `DOWNLOAD_DELAY` or `CONCURRENT_REQUESTS_PER_DOMAIN` to control crawl speed and be respectful to the target server.
