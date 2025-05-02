import requests
from datetime import datetime
import pytz

API_KEY = "4181da22eab744a184f437a809dc9fd8"  # Replace with your actual NewsAPI key

def get_news(query, max_articles):
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&language=en&pageSize={max_articles}&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching news for '{query}': {response.status_code}")
        return []
    articles = response.json().get("articles", [])
    return [{
        "title": a["title"],
        "source": a["source"]["name"],
        "published": a["publishedAt"],
        "url": a["url"],
        "description": a["description"]
    } for a in articles]

def display_articles(topic, max_articles):
    print(f"\n========== {topic.upper()} NEWS ==========")
    articles = get_news(topic, max_articles)
    if not articles:
        print("⚠️ No news found or API limit exceeded.")
        return

    for article in articles:
        pub_time = datetime.fromisoformat(article["published"].replace("Z", "+00:00"))
        pub_time = pub_time.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%b %d, %Y %I:%M %p")
        print(f"\n🔹 {article['title']}")
        print(f"   📰 {article['source']} • {pub_time}")
        print(f"   📄 {article['description']}")
        print(f"   🔗 {article['url']}")

if __name__ == "__main__":
    print("🗞️ Real-Time News Tracker (Console Edition)")
    print("Stay updated with the latest breaking news.\n")

    topics = ["World News","Stock Market", "US Dollar"]  # You can edit or expand this list
    max_articles = 5  # You can change the number of articles per topic

    for topic in topics:
        display_articles(topic, max_articles)
