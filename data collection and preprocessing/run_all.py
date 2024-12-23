import subprocess
import os

# Run the Python script to fetch websites and save them to websites.json
print("Running Python script to fetch websites...")
subprocess.run(["python", "d:\\vscode\\SIH\\integrate\\get_websites.py"], check=True)

# Verify that websites.json was created
if not os.path.exists("websites.json"):
    print("Error: websites.json was not generated. Exiting.")
else:
    print("websites.json generated. Running Node.js script...")

    # Run the Node.js script to process the URLs
    subprocess.run(["node", "d:\\vscode\\SIH\\integrate\\live_data.js"], check=True)

    print("Node.js script executed successfully.")
