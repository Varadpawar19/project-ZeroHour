# Import necessary libraries
import feedparser
import json
import random
import datetime
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from transformers import pipeline
import subprocess
import schedule
import time
import re

# Initialize geolocator for extracting location details
geolocator = Nominatim(user_agent="geoapiExercises")

# Initialize sentiment analysis and named entity recognition pipelines
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER")

# RSS feeds and websites
rss_feeds = [
    "https://thehackernews.com/rss.xml",
    "https://www.securityweek.com/rss",
    "https://www.infosecurity-magazine.com/rss/news/",
    "https://thecyberexpress.com/feed/",
]

extra_websites = [
    "https://website.rbi.org.in/web/rbi/search?q=cyberattack",
    "https://www.sebi.gov.in/search.html?searchval=cyberattacks",
    "https://irdai.gov.in/search?q=cyberattacks",
    "https://trai.gov.in/whats-new",
    "https://www.nciipc.gov.in/alert_and_Advisories.html",
    "https://cybercrime.gov.in/",
    "https://www.cybersecurityintelligence.com/blog.php?keywords=cyberattacks&submit=",
    "https://www.bing.com/news/search?q=CERT-In+Cyber+Attack",
    "https://flashpoint.io/intelligence-101/advanced-persistent-threat/",
    "https://newsroom.cisco.com/c/services/i/servlets/newsroom/rssfeed.json?feed=articles",
    "https://www.hackerone.com/press",
    "https://www.infosecurity-magazine.com/advanced-persistent-threats",
    "https://www.securitymagazine.com/keywords/4547-advanced-persistent-threat"
]

# Helper functions
def random_coordinates():
    """Generate random latitude and longitude values."""
    return round(random.uniform(-90, 90), 6), round(random.uniform(-180, 180), 6)

def fetch_rss_feeds():
    """Fetch articles from RSS feeds."""
    articles = []
    for url in rss_feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            if "India" in entry.get("summary", "") or "India" in entry.get("title", ""):
                articles.append({
                    "title": entry.get("title", "No Title"),
                    "link": entry.get("link", "No Link"),
                    "description": entry.get("summary", "No Description"),
                    "published": entry.get("published", str(datetime.datetime.utcnow()))
                })
    return articles

def scrape_websites():
    """Scrape additional data from websites."""
    articles = []
    for url in extra_websites:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Custom scraping logic for websites
            for tag in soup.find_all(["h1", "h2", "h3", "p", "div"], text=True):
                text = tag.get_text(strip=True)
                if "India" in text or "CERT-In" in text:
                    link = tag.find("a")["href"] if tag.find("a") else url
                    articles.append({
                        "title": text[:80],
                        "link": link,
                        "description": text,
                        "published": str(datetime.datetime.utcnow())
                    })
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    return articles

def extract_ner(text):
    """Extract named entities like organizations, threat actors, etc.""" 
    ner_results = ner_pipeline(text)
    entities = {result["entity"]: result["word"] for result in ner_results}
    return entities

def calculate_severity(sentiment_label, sentiment_score):
    """Calculate severity based on sentiment label and score.""" 
    severity = "Low"
    if sentiment_label == "NEGATIVE" and sentiment_score > 0.75:
        severity = "High"
    elif sentiment_label == "NEGATIVE":
        severity = "Medium"
    return severity

def generate_article_data(article, severity_threshold):
    """Generate additional fields for each article, filtered by severity."""
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

    if severity == "High" or severity == severity_threshold:
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
            "incident_id": incident_id
        }

# Scheduler Function
def run_scraper(severity_threshold="Medium"):
    """Run the scraper with the given severity threshold."""
    print("Fetching RSS feeds...")
    rss_articles = fetch_rss_feeds()

    print("Scraping additional websites...")
    web_articles = scrape_websites()

    all_articles = rss_articles + web_articles
    processed_articles = [generate_article_data(article, severity_threshold) for article in all_articles if article]

    print("Saving articles to a JSON file...")
    new_json_filename = "india_cybersecurity_incidents.json"
    with open(new_json_filename, "w") as f:
        json.dump(processed_articles, f, indent=4)

    print(f"Saved {len(processed_articles)} articles to {new_json_filename}.")

# Schedule the scraper to run every 20 minutes
schedule.every(20).minutes.do(run_scraper)

if _name_ == "_main_":
    print("Starting the real-time scraper...")
    while True:
        schedule.run_pending()
        time.sleep(1)