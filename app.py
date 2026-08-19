from flask import Flask, render_template, request, jsonify
import requests
import math

# Tenta importar o conector do MySQL
try:
    import mysql.connector
    MYSQL_DISPONIVEL = True
except ImportError:
    MYSQL_DISPONIVEL = False

app = Flask(__name__)

# ==============================================================================
#  CONFIGURAÇÃO DO BANCO DE DADOS MYSQL
# ==============================================================================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",          # Usuário do MySQL
    "password": "sua_senha",  # Senha do MySQL
    "database": "ecomap"     # Nome do banco
}

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

# ==============================================================================
# 🌐 BUSCA NA API GRATUITA (OPENSTREETMAP - QUERY EXPANDIDA)
# ==============================================================================
def buscar_api_gratuita(lat, lng):
    pontos = []
    try:
        # Aumentamos o timeout interno do servidor Overpass para 25 segundos
        query_overpass = f"""[out:json][timeout:25];
        (
          node["amenity"="recycling"](around:15000, {lat}, {lng});
          way["amenity"="recycling"](around:15000, {lat}, {lng});
        );
        out center 20;"""

        url_overpass = "https://overpass-api.de/api/interpreter"
        headers = {"User-Agent": "EcoMap-Brasil-App/6.0"}
        
        # Aumentamos o timeout de conexão do Python para 30 segundos
        res = requests.post(
            url_overpass, 
            data={"data": query_overpass}, 
            headers=headers, 
            timeout=30
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

# ==============================================================================
# 🌐 ROTAS DA APLICAÇÃO
# ==============================================================================
@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/buscar", methods=["GET"])
def buscar_locais():
    endereco = request.args.get("endereco")
    if not endereco:
        return jsonify({"erro": "Por favor, digite um endereço ou cidade."}), 400

    try:
        # 1. Converte o endereço em Coordenadas
        url_nominatim = "https://nominatim.openstreetmap.org/search"
        headers = {"User-Agent": "EcoMap-Brasil-Free/1.0"}
        params_geo = {"q": endereco, "format": "json", "limit": 1, "countrycodes": "br"}
        
        res_geo = requests.get(url_nominatim, params=params_geo, headers=headers, timeout=8).json()
        
        if not res_geo:
            return jsonify({"erro": "Endereço não encontrado."}), 400

        lat_user = float(res_geo[0]["lat"])
        lng_user = float(res_geo[0]["lon"])

        pontos_finais = []

        # 2. Tenta buscar no MySQL
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

                    if dist <= 50.0:  # Raio de 50km
                        mat_raw = ponto.get("materiais", "")
                        mat_lista = [m.strip() for m in mat_raw.split(",")] if mat_raw else ["Recicláveis Gerais"]
                        pontos_finais.append({
                            "nome": ponto["nome"],
                            "cidade": ponto.get("cidade", "Cadastrado no Banco"),
                            "lat": p_lat,
                            "lng": p_lng,
                            "materiais": mat_lista
                        })
        except Exception:
            print("⚠️ MySQL ausente ou não configurado. Prosseguindo sem o banco local.")

        # 3. Busca complementar na API Gratuita do OpenStreetMap
        pontos_api = buscar_api_gratuita(lat_user, lng_user)
        
        # Junta os pontos do MySQL com os da API Gratuita (sem duplicar)
        for p_api in pontos_api:
            # Evita adicionar duplicados baseados na posição exata
            if not any(abs(p["lat"] - p_api["lat"]) < 0.0001 for p in pontos_finais):
                pontos_finais.append(p_api)

        return jsonify({
            "lat_usuario": lat_user,
            "lng_usuario": lng_user,
            "pontos": pontos_finais
        })

    except Exception as e:
        print("Erro no servidor:", e)
        return jsonify({"erro": "Erro ao processar a busca."}), 500

if __name__ == "__main__":
    app.run(debug=True)