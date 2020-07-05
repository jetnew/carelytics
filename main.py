import os
from youtube_searcher.youtube_searcher import search_queries

"""Get video results from list of queries"""
# # [[{query1_video1}, {query2_video2}], [{query2_video1}]
# results = search_queries("youtube_searcher/queries.txt")
#
"""Download videos onto local computer"""
# from tqdm import tqdm
# from video_indexer.youtube_downloader import download_youtube
# for query_result in results:
#     for video_result in tqdm(query_result):
#         title, link, duration = video_result['title'], video_result['link'], video_result['duration']
#         download_youtube(video_url=link, videoname=title)

"""Upload all videos to indexer"""
# from utils.util import append_cache, read_cache
# from video_indexer.youtube_indexer import upload_to_indexer
# videonames = read_cache("utils/videofile.txt")
# for videofile in os.listdir("videos"):
#     if videofile.endswith(".mp4") and videofile not in videonames:
#         vid_id = upload_to_indexer(videofile)
#         append_cache(vid_id, 'utils/video_id.txt')
#         append_cache(videofile, 'utils/videofile.txt')

"""Retrieve indexed video info"""
# from utils.util import read_cache, save_pickle
# from video_indexer.youtube_indexer import get_indexer_results, collect_indexed_info
# video_ids = read_cache("utils/video_id.txt")
# videos_indexed = [get_indexer_results(video_id) for video_id in video_ids]
# dataset = collect_indexed_info(videos_indexed)
# save_pickle("dataset.pkl", dataset)

"""Get youtube dataset in pkl"""
# from utils.util import load_pickle
# dataset = load_pickle("dataset.pkl")

"""Get reddit dataset in dataframe"""
# from reddit_searcher.reddit_searcher import get_subreddit_df
# get_subreddit_df("AsianBeauty", limit=100)

"""Get twitter dataset in dataframe"""
