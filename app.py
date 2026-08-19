from flask import Flask, render_template, request, jsonify
import requests
import math
from rotas_usuarios import registrar_rotas_usuario

app = Flask(__name__)

# Registra as rotas de login e cadastro (/login e /cadastro)
registrar_rotas_usuario(app)


#CONFIGURAÇÃO DO BANCO DE DADOS MYSQL

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",          # Usuário do MySQL
    "password": "Senac2026",  # Senha do MySQL
    "database": "EcoMap"     # Nome do banco
}

try:
    import mysql.connector
    MYSQL_DISPONIVEL = True
except ImportError:
    MYSQL_DISPONIVEL = False

def get_db_connection():
    if not MYSQL_DISPONIVEL:
        return None
    return mysql.connector.connect(**DB_CONFIG)

def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


#BUSCA NA API (OPENSTREETMAP OVERPASS - COM TIMEOUT ESTENDIDO)

def buscar_api_gratuita(lat, lng):
    pontos = []
    try:
        # Query Overpass com limite estendido para 50s
        query_overpass = f"""[out:json][timeout:50];
        (
          node["amenity"="recycling"](around:15000, {lat}, {lng});
          way["amenity"="recycling"](around:15000, {lat}, {lng});
        );
        out center 10;"""

        url_overpass = "https://overpass-api.de/api/interpreter"
        headers = {"User-Agent": "EcoMap-Brasil-App/6.0"}
        
        # Timeout de conexao mantido em 50s no servidor Python
        res = requests.post(
            url_overpass, 
            data={"data": query_overpass}, 
            headers=headers, 
            timeout=50
        ).json()

        for item in res.get("elements", []):
            i_lat = item.get("lat") or item.get("center", {}).get("lat")
            i_lng = item.get("lon") or item.get("center", {}).get("lon")
            tags = item.get("tags", {})
            
            nome = tags.get("name") or tags.get("description") or tags.get("operator") or "Ponto de Reciclagem Público"
            cidade = tags.get("addr:city") or tags.get("addr:suburb") or "Região Próxima"

            materiais = []
            if tags.get("recycling:glass") == "yes": materiais.append("Vidro")
            if tags.get("recycling:paper") == "yes": materiais.append("Papel")
            if tags.get("recycling:plastic") == "yes": materiais.append("Plástico")
            if tags.get("recycling:cans") == "yes": materiais.append("Metal")
            if not materiais: materiais = ["Recicláveis Gerais", "Plástico", "Papel"]

            if i_lat and i_lng:
                pontos.append({
                    "nome": nome,
                    "cidade": cidade,
                    "lat": i_lat,
                    "lng": i_lng,
                    "materiais": materiais
                })

    except requests.exceptions.Timeout:
        print("⚠️ A requisição à API do Overpass demorou mais de 30 segundos e expirou.")
    except Exception as err:
        print(f"⚠️ Erro ao consultar a API pública: {err}")

    return pontos

#ROTAS DA APLICAÇÃO

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/buscar", methods=["GET"])
def buscar_locais():
    endereco = request.args.get("endereco")
    lat_param = request.args.get("lat")
    lng_param = request.args.get("lng")

    lat_user = None
    lng_user = None

    try:
        # 1. Se recebeu coordenadas via GPS
        if lat_param and lng_param:
            lat_user = float(lat_param)
            lng_user = float(lng_param)
        elif endereco:
            # 2. Converte endereço/cidade via Nominatim com tratamento de conexao
            url_nominatim = "https://nominatim.openstreetmap.org/search"
            headers = {
                "User-Agent": "EcoMap-Brasil-App-v2/1.0 (contato@ecomap.com.br)",
                "Accept-Language": "pt-BR,pt;q=0.9"
            }
            params_geo = {
                "q": endereco, 
                "format": "json", 
                "limit": 1, 
                "countrycodes": "br",
                "addressdetails": 1
            }
            
            try:
                res_geo_raw = requests.get(url_nominatim, params=params_geo, headers=headers, timeout=10)
                res_geo = res_geo_raw.json()
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as net_err:
                print(f"⚠️ Erro de rede ao acessar Nominatim: {net_err}")
                return jsonify({"erro": "Falha na conexão de internet ao buscar o endereço. Tente novamente."}), 503

            if not res_geo:
                return jsonify({"erro": f"Localização '{endereco}' não encontrada."}), 404

            lat_user = float(res_geo[0]["lat"])
            lng_user = float(res_geo[0]["lon"])
        else:
            return jsonify({"erro": "Por favor, digite um endereço ou ative o GPS."}), 400

        pontos_finais = []

        # 3. Busca no Banco de Dados Local (MySQL)
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

                    if dist <= 30.0:  # Raio de 30km
                        mat_raw = ponto.get("materiais", "")
                        mat_lista = [m.strip() for m in mat_raw.split(",")] if mat_raw else ["Recicláveis Gerais"]
                        pontos_finais.append({
                            "nome": ponto["nome"],
                            "cidade": ponto.get("cidade", "Cadastrado no Banco"),
                            "lat": p_lat,
                            "lng": p_lng,
                            "materiais": mat_lista
                        })
        except Exception as db_err:
            print(f"⚠️ MySQL ausente ou não configurado: {db_err}")

        # 4. Busca na API pública do Overpass
        pontos_api = buscar_api_gratuita(lat_user, lng_user)
        
        # Junta resultados sem duplicar marcadores
        for p_api in pontos_api:
            if not any(abs(p["lat"] - p_api["lat"]) < 0.0001 and abs(p["lng"] - p_api["lng"]) < 0.0001 for p in pontos_finais):
                pontos_finais.append(p_api)

        # Retorno sem armazenamento de cache
        resposta = jsonify({
            "lat_usuario": lat_user,
            "lng_usuario": lng_user,
            "pontos": pontos_finais
        })
        resposta.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        resposta.headers["Pragma"] = "no-cache"
        resposta.headers["Expires"] = "0"

        return resposta, 200

    except Exception as e:
        print("Erro interno no servidor:", e)
        return jsonify({"erro": "Erro ao processar a busca no servidor."}), 500

if __name__ == "__main__":
    app.run(debug=True)