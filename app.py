import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Netflix Content Analytics", layout="wide")

# -----------------------------
# Title
# -----------------------------
st.title("📺 Netflix Content Analytics Dashboard")

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("netflix_titles.csv")

# Convert 'date_added' to datetime
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added'] = df['date_added'].dt.year

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

# Type filter
content_type = st.sidebar.multiselect(
    "Select Type",
    options=df['type'].dropna().unique(),
    default=df['type'].dropna().unique()
)

# Country filter
country = st.sidebar.multiselect(
    "Select Country",
    options=df['country'].dropna().unique(),
    default=df['country'].dropna().unique()
)

# Apply filters
filtered_df = df[df['type'].isin(content_type)]
if country:
    filtered_df = filtered_df[filtered_df['country'].isin(country)]

# -----------------------------
# Movies vs TV Shows
# -----------------------------
st.subheader("🎬 Movies vs TV Shows")
fig, ax = plt.subplots()
sns.countplot(x='type', data=filtered_df, palette='Set2', ax=ax)
ax.set_title("Number of Movies and TV Shows")
ax.set_xlabel("Type")
ax.set_ylabel("Count")
st.pyplot(fig)

# -----------------------------
# Top Countries
# -----------------------------
st.subheader("🌍 Top Countries")
top_countries = filtered_df['country'].dropna().value_counts().head(10)
fig, ax = plt.subplots()
top_countries.plot(kind='bar', color='skyblue', ax=ax)
ax.set_title("Top 10 Countries by Content Count")
ax.set_xlabel("Country")
ax.set_ylabel("Count")
st.pyplot(fig)

# -----------------------------
# Content Added Over Years
# -----------------------------
st.subheader("📅 Content Added Over Years")
year_counts = filtered_df['year_added'].dropna().value_counts().sort_index()
fig, ax = plt.subplots()
year_counts.plot(kind='line', marker='o', color='green', ax=ax)
ax.set_title("Number of Titles Added Per Year")
ax.set_xlabel("Year Added")
ax.set_ylabel("Count")
st.pyplot(fig)

# -----------------------------
# Top Genres
# -----------------------------
st.subheader("🎭 Top Genres")
# Split genres and drop NaNs
genres = filtered_df['listed_in'].dropna().str.split(',', expand=True).stack()
top_genres = genres.value_counts().head(10)
fig, ax = plt.subplots()
top_genres.plot(kind='bar', color='orange', ax=ax)
ax.set_title("Top 10 Genres")
ax.set_xlabel("Genre")
ax.set_ylabel("Count")
st.pyplot(fig)

# -----------------------------
# Optional: Show Filtered Data
# -----------------------------
st.subheader("Filtered Dataset Preview")
st.dataframe(filtered_df.reset_index(drop=True))

