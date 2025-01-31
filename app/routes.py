import json
from flask import Blueprint, render_template, jsonify
from datetime import datetime
import locale
import re

main = Blueprint('main', __name__)

try:
    locale.setlocale(locale.LC_TIME, "en_US.UTF-8")
except locale.Error:
    print("Locale inglês não disponível, usando o padrão do sistema.")

@main.route('/')
def index():
    # Carregar e parsear o arquivo JSON
    try:
        with open('app/database/events.json', 'r', encoding='utf-8') as file:
            eventos = json.load(file)
        
        return render_template('index.html', eventos=eventos)
    except Exception as e:
        return f"Erro ao carregar eventos: {str(e)}"

DIAS_FR = {
    "lun": "Mon", "mar": "Tue", "mer": "Wed", "jeu": "Thu",
    "ven": "Fri", "sam": "Sat", "dim": "Sun"
}

MESES_FR = {
    "janv": "Jan", "févr": "Feb", "mars": "Mar", "avr": "Apr",
    "mai": "May", "juin": "Jun", "juil": "Jul", "août": "Aug",
    "sept": "Sep", "oct": "Oct", "nov": "Nov", "déc": "Dec"
}


def formatar_data(data_str):
    ano_atual = datetime.now().year

    # Remover ponto final do mês (exemplo: 'janv.')
    data_limpa = re.sub(r"\.$", "", data_str)

    # Substituir dia da semana
    for dia_fr, dia_en in DIAS_FR.items():
        if data_limpa.startswith(dia_fr):
            data_limpa = data_limpa.replace(dia_fr, dia_en, 1)
            break

    # Substituir mês
    for mes_fr, mes_en in MESES_FR.items():
        if mes_fr in data_limpa:
            data_limpa = data_limpa.replace(mes_fr, mes_en)
            break

    try:
        # print(f"Tentando converter: '{data_limpa} {ano_atual}'")
        return datetime.strptime(f"{data_limpa} {ano_atual}", "%a %d %b %Y")
    except ValueError as e:
        print(f"Erro ao processar data: '{data_str}'. Erro: {e}")
        return None


@main.route('/api/events')
def api_events():
    try:
        with open('app/database/events.json', 'r', encoding='utf-8') as file:
            eventos = json.load(file)

        eventos_agrupados = {}

        for evento in eventos:
            data_evento = formatar_data(evento["date"])
            if data_evento:
                status = "Done" if data_evento < datetime.now() else "Upcoming"

                evento_formatado = {
                    "title": evento["title"],
                    "venue": evento["club_name"],
                    "time_init": evento["time_init"],
                    "time_end": evento["time_end"],
                    "price": evento["price"],
                    "categories": evento["categories"],
                    "img_url": evento["img_url"],
                    "link": evento["link"],
                    "address": evento["address"],
                    "description": evento["description"],
                }

                if data_evento not in eventos_agrupados:
                    eventos_agrupados[data_evento] = {
                        "date": data_evento,
                        "events": [],
                        "status": status
                    }

                eventos_agrupados[data_evento]["events"].append(evento_formatado)

        eventos_formatados = list(eventos_agrupados.values())
        return jsonify(eventos_formatados)

    except FileNotFoundError:
        return jsonify({"error": "Arquivo events.json não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500