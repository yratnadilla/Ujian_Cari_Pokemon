from flask import Flask, request, send_from_directory, render_template, redirect, url_for
import requests

app = Flask(__name__, static_url_path = '')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods = ['GET', 'POST'])
def search():
    name = request.form['pokemonName']
    name = name.lower()
    url = 'https://pokeapi.co/api/v2/pokemon/'
    checkName = requests.get(url)
    listPokemon = []
    for i in range(len(checkName.json()['results'])):
        listPokemon.append(checkName.json()['results'][i]['name'])
    if name in listPokemon:
        return redirect(url_for('success', pokemonName = name))
    else:
        return redirect(url_for('notfound'))

@app.route('/search/<string:pokemonName>', methods = ['GET', 'POST'])
def success(pokemonName):
    url = 'https://pokeapi.co/api/v2/pokemon/'
    resultPokemon = requests.get(url + pokemonName)
    icon = resultPokemon.json()['sprites']['front_default']
    index = resultPokemon.json()['id']
    weight = resultPokemon.json()['weight']
    height = resultPokemon.json()['height']
    return render_template('search.html', pokeName = pokemonName.capitalize(), pokeIcon = icon, pokeId = index, pokeWeight = weight, pokeHeight = height)

@app.route('/notfound')
def notfound():
    return render_template('notfound.html')

@app.errorhandler(404)
def error404(error):
    return '<h1>Error: 404 Not Found</h1>'

if __name__ == '__main__':
    app.run(debug = True)