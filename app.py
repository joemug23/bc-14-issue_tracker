from flask import Flask, render_template, request, url_for, redirect, session, flash
from database import Database
from flask_oauth import OAuth

SECRET_KEY = 'development key'


app = Flask(__name__)
app.secret_key = SECRET_KEY
oauth = OAuth()

# Use Twitter as example remote application
twitter = oauth.remote_app('twitter',
    # unless absolute urls are used to make requests, this will be added
    # before all URLs.  This is also true for request_token_url and others.
    base_url='https://api.twitter.com/1/',
    # where flask should look for new request tokens
    request_token_url='https://api.twitter.com/oauth/request_token',
    # where flask should exchange the token with the remote application
    access_token_url='https://api.twitter.com/oauth/access_token',
    # twitter knows two authorizatiom URLs.  /authorize and /authenticate.
    # they mostly work the same, but for sign on /authenticate is
    # expected because this will give the user a slightly different
    # user interface on the twitter side.
    authorize_url='https://api.twitter.com/oauth/authenticate',
    # the consumer keys from the twitter application registry.
    consumer_key='uiXanIM81M3RiDjRzWyvREyof',
    consumer_secret='XkW5ihmwsD88pN3j0eyMSEdtLoDyIRi9ipIZb4HyS4QpA0Zj5L'
)

@app.route('/')
def index():
    return render_template('main.html')


@app.route('/add')
def got_to_add():
    return render_template('add_issue.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/twitter_login')
def twitter_login():
    return twitter.authorize(callback=url_for('oauth_authorized',
                                              next=request.args.get('next') or request.referrer or None))

@app.route('/logout')
def logout():
    session.pop('screen_name', None)
    flash('You were signed out')
    return redirect(request.referrer or url_for('index'))


@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    access_token = resp['oauth_token']
    session['access_token'] = access_token
    session['screen_name'] = resp['screen_name']

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
