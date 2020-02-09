import os
from flask import Flask, render_template, request, url_for, redirect, jsonify
import oauth2 as oauth
import urllib.request
import urllib.parse
import urllib.error
import json
import re
import twitter
import pickle
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB
app = Flask(__name__)

app.debug = False

request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authorize_url = 'https://api.twitter.com/oauth/authorize'
show_user_url = 'https://api.twitter.com/1.1/users/show.json'



# Support keys from environment vars (Heroku).
app.config['APP_CONSUMER_KEY'] = os.getenv(
    'TWAUTH_APP_CONSUMER_KEY', 'API_Key_from_Twitter')
app.config['APP_CONSUMER_SECRET'] = os.getenv(
    'TWAUTH_APP_CONSUMER_SECRET', 'API_Secret_from_Twitter')

# alternatively, add your key and secret to config.cfg
# config.cfg should look like:
# APP_CONSUMER_KEY = 'API_Key_from_Twitter'
# APP_CONSUMER_SECRET = 'API_Secret_from_Twitter'
app.config.from_pyfile('config.cfg', silent=True)

oauth_store = {}

access_tokens = []

global api

@app.route('/')
def hello():
    app_callback_url = url_for('callback', _external=True)

    # Generate the OAuth request tokens, then display them
    consumer = oauth.Consumer(
        app.config['APP_CONSUMER_KEY'], app.config['APP_CONSUMER_SECRET'])
    client = oauth.Client(consumer)
    resp, content = client.request(request_token_url, "POST", body=urllib.parse.urlencode({"oauth_callback": app_callback_url}))

    if resp['status'] != '200':
        error_message = 'Invalid response, status {status}, {message}'.format(
            status=resp['status'], message=content.decode('utf-8'))
        return render_template('error.html', error_message=error_message)

    request_token = dict(urllib.parse.parse_qsl(content))
    oauth_token = request_token[b'oauth_token'].decode('utf-8')
    oauth_token_secret = request_token[b'oauth_token_secret'].decode('utf-8')
    oauth_store[oauth_token] = oauth_token_secret
    return render_template('start.html', authorize_url=authorize_url, oauth_token=oauth_token, request_token_url=request_token_url)
    # print(app.config['APP_CONSUMER_KEY'], app.config['APP_CONSUMER_SECRET'],'hereeee')
    # return render_template('index.html')


# @app.route('/start')
# def start():
#     # note that the external callback URL must be added to the whitelist on
#     # the developer.twitter.com portal, inside the app settings
#     app_callback_url = url_for('callback', _external=True)

#     # Generate the OAuth request tokens, then display them
#     consumer = oauth.Consumer(
#         app.config['APP_CONSUMER_KEY'], app.config['APP_CONSUMER_SECRET'])
#     client = oauth.Client(consumer)
#     resp, content = client.request(request_token_url, "POST", body=urllib.parse.urlencode({"oauth_callback": app_callback_url}))

#     if resp['status'] != '200':
#         error_message = 'Invalid response, status {status}, {message}'.format(
#             status=resp['status'], message=content.decode('utf-8'))
#         return render_template('error.html', error_message=error_message)

#     request_token = dict(urllib.parse.parse_qsl(content))
#     oauth_token = request_token[b'oauth_token'].decode('utf-8')
#     oauth_token_secret = request_token[b'oauth_token_secret'].decode('utf-8')
#     oauth_store[oauth_token] = oauth_token_secret
#     return render_template('start.html', authorize_url=authorize_url, oauth_token=oauth_token, request_token_url=request_token_url)




@app.route('/callback')
def callback():
    # Accept the callback params, get the token and call the API to
    # display the logged-in user's name and handle
    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')
    oauth_denied = request.args.get('denied')

    # if the OAuth request was denied, delete our local token
    # and show an error message
    if oauth_denied:
        if oauth_denied in oauth_store:
            del oauth_store[oauth_denied]
        return render_template('error.html', error_message="the OAuth request was denied by this user")

    if not oauth_token or not oauth_verifier:
        return render_template('error.html', error_message="callback param(s) missing")

    # unless oauth_token is still stored locally, return error
    if oauth_token not in oauth_store:
        return render_template('error.html', error_message="oauth_token not found locally")

    oauth_token_secret = oauth_store[oauth_token]

    # if we got this far, we have both callback params and we have
    # found this token locally

    consumer = oauth.Consumer(
        app.config['APP_CONSUMER_KEY'], app.config['APP_CONSUMER_SECRET'])
    token = oauth.Token(oauth_token, oauth_token_secret)
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)

    resp, content = client.request(access_token_url, "POST")
    access_token = dict(urllib.parse.parse_qsl(content))

    screen_name = access_token[b'screen_name'].decode('utf-8')
    user_id = access_token[b'user_id'].decode('utf-8')

    # These are the tokens you would store long term, someplace safe
    real_oauth_token = access_token[b'oauth_token'].decode('utf-8')
    real_oauth_token_secret = access_token[b'oauth_token_secret'].decode(
        'utf-8')

    access_tokens.append(real_oauth_token)
    access_tokens.append(real_oauth_token_secret)
    # Call api.twitter.com/1.1/users/show.json?user_id={user_id}
    real_token = oauth.Token(real_oauth_token, real_oauth_token_secret)
    real_client = oauth.Client(consumer, real_token)
    real_resp, real_content = real_client.request(
        show_user_url + '?user_id=' + user_id, "GET")

    if real_resp['status'] != '200':
        error_message = "Invalid response from Twitter API GET users/show: {status}".format(
            status=real_resp['status'])
        return render_template('error.html', error_message=error_message)

    response = json.loads(real_content.decode('utf-8'))

    friends_count = response['friends_count']
    statuses_count = response['statuses_count']
    followers_count = response['followers_count']
    name = response['name']


   
    # don't keep this token and secret in memory any longer
    # del oauth_store[oauth_token]
    global api
    api = twitter.Api(consumer_key = app.config['APP_CONSUMER_KEY'], consumer_secret = app.config['APP_CONSUMER_SECRET'], access_token_key = real_oauth_token, access_token_secret = real_oauth_token_secret)
    #api.PostDirectMessage("hola", screen_name="steelcitycodes")
    return redirect(url_for("user", screenname = screen_name))
    # return render_template('callback-success.html', screen_name=screen_name, user_id=user_id, name=name,
    #                        friends_count=friends_count, statuses_count=statuses_count, followers_count=followers_count, access_token_url=access_token_url)




loaded_model = pickle.load(open('newmodel.sav', 'rb'))
vectorizer = pickle.load(open('newvectorizer.pickle', 'rb'))

def get_mutual_friends(user):
  friends = api.GetFriends(screen_name = user)
  followers = api.GetFollowers(screen_name = user)
  #print(friends[0].screen_name)
  friendnames = []
  for friend in friends:
    if(friend in followers):
        friendnames.append(friend)
  if(len(friendnames) > 20):
    friendnames = friendnames[:21]
  return friendnames



def clean_tweet(tweet):
  return re.sub(r'\W+', ' ', tweet)


def get_tweet_sentiment(tweet):
  result = loaded_model.predict(vectorizer.transform([tweet]))
  return result[0]

def get_tweets(screen_name, count = 15):
  tweets = []
  #fetched_tweets = api.GetUserTimeline(screen_name = screen_name, count = count)
  try:
    fetched_tweets = api.GetUserTimeline(screen_name = screen_name, count = count)
    tweets = [i.AsDict() for i in fetched_tweets]
    #print(t['id'], t['text'])
    return tweets
  except:
    return []

def get_friends_tweets_avgscore(user):
  tweets = get_tweets(user)
  userAvgScore = dict()
  sums = 0
  for i in range(len(tweets)):
    nums = int(get_tweet_sentiment(clean_tweet(tweets[i]['text'])))
    sums += nums
  userAvgScore= (sums/len(tweets))
  return userAvgScore

def get_friends_data(user):
  friends = get_mutual_friends(user)
  print(friends)
  jsonobj = {}
  finalobj = {}
  finalobj[user] = api.GetUser(screen_name = user).name
  for friend in friends:
    jsonobj['name'] = friend.name
    jsonobj['username'] = friend.screen_name
    jsonobj["profile_url"] = friend.profile_image_url_https
    jsonobj["avgscore"] = int(100*get_friends_tweets_avgscore(friend.screen_name))
    finalobj[friend.screen_name] = jsonobj
    jsonobj = {}
  return finalobj


@app.route('/test', methods=['POST'])
def getResults():
    if request.method == 'POST':
        datas = request.get_json()
        print(datas)
        allData = get_friends_data(datas['username'])
        #llData = get_friends_data(request.dat)
    return allData






@app.route('/user/<screenname>')
def user(screenname):
    #api = twitter.Api(consumer_key = app.config['APP_CONSUMER_KEY'], consumer_secret = app.config['APP_CONSUMER_SECRET'], access_token_key = access_tokens[0], access_token_secret = access_tokens[1])
    #api.PostDirectMessage("test2", screen_name="joshjzhou")

    name = api.GetUser(screen_name = screenname).name
    # followers = get_mutual_friends(screenname)
    # for follower in followers:
    #     print(follower.screen_name)
    return render_template('index.html', screenname = screenname, name = name)


@app.route('/dm', methods=['POST'])
def sendDM():
  if request.method == 'POST':
    datas = request.get_json()
    try:
      api.PostDirectMessage(datas['text'], screen_name = datas['username'])
      return {'status':'success'}
    except:
      return {'status':'failure'}

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_message='uncaught exception'), 500

  
if __name__ == '__main__':
    app.run()
