import streamlit as st
import requests
from datetime import datetime
import pytz

st.set_page_config(page_title="🗞️ Top 10 Global Headlines", layout="wide")
st.title("🗞️ Top 10 Latest News Headlines")
st.caption("Stay updated with the latest breaking news around the world.")

API_KEY = "4181da22eab744a184f437a809dc9fd8"  # Move to Streamlit Secrets for security

def get_top_headlines(country="us", max_articles=10):
    url = f"https://newsapi.org/v2/top-headlines?country={country}&pageSize={max_articles}&apiKey={API_KEY}"
    response = requests.get(url)

    if response.status_code == 429:
        st.error("❌ Rate limit exceeded. Please try again later.")
        return []    
    elif response.status_code != 200:
        st.error("❌ Failed to fetch news.")
        return []

    articles = response.json().get("articles", [])
    return [{
        "title": a["title"],
        "source": a["source"]["name"],
        "published": a["publishedAt"],
        "url": a["url"],
        "description": a["description"]
    } for a in articles]


# Country selector
country = st.selectbox("Choose country for headlines", {
    "USA": "us",
    "India": "in",
    "UK": "gb",
    "Australia": "au",
    "Global (no filter)": ""
})

articles = get_top_headlines(country=country, max_articles=10)

if not articles:
    st.warning("No news available or API limit exceeded.")
else:
    for article in articles:
        pub_time = datetime.fromisoformat(article["published"].replace("Z", "+00:00"))
        pub_time = pub_time.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%b %d, %Y %I:%M %p")
        st.markdown(f"### [{article['title']}]({article['url']})")
        st.markdown(f"**{article['source']}** • _{pub_time}_")
        st.markdown(f"{article['description']}")
        st.markdown("---")
