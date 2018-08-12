from flask import Flask, request, render_template,redirect,url_for,session,escape

from models.user_model import user_signup, search_user_by_username

app = Flask(__name__)
app.secret_key = 'any random string'

@app.route("/")
def index():
	if("username" in session.keys()):
        	return render_template('welcome.html', login= "True")
	else:
		return render_template('welcome.html', login= "False")

@app.route("/login", methods=['POST'])
def login():
	inbound_username = request.form["username"]
	existing_user = search_user_by_username(inbound_username)
	if(existing_user is None):
		return render_template('error.html', message="You have to sign up first")
	
	elif(request.form["password"] == "what" and request.form["username"] == "shashank"):
		print ("Login successful. Redirecting to products page")
		session['username'] = str(existing_user['_id'])
		return redirect(url_for('index'))

	else:
	    	return render_template('error.html', message="username or password not correct")

@app.route("/signup", methods=["POST"])
def signup():
	user_info={}
	user_info["username"] = request.form["username"]
	user_info["name"] = request.form["name"]
	user_info["email"] = request.form["email"]
	user_info["password"] = request.form["password"]
	
	#import pdb;pdb.set_trace()
	results =user_signup(user_info)
	if(results is True):

	 session['user_id'] = str(user_info['_id'])
	return("successfully saved")
	#return redirect(url_for('index'))


@app.route("/products")
def product_page():
	return render_template('products.html')

@app.route('/logout')
def logout():
	session.pop('user_id', None)
	return redirect(url_for('index'))

if (__name__ == "__main__"):
	app.run()
