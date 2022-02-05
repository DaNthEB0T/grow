import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Case, When
from django.apps import apps

def get_metadata():
    Post = apps.get_model("media_handler", "Post")
    metadata = pd.DataFrame(list(Post.objects.values('id', 'title')))
    additional = pd.DataFrame([
        {
            'id': post.id, 'description': post.description_raw, 'tags': clean_data(list(post.tags.names())), 
            'popularity': post.popularity, 'save_popularity': post.save_popularity_index, 
            'watchlist_popularity': post.watchlist.count(), 'author': post.author.username
        } 
        for post in Post.objects.all()])
    
    metadata['id'] = metadata['id'].astype("int")
    additional['id'] = additional['id'].astype("int")
    
    metadata = metadata.merge(additional, on='id')
    
    metadata['soup'] = metadata.apply(lambda x: x['title'] + " " + x['description'] + " " + " ".join(x["tags"]), axis=1)
    return metadata

def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''
    
def get_similar_posts(post):
    Post = apps.get_model("media_handler", "Post")
    metadata = get_metadata()
    
    indices = pd.Series(metadata.index, index=metadata['id'])
    idx = indices[post.id]
    
    count = CountVectorizer(stop_words="english")
    count_matrix = count.fit_transform(metadata['soup'])
    
    cos_sim = cosine_similarity(count_matrix, count_matrix)
    
    relevancy_scores = list(enumerate(cos_sim[idx]))
    relevancy_scores = sorted(relevancy_scores, key=lambda x: x[1], reverse=True)
    
    relevancy_scores = relevancy_scores[1:]
    
    post_indices = [i[0] for i in relevancy_scores]
    
    pks = metadata['id'].iloc[post_indices].values
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pks)])
    
    return Post.objects.filter(pk__in=pks).order_by(preserved)