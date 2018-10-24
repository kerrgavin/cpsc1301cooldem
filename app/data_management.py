import sqlite3
import datetime
import json
import requests
import shutil
from app.path import *

def update_list():
    if difference("pokemon") >= 3:
        print("here")
        r = requests.get("https://pokeapi.co/api/v2/pokemon/")
        file = open(DATA_PATH + "pokemon.json","w")
        file.write(r.text)
        reset_time("pokemon")

def difference(item):
    now = datetime.datetime.now()
    conn = sqlite3.connect(DATA_PATH + "data.db")
    cur = conn.cursor()
    cur.execute('''SELECT MONTH, DAY, YEAR, HOUR, MINUTE FROM CACHE_INFO WHERE NAME = ?''', (item, ))
    r = cur.fetchone()
    if r is None:
        print("it is null still")
        cur.execute('''INSERT INTO CACHE_INFO (NAME, MONTH, DAY, YEAR, HOUR, MINUTE) VALUES (?, ?, ?, ?, ?, ?)''', (item, now.month, now.day, now.year, now.hour, now.minute))
        conn.commit()
        return 3
    diff = (((now.month - r[0]) * 30) * 24) * 60
    diff += ((now.day - r[1]) * 24) * 60
    diff += (((((now.year - r[2]) * 12) * 30) * 24) * 60)
    diff += (now.hour - r[3]) * 60
    diff += now.minute - r[4]
    conn.close()
    return diff//60

def reset_time(item):
    now = datetime.datetime.now()
    conn = sqlite3.connect(DATA_PATH + "data.db")
    cur = conn.cursor()
    cur.execute('''UPDATE CACHE_INFO SET MONTH = ?, DAY = ?, YEAR = ?, HOUR = ?, MINUTE = ? WHERE NAME = ?''', (now.month, now.day, now.year, now.hour, now.minute, item))
    conn.commit()
    conn.close()

def exists(pokemon):
    file = open(DATA_PATH + "pokemon.json", "r")
    json_data = file.read()
    pokemons = json.loads(json_data)
    for mon in pokemons["results"]:
        if mon["name"] == pokemon:
            return True
    return False

def get_pokemon_data(pokemon):
    diff = difference(pokemon)
    if diff >= 3:
        r = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemon + "/")
        file = open(DATA_PATH + pokemon + ".json","w")
        file.write(r.text)
        reset_time(pokemon)
    file = open(DATA_PATH + pokemon + ".json", "r")
    json_data = file.read()
    d = json.loads(json_data)
    if diff >= 3:
        print("getting sprites")
        get_pokemon_sprites(pokemon, d["sprites"])
    return d

def get_pokemon_sprites(pokemon, sprites):
    save_sprite(pokemon + "_back_default", sprites["back_default"])
    save_sprite(pokemon + "_front_default", sprites["front_default"])
    save_sprite(pokemon + "_back_shiny", sprites["back_shiny"])
    save_sprite(pokemon + "_front_shiny", sprites["front_shiny"])

def save_sprite(name, url):
    r = requests.get(url, stream=True)
    with open(SPRITE_SAVE_PATH + name + ".png", "wb") as out_file:
        shutil.copyfileobj(r.raw, out_file)

def get_sprites_dict(pokemon):
    sprites = {}
    sprites["back_default"] = SPRITE_PATH + pokemon + "_back_default.png"
    sprites["front_default"] = SPRITE_PATH + pokemon + "_front_default.png"
    sprites["back_shiny"] = SPRITE_PATH + pokemon + "_back_shiny.png"
    sprites["front_shiny"] = SPRITE_PATH + pokemon + "_front_shiny.png"
    return sprites
