import requests

# Replace these placeholders with your actual API key and CSE ID
API_KEY = ' '
CSE_ID = ' '

# Trusted and relevant domains for cybersecurity news
TRUSTED_DOMAINS = [
        '.org', '.edu', '.gov', '.ac.in', '.co.in', '.res.in', '.in', '.nic.in',
    '.org.in', '.firm.in', '.gen.in', '.edu.in', '.gov.in', '.web.in', '.ind.in', '.mobi.in', '.net.in'
]

# Blacklisted domains (e.g., YouTube, social media, irrelevant platforms)
BLACKLISTED_DOMAINS = [
    'youtube.com', 'tiktok.com'
]

# Relevant keywords to filter results
RELEVANT_KEYWORDS = [
    "cybersecurity", "cyber attack", "cyber crime", "data breach",
    "security breach", "hacking", "phishing", "malware", "ransomware",
    "APT", "threat intelligence", "vulnerability", "zero-day", "exploit",
    "cyber espionage", "DDOS", "botnet", "cyber incident", "security incident",
    "data leak", "cyber report", "cyber investigation", "cyber response",
    "cyber alert", "cybersecurity news", "breaking news", "cyber updates",
    "threat analysis", "cyber insights", "critical infrastructure",
    "government cyber attack", "financial sector", "healthcare security",
    "power grid attack", "cyber defense", "cyber threats", "real-time monitoring",
    "incident response", "cyber forensics", "cyber law", "cyber resilience",
    "ethical hacking", "cyber awareness", "cyber risk"
]


def check_safe_browsing(url, api_key):
    """
    Checks if the given URL is flagged as unsafe using Google's Safe Browsing API.
    """
    safe_browsing_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"

    payload = {
        "client": {
            "clientId": "yourclientid",
            "clientVersion": "1.0.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    response = requests.post(safe_browsing_url, json=payload)

    if response.status_code == 200:
        data = response.json()
        if "matches" in data:
            return "Unsafe URL"
        else:
            return "Safe URL"
    else:
        return "Error checking URL"

def get_cyber_attack_websites(query, api_key, cse_id, seen_links):
    """
    Fetches search results using Google's Custom Search API, ensuring no duplicate websites are included.
    """
    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        'key': api_key,
        'cx': cse_id,
        'q': query,
        'num': 10,
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        if 'items' in search_results:
            relevant_websites = []

            for item in search_results['items']:
                link = item['link']
                title = item['title']

                # Skip if the link is blacklisted or already seen
                if any(domain in link for domain in BLACKLISTED_DOMAINS) or link in seen_links:
                    continue

                # Include only trusted domains and relevant keywords
                if (
                    any(domain in link for domain in TRUSTED_DOMAINS)
                    and any(keyword.lower() in title.lower() for keyword in RELEVANT_KEYWORDS)
                ):
                    safe_status = check_safe_browsing(link, api_key)
                    if safe_status == "Safe URL":
                        relevant_websites.append({'title': title, 'link': link, 'safe_status': safe_status})
                        seen_links.add(link)  # Add to the set of seen links

            return relevant_websites
        else:
            return []
    else:
        return []

# Track seen links to avoid duplicates across multiple queries
seen_links = set()

# List of queries
queries = [
    "cyber attack hackernews",
    "real time cyber attack news",
    "real time cyber incidents news",
    "cyber attack",
    "cyber incidents",
    "cyber incidents 2024",
    "critical infrastructure cyber attacks India 2024",
    "India cybersecurity breach 2024",
    "cyber attack 2024",
    "latest global cyber attack updates 2024",
    "cybersecurity news 2024",
    "recent cyber incidents worldwide 2024",
    "cybercrime reports 2024"
]

# Fetch and display results for each query
for query in queries:
    print(f"Searching for: {query}\n")

    websites = get_cyber_attack_websites(query, API_KEY, CSE_ID, seen_links)

    if websites:
        print("Relevant Websites:")
        for i, website in enumerate(websites):
            print(f"{i + 1}. Title: {website['title']}\n   Link: {website['link']}")
            print(f"   Safe Browsing Status: {website['safe_status']}\n")
    else:
        print("No new relevant websites found for this query.")
