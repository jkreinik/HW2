## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests 
import json
#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):
	album_name = StringField('Enter the name of an album:', validators=[Required()])
	radio = RadioField('How much do you like this album? (1 low, 3 high)', choices = [('1','1'),('2','2'),('3','3')], validators=[Required()])
	submit = SubmitField('Submit')



####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/artistform')
def artistform():
    return render_template('artistform.html')

@app.route('/artistinfo', methods = ["GET"])
def artistinfo():
	if request.method == 'GET':
		artist = request.args.get('artist')
		base_url = 'https://itunes.apple.com/search'
		params = {}
		params['term'] = artist
		req = requests.get(base_url, params=params).text
		js = json.loads(req)
		res = js['results']
		return render_template('artist_info.html', objects=res)
	flash('All Fields are required')
	return redirect(url_for('artistform'))



@app.route('/artistlinks')
def artistlinks():
    return render_template('artist_links.html')


@app.route('/specific/song/<artist_name>')
def specificartist(artist_name):
	artist = artist_name
	base_url = 'https://itunes.apple.com/search'
	params = {}
	params['term'] = artist
	params['entity'] = 'musicTrack'
	req = requests.get(base_url, params=params).text
	js = json.loads(req)
	res = js['results']
	return render_template('specific_artist.html', results=res)

@app.route('/album_entry')
def albumentry():
	form = AlbumEntryForm()
	return render_template('album_entry.html', form=form)


@app.route('/album_result', methods = ['GET', 'POST'])
def albumresult():
	form = AlbumEntryForm(request.form)
	if request.method == "POST" and form.validate_on_submit():
		album_name = form.album_name.data
		radio = form.radio.data
		return render_template('album_data.html', album_name=album_name, radio=radio)
		flash('All fields are required!')
	return redirect(url_for('albumentry'))



@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)


if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
