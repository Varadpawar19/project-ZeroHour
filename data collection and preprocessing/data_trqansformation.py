# import json
# from datetime import datetime
# import hashlib

# # Load the dataset
# # Load the dataset with the correct encoding
# with open("cybersecurity_news_data.json", "r", encoding="utf-8") as file:
#     dataset = json.load(file)

# # Function to extract features and transform data
# def transform_record(record):
#     # Generate a unique Incident ID
#     unique_string = record.get("link", "") + record.get("pubDate", "")
#     incident_id = f"INC{datetime.now().strftime('%Y%m%d')}{hashlib.md5(unique_string.encode()).hexdigest()[:6]}"
    
#     # Infer the sector from keywords (simple example)
#     content = record.get("contentSnippet", "").lower()
#     if "finance" in content:
#         sector = "Finance"
#     elif "cybersecurity" in content or "PAM" in content:
#         sector = "Cybersecurity"
#     else:
#         sector = "General"
    
#     # Infer incident type (customize logic as needed)
#     if "phishing" in content:
#         incident_type = "Phishing"
#     elif "access" in content:
#         incident_type = "Unauthorized Access"
#     else:
#         incident_type = "Miscellaneous"
    
#     # Threat level (example: assign based on keywords)
#     if "critical" in content or "high risk" in content:
#         threat_level = "High"
#     elif "medium" in content:
#         threat_level = "Medium"
#     else:
#         threat_level = "Low"

#     # Default values for fields not present
#     location = "Global"  # Assume "Global" if location data is missing
    
#     # Transform record to target format
#     transformed = {
#         "Incident_ID": incident_id,
#         "Date": datetime.now().strftime('%Y-%m-%d'),
#         "Platform": record.get("site", "Unknown"),
#         "Sector": sector,
#         "Incident_Type": incident_type,
#         "Threat_Level": threat_level, 
#         "Location": location,
#         "Description": record.get("contentSnippet", "No description available."),
#         "Incident_Solved": False,  # Default value
#         "Source": record.get("link", "Unknown")
#     }
#     return transformed

# # Transform the entire dataset
# transformed_data = [transform_record(record) for record in dataset]

# # Save the transformed data
# with open("transformed_dataset.json", "w") as file:
#     json.dump(transformed_data, file, indent=4)

# print("Data transformation complete. Output saved to 'transformed_dataset.json'.")

# import json
# from datetime import datetime
# import hashlib
# import spacy

# nlp = spacy.load("en_core_web_sm")

# with open("cybersecurity_news_data.json", "r", encoding="utf-8") as file:
#     dataset = json.load(file)

# # Function to extract features using NLP
# def extract_features(text):
#     doc = nlp(text)
#     keywords = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]
#     entities = {ent.label_: ent.text for ent in doc.ents}  # Named entities like locations, dates, etc.
#     return keywords, entities

# # Function to classify incident type based on keywords
# def classify_incident_type(keywords):
#     if "phishing" in keywords:
#         return "Phishing"
#     elif "access" in keywords or "privilege" in keywords:
#         return "Unauthorized Access"
#     elif "attack" in keywords or "breach" in keywords:
#         return "Data Breach"
#     else:
#         return "Miscellaneous"

# # Function to determine threat level based on keywords
# def determine_threat_level(keywords):
#     if "critical" in keywords or "high" in keywords:
#         return "High"
#     elif "medium" in keywords:
#         return "Medium"
#     else:
#         return "Low"

# # Function to extract time from pubDate
# def extract_time_from_pubdate(pub_date):
#     try:
#         dt = datetime.fromisoformat(pub_date.replace("Z", "+00:00"))  # Convert to datetime object
#         return dt.strftime("%H:%M:%S")  # Extract and format time
#     except Exception as e:
#         return "Not Specified"

# # Function to transform a single record
# def transform_record(record):
#     # NLP Analysis
#     content = record.get("contentSnippet", "")
#     keywords, entities = extract_features(content)

#     # Generate a unique Incident ID
#     unique_string = record.get("link", "") + record.get("pubDate", "")
#     incident_id = f"INC{datetime.now().strftime('%Y%m%d')}{hashlib.md5(unique_string.encode()).hexdigest()[:6]}"

#     # Infer sector based on content or keywords
#     if "finance" in keywords or "bank" in keywords or "fina" in keywords:
#         sector = "Finance"
#     elif "cybersecurity" in keywords or "network" in keywords:
#         sector = "Cybersecurity"
#     else:
#         sector = "General"

#     # Classify incident type and determine threat level
#     incident_type = classify_incident_type(keywords)
#     threat_level = determine_threat_level(keywords)

#     # Extract location and time information
#     location = entities.get("GPE", "Global")  # GPE = Geopolitical entity (e.g., countries, cities)
#     time = extract_time_from_pubdate(record.get("pubDate", ""))  # Extract time from pubDate
#     date = entities.get("DATE", "Not Specified")  # Extract date from contentSnippet if available

#     # Transform record into the desired format
#     transformed = {
#         "Incident_ID": incident_id,
#         "Date": datetime.now().strftime('%Y-%m-%d'),
#         "Platform": record.get("site", "Unknown"),
#         "Sector": sector,
#         "Incident_Type": incident_type,
#         "Threat_Level": threat_level,
#         "Location": location,
#         "Time": time,  # Time from pubDate
#         "Reported_Date": date,  # Extracted date from contentSnippet
#         "Description": content,
#         "Incident_Solved": False,
#         "Source": record.get("link", "Unknown")
#     }
#     return transformed

# # Transform the entire dataset
# transformed_data = [transform_record(record) for record in dataset]

# # Save the transformed data into a new JSON file
# with open("transformed_dataset.json", "w", encoding="utf-8") as file:
#     json.dump(transformed_data, file, indent=4)

# print("Data transformation with time extraction complete. Output saved to 'transformed_dataset.json'.")

import json
from datetime import datetime
import hashlib
import spacy
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Load the dataset
with open("cybersecurity_news_data.json", "r", encoding="utf-8") as file:
    dataset = json.load(file)

# Function to extract features using NLP
def extract_features(text):
    doc = nlp(text)
    keywords = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]
    entities = {ent.label_: ent.text for ent in doc.ents}  # Named entities like locations, dates, etc.
    return keywords, entities

# Function to classify incident type based on keywords
def classify_incident_type(keywords):
    if "phishing" in keywords:
        return "Phishing"
    elif "access" in keywords or "privilege" in keywords:
        return "Unauthorized Access"
    elif "attack" in keywords or "breach" in keywords:
        return "Data Breach"
    else:
        return "Miscellaneous"

# Function to determine threat level based on keywords
def determine_threat_level(keywords):
    if "critical" in keywords or "high" in keywords:
        return "High"
    elif "medium" in keywords:
        return "Medium"
    else:
        return "Low"

# Function to extract time from pubDate
def extract_time_from_pubdate(pub_date):
    if not pub_date:  # Handle None or empty pubDate
        logging.warning("Missing or None pubDate encountered.")
        return "Not Specified"
    try:
        dt = datetime.fromisoformat(pub_date.replace("Z", "+00:00"))  # Convert to datetime object
        return dt.strftime("%H:%M:%S")  # Extract and format time
    except ValueError as e:  # Handle invalid date formats
        logging.error(f"Invalid pubDate format: {pub_date}. Error: {e}")
        return "Not Specified"

# Function to transform a single record
def transform_record(record):
    # NLP Analysis
    content = record.get("contentSnippet", "")
    keywords, entities = extract_features(content)

    # Generate a unique Incident ID
    unique_string = str(record.get("link", "")) + str(record.get("pubDate", ""))
    incident_id = f"INC{datetime.now().strftime('%Y%m%d')}{hashlib.md5(unique_string.encode()).hexdigest()[:6]}"

    # Infer sector based on content or keywords
    if "finance" in keywords or "bank" in keywords or "fina" in keywords:
        sector = "Finance"
    elif "cybersecurity" in keywords or "network" in keywords:
        sector = "Cybersecurity"
    else:
        sector = "General"

    # Classify incident type and determine threat level
    incident_type = classify_incident_type(keywords)
    threat_level = determine_threat_level(keywords)

    # Extract location and time information
    location = entities.get("GPE", "Global")  # GPE = Geopolitical entity (e.g., countries, cities)
    time = extract_time_from_pubdate(record.get("pubDate", ""))  # Extract time from pubDate
    date = entities.get("DATE", "Not Specified")  # Extracted date from contentSnippet if available

    # Transform record into the desired format
    transformed = {
        "Incident_ID": incident_id,
        "Date": datetime.now().strftime('%Y-%m-%d'),
        "Platform": record.get("site", "Unknown"),
        "Sector": sector,
        "Incident_Type": incident_type,
        "Threat_Level": threat_level,
        "Location": location,
        "Time": time,  # Time from pubDate
        "Reported_Date": date,  # Extracted date from contentSnippet
        "Description": content,
        "Incident_Solved": False,
        "Source": record.get("link", "Unknown")
    }
    return transformed

# Transform the entire dataset
logging.info("Starting data transformation...")
try:
    transformed_data = [transform_record(record) for record in dataset]
    logging.info("Data transformation complete.")
except Exception as e:
    logging.error(f"An error occurred during data transformation: {e}")
    transformed_data = []

# Save the transformed data into a new JSON file
if transformed_data:
    output_file = "transformed_dataset.json"
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(transformed_data, file, indent=4)
    logging.info(f"Transformed data saved to '{output_file}'.")
else:
    logging.error("No data to save due to errors in transformation.")

print("Data transformation complete. Check logs for details.")
