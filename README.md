# Game-Jam

# 🌱 EcoMap Brasil

<div align="center">

### ♻️ Encontre pontos de reciclagem perto de você

**Uma solução tecnológica para facilitar o descarte correto de resíduos e incentivar a sustentabilidade.**

</div>

---

## 📌 Sobre o projeto

O **EcoMap Brasil** é uma aplicação web desenvolvida para facilitar a localização de **pontos de reciclagem e ecopontos** próximos ao usuário.

O sistema permite que o usuário informe uma **cidade, bairro ou endereço** ou utilize sua **localização atual através do GPS**. A partir dessa localização, o sistema busca pontos de reciclagem próximos, apresenta os resultados em um **mapa interativo** e informa os **materiais aceitos** em cada local.

O projeto utiliza dados do **OpenStreetMap**, consultas através da **Overpass API** e possui suporte opcional a um banco de dados **MySQL** para armazenamento de ecopontos próprios.

---

## 🎯 Problema

Muitas pessoas possuem materiais recicláveis em casa, mas não sabem onde realizar o descarte correto.

Entre os principais problemas estão:

* Falta de informação sobre pontos de coleta;
* Dificuldade para encontrar ecopontos próximos;
* Falta de informação sobre os materiais aceitos;
* Dificuldade para saber como chegar ao local;
* Descarte incorreto de materiais recicláveis.

O **EcoMap Brasil** foi criado para tornar esse processo mais simples, rápido e acessível.

---

## 💡 Solução

O EcoMap transforma a localização do usuário em uma busca por pontos de reciclagem.

```text
👤 USUÁRIO
    │
    ├── 🔎 Digita endereço
    │
    └── 📍 Utiliza GPS
             │
             ▼
       🌐 ECOMap Brasil
             │
             ▼
       🐍 Backend Flask
             │
       ┌─────┴─────┐
       │           │
       ▼           ▼
  🌎 OpenStreetMap  🗄️ MySQL
       │           │
       └─────┬─────┘
             ▼
       ♻️ ECOPONTOS
             │
       ┌─────┴─────┐
       ▼           ▼
    🗺️ MAPA      📋 LISTA
       │           │
       └─────┬─────┘
             ▼
       🚗 COMO CHEGAR
```

---

# 🚀 Funcionalidades

### 📍 Localização por endereço

O usuário pode pesquisar por:

* Cidade;
* Bairro;
* Endereço;
* Localidade.

O sistema utiliza o **Nominatim**, serviço de geocodificação do OpenStreetMap, para transformar o endereço em coordenadas geográficas.

---

### 📡 Localização por GPS

O usuário pode clicar no botão:

```text
📍 GPS
```

O navegador solicita permissão para acessar a localização atual.

Após obter a latitude e longitude, o sistema procura os ecopontos próximos.

---

### 🗺️ Mapa interativo

Os resultados são apresentados em um mapa utilizando **Leaflet.js**.

O mapa apresenta:

* 📍 Localização do usuário;
* ♻️ Ecopontos;
* 📏 Distância;
* ℹ️ Informações dos pontos;
* 🗺️ Opção para obter uma rota.

---

### 📏 Distância

O sistema calcula a distância entre o usuário e cada ecoponto utilizando a **fórmula de Haversine**.

Os pontos são organizados do mais próximo para o mais distante.

Exemplo:

```text
🥇 Ecoponto Central
📏 350 metros

🥈 Ecoponto Norte
📏 1.2 km

🥉 Ecoponto Sul
📏 2.8 km
```

---

### ♻️ Materiais aceitos

O sistema identifica os materiais disponíveis em cada ecoponto.

| Material           | Emoji |
| ------------------ | ----- |
| Plástico           | 🥤    |
| Vidro              | 🍾    |
| Papel              | 📦    |
| Metal              | 🥫    |
| Roupas             | 👕    |
| Pilhas/Baterias    | 🔋    |
| Eletrônicos        | 💻    |
| Óleo               | 🛢️   |
| Entulho            | 🧱    |
| Recicláveis gerais | ♻️    |

---

### 🔎 Filtros

O usuário pode filtrar os resultados por tipo de material.

```text
Todos
🥤 Plástico
🍾 Vidro
📦 Papel
🥫 Metal
```

---

### 🗺️ Como chegar

Cada ecoponto possui um botão que abre uma rota utilizando o Google Maps.

```text
🗺️ Como Chegar
```

---

### 🌙 Modo escuro

A aplicação possui suporte para:

* ☀️ Tema claro;
* 🌙 Tema escuro.

---

### 📱 Interface responsiva

A interface foi desenvolvida para funcionar em:

* 💻 Computadores;
* 📱 Celulares;
* 📲 Tablets.

---

# 🛠️ Tecnologias utilizadas

## Backend

* 🐍 Python
* 🌐 Flask
* 📡 Requests
* 🗄️ MySQL Connector
* 📐 Math

## Frontend

* HTML5
* CSS3
* JavaScript
* Leaflet.js

## APIs e serviços

* OpenStreetMap
* Nominatim
* Overpass API
* Google Maps

## Banco de dados

* MySQL

---

# 📁 Estrutura do projeto

```text
EcoMap-Brasil/
│
├── app.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── script.js
│
├── requirements.txt
│
├── README.md
│
└── LICENSE
```

> No código atual, o HTML, CSS e JavaScript podem estar juntos no `index.html`. A separação em arquivos `static` é recomendada para organização futura.

---

# ⚙️ Instalação

## 📋 Pré-requisitos

Antes de iniciar, certifique-se de possuir:

* Python 3 instalado;
* pip instalado;
* MySQL instalado, caso queira utilizar o banco de dados;
* Git instalado;
* Um navegador moderno.

---

# 🐍 1. Verificar o Python

Verifique se o Python está instalado:

```bash
python --version
```

ou:

```bash
python3 --version
```

---

# 📦 2. Clonar o projeto

```bash
git clone https://github.com/SEU-USUARIO/EcoMap-Brasil.git
```

Entre na pasta:

```bash
cd EcoMap-Brasil
```

---

# 🔧 3. Criar ambiente virtual

O ambiente virtual é recomendado para manter as dependências do projeto separadas do restante do sistema.

### Windows

```bash
python -m venv venv
```

Ative o ambiente:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Ative:

```bash
source venv/bin/activate
```

---

# 📚 4. Instalar Flask

```bash
pip install flask
```

O **Flask** é utilizado para criar o servidor e as rotas do backend.

---

# 📡 5. Instalar Requests

```bash
pip install requests
```

O **Requests** é utilizado para realizar as requisições às APIs externas.

---

# 🗄️ 6. Instalar MySQL Connector

```bash
pip install mysql-connector-python
```

O **MySQL Connector** permite que o Python se conecte ao banco de dados MySQL.

---

# 📦 7. Instalar todas as dependências de uma vez

Também é possível instalar todas as bibliotecas com apenas um comando:

```bash
pip install flask requests mysql-connector-python
```

---

# 📄 8. requirements.txt

O projeto pode utilizar um arquivo `requirements.txt` para facilitar a instalação.

Crie o arquivo:

```text
requirements.txt
```

Adicione:

```text
Flask
requests
mysql-connector-python
```

Depois execute:

```bash
pip install -r requirements.txt
```

---

# 🗄️ Configuração do MySQL

O MySQL é **opcional**.

O sistema consegue buscar pontos diretamente através do OpenStreetMap/Overpass, mas o MySQL permite utilizar uma base própria de ecopontos.

---

## 1. Criar o banco

Entre no MySQL:

```bash
mysql -u root -p
```

Crie o banco:

```sql
CREATE DATABASE ecomap;
```

Selecione o banco:

```sql
USE ecomap;
```

---

## 2. Criar a tabela

```sql
CREATE TABLE ecopontos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cidade VARCHAR(255),
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL,
    materiais TEXT
);
```

---

## 3. Adicionar um exemplo

```sql
INSERT INTO ecopontos
(nome, cidade, latitude, longitude, materiais)
VALUES
(
    'Ecoponto Central',
    'Curitiba',
    -25.4284,
    -49.2733,
    'Plástico,Vidro,Papel,Metal'
);
```

---

# 🔐 Configurar o banco no Python

No arquivo `app.py`, configure:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "sua_senha",
    "database": "ecomap"
}
```

Altere:

```text
sua_senha
```

para a senha do seu MySQL.

### Exemplo

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "ecomap"
}
```

> ⚠️ Em ambientes de produção, não coloque senhas diretamente no código. Utilize variáveis de ambiente.

---

# ▶️ Executando o projeto

Depois de instalar as dependências, execute:

```bash
python app.py
```

No Linux/macOS:

```bash
python3 app.py
```

O servidor será iniciado.

Acesse:

```text
http://127.0.0.1:5000
```

ou:

```text
http://localhost:5000
```

---

# 🔌 Endpoints

O backend possui dois endpoints principais.

## 🔎 Buscar por endereço

```http
GET /buscar?endereco=Curitiba
```

Exemplo:

```text
http://localhost:5000/buscar?endereco=Curitiba
```

---

## 📍 Buscar por coordenadas

```http
GET /buscar_coords?lat=-25.4284&lng=-49.2733
```

Exemplo:

```text
http://localhost:5000/buscar_coords?lat=-25.4284&lng=-49.2733
```

---

# 🔄 Funcionamento da busca

Quando o usuário realiza uma pesquisa:

```text
1. 👤 Usuário informa localização
             ↓
2. 🌐 Frontend envia requisição
             ↓
3. 🐍 Flask recebe os dados
             ↓
4. 📍 Endereço é convertido em coordenadas
             ↓
5. 🗄️ MySQL é consultado, se disponível
             ↓
6. 🌎 OpenStreetMap/Overpass é consultado
             ↓
7. ♻️ Pontos duplicados são removidos
             ↓
8. 📏 Distâncias são calculadas
             ↓
9. 🔢 Pontos são ordenados
             ↓
10. 🗺️ Resultados aparecem no mapa
             ↓
11. 📋 Lista de ecopontos é exibida
```

---

# 🌎 APIs externas

## OpenStreetMap

O OpenStreetMap fornece os dados geográficos utilizados pelo projeto.

https://www.openstreetmap.org/

---

## Nominatim

O Nominatim transforma endereços em coordenadas geográficas.

https://nominatim.openstreetmap.org/

---

## Overpass API

A Overpass API é utilizada para consultar pontos de reciclagem registrados no OpenStreetMap.

O sistema procura locais utilizando:

```text
amenity = recycling
```

A busca é realizada em um raio de aproximadamente:

```text
30 km
```

---

## Leaflet

O mapa interativo é desenvolvido utilizando Leaflet.js.

https://leafletjs.com/

---

# 📐 Cálculo de distância

O projeto utiliza a **fórmula de Haversine** para calcular a distância geográfica entre duas coordenadas.

A fórmula considera:

* Latitude;
* Longitude;
* Raio aproximado da Terra.

O resultado é apresentado em quilômetros ou metros.

Exemplo:

```text
📏 450m
```

ou:

```text
📏 2.3 km
```

---

# 🌱 Sustentabilidade

O EcoMap Brasil tem como objetivo facilitar o acesso da população à reciclagem e incentivar o descarte correto de resíduos.

A solução pode contribuir para:

* ♻️ Aumentar a reciclagem;
* 🗑️ Reduzir o descarte incorreto;
* 🌎 Reduzir impactos ambientais;
* 🔄 Incentivar a economia circular;
* 📚 Facilitar o acesso à informação;
* 🏙️ Contribuir para cidades mais sustentáveis.

---

# 🎯 ODS relacionados

## ODS 11 — Cidades e Comunidades Sustentáveis

O projeto contribui para cidades mais sustentáveis ao facilitar o acesso da população a pontos de descarte e reciclagem.

## ODS 12 — Consumo e Produção Responsáveis

É o principal ODS relacionado ao projeto, incentivando o descarte adequado e o reaproveitamento de materiais.

## ODS 13 — Ação Contra a Mudança Global do Clima

A reciclagem e a redução do descarte inadequado podem contribuir para diminuir impactos ambientais.

---

# 🏆 Hackathon

## 💭 Nossa ideia

> **"Se existe um lugar correto para descartar, por que deveria ser difícil encontrá-lo?"**

O EcoMap Brasil foi desenvolvido para aproximar as pessoas da reciclagem através da tecnologia.

O usuário não precisa procurar manualmente por diferentes pontos de coleta.

Basta informar sua localização.

```text
📍 Informar localização
        ↓
♻️ Encontrar ecopontos
        ↓
🧴 Ver materiais aceitos
        ↓
📏 Comparar distâncias
        ↓
🗺️ Visualizar no mapa
        ↓
🚗 Encontrar uma rota
        ↓
🌱 Reciclar corretamente
```

### Nossa proposta

**Tecnologia + Geolocalização + Dados Abertos + Sustentabilidade**

---

# 🔮 Futuras melhorias

* [ ] 👤 Sistema de usuários
* [ ] ♻️ Cadastro de novos ecopontos
* [ ] ⭐ Avaliação dos ecopontos
* [ ] 📸 Fotos dos locais
* [ ] 🕐 Horários de funcionamento
* [ ] 📞 Informações de contato
* [ ] ❤️ Sistema de favoritos
* [ ] 🏆 Sistema de pontos
* [ ] 🥇 Ranking de usuários
* [ ] 📊 Dashboard de impacto ambiental
* [ ] 🔔 Notificações
* [ ] 🏢 Integração com cooperativas
* [ ] 📱 Aplicativo mobile
* [ ] 🌎 Expansão para outras regiões

---

# 🔐 Privacidade

A localização do usuário é utilizada para encontrar pontos de reciclagem próximos.

Quando o usuário utiliza o GPS, o navegador solicita permissão antes de disponibilizar sua localização.

O projeto não depende do armazenamento permanente da localização do usuário para realizar sua função principal.

---

# 🤝 Contribuição

Contribuições são bem-vindas!

### 1. Faça um Fork

Clique em **Fork** no GitHub.

### 2. Clone o projeto

```bash
git clone https://github.com/SEU-USUARIO/EcoMap-Brasil.git
```

### 3. Entre na pasta

```bash
cd EcoMap-Brasil
```

### 4. Crie uma branch

```bash
git checkout -b minha-feature
```

### 5. Faça suas alterações

### 6. Adicione as alterações

```bash
git add .
```

### 7. Faça o commit

```bash
git commit -m "Adiciona nova funcionalidade"
```

### 8. Envie para o GitHub

```bash
git push origin minha-feature
```

Depois abra um **Pull Request**.

---

# 📄 Licença

Este projeto está sob a licença MIT.

Consulte o arquivo [`LICENSE`](LICENSE) para mais informações.

---

<div align="center">

# 🌱 EcoMap Brasil

### Encontre. Recicle. Transforme. ♻️

**Tecnologia a favor da sustentabilidade.**

</div>
