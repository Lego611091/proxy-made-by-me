import pycurl
from io import BytesIO
import json
import webbrowser

def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except:
        return {"proxy": None}

def fetch(url, proxy=None):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)

    if proxy:
        c.setopt(c.PROXY, proxy)

    c.perform()
    c.close()
    return buffer.getvalue().decode("utf-8", errors="ignore")

def main():
    config = load_config()
    proxy = config.get("proxy")

    print("Simple Libcurl Browser")
    print("Type a URL to fetch its HTML.")
    print("Type 'open' after a URL to open it in your real browser.")
    print("Type 'exit' to quit.\n")

    while True:
        url = input("URL: ").strip()
        if url.lower() == "exit":
            break

        # If user types "open <url>"
        if url.lower().startswith("open "):
            real_url = url.split(" ", 1)[1]
            print(f"Opening {real_url} in your browser...")
            webbrowser.open(real_url)
            continue

        try:
            html = fetch(url, proxy)
            print("\n=== PAGE HTML START ===\n")
            print(html)
            print("\n=== PAGE HTML END ===\n")
        except Exception as e:
            print(f"Error fetching page: {e}")

if __name__ == "__main__":
    main()
