from flask import Flask, render_template, request, jsonify
import requests
import math

try:
    import mysql.connector
    MYSQL_DISPONIVEL = True
except ImportError:
    MYSQL_DISPONIVEL = False

app = Flask(__name__)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "sua_senha",
    "database": "ecomap"
}

def get_db_connection():
    if not MYSQL_DISPONIVEL:
        return None
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Exception:
        return None

def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def buscar_api_gratuita(lat, lng):
    pontos = []
    
    # Raio aumentado para 30km para pegar toda a região metropolitana (ex: Florianópolis + São José + Palhoça)
    query_overpass = f"""[out:json][timeout:50];
    (
      node["amenity"="recycling"](around:30000, {lat}, {lng});
      way["amenity"="recycling"](around:30000, {lat}, {lng});
    );
    out center 60;"""

    # Servidores públicos do Overpass (se o primeiro falhar, tenta o segundo)
    servidores_overpass = [
        "https://overpass-api.de/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter"
    ]

    headers = {"User-Agent": "EcoMap-Brasil-App/6.0"}

    for url_overpass in servidores_overpass:
        try:
            res = requests.post(
                url_overpass, 
                data={"data": query_overpass}, 
                headers=headers, 
                timeout=50
            ).json()

            elements = res.get("elements", [])
            if not elements:
                continue

            for item in elements:
                i_lat = item.get("lat") or item.get("center", {}).get("lat")
                i_lng = item.get("lon") or item.get("center", {}).get("lon")
                tags = item.get("tags", {})
                
                nome = tags.get("name") or tags.get("description") or tags.get("operator") or "Ponto de Reciclagem"
                cidade = tags.get("addr:city") or tags.get("addr:suburb") or "Região Próxima"

                materiais = []
                if tags.get("recycling:glass") == "yes": materiais.append("Vidro")
                if tags.get("recycling:paper") == "yes": materiais.append("Papel")
                if tags.get("recycling:plastic") == "yes": materiais.append("Plástico")
                if tags.get("recycling:cans") == "yes": materiais.append("Metal")
                if tags.get("recycling:clothes") == "yes": materiais.append("Roupas")
                if tags.get("recycling:batteries") == "yes": materiais.append("Pilhas/Baterias")
                
                if not materiais: 
                    materiais = ["Recicláveis Gerais"]

                if i_lat and i_lng:
                    pontos.append({
                        "nome": nome,
                        "cidade": cidade,
                        "lat": i_lat,
                        "lng": i_lng,
                        "materiais": materiais
                    })

            # Se conseguiu buscar pontos reais com sucesso, encerra o loop
            if pontos:
                break

        except Exception as err:
            print(f"⚠️ Erro ao consultar servidor {url_overpass}: {err}")

    return pontos

def processar_pontos_por_coordenada(lat_user, lng_user):
    pontos_finais = []

    # 1. Tenta buscar no MySQL se estiver configurado
    try:
        conn = get_db_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM ecopontos")
            todos_pontos_db = cursor.fetchall()
            cursor.close()
            conn.close()

            for ponto in todos_pontos_db:
                p_lat = float(ponto["latitude"])
                p_lng = float(ponto["longitude"])
                dist = calcular_distancia(lat_user, lng_user, p_lat, p_lng)

                if dist <= 50.0:
                    mat_raw = ponto.get("materiais", "")
                    mat_lista = [m.strip() for m in mat_raw.split(",")] if mat_raw else ["Recicláveis Gerais"]
                    pontos_finais.append({
                        "nome": ponto["nome"],
                        "cidade": ponto.get("cidade", "Cadastrado no Banco"),
                        "lat": p_lat,
                        "lng": p_lng,
                        "materiais": mat_lista
                    })
    except Exception as e:
        print(f"⚠️ MySQL não disponível: {e}")

    # 2. Busca pontos reais na API do OpenStreetMap
    pontos_api = buscar_api_gratuita(lat_user, lng_user)
    
    # Deduplicação baseada em coordenadas (lat + lng)
    for p_api in pontos_api:
        duplicado = any(
            abs(p["lat"] - p_api["lat"]) < 0.0001 and abs(p["lng"] - p_api["lng"]) < 0.0001 
            for p in pontos_finais
        )
        if not duplicado:
            pontos_finais.append(p_api)

    return pontos_finais

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/buscar", methods=["GET"])
def buscar_locais():
    endereco = request.args.get("endereco")
    if not endereco:
        return jsonify({"erro": "Por favor, digite um endereço ou cidade."}), 400

    try:
        url_nominatim = "https://nominatim.openstreetmap.org/search"
        headers = {"User-Agent": "EcoMap-Brasil-Free/1.0"}
        params_geo = {"q": endereco, "format": "json", "limit": 1, "countrycodes": "br"}
        
        res_geo = requests.get(url_nominatim, params=params_geo, headers=headers, timeout=15).json()
        
        if not res_geo:
            return jsonify({"erro": "Endereço não encontrado."}), 400

        lat_user = float(res_geo[0]["lat"])
        lng_user = float(res_geo[0]["lon"])

        pontos = processar_pontos_por_coordenada(lat_user, lng_user)

        return jsonify({
            "lat_usuario": lat_user,
            "lng_usuario": lng_user,
            "pontos": pontos
        })

    except Exception as e:
        print("Erro no servidor:", e)
        return jsonify({"erro": "Erro ao processar a busca."}), 500

@app.route("/buscar_coords", methods=["GET"])
def buscar_por_coordenadas():
    try:
        lat_user = float(request.args.get("lat"))
        lng_user = float(request.args.get("lng"))

        pontos = processar_pontos_por_coordenada(lat_user, lng_user)

        return jsonify({
            "lat_usuario": lat_user,
            "lng_usuario": lng_user,
            "pontos": pontos
        })
    except (TypeError, ValueError):
        return jsonify({"erro": "Coordenadas inválidas."}), 400
    except Exception as e:
        print("Erro no servidor:", e)
        return jsonify({"erro": "Erro ao processar localização."}), 500

if __name__ == "__main__":
    app.run(debug=True)