import json
from flask import Blueprint, render_template, jsonify

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Carregar e parsear o arquivo JSON
    try:
        with open('app/database/events.json', 'r', encoding='utf-8') as file:
            eventos = json.load(file)
        
        return render_template('index.html', eventos=eventos)
    except Exception as e:
        return f"Erro ao carregar eventos: {str(e)}"
    
@main.route('/api/events')
def api_events():
    try:
        with open('app/database/events.json', 'r', encoding='utf-8') as file:
            eventos = json.load(file)

        # Agrupar eventos por data
        eventos_agrupados = {}
        for evento in eventos:
            data = evento["date"]
            evento_formatado = {
                "title": evento["title"],
                "venue": evento["club_name"],  # Usando 'club_name' como o local do evento
                "time_init": evento["time_init"],  # Novo campo
                "time_end": evento["time_end"],  # Novo campo
                "price": evento["price"],
                "categories": evento["categories"],
                "img_url": evento["img_url"],
                "link": evento["link"],
                "address": evento["address"],  # Novo campo
                "description": evento["description"],  # Novo campo
            }
            if data not in eventos_agrupados:
                eventos_agrupados[data] = {
                    "date": data,
                    "events": [],
                    "status": "Done"
                }
            eventos_agrupados[data]["events"].append(evento_formatado)

        eventos_formatados = list(eventos_agrupados.values())

        return jsonify(eventos_formatados)
    except FileNotFoundError:
        return jsonify({"error": "Arquivo events.json não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500