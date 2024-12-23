const RSSParser = require("rss-parser");
const fs = require("fs");
const schedule = require("node-schedule");

const parser = new RSSParser();

// List of valid RSS feed URLs
const feedUrls = [
    "https://thehackernews.com/rss.xml", // Hacker News RSS Feed
    "https://threatpost.com/feed/",       // ThreatPost RSS Feed
    "https://www.darkreading.com/rss_simple.asp", // Dark Reading RSS Feed
    "https://www.bleepingcomputer.com/feed/",         // BleepingComputer
    "https://feeds.feedburner.com/TheHackersNews",    // The Hackers News
    "https://www.schneier.com/feed/",                 // Bruce Schneier's Blog
    "https://www.cisa.gov/news.xml",                  // CISA (Government Alerts)
    "https://www.us-cert.gov/ncas/all.xml",          // US-CERT Alerts
    "https://www.zdnet.com/topic/security/rss.xml",   // ZDNet Security
    "https://nakedsecurity.sophos.com/feed",          // Sophos Security
    "https://www.infosecurity-magazine.com/rss/news", // InfoSecurity Magazine
    "https://feeds.feedburner.com/securityweek",      // SecurityWeek
    "https://www.helpnetsecurity.com/feed",           // Help Net Security
];

let allArticles = []; // Consolidated list to store all articles

async function scrapeRSSFeeds() {
    console.log("Starting RSS scraping...");

    let newArticles = [];

    for (const url of feedUrls) {
        try {
            console.log(`Fetching data from: ${url}`);
            const feed = await parser.parseURL(url);
            const siteArticles = feed.items.map((item) => ({
                site: feed.title,
                title: item.title,
                link: item.link,
                pubDate: new Date(item.pubDate), // Convert publication date to a Date object
                contentSnippet: item.contentSnippet || "",
            }));

            console.log(`Fetched ${siteArticles.length} articles from ${url}`);
            // Log the fetched articles
            siteArticles.forEach(article => {
                console.log(`Title: ${article.title}`);
                console.log(`Link: ${article.link}`);
                console.log(`Published Date: ${article.pubDate}`);
                console.log(`Snippet: ${article.contentSnippet}`);
                console.log('-------------------');
            });

            // Add to newArticles
            newArticles = [...newArticles, ...siteArticles];
        } catch (error) {
            console.error(`Error fetching data from ${url}:`, error.message || error);
        }
    }

    // Merge the new articles with the existing articles
    allArticles = [...newArticles, ...allArticles];

    // Remove duplicate articles based on the 'link'
    allArticles = allArticles.filter(
        (article, index, self) =>
            index === self.findIndex((a) => a.link === article.link)
    );

    // Sort the consolidated list by publication date, newest first
    allArticles.sort((a, b) => b.pubDate - a.pubDate);

    // Save the combined results to a JSON file
    fs.writeFileSync("cybersecurity_news_combined.json", JSON.stringify(allArticles, null, 2));
    console.log("Scraped data saved to cybersecurity_news_combined.json");
}
let scraper_number = 1
// Schedule the scraper to run every 5 minutes
schedule.scheduleJob("*/5 * * * *", async () => {
    console.log("Scheduled scraping started...");
    await scrapeRSSFeeds();
    console.log("Scheduled scraping completed. number :",scraper_number);
    scraper_number++;
});

// Run the scraper immediately on startup
scrapeRSSFeeds()
    .then(() => console.log("Initial scraping completed."))
    .catch((error) => console.error("Error during initial scraping:", error));