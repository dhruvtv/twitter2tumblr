__author__ = 'dvemula'

import ConfigParser
import twitter
from twitter import TwitterError
from tumblpy import Tumblpy, TumblpyError, TumblpyRateLimitError
import urllib2

config = ConfigParser.RawConfigParser()
CONFIG_FILE = 'settings.cfg'

def write_to_config_file(config):
    with open(CONFIG_FILE, 'wb') as configfile:
        config.write(configfile)

def get_twitter_api(config):
    """ uses http://code.google.com/p/python-twitter/
        easy_install python-twitter
    """
    api = twitter.Api(
        consumer_key = config.get('twitter', 'consumer_key'),
        consumer_secret = config.get('twitter', 'consumer_secret'),
        access_token_key = config.get('twitter', 'access_token_key'),
        access_token_secret = config.get('twitter', 'access_token_secret'))
    return api

def read_tweets(api, user, since_id):
    """ reads user's tweets
    """

    # fetch the next 200 tweets starting the below id
    max_id = None

    # list of 'Status' objects to be populated
    statuses = []

    while True:
        new_statuses = []
        try:
            new_statuses = api.GetUserTimeline(screen_name=user,
                count=200, include_rts=True, max_id=max_id, since_id=since_id)
        except (TwitterError, urllib2.HTTPError) as e:
            print e

        if len(new_statuses) > 0:
            statuses.extend(new_statuses)
            max_id = new_statuses[-1].id - 1
        else:
            break

    print "Fetched", len(statuses), "tweets."

    last_statuses = statuses[-10:]

    for status in last_statuses:
        print status.text, status.created_at, status.id

    return statuses

def get_tumblr_api(config):
    """ uses https://github.com/michaelhelmick/python-tumblpy
        pip install python-tumblpy
    """
    app_key = config.get('tumblr', 'app_key')
    app_secret = config.get('tumblr', 'app_secret')

    oauth_token = config.get('tumblr', 'oauth_token')
    oauth_token_secret = config.get('tumblr', 'oauth_token_secret')

    def authorize():
        # Authorization Step 1
        t = Tumblpy(app_key = app_key, app_secret = app_secret)

        auth_props = t.get_authentication_tokens()
        auth_url = auth_props['auth_url']

        # temp tokens
        oauth_token = auth_props['oauth_token']
        oauth_token_secret = auth_props['oauth_token_secret']

        # Authorization Step 2
        t = Tumblpy(app_key = app_key,
            app_secret = app_secret,
            oauth_token=oauth_token,
            oauth_token_secret=oauth_token_secret, callback_url='oob')

        # oauth_verifier = *Grab oauth verifier from URL*
        # At this point, follow instructions in commandline.
        print "Go to the link ", auth_url
        print "Click 'Allow' and when the page redirects, "\
              "grab the value of oauth_verifier from the URL and enter it here."
        oauth_verifier = raw_input('oauth_verifier:')
        authorized_tokens = t.get_access_token(oauth_verifier)

        # Final access tokens
        oauth_token = authorized_tokens['oauth_token']
        oauth_token_secret = authorized_tokens['oauth_token_secret']

        return oauth_token, oauth_token_secret

    if not oauth_token:
        oauth_token, oauth_token_secret = authorize()
        config.set('tumblr', 'oauth_token', oauth_token)
        config.set('tumblr', 'oauth_token_secret', oauth_token_secret)

        # write these access tokens to config file for future use
        write_to_config_file(config)

    t= Tumblpy(app_key = app_key, app_secret= app_secret,
        oauth_token = oauth_token, oauth_token_secret = oauth_token_secret)

    return t

def post_to_tumblr(t, blog_url, twitter_handle, statuses):
    """ posts tweets to tumblr
    """

    last_successful_status_id = None

    twitter_url_part = 'https://twitter.com/' + twitter_handle + '/status/'
    for status in reversed(statuses):
        try:
            post = t.post('post', blog_url = blog_url,
                params={
                    'type' : 'text',
                    'body' : status.text.encode('utf-8'),
                    'date' : status.created_at,
                    'slug' : status.id,
                    'source_url' : twitter_url_part + str(status.id)
                })
            print post
            last_successful_status_id = status.id
        except TumblpyRateLimitError:
            print "Hit Tumblr's rate limit. Come back in an hour."
            break
        except TumblpyError as e:
            print str(e)
            if str(e).__contains__('limit'):
                print "Come back in a day."
            break

    if last_successful_status_id:
        config.set('twitter', 'since_id', last_successful_status_id)
        write_to_config_file(config)

def main():
    """ read config file
        read tweets
        post to tumblr
    """
    config.read(CONFIG_FILE)

    twitter_api = get_twitter_api(config)
    twitter_handle = config.get('twitter', 'user_handle')
    since_id = config.getint('twitter', 'since_id')
    statuses = read_tweets(twitter_api, twitter_handle, since_id if since_id else None)

    tumblr_api = get_tumblr_api(config)
    blog_url = config.get('tumblr', 'blog_url')
    post_to_tumblr(tumblr_api, blog_url, twitter_handle, statuses)

if __name__ == '__main__':
    main()