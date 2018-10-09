from flask import render_template
from app import app
from app.base import Base

@app.route('/')
@app.route('/index')

def index():
	form = Base()
	return render_template("base.html", title="Index", form=form)
