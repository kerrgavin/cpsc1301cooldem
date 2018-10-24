from flask import render_template
from flask import request
from flask import redirect
from app import app
from app import data_management
from app.base import Base

@app.route('/')
@app.route('/index', methods=["GET", "POST"])

def index():
	form = Base()
	if form.validate_on_submit():
		pokemon = form.text.data.lower().strip()
		data_management.update_list()
		if data_management.exists(pokemon):
			return redirect("/pokemon?p="+pokemon)
		else:
			return redirect("/index")
	return render_template("base.html", title="Index", form=form)

@app.route('/pokemon', methods=["GET", "POST"])
def pokemon():

	form = Base()
	p = request.args.get("p")
	print("p is: ", p)
	data = data_management.get_pokemon_data(p)
	sprites = data_management.get_sprites_dict(p)
	if form.validate_on_submit():
		pokemon = form.text.data.lower().strip()
		data_management.update_list()
		if data_management.exists(pokemon):
			return redirect("/pokemon?p="+pokemon)
		else:
			return redirect("/index")
	return render_template("pokemon.html", title="Pokemon", form=form, name = data["name"].upper(), moves=data["moves"], abilities=data["abilities"], types=data["types"], sprites = sprites)
