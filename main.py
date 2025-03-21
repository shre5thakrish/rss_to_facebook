import os
import feedparser
from facebook import GraphAPI

# Debug: Print environment variables safely
print("FB_PAGE_ID:", os.getenv('615481804977173'))
print("FB_ACCESS_TOKEN:", "[EAAHs4IJ1IwcBO0uBjvIZBxBzLNaC0N9BZBXPvPEIrPxIaDCbqR3pqYyh5fQNl6UilrjSJ7Gi5IXBJzGSljsrwn05GgKxESbyGpYAKzpgOnfyU42ZAxJyGUpJZBxqLvGrZCbt2vtNUzI9dMUZAWbXpiV6LWIgFaZAIkdDZC16Knj3YyjXuAP8H1f209EwYFhzZCXcCVZBaJxLWZCgYVQvnz10poZBHkLucKtHEOR4gZAMEmdHS


]")  # Do not print the actual token for security reasons

# Facebook setup
FB_PAGE_ID = os.getenv('615481804977173')
FB_ACCESS_TOKEN = os.getenv('EAAHs4IJ1IwcBO0uBjvIZBxBzLNaC0N9BZBXPvPEIrPxIaDCbqR3pqYyh5fQNl6UilrjSJ7Gi5IXBJzGSljsrwn05GgKxESbyGpYAKzpgOnfyU42ZAxJyGUpJZBxqLvGrZCbt2vtNUzI9dMUZAWbXpiV6LWIgFaZAIkdDZC16Knj3YyjXuAP8H1f209EwYFhzZCXcCVZBaJxLWZCgYVQvnz10poZBHkLucKtHEOR4gZAMEmdHS


')

if not FB_PAGE_ID or not FB_ACCESS_TOKEN:
    raise ValueError("Missing Facebook credentials. Check GitHub Secrets.")

# Debug: Print the page ID and confirm token is set
print("Using Page ID:", FB_PAGE_ID)
print("Access Token is set:", bool(FB_ACCESS_TOKEN))  # Confirm token is not empty

graph = GraphAPI(access_token=FB_ACCESS_TOKEN, version="3.0")

# RSS feeds (customize as needed)
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
            entry_id = entry.get('id', entry.get('link', ''))
            title = entry.get('title', 'No Title')
            link = entry.get('link', '')
            description = entry.get('description', '')
            
            if entry_id not in last_run_entries:
                content = (description[:500] + '...') if description else ""
                new_entries.append({
                    'id': entry_id,
                    'title': title,
                    'link': link,
                    'content': content
                })
    return new_entries

def post_to_facebook(message, link):
    try:
        if link:
            graph.put_object(
                parent_object=FB_PAGE_ID,
                connection_name='feed',
                message=message,
                link=link
            )
            print(f"Posted: {message}")
        else:
            print("Skipped post - Missing link")
    except Exception as e:
        print(f"Facebook API Error: {str(e)}")

if __name__ == "__main__":
    last_run_entries = set()
    
    try:
        with open('posted_entries.txt', 'r') as f:
            last_run_entries = set(f.read().splitlines())
    except FileNotFoundError:
        pass

    new_entries = get_new_entries(last_run_entries)
    
    with open('posted_entries.txt', 'a') as f:
        for entry in new_entries:
            post_text = f"📢 {entry['title']}"
            if entry['content']:
                post_text += f"\n\n{entry['content']}"
                
            post_to_facebook(post_text, entry['link'])
            f.write(f"{entry['id']}\n")
