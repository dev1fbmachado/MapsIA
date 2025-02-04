from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Chave da API do OpenRoute
OPENROUTE_API_KEY = '5b3ce3597851110001cf62486075cae1dae749de8558a2e3ac181254Y'

# Página inicial com formulário de origem e destino
@app.route('/')
def home():
    return render_template('index.html')

# Rota para calcular a rota entre origem e destino
@app.route('/rota', methods=['POST'])
def rota():
    origem = request.form.get('origem')
    destino = request.form.get('destino')

    # Formatar as coordenadas para as URLs da API (exemplo simples, mas poderia ser tratado mais detalhadamente)
    origem_coords = obter_coords(origem)
    destino_coords = obter_coords(destino)

    # Fazer a requisição à OpenRoute
    route = obter_rota(origem_coords, destino_coords)
    
    return jsonify(route)

# Função para buscar as coordenadas com base em um endereço (usando o Nominatim do OpenStreetMap)
def obter_coords(endereco):
    url = f"https://nominatim.openstreetmap.org/search?q={endereco}&format=json"
    response = requests.get(url)
    data = response.json()
    if data:
        lat = data[0]['lat']
        lon = data[0]['lon']
        return {'lat': lat, 'lon': lon}
    return None

# Função para buscar a rota entre a origem e o destino utilizando a OpenRoute
def obter_rota(origem, destino):
    url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={OPENROUTE_API_KEY}"
    
    # Definir as coordenadas de origem e destino
    coordinates = f"{origem['lon']},{origem['lat']}&{destino['lon']},{destino['lat']}"
    
    params = {
        'coordinates': coordinates
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    # Retornar a rota em formato simplificado (pode ser expandido para mais detalhes)
    return data['features'][0]['geometry']['coordinates']

# Rota para alterar a rota com base nos comandos do usuário
@app.route('/comando', methods=['POST'])
def comando():
    comando = request.form.get('comando')
    # Aqui você pode adicionar a lógica para alterar a rota, como adicionar pontos turísticos, etc.
    # Por enquanto, vamos apenas retornar o comando.
    return jsonify({"comando": comando})

if __name__ == '__main__':
    app.run(debug=True)
