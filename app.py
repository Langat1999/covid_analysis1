import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import StringIO

# ✅ Page setup
st.set_page_config(
    page_title="CORD-19 Explorer",
    layout="wide",
    page_icon="🦠"
)

# ✅ App title and description
st.title("🦠 CORD-19 Research Papers Explorer")

st.markdown("""
Welcome to the **CORD-19 Explorer** — a tool to help visualize and analyze COVID-19 research trends from the CORD-19 dataset.

Use the sidebar filters to refine the data by **year** and **journal**. You can also search paper titles and download filtered data.
""")

# ✅ Load and cache data from Google Drive (large file support)
@st.cache_data
def load_data():
    try:
        file_id = "18trAu6UY9hnGUEF8_YHKcJrMXXzqGu6a"
        base_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        session = requests.Session()
        response = session.get(base_url, stream=True)

        # Detect and bypass large file confirmation prompt
        for key, value in response.cookies.items():
            if key.startswith("download_warning"):
                confirm_token = value
                base_url = f"https://drive.google.com/uc?export=download&confirm={confirm_token}&id={file_id}"
                response = session.get(base_url, stream=True)
                break

        content = response.content.decode('utf-8')
        csv_data = StringIO(content)

        df = pd.read_csv(csv_data, low_memory=False)
        df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
        df['year'] = df['publish_time'].dt.year.fillna(0).astype(int)
        return df

    except Exception as e:
        st.error(f"❌ Error loading data from Google Drive: {e}")
        return pd.DataFrame()

df = load_data()

# ✅ Stop app if data is not loaded
if df.empty:
    st.stop()

# ✅ Sidebar: Filters
with st.sidebar:
    st.header("🔧 Filters")

    # Year range
    min_year = max(2019, int(df['year'].min()))
    max_year = int(df['year'].max())
    year_range = st.slider("Select year range:", min_year, max_year, (min_year, max_year))

    # Journal selector
    journals = ['All'] + sorted(df['journal'].dropna().unique().tolist())
    selected_journal = st.selectbox("Filter by journal:", journals)

# ✅ Filter data based on sidebar
filtered_df = df[
    (df['year'] >= year_range[0]) & (df['year'] <= year_range[1])
]
if selected_journal != 'All':
    filtered_df = filtered_df[filtered_df['journal'] == selected_journal]

# ✅ Metrics Summary
st.subheader("📊 Summary Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Papers", len(filtered_df))
col2.metric("Unique Journals", filtered_df['journal'].nunique())
col3.metric("Date Range", f"{year_range[0]} - {year_range[1]}")
col4.metric("Latest Year", int(filtered_df['year'].max()) if not filtered_df.empty else "N/A")

# ✅ Data Preview
st.subheader("📄 Sample Papers")
if not filtered_df.empty:
    st.dataframe(
        filtered_df[['title', 'journal', 'year', 'publish_time']].head(10),
        use_container_width=True
    )
else:
    st.info("No data available for the selected filters.")

# ✅ Visualizations
st.subheader("📈 Visual Insights")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Publications by Year")
    if not filtered_df.empty:
        year_counts = filtered_df['year'].value_counts().sort_index()
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        ax1.bar(year_counts.index, year_counts.values, color='skyblue', edgecolor='black')
        ax1.set_xlabel("Year")
        ax1.set_ylabel("Number of Papers")
        ax1.set_title("COVID-19 Publications by Year")
        ax1.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig1)
    else:
        st.info("No data available.")

with col2:
    st.markdown("#### Top 10 Journals")
    if not filtered_df.empty:
        top_journals = filtered_df['journal'].value_counts().head(10)
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        ax2.barh(top_journals.index[::-1], top_journals.values[::-1], color='lightgreen', edgecolor='black')
        ax2.set_xlabel("Number of Papers")
        ax2.set_title("Top Journals Publishing COVID-19 Research")
        ax2.grid(axis='x', linestyle='--', alpha=0.7)
        st.pyplot(fig2)
    else:
        st.info("No journal data to display.")

# ✅ Advanced Search
with st.expander("🔍 Advanced Title Search"):
    search_term = st.text_input("Enter a keyword to search paper titles:")
    if search_term:
        search_results = filtered_df[filtered_df['title'].str.contains(search_term, case=False, na=False)]
        st.success(f"Found {len(search_results)} matching paper(s).")
        st.dataframe(search_results[['title', 'journal', 'year', 'publish_time']].head(10), use_container_width=True)

# ✅ Download section
st.subheader("💾 Export Filtered Data")
if not filtered_df.empty:
    csv = filtered_df[['title', 'journal', 'year', 'publish_time']].to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"cord19_filtered_{year_range[0]}_{year_range[1]}.csv",
        mime="text/csv"
    )

# ✅ Footer
st.markdown("---")
st.markdown("📘 Made with ❤️ by **Jackson Mutiso Langat** | 📧 mutisojackson55@gmail.com")
