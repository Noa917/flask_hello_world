from flask import Flask
from flask import render_template
from flask import json
from flask import jsonify
from urllib.request import urlopen


import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world_menu():
    return render_template('hello.html')
  
@app.route('/flask/')
def hello_world():
    return render_template('hello.html')
  
@app.route('/fr/')
def bonjour():
    return render_template('bonjour.html')
  
@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route('/recherche/<string:nom>')
def searchclient(nom):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
  #Recherche du nom avec LIKE et WHERE
    cursor.execute('SELECT * FROM clients WHERE nom LIKE ?', ('%' + nom + '%',))
    data = cursor.fetchall()
    conn.close()
    
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/paris/')
def meteo():
    response = urlopen('https://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&cnt=16&appid=bd5e378503939ddaee76f12ad7a97608')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('temp', {}).get('day') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route('/histogramme/')
def histogram():
    return render_template("histogramme.html")

                                                                                                                                       
if __name__ == "__main__":
  app.run(debug=True)
