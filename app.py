from flask import Flask, render_template, request, url_for, redirect, session, flash, jsonify
from database import Database
from flask_oauth import OAuth

SECRET_KEY = 'development key'

app = Flask(__name__)
app.secret_key = SECRET_KEY
oauth = OAuth()

# Use Twitter as example remote application
twitter = oauth.remote_app('twitter',
                           # Entry point of the twiiter app
                           base_url='https://api.twitter.com/oauth2/token',
                           # where flask should look for new request tokens
                           request_token_url='https://api.twitter.com/oauth/request_token',
                           # where flask should exchange the token with the remote application
                           access_token_url='https://api.twitter.com/oauth/access_token',
                           # twitter knows two authorizatiom URLs.  /authorize and /authenticate.
                           # they mostly work the same, but for sign on /authenticate is
                           # expected because this will give the user a slightly different
                           # user interface on the twitter side.
                           authorize_url='https://api.twitter.com/oauth/authorize',
                           # the consumer keys from the twitter application registry.
                           consumer_key='uiXanIM81M3RiDjRzWyvREyof',
                           consumer_secret='XkW5ihmwsD88pN3j0eyMSEdtLoDyIRi9ipIZb4HyS4QpA0Zj5L'
                           )


@twitter.tokengetter
def get_twitter_token(token=None):
    # get twitter token
    return session.get('twitter_token')


@app.route('/')
def index():
    # app entry point
    return render_template('login.html')


@app.route('/raise_issue', methods=['POST'])
def raise_issue():
    # adding an issue to the database
    issue_desc = request.form['description']
    department = request.form['department']
    priority = request.form['priority']
    raised_by = session['screen_name']

    Database.insert('issues', {'description': issue_desc, 'department': department, 'priority': priority,
                                     'raise_person': raised_by})
    return redirect(url_for('go_home'))


@app.route('/delete_issue/<card_id>')
def delete_issue(card_id):
	# deleting element by id
	Database.deleting('issues',{'issues_id':card_id})
	return redirect(url_for('go_home'))


@app.route('/assign_user/<card_id>', methods=['POST'])
def assign_user(card_id):
	# update the record setting assigned to user
    assigned_user = request.form['staffname']
	# call to Database.update() with proper arguments
    Database.update('issues', {'issues_id':card_id, 'assigned_to': assigned_user})
    return redirect(url_for('go_home'))


@app.route('/get_open_issues', methods=['GET'])
def get_open_issues():
	# return open issues from db
    results = Database.select_cond('issues', "where status='open'")

    return jsonify(results)

@app.route('/get_closed_issues', methods=['GET'])
def get_closed_issues():
	# return closed issues from db
    results = Database.select_cond('issues', "where status='closed'")
    if results == 'No record found':
        return "Empty"
    return jsonify(results)

@app.route('/update_issue_status/<tar>/<eid>', methods=['POST'])
def update_issue_status(tar, eid):
    # update user issue status
    el_id = eid
    target = tar
    Database.update('issues', {'issues_id': el_id, 'status': target})
    return redirect(url_for('go_home'))



@app.route('/do_login', methods=['POST'])
def do_login():
    # login
    username = request.form['username']
    password = request.form['password_in']
    res = Database.select_cond('users', "where username='{}' and password='{}'".format(username, password))
    if res == "No record found":
        return redirect(url_for('login'))

    session['screen_name'] = res[1]['username']
    return redirect(url_for('go_home'))


@app.route('/home')
def go_home():
    # app main point
    return render_template('home.html')


@app.route('/twitter_login')
def twitter_login():
    # twitter authentication
    return twitter.authorize(callback=url_for('oauth_authorized',
                                              next=request.args.get('next') or request.referrer or None))


@app.route('/logout')
def logout():
    # log out and clear session details
    if session['screen_name']:
        del session['screen_name']
    if session['access_token']:
        del session['access_token']
    if session['twitter_token']:
        del session['twitter_token']
    flash('You were signed out')
    return redirect(request.referrer or url_for('index'))


@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    # callback form authentication redirect the user to a particular page
    next_url = request.args.get('next') or url_for('login')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)
    print("I am here")
    access_token = resp['oauth_token']
    print(access_token)
    session['access_token'] = access_token
    session['screen_name'] = resp['screen_name']

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )

    return redirect(url_for('go_home'))


if __name__ == '__main__':
    app.run(debug=True)
