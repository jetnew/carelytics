import json
from video_indexer.video_indexer_api import VideoIndexerAPI

with open('config.json', 'r') as f:
    config = json.loads(f.read())

vi = VideoIndexerAPI(
    vi_subscription_key=config['primary_key'],
    vi_location='trial',
    vi_account_id=config['account_id'])

def upload_to_indexer(videoname, vi_api=vi):
    """Upload video to Azure video indexer, returns video id"""
    video_id = vi_api.upload_to_video_indexer(
        input_filename=f"videos/{videoname}",
        video_name=videoname,
        video_language='English')
    return video_id

def get_indexer_results(video_id, vi_api=vi):
    info = vi_api.get_video_info(
        video_id=video_id,
        video_language='English')

    duration = info['durationInSeconds']  # duration of video
    insight = info['summarizedInsights']
    keywords = [kw['name'] for kw in insight['keywords']]  # list of keywords
    sentiments = {sent['sentimentKey']: sent['seenDurationRatio']
                 for sent in insight['sentiments']}  # dict of sentiments & duration ratio
    emotions = {emo['type']: emo['seenDurationRatio']  # dict of emotions and duration ratio
                for emo in insight['emotions']}
    labels = [label['name'] for label in insight['labels']]  # list of labels
    topics = {topic['name']: topic['confidence']
              for topic in insight['topics']}  # dict of topics & confidence
    brands = {brand['referenceId']: brand['confidence']
              for brand in insight['brands']}
    return {
        'duration': duration,
        'keywords': keywords,
        'sentiments': sentiments,
        'emotions': emotions,
        'labels': labels,
        'topics': topics,
        'brands': brands,
    }

# vid_id = upload_to_indexer('2')
# result = get_indexer_results("80eab2790a")

def collect_indexed_info(videos_indexed):
    n = len(videos_indexed)
    keywords = []
    labels = []
    topics = []
    brands = []
    for i in range(n):
        keywords += videos_indexed[i]['keywords']
        labels += videos_indexed[i]['labels']
        topics += videos_indexed[i]['topics'].keys()
        brands += videos_indexed[i]['brands'].keys()
    return {
        'keywords': keywords,
        'labels': labels,
        'topics': topics,
        'brands': brands,
    }