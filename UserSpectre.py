import requests
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, init
import argparse
from datetime import datetime


from colorama import Fore, Style, init
init(autoreset=True)

print(Fore.BLUE + " _   _                 _____                 _            ")
print(Fore.BLUE + "| | | |               /  ___|               | |           ")
print(Fore.WHITE + "| | | |___  ___ _ __  \\ `--. _ __   ___  ___| |_ _ __ ___ ")
print(Fore.WHITE + "| | | / __|/ _ \\ '__|  `--. \\ '_ \\ / _ \\/ __| __| '__/ _ \\")
print(Fore.BLUE + "| |_| \\__ \\  __/ |    /\\__/ / |_) |  __/ (__| |_| | |  __/")
print(Fore.BLUE + " \\___/|___/\\___|_|    \\____/| .__/ \\___|\\___|\\__|_|  \\___|")
print(Fore.WHITE + "                            | |                           ")
print(Fore.WHITE + "                            |_|                           ")
print(Fore.YELLOW + "Username Spectre - A tool for username reconnaissance across multiple sites By Vecter61\n")
# UserSpectre.py - A tool for username reconnaissance across multiple sites


init(autoreset=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; UsernameReconBot/1.0)"
}

def load_sites(file_paths):
    sites = []
    for path in file_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

                if isinstance(data, dict):
                    # Your file format: dict with site names as keys
                    # Convert to list of site dicts, adding 'name' field from key
                    for site_name, site_info in data.items():
                        site_info['name'] = site_name
                        sites.append(site_info)

                elif isinstance(data, list):
                    # Existing expected format: list of sites
                    sites.extend(data)

                else:
                    print(f"Skipping invalid file format: {path} (unexpected structure)")
        except Exception as e:
            print(f"Failed to load {path}: {e}")

    return sites


def save_results(username, results_json, results_text):
    os.makedirs("scan", exist_ok=True)
    json_path = os.path.join("scan", f"{username}_result.json")
    text_path = os.path.join("scan", f"{username}_result.txt")

    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(results_json, jf, indent=2)

    with open(text_path, "w", encoding="utf-8") as tf:
        for line in results_text:
            tf.write(line + "\n")

    print(f"\nResults saved to: {json_path} and {text_path}")

def check_site(site, username):
    url = site['url'].replace("{}", username)
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        html = response.text.lower()

        if site.get("error_type") == "status_code":
            if response.status_code == 200:
                return {"site": site["name"], "url": url, "status": "FOUND", "http_code": 200}
            else:
                return {"site": site["name"], "url": url, "status": "NOT FOUND", "http_code": response.status_code}

        elif site.get("error_type") == "keyword":
            error_msg = site.get("error_msg", "").lower()
            if error_msg in html:
                return {"site": site["name"], "url": url, "status": "NOT FOUND", "http_code": response.status_code}
            else:
                return {"site": site["name"], "url": url, "status": "FOUND", "http_code": response.status_code}

        if response.status_code == 200:
            return {"site": site["name"], "url": url, "status": "FOUND", "http_code": 200}
        else:
            return {"site": site["name"], "url": url, "status": "NOT FOUND", "http_code": response.status_code}

    except Exception as e:
        return {"site": site["name"], "url": url, "status": "ERROR", "error": str(e)}

def main(username=None, sites_file=None, workers=25):
    if username is None:
        username = input("USERNAME : ").strip()

    if sites_file is None:
        sites_file = ["sites.json"]

    sites = load_sites(sites_file)
    found = []
    results_text = []

    print(f"\nStarting scan for username: {username}")
    print(f"🌐 Sites to scan: {len(sites)}\n")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(check_site, site, username) for site in sites]

        for future in as_completed(futures):
            result = future.result()
            status = result["status"]

            if status == "FOUND":
                line = f"[FOUND] {result['site']}: {result['url']}"
                print(Fore.GREEN + line)
                found.append(result)
                results_text.append(line)
            else:
                if status == "NOT FOUND":
                    print(Fore.RED + f"[NOT FOUND] {result['site']}")
                else:
                    print(Fore.YELLOW + f"[ERROR] {result['site']} — {result.get('error')}")

    all_results = {
        "username": username,
        "scanned_at": datetime.now().isoformat(),
        "found": found,
    }

    save_results(username, all_results, results_text)



if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        import argparse
        parser = argparse.ArgumentParser(description="Username Recon Tool (Advanced)")
        parser.add_argument("--username", help="Username to search")
        parser.add_argument("--sites", nargs='+', default=["sites.json"], help="Paths to one or more sites JSON files")
        parser.add_argument("--workers", type=int, default=25, help="Number of concurrent threads")
        args = parser.parse_args()

        if not args.username:
            args.username = input("USERNAME : ").strip()

        main(args.username, args.sites, args.workers)

    else:
        # No CLI args, prompt for username interactively
        main()

# recon.py - A tool for username reconnaissance across multiple sites
# Usage: python recon.py --username <username> --sites <path_to_sites_json>