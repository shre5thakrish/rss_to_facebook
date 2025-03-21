import os
import feedparser
from facebook import GraphAPI

# Facebook setup
FB_PAGE_ID = os.getenv('615481804977173')
FB_ACCESS_TOKEN = os.getenv('EAAHs4IJ1IwcBOZCVnZACq4yS9ffyb1MVwjtZBJDhsNXMRZCVZAM2TabeXrekzL2KMaF7C4qDqwVZBfCx3s6EZBA2JfZBw83oZCvtv20hxaFnLKEcfMU4mz8MD7J7a0jqPOJUw0JoCtzfZBLEJe11iricqsjtH6C40gRnIeB2zNwKqnA5nvP6jth7TdxZCPiSv9drW2oGBhoMGmJ3N9rFOZBZC4ysJm22nhnTUh9zo6v5pfZB2y')
graph = GraphAPI(FB_ACCESS_TOKEN)

RSS_FEEDS = [
     'http://feeds.bbci.co.uk/news/world/rss.xml',
    'http://rss.cnn.com/rss/edition_world.rss',
    'https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best',
    'https://rss.nytimes.com/services/xml/rss/nyt/World.xml',
    'https://www.theguardian.com/world/rss',
     'https://www.aljazeera.com/xml/rss/all.xml',
     'https://apnews.com/rss',
   'https://rss.dw.com/rdf/rss-en-world'
]

def get_new_entries(last_run_entries):
    new_entries = []
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            # Use link as fallback ID if no entry.id exists
            entry_id = entry.get('id', entry.link)
            if entry_id not in last_run_entries:
                new_entries.append({
                    'id': entry_id,
                    'title': entry.title,
                    'link': entry.link,
                    'content': entry.description[:500] + '...' if entry.description else ""
                })
    return new_entries

def post_to_facebook(message, link):
    try:
        graph.put_object(
            parent_object=FB_PAGE_ID,
            connection_name='feed',
            message=message,
            link=link
        )
        print(f"Posted: {message}")
    except Exception as e:
        print(f"Error posting: {str(e)}")

if __name__ == "__main__":
    # Track posted entries
    last_run_entries = set()
    
    try:
        with open('posted_entries.txt', 'r') as f:
            last_run_entries = set(f.read().splitlines())
    except FileNotFoundError:
        pass

    new_entries = get_new_entries(last_run_entries)
    
    with open('posted_entries.txt', 'a') as f:
        for entry in new_entries:
            post_text = f"📢 {entry['title']}\n\n{entry['content']}"
            post_to_facebook(post_text, entry['link'])
            f.write(f"{entry['id']}\n")
