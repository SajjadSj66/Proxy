#  Proxy Manager API (FastAPI)

This project allows you to fetch free proxy servers from the web, test which ones are working, and then use them to send web requests.

---

##  Function Overview

### 1. `fetch_proxies()`

**Route:** `GET /f/`

- Connects to [ProxyScrape API](https://proxyscrape.com) to get a list of free HTTPS proxies.
- Parses the returned text list of IP:PORT.
- For each proxy, it sends a test request to a simple site (like `https://httpbin.org/ip`) to check if it's alive.
- Only working proxies are stored in memory.

#### What it returns:
A JSON object showing how many proxies were found and a preview list of the first few.

---

### 2. `request_via_proxy(url: str)`

**Route:** `GET /r/`

**Query parameter:** `url` – The target URL you want to visit through a proxy.

- Goes through the list of working proxies obtained from `/f/`.
- Tries to access the given `url` using each proxy until one succeeds.
- Returns the full HTML content of the page from the first successful proxy.

#### What it returns:
- If successful: The raw HTML content of the page.
- If all proxies fail: A message indicating that all proxies failed.

---

##  Notes

- Always call `/f/` first to load and test working proxies before using `/r/`.
- Only HTTPS proxies are used.
- Proxy quality varies — some may not work on every request or every target site.

