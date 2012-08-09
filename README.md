# twitter2tumblr #

When I tweet, I consider myself to be a microblogger. I don't post stuff like
what I ate for breakfast etc., but thoughts that reflect my state of mind. In
other words, my Twitter account is like a diary to me.

It's a diary that I'd like to go through every now and then. But with
Twitter's API restrictions, you can only access your last 3200 tweets. The
rest are lost!

This script lets you back up your tweets to Tumblr, where they are archived by
month, year etc. and can be tagged.

**How is it different from [IFTTT](http://ifttt.com/recipes/search?utf8=%E2%9C%93&q=twitter+to+tumblr)?**   
With IFTTT, you can only backup your tweets *starting now*. This script will
back up your old tweets, as many as it can.

**What do I need to do?**   
Download the app (has a python file and a config file).

#### Twitter part ####
Setup your Twitter developer account, get the credentials and put them in the
config file.

Here's what you'll do:

1. Sign in to [dev.twitter.com](dev.twitter.com) with your user ID.
2. Go to My applications > Create a new Application
3. Enter a name, description, website (can be anything). Leave the callback URL
blank. Agree to the rules, enter the CAPTCHA and create the application.
4. Scroll down to the bottom and create the access tokens.
5. Copy the Consumer key, secret, Access token and secret into settings.cfg.
6. Enter your Twitter user handle against the user_handle key.
7. Leave since_id as is. The script will use it to track progress.

#### Tumblr part ####
Setup your Tumblr developer account, get the credentials and put them in the
config file.

Here's what you'll do:

1. Go to [http://www.tumblr.com/oauth/apps](http://www.tumblr.com/oauth/apps)
and sign in when asked for.
2. Click 'Register Application'.
3. Enter a name (can be anything), email and set callback URL to oob. Save.
4. The application will show up on top. Grab the Oauth Consumer key and
Secret key (click 'Show' for it to be shown).
5. Copy them into settings.cfg (in the Tumblr section - app_key and app_secret)
6. Leave the oauth_token and oauth_secret blank (the script will fill them out)
7. Create your target Tumblr blog (if you haven't) and enter your tumblr URL
against blog_url.

**How to use the app**

1. Open a shell to the containing folder.
2. Run 'python twitter2tumblr.py'
3. Follow the instructions on the command line.
4. The app first fetches all your tweets. If it throws an error, rerun after
a while.
5. Somewhere along, it prints a URL, asks you to go to that URL in your browser, hit
'Allow' to authorize your Tumblr account with your app.
6. Hit 'Allow', check out the redirected URL, copy the value associated with
the 'oauth_verifier' key, paste it back at the command prompt and hit Enter.
7. The app will start posting your tweets to Tumblr until it hits the rate
limit (250 posts per day).
8. It will then prompt you to come back a day later.
9. Come back the next day and it will pick up where it left off.
10. You need to do this for 3200/250 ~ 13 days to fully backup.

Happy archiving!

