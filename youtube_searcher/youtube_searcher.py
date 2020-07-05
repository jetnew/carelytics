import json
from youtubesearchpython import searchYoutube

def search(query):
    """Given a query, return list of json results
    (index, id, link, title, channel, duration, views, thumbnails)
    """
    search = searchYoutube(
        keyword=query,
        offset=1,
        mode="json"
    )
    result = json.loads(search.result())['search_result']
    print(f"youtube_searcher.py: {len(result)} results found.")
    return [{'index': r['index'], 'link': r['link'], 'title': r['title'],
             'duration': r['duration'], 'views': r['views'], 'channel': r['channel']}
            for r in result]

# List of json results - (index, id, link, title, channel, duration, views, thumbnails)
# print(search("hong kong beauty product review"))

def search_queries(txtfile="queries.txt"):
    with open(txtfile, 'r') as f:
        results = [search(query.strip()) for query in f]
    return results

# print(search_queries("queries.txt"))