Game-Jam

🌱 EcoMap Brasil

<div align="center">

♻️ Encontre pontos de reciclagem perto de você

Uma solução tecnológica para facilitar o descarte correto de resíduos e incentivar a sustentabilidade.

</div>

📌 Sobre o projeto

O EcoMap Brasil é uma aplicação web desenvolvida para facilitar a localização de pontos de reciclagem e ecopontos próximos ao usuário.

O sistema permite que o usuário informe uma cidade, bairro ou endereço ou utilize sua localização atual através do GPS. A partir dessa localização, o sistema busca pontos de reciclagem próximos, apresenta os resultados em um mapa interativo e informa os materiais aceitos em cada local.

O projeto utiliza dados abertos do OpenStreetMap, com geocodificação através do Nominatim e consultas de pontos de reciclagem através da Overpass API. Também possui suporte opcional a um banco de dados MySQL para armazenamento de ecopontos próprios.

⚠️ Importante: os resultados dependem da disponibilidade e atualização dos dados dos serviços externos. Se você pesquisar o nome de um lugar e nenhum ecoponto aparecer, tente pesquisar o mesmo lugar novamente. Uma nova consulta pode retornar resultados diferentes dependendo da resposta momentânea dos serviços de mapas.

🎯 Problema

Muitas pessoas possuem materiais recicláveis em casa, mas não sabem onde realizar o descarte correto.

Entre os principais problemas estão:

Falta de informação sobre pontos de coleta;

Dificuldade para encontrar ecopontos próximos;

Falta de informação sobre os materiais aceitos;

Dificuldade para saber como chegar ao local;

Descarte incorreto de materiais recicláveis.

O EcoMap Brasil foi criado para tornar esse processo mais simples, rápido e acessível.

💡 Solução

O EcoMap transforma a localização do usuário em uma busca por pontos de reciclagem.

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

🚀 Funcionalidades

📍 Localização por endereço

O usuário pode pesquisar por:

Cidade;

Bairro;

Endereço;

Localidade.

O sistema utiliza o Nominatim, serviço de geocodificação do OpenStreetMap, para transformar o endereço em coordenadas geográficas.

⚠️ Aviso sobre a pesquisa: caso o local seja encontrado, mas nenhum ecoponto apareça nos resultados, pesquise o mesmo lugar novamente. A busca depende de serviços externos e dos dados disponíveis no momento da consulta.

📡 Localização por GPS

O usuário pode clicar no botão:

📍 GPS

O navegador solicita permissão para acessar a localização atual.

Após obter a latitude e longitude, o sistema procura os ecopontos próximos.

🗺️ Mapa interativo

Os resultados são apresentados em um mapa utilizando Leaflet.js.

O mapa apresenta:

📍 Localização do usuário;

♻️ Ecopontos;

📏 Distância;

ℹ️ Informações dos pontos;

🗺️ Opção para obter uma rota.

📏 Distância

O sistema calcula a distância entre o usuário e cada ecoponto utilizando a fórmula de Haversine.

Os pontos são organizados do mais próximo para o mais distante.

Exemplo:

🥇 Ecoponto Central
📏 350 metros

🥈 Ecoponto Norte
📏 1.2 km

🥉 Ecoponto Sul
📏 2.8 km

♻️ Materiais aceitos

O sistema identifica os materiais disponíveis em cada ecoponto.

Material

Emoji

Plástico

🥤

Vidro

🍾

Papel

📦

Metal

🥫

Roupas

👕

Pilhas/Baterias

🔋

Eletrônicos

💻

Óleo

🛢️

Entulho

🧱

Recicláveis gerais

♻️

🔎 Filtros

O usuário pode filtrar os resultados por tipo de material.

Todos
🥤 Plástico
🍾 Vidro
📦 Papel
🥫 Metal

🗺️ Como chegar

Cada ecoponto possui um botão que abre uma rota utilizando o Google Maps.

🗺️ Como Chegar

🌙 Modo escuro

A aplicação possui suporte para:

☀️ Tema claro;

🌙 Tema escuro.

📱 Interface responsiva

A interface foi desenvolvida para funcionar em:

💻 Computadores;

📱 Celulares;

📲 Tablets.

🛠️ Tecnologias utilizadas

Backend

🐍 Python

🌐 Flask

📡 Requests

🗄️ MySQL Connector

📐 Math

Frontend

HTML5

CSS3

JavaScript

Leaflet.js

APIs e serviços

OpenStreetMap

Nominatim

Overpass API

Google Maps

Banco de dados

MySQL

📁 Estrutura do projeto

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

No código atual, o HTML, CSS e JavaScript podem estar juntos no index.html. A separação em arquivos static é recomendada para organização futura.

⚙️ Instalação

📋 Pré-requisitos

Antes de iniciar, certifique-se de possuir:

Python 3 instalado;

pip instalado;

MySQL instalado, caso queira utilizar o banco de dados;

Git instalado;

Um navegador moderno.

🐍 1. Verificar o Python

Verifique se o Python está instalado:

python --version

ou:

python3 --version

📦 2. Clonar o projeto

git clone https://github.com/SEU-USUARIO/EcoMap-Brasil.git

Entre na pasta:

cd EcoMap-Brasil

🔧 3. Criar ambiente virtual

O ambiente virtual é recomendado para manter as dependências do projeto separadas do restante do sistema.

Windows

python -m venv venv

Ative o ambiente:

venv\Scripts\activate

Linux / macOS

python3 -m venv venv

Ative:

source venv/bin/activate

📚 4. Instalar Flask

pip install flask

O Flask é utilizado para criar o servidor e as rotas do backend.

📡 5. Instalar Requests

pip install requests

O Requests é utilizado para realizar as requisições às APIs externas.

🗄️ 6. Instalar MySQL Connector

pip install mysql-connector-python

O MySQL Connector permite que o Python se conecte ao banco de dados MySQL.

📦 7. Instalar todas as dependências de uma vez

Também é possível instalar todas as bibliotecas com apenas um comando:

pip install flask requests mysql-connector-python

📄 8. requirements.txt

O projeto pode utilizar um arquivo requirements.txt para facilitar a instalação.

Crie o arquivo:

requirements.txt

Adicione:

Flask
requests
mysql-connector-python

Depois execute:

pip install -r requirements.txt

🗄️ Configuração do MySQL

O MySQL é opcional.

O sistema consegue buscar pontos diretamente através do OpenStreetMap/Overpass, mas o MySQL permite utilizar uma base própria de ecopontos.

1. Criar o banco

Entre no MySQL:

mysql -u root -p

Crie o banco:

CREATE DATABASE ecomap;

Selecione o banco:

USE ecomap;

2. Criar a tabela

CREATE TABLE ecopontos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cidade VARCHAR(255),
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL,
    materiais TEXT
);

3. Adicionar um exemplo

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

🔐 Configurar o banco no Python

No arquivo app.py, configure:

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "SUA_SENHA",
    "database": "EcoMap"
}

Altere:

sua_senha

para a senha do seu MySQL.

Exemplo

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "123456",
    "database": "EcoMap"
}

⚠️ Em ambientes de produção, não coloque senhas diretamente no código. Utilize variáveis de ambiente.

▶️ Executando o projeto

Depois de instalar as dependências, execute:

python app.py

No Linux/macOS:

python3 app.py

O servidor será iniciado.

Acesse:

http://127.0.0.1:5000

ou:

http://localhost:5000

🔌 Endpoints

O backend possui uma rota principal de busca.

🔎 Buscar por endereço

GET /buscar?endereco=Curitiba

Exemplo:

http://localhost:5000/buscar?endereco=Curitiba

O endereço é convertido em coordenadas pelo Nominatim antes da busca dos ecopontos.

📍 Buscar por coordenadas / GPS

A mesma rota /buscar também aceita latitude e longitude:

GET /buscar?lat=-25.4284&lng=-49.2733

Exemplo:

http://localhost:5000/buscar?lat=-25.4284&lng=-49.2733

Quando lat e lng são enviados, o sistema utiliza diretamente essas coordenadas.

Observação: não existe uma rota /buscar_coords no app.py atual.

🔄 Funcionamento da busca

Quando o usuário realiza uma pesquisa:

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

📜 Créditos e atribuições de terceiros

O EcoMap Brasil utiliza bibliotecas, serviços e dados de terceiros. Eles são utilizados de acordo com suas respectivas licenças, termos de uso e políticas.

🌎 OpenStreetMap

O OpenStreetMap (OSM) fornece os dados geográficos utilizados pelo projeto.

Site oficial: https://www.openstreetmap.org/

📍 Nominatim

O Nominatim é utilizado para transformar o endereço informado pelo usuário em coordenadas geográficas.

Site oficial: https://nominatim.openstreetmap.org/

🔎 Overpass API

A Overpass API é utilizada para consultar os pontos de reciclagem registrados no OpenStreetMap.

No app.py, a consulta procura locais utilizando:

amenity = recycling

A aplicação utiliza o servidor público:

https://overpass-api.de/api/interpreter

Site do projeto: https://overpass-api.de/

🗺️ Leaflet.js

O Leaflet.js é utilizado no frontend para a exibição do mapa interativo.

Site oficial: https://leafletjs.com/

🐍 Flask

O Flask é utilizado para criar o servidor web e as rotas do backend.

Site oficial: https://flask.palletsprojects.com/

📡 Requests

A biblioteca Requests é utilizada pelo backend Python para realizar requisições HTTP aos serviços externos.

Site oficial: https://requests.readthedocs.io/

🗄️ MySQL Connector/Python

O MySQL Connector/Python é utilizado para realizar a conexão entre o Python e o banco de dados MySQL.

Site oficial: https://dev.mysql.com/doc/connector-python/en/

🗺️ Google Maps

O Google Maps é utilizado pelo frontend para a funcionalidade de Como Chegar, conforme descrito na aplicação.

Site oficial: https://maps.google.com/

Importante: os serviços, bibliotecas e dados de terceiros não pertencem ao EcoMap Brasil. O projeto apenas utiliza essas tecnologias e serviços para implementar suas funcionalidades.

Dados de terceiros: os pontos encontrados por meio do OpenStreetMap/Overpass são dados disponibilizados por colaboradores da comunidade do OpenStreetMap. O EcoMap Brasil não garante que todos os pontos existentes estejam cadastrados, atualizados ou disponíveis em todas as pesquisas.

📐 Cálculo de distância

O projeto utiliza a fórmula de Haversine para calcular a distância geográfica entre duas coordenadas.

A fórmula considera:

Latitude;

Longitude;

Raio aproximado da Terra.

O resultado é apresentado em quilômetros ou metros.

Exemplo:

📏 450m

ou:

📏 2.3 km

🌱 Sustentabilidade

O EcoMap Brasil tem como objetivo facilitar o acesso da população à reciclagem e incentivar o descarte correto de resíduos.

A solução pode contribuir para:

♻️ Aumentar a reciclagem;

🗑️ Reduzir o descarte incorreto;

🌎 Reduzir impactos ambientais;

🔄 Incentivar a economia circular;

📚 Facilitar o acesso à informação;

🏙️ Contribuir para cidades mais sustentáveis.

🎯 ODS relacionados

ODS 11 — Cidades e Comunidades Sustentáveis

O projeto contribui para cidades mais sustentáveis ao facilitar o acesso da população a pontos de descarte e reciclagem.

ODS 12 — Consumo e Produção Responsáveis

É o principal ODS relacionado ao projeto, incentivando o descarte adequado e o reaproveitamento de materiais.

ODS 13 — Ação Contra a Mudança Global do Clima

A reciclagem e a redução do descarte inadequado podem contribuir para diminuir impactos ambientais.

🏆 Hackathon

💭 Nossa ideia

"Se existe um lugar correto para descartar, por que deveria ser difícil encontrá-lo?"

O EcoMap Brasil foi desenvolvido para aproximar as pessoas da reciclagem através da tecnologia.

O usuário não precisa procurar manualmente por diferentes pontos de coleta.

Basta informar sua localização.

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

Nossa proposta

Tecnologia + Geolocalização + Dados Abertos + Sustentabilidade

🔮 Futuras melhorias

👤 Sistema de usuários

♻️ Cadastro de novos ecopontos

⭐ Avaliação dos ecopontos

📸 Fotos dos locais

🕐 Horários de funcionamento

📞 Informações de contato

❤️ Sistema de favoritos

🏆 Sistema de pontos

🥇 Ranking de usuários

📊 Dashboard de impacto ambiental

🔔 Notificações

🏢 Integração com cooperativas

📱 Aplicativo mobile

🌎 Expansão para outras regiões

🔐 Privacidade

A localização do usuário é utilizada para encontrar pontos de reciclagem próximos.

Quando o usuário utiliza o GPS, o navegador solicita permissão antes de disponibilizar sua localização.

O projeto não depende do armazenamento permanente da localização do usuário para realizar sua função principal.

🤝 Contribuição

Contribuições são bem-vindas!

1. Faça um Fork

Clique em Fork no GitHub.

2. Clone o projeto

git clone https://github.com/SEU-USUARIO/EcoMap-Brasil.git

3. Entre na pasta

cd EcoMap-Brasil

4. Crie uma branch

git checkout -b minha-feature

5. Faça suas alterações

6. Adicione as alterações

git add .

7. Faça o commit

git commit -m "Adiciona nova funcionalidade"

8. Envie para o GitHub

git push origin minha-feature

Depois abra um Pull Request.

📄 Licença

Este projeto está sob a licença MIT.

Consulte o arquivo LICENSE para mais informações.

<div align="center">

🌱 EcoMap Brasil

Encontre. Recicle. Transforme. ♻️

Tecnologia a favor da sustentabilidade.

</div>
