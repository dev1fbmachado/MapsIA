from flask import Flask, render_template, request, jsonify
import requests
import urllib.parse

app = Flask(__name__)

# Função para obter as coordenadas a partir de um endereço
def obter_coords(endereco):
    endereco_codificado = urllib.parse.quote(endereco)  # Codificar o endereço para a URL
    url = f"https://nominatim.openstreetmap.org/search?q={endereco_codificado}&format=json"

    print(f"URL de requisição: {url}")  # Exibir a URL para depuração

    response = requests.get(url)

    if response.status_code != 200:
        print(f"Erro na requisição, status code: {response.status_code}")
        return None

    try:
        data = response.json()
        print("Resposta JSON recebida:", data)  # Imprimir a resposta para depuração
    except Exception as e:
        print(f"Erro ao decodificar a resposta JSON: {e}")
        return None

    if data:
        lat = data[0]['lat']
        lon = data[0]['lon']
        return {'lat': lat, 'lon': lon}
    else:
        print(f"Nenhum dado encontrado para o endereço: {endereco}")
        return None

# Rota inicial para renderizar a página principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para calcular a rota entre os dois pontos
@app.route('/calcular_rota', methods=['POST'])
def calcular_rota():
    origem = request.form['origem']
    destino = request.form['destino']

    origem_coords = obter_coords(origem)
    destino_coords = obter_coords(destino)

    if not origem_coords or not destino_coords:
        return jsonify({'error': 'Não foi possível encontrar as coordenadas de um dos locais. Tente novamente.'})

    # Se as coordenadas foram encontradas, podemos retornar as coordenadas de origem e destino
    return jsonify({
        'origem': origem_coords,
        'destino': destino_coords
    })

if __name__ == '__main__':
    app.run(debug=True)
