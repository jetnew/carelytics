def append_cache(text, cachefile):
    """Append the text to a cache file"""
    with open(cachefile, "a") as f:
        f.write(text+'\n')

def read_cache(cachefile):
    """Return the list of text from cache file"""
    with open(cachefile, 'r') as f:
        cache = [video_id.strip() for video_id in f]
    return cache

def check_cache(text, cachefile):
    """Check if cachefile contains given text"""
    cache = read_cache(cachefile)
    return text in cache

import pickle
def save_pickle(filename, obj):
    """Save an object to filename."""
    with open("utils/"+filename, 'wb') as f:
        pickle.dump(obj, f)
    print(f"Saved to utils/{filename}")

def load_pickle(filename):
    """Load a pickle by filename."""
    print(f"Loaded from utils/{filename}")
    with open("utils/"+filename, 'rb') as f:
        return pickle.load(f)