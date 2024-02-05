from flask import Flask, render_template
from urllib.request import urlopen
from flask import json, jsonify
import plotly.express as px

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/fr")
def bonjour_world():
    return render_template('bonjour.html')

@app.route('/paris/')
def meteo():
    response = urlopen('https://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&cnt=16&appid=bd5e378503939ddaee76f12ad7a97608')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('temp', {}).get('day') - 273.15  # Conversion de Kelvin en °C
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    response = urlopen('https://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&cnt=16&appid=bd5e378503939ddaee76f12ad7a97608')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))

    dates = []
    temperatures = []

    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('temp', {}).get('day') - 273.15  # Conversion de Kelvin en °C
        dates.append(dt_value)
        temperatures.append(temp_day_value)

    # Création du graphique à colonnes avec Plotly
    fig = px.bar(x=dates, y=temperatures, labels={'x': 'Jour', 'y': 'Température (°C)'}, title='Températures à Paris pour les 16 prochains jours')

    # Sauvegarde du graphique en fichier HTML dans le répertoire "templates"
    fig.write_html("templates/graphique.html")

    return render_template("graphique.html")

if __name__ == "__main__":
    app.run(debug=True)
