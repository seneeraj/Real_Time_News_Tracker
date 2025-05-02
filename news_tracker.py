import streamlit as st
import requests
from datetime import datetime
import pytz

st.set_page_config(page_title="🗞️ Real-Time News Tracker", layout="wide")
st.title("🗞️ Real-Time News Tracker")
st.caption("Stay updated with the latest breaking news.")

API_KEY = "4181da22eab744a184f437a809dc9fd8"  # Put this in secrets for security

def get_news(query, max_articles):
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&language=en&pageSize={max_articles}&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    articles = response.json().get("articles", [])
    return [{
        "title": a["title"],
        "source": a["source"]["name"],
        "published": a["publishedAt"],
        "url": a["url"],
        "description": a["description"]
    } for a in articles]

topics = st.multiselect("Choose topics", ["World News", "Stock Market", "US Dollar", "Politics", "Technology"], default=["Stock Market", "US Dollar"])
max_articles = st.slider("Number of articles per topic", 1, 10, 5)

for topic in topics:
    st.subheader(f"📌 {topic} News")
    articles = get_news(topic, max_articles)
    if not articles:
        st.warning("No news found or API limit exceeded.")
        continue

    for article in articles:
        pub_time = datetime.fromisoformat(article["published"].replace("Z", "+00:00"))
        pub_time = pub_time.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%b %d, %Y %I:%M %p")

        with st.container():
            st.markdown(f"### [{article['title']}]({article['url']})")
            st.markdown(f"**{article['source']}** • _{pub_time}_")
            st.markdown(f"{article['description']}")
            st.markdown("---")
