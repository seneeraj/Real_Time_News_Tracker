import requests
import pandas as pd

API_KEY = "4181da22eab744a184f437a809dc9fd8"
TOPICS = ["NSE stock market", "World News", "India Pakistan", "Sports", "Gold Trend"]
MAX_ARTICLES = 1

def get_news(query):
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&language=en&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error {response.status_code}")
        return []
    articles = response.json().get("articles", [])
    return [{
        "Topic": query,
        "Title": a["title"],
        "Source": a["source"]["name"],
        "Published": a["publishedAt"],
        "URL": a["url"]
    } for a in articles[:MAX_ARTICLES]]

# Collect and display
all_news = []
for topic in TOPICS:
    all_news.extend(get_news(topic))

df = pd.DataFrame(all_news)
df.head()list
    max_articles = 5  # You can change the number of articles per topic

    for topic in topics:
        display_articles(topic, max_articles)
