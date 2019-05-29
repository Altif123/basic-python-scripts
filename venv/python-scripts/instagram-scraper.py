from IPython.core.display import Image
import InstagramAPI
from tqdm import tqdm
import pandas as pd
from IPython.display import Image, display
import networkx as nx
import numpy as np
import time
import datetime

def connections():

    api = InstagramAPI("altif.ali", "teefo123")
    api.login() # login

    api.getSelfUsernameInfo()
    result = api.LastJson
    user_id = result['user']['pk'] # my own personal user id
    me = result['user']['full_name'] # my own personal username


    api.getSelfUsersFollowing()
    result = api.LastJson
    follow_relationships = []
    for user in tqdm(result['users']):
        followed_user_id = user['pk']
        followed_user_name = user['full_name']
        follow_relationships.append((user_id, followed_user_id, me, followed_user_name))
        api.getUserFollowings(followed_user_id)
        result2 = api.LastJson
        if result2.get('users') is not None:
            for user2 in result2['users']:
                follow_relationships.append((followed_user_id, user2['pk'],
                                            followed_user_name, user2['full_name']))

    df = pd.DataFrame(follow_relationships,
                    columns=['src_id','dst_id', 'src_name', 'dst_name'])
    return print(df)

# get all users that I am directly following
"""
broken code need to fix

json.decoder.JSONDecodeError: Expecting ',' delimiter: line 1 column 58687 (char 58686)
"""
def toppost():
    api = InstagramAPI("altif.ali", "teefo123")
    api.login()  # login

    api.getSelfUsernameInfo()
    result = api.LastJson
    user_id = result['user']['pk']  # my own personal user id
    me = result['user']['full_name']  # my own personal username

    # get all users that I am directly following
    api.getSelfUsersFollowing()
    result = api.LastJson
    follow_relationships = []
    for user in tqdm(result['users']):
        followed_user_id = user['pk']
        followed_user_name = user['full_name']
        follow_relationships.append((user_id, followed_user_id, me, followed_user_name))

    df_local = pd.DataFrame(follow_relationships, columns=['src_id', 'dst_id', 'src_name', 'dst_name'])
    all_user_ids_local = np.unique(df_local[['src_id', 'dst_id']].values.reshape(1, -1))

    # grab all my likes from the past year
    last_year = datetime.datetime.now() - datetime.timedelta(days=365)
    now = datetime.datetime.now()
    last_result_time = now
    all_likes = []
    max_id = 0

    while last_result_time > last_year:
        api.getLikedMedia(maxid=max_id)
        results = api.LastJson
        [all_likes.append(item) for item in results['items']]
        max_id = results['items'][-1]['pk']
        last_result_time = pd.to_datetime(results['items'][-1]['taken_at'], unit='s')

    like_counts = pd.Series([i['user']['pk'] for i in all_likes]).value_counts()

    # calculate number of times I've liked each users post
    for i in tqdm(like_counts.index):
        if i in df_local['dst_id'].values:  # only count likes from people I follow (naive but simple)
            ind = df_local[(df_local['src_id'] == user_id) & (df_local['dst_id'] == i)].index[0]
            if like_counts[i] is not None:
                df_local = df_local.set_value(ind, 'weight', like_counts[i])
    ind = df_local[df_local['weight'].isnull()].index
    df_local = df_local.set_value(ind, 'weight', 0.5)
    print(df_local)
    # create social graph and calculate pagerank
    G = nx.from_pandas_adjacency(df_local)####
    # calculate personalized pagerank
    perzonalization_dict = dict(zip(G.nodes(), [0] * len(G.nodes())))
    perzonalization_dict[user_id] = 1
    ppr = nx.pagerank(G, personalization=perzonalization_dict)

    # this may take a while if you follow a lot of people
    urls = []
    taken_at = []
    num_likes = []
    num_comments = []
    page_rank = []
    users = []
    weight = []
    for user_id in tqdm(all_user_ids_local):
        api.getUserFeed(user_id)
        result = api.LastJson
        if 'items' in result.keys():
            for item in result['items']:
                if 'image_versions2' in item.keys():  # only grabbing pictures (no videos or carousels)
                    # make sure we can grab keys before trying to append

                    url = item['image_versions2']['candidates'][1]['url']
                    taken = item['taken_at']
                    try:
                        likes = item['like_count']
                    except KeyError:
                        likes = 0
                    try:
                        comments = item['comment_count']
                    except KeyError:
                        comments = 0

                    pr = ppr[item['user']['pk']]
                    user = item['user']['full_name']
                    if user != me:  # don't count myself!
                        urls.append(url)
                        taken_at.append(taken)
                        num_likes.append(likes)
                        num_comments.append(comments)
                        page_rank.append(pr)
                        users.append(user)
                        weight.append(df_local[df_local['dst_name'] == user]['weight'].values[0])

    # now we can make a dataframe with all of that information
    scores_df = pd.DataFrame(
        {'urls': urls,
         'taken_at': taken_at,
         'num_likes': num_likes,
         'num_comments': num_comments,
         'page_rank': page_rank,
         'users': users,
         'weight': weight
         })
    # don't care about anything older than 1 week
    oldest_time = int((datetime.datetime.now()
                       - datetime.timedelta(weeks=1)).strftime('%s'))

    scores_df = scores_df[scores_df['taken_at'] > oldest_time]

    # /1e5 to help out with some machine precision (numbers get real small otherwise)
    scores_df['time_score'] = np.exp(-(int(time.time()) - scores_df['taken_at']) / 1e5)

    scores_df['total_score'] = (np.log10(scores_df['num_comments'] + 2) * np.log10(scores_df['num_likes'] + 1)
                                * scores_df['page_rank'] * scores_df['time_score']
                                * np.log(scores_df['weight'] + 1))

    # calculate top ten highest rated posts
    top_ten = scores_df['total_score'].nlargest(10)
    top_rows = scores_df.loc[top_ten.index].values
    top_personal_img = []

    top_graph_img = []
    # display the feed
    for row in top_rows:
        img: Image = Image(row[4], format='jpeg')
        top_graph_img.append(img)
        display(img)
        top_personal_img.append(img)
        print('taken_at: %s' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(row[3])))
        print('number of likes: %s' % row[1])
        print('number of comments: %s' % row[0])
        print('page_rank: %s' % row[2])
        print(row[5])

#connections()
toppost()
