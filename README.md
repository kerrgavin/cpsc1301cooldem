# cpsc1301cooldem
This is a project that makes use of Flask, Requests, and SQLite3 to develop a small web application that can makes calls to the [PokeAPI](https://pokeapi.co/), cache the response from that call, and then display the result to the user.
 
```
cpsc1301cooldem
|   .flaskenv
|   config.py
|   microblog.py
|   README.md
|   
\---app
    |   base.py
    |   data_management.py
    |   path.py
    |   routes.py
    |   __init__.py
    |   
    +---data
    |       cache_creation.sql
    |       data.db
    |       
    +---static
    |   |   Pokeball.PNG
    |   |   
    |   +---sprites
    |   \---styles
    |           style.css
    |           
    \---templates
            base.html
            pokemon.html
```
