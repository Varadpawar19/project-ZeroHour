# import requests
# import json
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin

# API_KEY = 'AIzaSyD73gou9IbY2kP25icadsfPT0Wo8UOUzys'
# CSE_ID = 'c4fa112e51c6d4e0f'

# TRUSTED_DOMAINS = ['.org', '.edu', '.gov', '.news', '.in', '.com']
# BLACKLISTED_DOMAINS = ['youtube.com', 'tiktok.com']
# RELEVANT_KEYWORDS = ["cyber attack", "cybersecurity", "incident", "breach", "crime", "threat", "APT", "hack",]

# seen_links = set()

# def check_rss_feed(website_url):
#     """
#     Check if a website has an RSS feed by testing common RSS paths or parsing HTML for RSS links.
#     """
#     rss_paths = ["/feed/", "/rss.xml", "/rss/", "/feeds/posts/default"]
    
#     # Check standard RSS paths
#     for path in rss_paths:
#         rss_url = website_url.rstrip("/") + path
#         try:
#             response = requests.get(rss_url, timeout=5)
#             if response.status_code == 200 and "xml" in response.headers.get("Content-Type", ""):
#                 return rss_url
#         except requests.RequestException:
#             continue

#     # If no standard RSS feed found, parse the HTML for <link> tags
#     try:
#         response = requests.get(website_url, timeout=5)
#         soup = BeautifulSoup(response.content, "html.parser")
        
#         # Find link tags for RSS feeds
#         rss_links = soup.find_all("link", type="application/rss+xml")
#         for rss_link in rss_links:
#             href = rss_link.get("href")
#             if href:
#                 # Handle relative URLs
#                 return urljoin(website_url, href)
#     except requests.RequestException:
#         pass

#     return None

# def check_safe_browsing(url, api_key):
#     """
#     Checks if a URL is flagged as unsafe using Google's Safe Browsing API.
#     """
#     safe_browsing_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
#     payload = {
#         "client": {"clientId": "yourclientid", "clientVersion": "1.0.0"},
#         "threatInfo": {
#             "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
#             "platformTypes": ["ANY_PLATFORM"],
#             "threatEntryTypes": ["URL"],
#             "threatEntries": [{"url": url}]
#         }
#     }
#     response = requests.post(safe_browsing_url, json=payload)
#     if response.status_code == 200 and "matches" in response.json():
#         return "Unsafe URL"
#     return "Safe URL"

# def get_cyber_attack_websites(query, api_key, cse_id):
#     """
#     Fetch search results using Google's Custom Search API.
#     """
#     url = "https://www.googleapis.com/customsearch/v1"
#     params = {'key': api_key, 'cx': cse_id, 'q': query, 'num': 10}
#     response = requests.get(url, params=params)

#     if response.status_code == 200:
#         search_results = response.json()
#         if 'items' in search_results:
#             relevant_websites = []
#             for item in search_results['items']:
#                 link = item['link']
#                 title = item['title']

#                 # Skip blacklisted or already-seen links
#                 if any(domain in link for domain in BLACKLISTED_DOMAINS) or link in seen_links:
#                     continue

#                 # Only consider trusted domains
#                 if any(domain in link for domain in TRUSTED_DOMAINS):
#                     safe_status = check_safe_browsing(link, API_KEY)
#                     if safe_status == "Safe URL":
#                         print(f"Checking RSS for: {link}")
#                         rss_feed = check_rss_feed(link)
#                         if rss_feed:
#                             print(f"RSS feed found: {rss_feed}")
#                             relevant_websites.append({'title': title, 'link': rss_feed})
#                             seen_links.add(link)
#                         else:
#                             print(f"No RSS feed found for: {link}")
#             return relevant_websites
#     return []

# def get_custom_websites():
#     """
#     Add websites like Hacker News, ThreatPost, DarkReading manually.
#     """
#     return [
#         {"title": "Hacker News", "link": "https://thehackernews.com/rss.xml"},
#         {"title": "ThreatPost", "link": "https://threatpost.com/feed/"},
#         {"title": "DarkReading", "link": "https://www.darkreading.com/rss_simple.asp"}
#     ]

# # List of queries to fetch websites
# queries = [
#     "site:hackernews.com RSS",
#     "site:threatpost.com RSS",
#     "site:darkreading.com RSS",
#     "cybersecurity news site:hackernews.com RSS",
#     "cybersecurity updates site:threatpost.com RSS",
#     "cybersecurity site:.edu RSS",
#     "real-time cybersecurity updates RSS",
#     "cybersecurity RSS feeds",
#     "real time cyber attack news",
#     "real time cyber incidents news",
#     "cyber attack",
#     "cyber incidents",
#     "cyber incidents 2024",
#     "critical infrastructure cyber attacks India 2024",
#     "India cybersecurity breach 2024"
# ]

# # Fetch and consolidate results
# all_links = []

# # Add custom websites
# custom_websites = get_custom_websites()
# all_links.extend(custom_websites)

# for query in queries:
#     print(f"Searching for: {query}")
#     websites = get_cyber_attack_websites(query, API_KEY, CSE_ID)
#     all_links.extend(websites)

# # Save results to a JSON file
# output_file = "websites.json"
# if all_links:
#     with open(output_file, "w") as file:
#         json.dump(all_links, file, indent=2)
#     print(f"Fetched RSS-supported websites saved to {output_file}.")
# else:
#     print("No RSS-supported websites were found.")
# import requests

import requests
import json
import feedparser

API_KEY = 'AIzaSyD73gou9IbY2kP25icadsfPT0Wo8UOUzys'
CSE_ID = 'c4fa112e51c6d4e0f'

TRUSTED_DOMAINS = [".org", ".edu", ".gov", ".com", ".in"]
BLACKLISTED_DOMAINS = [
    "youtube.com", "tiktok.com", "facebook.com", "twitter.com", "instagram.com", "github.com"
]

SEARCH_QUERIES = [
    "cyber attacks updates",
    "cyber attack reports 2024",
    "data breach news 2024",
    "APT group activities",
    "cybersecurity blogs",
    "cybersecurity monitoring platforms",
    "threatfox"
]

def google_search(query, api_key, cse_id):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": api_key, "cx": cse_id, "q": query, "num": 10}
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        search_results = response.json()
        if "items" in search_results:
            return [item["link"] for item in search_results["items"]]
    return []

def is_valid_domain(url):
    if any(domain in url for domain in BLACKLISTED_DOMAINS):
        return False
    return any(domain in url for domain in TRUSTED_DOMAINS)

def check_rss_support(url):
    try:
        feed = feedparser.parse(url)
        if feed.bozo == 0 and feed.entries:
            print(f"RSS feed found for {url}")
            return True
        else:
            print(f"No valid RSS feed for {url}")
    except Exception as e:
        print(f"Error checking RSS feed for {url}: {e}")
    return False

def generate_websites():
    discovered_websites = []
    for query in SEARCH_QUERIES:
        urls = google_search(query, API_KEY, CSE_ID)
        for url in urls:
            if is_valid_domain(url):
                rss_supported = check_rss_support(url)
                discovered_websites.append({"link": url, "rss": rss_supported})
    return discovered_websites

def save_websites_to_file(websites, filename="discovered_websites_updated.json"):
    with open(filename, "w") as file:
        json.dump(websites, file, indent=2)

if __name__ == "__main__":
    websites = generate_websites()
    save_websites_to_file(websites)