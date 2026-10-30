import argparse
import os
import sys
import re
from datetime import datetime
from ddgs import DDGS
import requests
from bs4 import BeautifulSoup
import markdownify

# Configuration
KNOWLEDGE_BASE_DIR = "./data/knowledge_base"

def setup_directory():
    """Ensure the knowledge base directory exists."""
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        os.makedirs(KNOWLEDGE_BASE_DIR)
        print(f"📁 Created directory: {KNOWLEDGE_BASE_DIR}")

def fetch_url_content(url):
    """Fetch and parse content from a URL, converting it to clean Markdown."""
    try:
        # Using a standard user-agent to avoid simple blocks
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove unnecessary tags like scripts, styles, navs
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()

        # Extract the main content (heuristic: usually in body or main)
        main_content = soup.find('main') or soup.find('article') or soup.body

        if not main_content:
            return "_Could not extract main content from this page._"

        # Convert to Markdown
        md_content = markdownify.markdownify(str(main_content), heading_style="ATX")

        # Basic cleanup: remove excessive newlines
        md_content = re.sub(r'\n{3,}', '\n\n', md_content).strip()

        return md_content

    except Exception as e:
        return f"_Failed to fetch content from {url}. Error: {e}_"

def conduct_research(query, num_results=3):
    """Conducts internet research and saves it to a Markdown file."""
    print(f"🔍 Searching the web for: '{query}'...")

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=num_results))

        if not results:
            print("⚠️ No results found.")
            return

        print(f"✅ Found {len(results)} results. Fetching content...")

        date_str = datetime.now().strftime("%Y-%m-%d")
        safe_query = re.sub(r'[^a-zA-Z0-9]', '_', query).lower()
        filename = f"{date_str}_research_{safe_query}.md"
        filepath = os.path.join(KNOWLEDGE_BASE_DIR, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Research Report: {query}\n")
            f.write(f"**Date:** {date_str}\n\n")
            f.write("---\n\n")

            for i, result in enumerate(results, 1):
                title = result.get('title', 'Unknown Title')
                url = result.get('href', 'Unknown URL')
                snippet = result.get('body', '')

                print(f"  [{i}/{len(results)}] Scraping: {title}")

                f.write(f"## {i}. {title}\n")
                f.write(f"**Source URL:** [{url}]({url})\n\n")
                f.write(f"**Brief:** {snippet}\n\n")

                # Fetch detailed content
                content = fetch_url_content(url)

                f.write(f"### Extracted Content\n")
                # Truncate content to avoid massively large files, focusing on the first part
                # Useful for SLMs with limited context windows
                f.write(f"{content[:5000]}...\n\n")

                f.write("---\n\n")

        print(f"🎉 Research complete! Data saved to: {filepath}")

    except Exception as e:
         print(f"❌ An error occurred during research: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Conduct internet research and save to the .ac Second Brain.")
    parser.add_argument("query", type=str, help="The search query you want to research.")
    parser.add_argument("--results", "-r", type=int, default=3, help="Number of search results to scrape (default: 3).")

    args = parser.parse_args()

    setup_directory()
    conduct_research(args.query, args.results)
