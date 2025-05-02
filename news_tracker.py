import streamlit as st
import requests
from datetime import datetime
import pytz

# Page setup
st.set_page_config(page_title="🗞️ Top 10 Global Headlines", layout="wide")
st.title("🗞️ Top 10 Latest News Headlines")
st.caption("Stay updated with the latest breaking news around the world.")

# 🔒 API key (Consider storing in secrets later)
API_KEY = "4181da22eab744a184f437a809dc9fd8"  # Replace with your real NewsAPI key

# 🧠 Country options
country_map = {
    "USA": "us",
    "India": "in",
    "UK": "gb",
    "Australia": "au",
    "Canada": "ca"
}

# 🔘 User Inputs
country_label = st.selectbox("🌍 Choose a country for top headlines", list(country_map.keys()))
country = country_map[country_label]
custom_topic = st.text_input("🔍 Optional: Search for a topic (e.g., AI, Bitcoin)")

# 🔁 Fetcher functions
def get_top_headlines(country="us", max_articles=10):
    url = f"https://newsapi.org/v2/top-headlines?country={country}&pageSize={max_articles}&apiKey={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 429:
        st.error("❌ Rate limit exceeded. Please try again later.")
        return []
    elif response.status_code != 200:
        st.error(f"❌ Failed to fetch news. Status code: {response.status_code}")
        return []

    articles = response.json().get("articles", [])
        # If no articles found, fallback to global news search (for general query)
    if not articles:
        st.warning(f"No top headlines found for {country}. Trying global news...")
        return get_global_news(max_articles=max_articles)
    return articles


def get_global_news(query="news", max_articles=10):
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&pageSize={max_articles}&language=en&apiKey={API_KEY}"
    response = requests.get(url)

    if response.status_code == 429:
        st.error("❌ Rate limit exceeded. Please try again later.")
        return []
    elif response.status_code != 200:
        st.error(f"❌ Failed to fetch global news. Status code: {response.status_code}")
        return []

    articles = response.json().get("articles", [])
    return articles

# 📰 Fetch articles
if custom_topic.strip():
    articles = get_global_news(custom_topic.strip(), max_articles=10)
else:
    articles = get_top_headlines(country=country, max_articles=10)

# 📄 Display articles
if not articles:
    st.warning("⚠️ No news available or API limit exceeded.")
else:
    for article in articles:
        title = article.get("title", "No Title")
        source = article.get("source", {}).get("name", "Unknown Source")
        published = article.get("publishedAt", "")
        url = article.get("url", "#")
        description = article.get("description", "No description available")

        try:
            pub_time = datetime.fromisoformat(published.replace("Z", "+00:00"))
            pub_time = pub_time.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%b %d, %Y %I:%M %p")
        except Exception:
            pub_time = "Unknown time"

        st.markdown(f"### [{title}]({url})")
        st.markdown(f"**{source}** • _{pub_time}_")
        st.markdown(description)
        st.markdown("---")
