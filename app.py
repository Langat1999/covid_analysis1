import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re
from collections import Counter

# ✅ Page setup
st.set_page_config(
    page_title="CORD-19 Explorer",
    layout="wide",
    page_icon="🦠"
)

st.title("🦠 CORD-19 Research Papers Explorer")
st.markdown("""
Explore trends in COVID-19 scientific research from the CORD-19 dataset.

This interactive app allows you to analyze paper counts, top journals, keywords, and more.
""")

# ✅ File uploader
uploaded_file = st.file_uploader("📂 Upload your `metadata.csv` file", type=["csv"])

# ✅ Load and validate uploaded file
@st.cache_data(show_spinner="📥 Loading uploaded data...")
def load_data(file):
    try:
        df = pd.read_csv(file, low_memory=False)

        # Fallback for missing publish_time
        if 'publish_time' not in df.columns:
            fallback_cols = ['pub_date', 'published', 'date', 'publication_date', 'created']
            for col in fallback_cols:
                if col in df.columns:
                    df.rename(columns={col: 'publish_time'}, inplace=True)
                    break
            else:
                st.error("❌ No valid date column found.")
                return pd.DataFrame()

        df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
        df['year'] = df['publish_time'].dt.year
        df = df[df['year'].notna()]
        df['year'] = df['year'].astype(int)

        if 'journal' not in df.columns:
            df['journal'] = "Unknown"

        return df

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        return pd.DataFrame()

if uploaded_file:
    df = load_data(uploaded_file)
    if df.empty:
        st.stop()
else:
    st.info("⬆️ Please upload the CORD-19 `metadata.csv` file to begin.")
    st.stop()

# ✅ Sidebar filters
with st.sidebar:
    st.header("🔧 Filters")
    min_year = max(2019, int(df['year'].min()))
    max_year = int(df['year'].max())
    year_range = st.slider("Select Year Range", min_year, max_year, (min_year, max_year))

    journals = ['All'] + sorted(df['journal'].dropna().unique().tolist())
    selected_journal = st.selectbox("Select Journal", journals)

# ✅ Filter data
filtered_df = df[df['year'].between(year_range[0], year_range[1])]
if selected_journal != 'All':
    filtered_df = filtered_df[filtered_df['journal'] == selected_journal]

# ✅ Summary metrics
st.subheader("📊 Summary Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Papers", len(filtered_df))
col2.metric("Unique Journals", filtered_df['journal'].nunique())
col3.metric("Year Range", f"{year_range[0]} - {year_range[1]}")

# ✅ Papers by Year
st.subheader("📈 Publications by Year")
all_years = list(range(year_range[0], year_range[1] + 1))
yearly_counts = filtered_df['year'].value_counts().reindex(all_years, fill_value=0).sort_index()
fig, ax = plt.subplots()
ax.plot(yearly_counts.index, yearly_counts.values, marker='o')
ax.set_xlabel("Year")
ax.set_ylabel("Number of Publications")
ax.set_title("COVID-19 Papers Published Over Time")
ax.grid(True)
st.pyplot(fig)

# ✅ Top Journals
st.subheader("🏆 Top 10 Journals")
top_journals = filtered_df['journal'].value_counts().head(10)
fig2, ax2 = plt.subplots()
sns.barplot(x=top_journals.values, y=top_journals.index, ax=ax2)
ax2.set_xlabel("Number of Papers")
ax2.set_title("Top Journals Publishing COVID-19 Research")
st.pyplot(fig2)

# ✅ Source Distribution
if 'source_x' in filtered_df.columns:
    st.subheader("📦 Distribution by Source")
    fig3, ax3 = plt.subplots()
    filtered_df['source_x'].value_counts().plot(kind='bar', ax=ax3)
    ax3.set_title("Number of Papers by Source")
    ax3.set_xlabel("Source")
    ax3.set_ylabel("Paper Count")
    st.pyplot(fig3)

# ✅ Word Frequency (Titles)
st.subheader("🧠 Most Frequent Words in Titles")
def clean_and_tokenize(texts):
    words = []
    for text in texts:
        tokens = re.findall(r'\b\w+\b', str(text).lower())
        words.extend(tokens)
    stopwords = set([
        'the', 'and', 'of', 'in', 'a', 'to', 'for', 'on', 'with',
        'by', 'from', 'an', 'as', 'is', 'are', 'at', 'this', 'that',
        'we', 'study', 'covid', 'using', 'use', 'data', 'paper'
    ])
    return [word for word in words if word not in stopwords and len(word) > 2]

words = clean_and_tokenize(filtered_df['title'])
word_freq = Counter(words)
common_words = dict(word_freq.most_common(100))

# ✅ Word Cloud
st.subheader("☁️ Word Cloud of Titles")
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(common_words)
fig4, ax4 = plt.subplots(figsize=(10, 5))
ax4.imshow(wordcloud, interpolation='bilinear')
ax4.axis('off')
st.pyplot(fig4)

# ✅ Sample data
st.subheader("📄 Sample Papers")
st.dataframe(filtered_df[['title', 'journal', 'year', 'publish_time']].head(10), use_container_width=True)

# ✅ Download option
st.subheader("💾 Download Filtered Data")
csv = filtered_df.to_csv(index=False)
st.download_button("📥 Download CSV", data=csv, file_name="cord19_filtered.csv", mime="text/csv")

# ✅ Footer
st.markdown("---")
st.markdown("📘 Built by **Jackson Mutiso Langat** | 📧 mutisojackson55@gmail.com")
