from fastapi import FastAPI, HTTPException
import requests
from fastapi.responses import HTMLResponse
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()
proxies = []


# Function to test a proxy
def is_proxy_working(proxy: str) -> str | None:
    try:
        response = requests.get(
            "https://httpbin.org/ip",
            proxies={"http": proxy, "https": proxy},
            timeout=5
        )
        if response.status_code == 200:
            print(f"work: {proxy}")
            return proxy
    except:
        pass
    return None


# API: Getting and testing proxies
@app.get("/f/")
def fetch_proxies():
    global proxies
    url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch proxies")

    raw_text = response.text.strip()
    lines = raw_text.splitlines()
    candidate_proxies = [f"http://{line.strip()}" for line in lines if line.strip()]

    if not candidate_proxies:
        raise HTTPException(status_code=404, detail="No proxies found")

    # Just test the first 50 for speed.
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(is_proxy_working, candidate_proxies[:50]))

    working = [p for p in results if p]
    proxies = working

    return {"count": len(working), "proxies": working[:10]}


# 2. Send a request to the URL using a random proxy
@app.get("/r/", response_class=HTMLResponse)
def request_via_proxy(url: str = "https://github.com"):
    if not proxies:
        raise HTTPException(status_code=404, detail="The proxy list is empty")

    for proxy in proxies:
        try:
            print(f"testing: {proxy}")
            response = requests.get(
                url,
                proxies={"https": proxy},
                timeout=10
            )
            # The response is returned in html format.
            return HTMLResponse(content=response.text, status_code=response.status_code)

        except Exception as e:
            print(f"proxies failed {proxy}: {e}")

    return HTMLResponse(content="all proxies failed", status_code=404)