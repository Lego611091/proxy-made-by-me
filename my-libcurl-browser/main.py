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
    print("Type 'open <url>' to open it in your real browser.")
    print("Type 'exit' to quit.\n")

    while True:
        url = input("URL: ").strip()
        if url.lower() == "exit":
            break

        # If user types "open <url>"
        if url.lower().startswith("open "):
            real_url = url.split(" ", 1)[1]

            # If proxy is set, open THROUGH the proxy
            if proxy:
                proxied_url = f"{proxy}/{real_url}"
                print(f"Opening through proxy: {proxied_url}")
                webbrowser.open(proxied_url)
            else:
                print(f"Opening: {real_url}")
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
