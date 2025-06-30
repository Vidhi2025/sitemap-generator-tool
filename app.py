import streamlit as st
import pandas as pd
from datetime import datetime
from urllib.parse import urlparse

st.set_page_config(page_title="Free Sitemap Generator", layout="centered")

st.title("🗺️ Free Sitemap Generator Tool")

urls_text = st.text_area("Paste URLs (one per line)", height=250)

col1, col2 = st.columns(2)
with col1:
    freq = st.selectbox("Change Frequency", ["always", "hourly", "daily", "weekly", "monthly", "yearly", "never"], index=2)
with col2:
    lastmod = st.date_input("Last Modified Date", value=datetime.today())

file_type = st.selectbox("Sitemap Type", ["XML", "HTML"])
file_name = st.text_input("Output File Name (no extension)", value="sitemap")

def get_priority(url):
    parsed = urlparse(url)
    return 1.0 if parsed.path in ["", "/"] else 0.9

def generate_xml(df):
    xml = """<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n"""
    for _, row in df.iterrows():
        xml += f"""  <url>
    <loc>{row['url']}</loc>
    <lastmod>{row['lastmod']}</lastmod>
    <changefreq>{row['frequency']}</changefreq>
    <priority>{row['priority']}</priority>
  </url>\n"""
    xml += "</urlset>"
    return xml

def generate_html(df):
    html = "<html><body><ul>\n"
    for _, row in df.iterrows():
        html += f"<li><a href='{row['url']}'>{row['url']}</a></li>\n"
    html += "</ul></body></html>"
    return html

if st.button("Generate Sitemap"):
    urls = [u.strip() for u in urls_text.strip().splitlines() if u.strip()]
    if not urls:
        st.error("Please enter at least one URL.")
    else:
        data = pd.DataFrame({
            "url": urls,
            "frequency": freq,
            "lastmod": lastmod,
            "priority": [get_priority(url) for url in urls]
        })

        content = generate_html(data) if file_type == "HTML" else generate_xml(data)
        mime = "text/html" if file_type == "HTML" else "application/xml"
        st.download_button(f"⬇ Download {file_name}.{file_type.lower()}", content, file_name=f"{file_name}.{file_type.lower()}", mime=mime)
