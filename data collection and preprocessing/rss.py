# Install required packages (only needed in specific environments)
try:
    import feedparser  
    import requests
    from bs4 import BeautifulSoup  
    from geopy.geocoders import Nominatim  
    from transformers import pipeline  
except ImportError:
    import subprocess
    import sys
    required_packages = [
        "feedparser",
        "requests",
        "beautifulsoup4",
        "geopy",
        "transformers"
    ]
    for package in required_packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Import libraries
import feedparser
import json
import random
import datetime
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from transformers import pipeline  

# Initialize geolocator for extracting location details
geolocator = Nominatim(user_agent="geoapiExercises")

# Initialize sentiment analysis and named entity recognition pipelines
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER")

# RSS feeds and websites for news articles
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

extra_websites = [
    "https://www.sans.org/white-papers/",
    "https://www.darkreading.com/cyberattacks-data-breaches",
    "https://www.trellix.com/advanced-research-center/threat-reports/",
    "https://portswigger.net/daily-swig",
    "https://threatpost.com/",
    "https://cyberscoop.com/news/threats/cybercrime/",
    "https://thisweekin4n6.com/page/2/",
    "https://www.bleepingcomputer.com/"
]

# IOC sources (example URLs)
ioc_sources = [
    "https://threatfox.abuse.ch/",
    "https://otx.alienvault.com/",
    "https://www.abuseipdb.com/",
]

# Helper functions
def random_coordinates():
    """Generate random latitude and longitude values."""
    return round(random.uniform(-90, 90), 6), round(random.uniform(-180, 180), 6)

def fetch_rss_feeds():
    """Fetch articles from RSS feeds."""
    articles = []
    for url in rss_feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                articles.append({
                    "title": entry.get("title", "No Title"),
                    "link": entry.get("link", "No Link"),
                    "description": entry.get("summary", "No Description"),
                    "published": entry.get("published", str(datetime.datetime.utcnow()))
                })
        except Exception as e:
            print(f"Error fetching RSS feed from {url}: {e}")
    return articles

def scrape_websites():
    """Scrape additional data from websites."""
    articles = []
    for url in extra_websites:
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
            for tag in soup.find_all(["h1", "h2", "h3"]):
                title = tag.text.strip()
                link = tag.find("a")["href"] if tag.find("a") else url
                description = tag.text.strip()
                articles.append({"title": title, "link": link, "description": description, "published": str(datetime.datetime.utcnow())})
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    return articles

def scrape_iocs():
    """Scrape IOCs from specified sources."""
    iocs = []
    for url in ioc_sources:
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Example logic to find IOCs; adjust based on actual HTML structure of your sources.
            for row in soup.find_all('tr'):  # Assuming IOCs are listed in table rows.
                cells = row.find_all('td')
                if len(cells) >= 2:  # Adjust based on expected number of cells.
                    ioc_value = cells[0].text.strip()
                    ioc_type = cells[1].text.strip()  # Assuming second cell indicates type (IP/Domain).
                    iocs.append({"ioc": ioc_value, "type": ioc_type})
                    
        except Exception as e:
            print(f"Error scraping IOCs from {url}: {e}")
    
    return iocs

def extract_ner(text):
    """Extract named entities like organizations, threat actors, etc.""" 
    try:
        ner_results = ner_pipeline(text)
        entities = {result["entity"]: result["word"] for result in ner_results}
        return entities
    except Exception as e:
        print(f"Error in NER extraction: {e}")
        return {}

def calculate_severity(sentiment_label, sentiment_score):
    """Calculate severity based on sentiment label and score."""
    severity = "Low"
    if sentiment_label == "NEGATIVE" and sentiment_score > 0.75:
        severity = "High"
    elif sentiment_label == "NEGATIVE":
        severity = "Medium"
    return severity

def generate_article_data(article):
    """Generate additional fields for each article."""
    title = article.get("title", "No Title")
    description = article.get("description", "")
    
    sentiment = sentiment_analyzer(description[:512])[0]  # Limit to 512 tokens

    latitude, longitude = random_coordinates()
    location = f"{latitude}, {longitude}"
    
    incident_id = f"{random.randint(1000, 9999)}"

    sectors = ["Banking", "Defense", "Telecom", "Energy", "Healthcare", "Transportation", "IT"]
    affected_sector = random.choice(sectors)

    ner_entities = extract_ner(description)
    organization = ner_entities.get("ORG", "Unknown")
    
    severity = calculate_severity(sentiment["label"], sentiment["score"])

    solved_status = random.choice(["Yes", "No"])
    
    solved_date = str(datetime.datetime.utcnow()) if solved_status == "Yes" else "Unsolved"

    return {
        "title": title,
        "description": description,
        "sentiment_score": sentiment["score"],
        "sentiment_label": sentiment["label"],
        "severity": severity,
        "affected_sector": affected_sector,
        "solved_status": solved_status,
        "solved_date": solved_date,
        "organization": organization,
        "attack_type": random.choice(["Ransomware", "Phishing", "DDoS", "Malware", "Insider Threat"]),
        "economic_impact": f"${random.randint(1000, 1000000)}",  # Example monetary loss in USD
        "location": location,
        "latitude": latitude,
        "longitude": longitude,
        "published": article.get("published"),
        'incident_id': incident_id,
        'iocs': []  # Placeholder for IOCs to be filled later.
   }

# Main Execution
if _name_ == "_main_":
    
   print("Fetching RSS feeds...")
   rss_articles = fetch_rss_feeds()

   print("Scraping additional websites...")
   web_articles = scrape_websites()

   print("Scraping IOCs...")
   iocs_data = scrape_iocs()  # Fetching IOCs

   all_articles = rss_articles + web_articles
   
   processed_articles = [generate_article_data(article) for article in all_articles]

   # Integrate IOCs into processed articles (you can customize this logic)
   for article in processed_articles:
       article['iocs'] += [{"ioc": ioc['ioc'], 'type': ioc['type']} for ioc in iocs_data]

   print("Saving articles to a new JSON file...")
   new_json_filename = 'new_cybersecurity_incidents.json'
   with open(new_json_filename, 'w') as f:
       json.dump(processed_articles, f, indent=4)

   print(f"Saved {len(processed_articles)} articles to {new_json_filename}.")