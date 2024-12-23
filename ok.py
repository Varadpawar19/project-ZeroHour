import feedparser
import json
import random
import datetime
from geopy.geocoders import Nominatim

# List of RSS feed URLs for the given websites
rss_feeds = [
    "https://thehackernews.com/rss.xml",
    "https://www.itsecurityguru.org/feed/",
    "https://www.securityweek.com/rss",
    "https://www.infosecurity-magazine.com/rss/news/",
    "https://www.csoonline.com/index.rss",
    "https://news.sophos.com/en-us/feed/",
    "https://www.darkreading.com/rss_simple.asp",
    "https://grahamcluley.com/feed/",
    "https://www.wired.com/feed/category/security/latest/rss",
    "https://thecyberexpress.com/feed/",
    "https://social.cyware.com/rss",
    "https://cybermagazine.com/rss",
    "https://krebsonsecurity.com/feed/",
    "https://www.schneier.com/feed/",
    "https://unit42.paloaltonetworks.com/feed/",
    "https://thedfirreport.com/feed/"
]

# Initialize geolocator for extracting location details
geolocator = Nominatim(user_agent="geoapiExercises")

def random_coordinates():
    """Generate random latitude and longitude values."""
    return round(random.uniform(-90, 90), 6), round(random.uniform(-180, 180), 6)

def fetch_and_process_rss():
    all_articles = []

    for url in rss_feeds:
        print(f"Fetching RSS feed from: {url}")
        feed = feedparser.parse(url)

        for entry in feed.entries:
            # Extract data fields
            title = entry.get("title", "No Title")
            link = entry.get("link", "No Link")
            description = entry.get("summary", "No Description")
            published = entry.get("published", str(datetime.datetime.utcnow()))

            # Randomly generate incident details
            incident_id = f"{random.randint(1000, 9999)}"
            severity_value = random.randint(1, 10)
            severity_level = "High" if severity_value > 5 else "Low"
            threat_level = "Critical" if severity_value > 7 else "Low"

            # Random location (can be extended to extract actual location if mentioned in the feed)
            latitude, longitude = random_coordinates()
            location = f"{latitude}, {longitude}"

            article = {
                "title": title,
                "link": link,
                "description": description,
                "published": published,
                "incident_id": incident_id,
                "severity_value": severity_value,
                "severity_level": severity_level,
                "date_of_attack": published,
                "platform": "Web",
                "source": "RSS Feed",
                "threat_level": threat_level,
                "location": location,
                "latitude": latitude,
                "longitude": longitude
            }

            all_articles.append(article)

    return all_articles

def save_articles_to_json(articles, filename="cybersecurity_incidents.json"):
    """Save articles to a JSON file."""
    with open(filename, "w") as f:
        json.dump(articles, f, indent=4)
    print(f"Saved {len(articles)} articles to {filename}")

# Main execution
if __name__ == "__main__":
    print("Starting RSS feed scraping...")
    articles = fetch_and_process_rss()
    save_articles_to_json(articles)
