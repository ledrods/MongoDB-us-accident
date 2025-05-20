# 🚗 US Accidents - MongoDB Import Guide

Este guia ensina como processar e importar um dataset de acidentes de trânsito dos EUA em um banco de dados **MongoDB**, aproveitando os benefícios de bancos **NoSQL**. Ele cobre a instalação das ferramentas necessárias, preparação dos dados e visualização no shell do Mongo.

---

## ✅ Requisitos

- **Windows 10 ou superior**  
- **Python 3 instalado**  
- Arquivo `us-accident.json` contendo os dados integrados  
- Permissões de administrador (para instalações)  

---

## 🧰 1. Instalar MongoDB e Ferramentas

### 1.1. Instalar **MongoDB Server**

1. Baixe o instalador do MongoDB Community:  
   [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)  
   - Versão: MongoDB 8.0 ou superior  
   - Sistema: Windows  
   - Tipo: `.msi`

2. Durante a instalação:  
   - Selecione **"Complete"** setup  
   - Marque a opção **"Install MongoDB as a Service"**  
   - **Não instale o Compass**, se não for necessário  

> **Caminho padrão de instalação:**  
> `C:\Program Files\MongoDB\Server\8.0\`

---

### 1.2. Instalar **MongoDB Shell (mongosh)**

1. Baixe o MongoDB Shell separadamente:  
   [https://www.mongodb.com/try/download/shell](https://www.mongodb.com/try/download/shell)

2. Extraia ou instale em:  
   Exemplo: `C:\Program Files\MongoDB\Shell\`

> Certifique-se de que o executável `mongosh.exe` esteja acessível.

---

### 1.3. Instalar **MongoDB Database Tools**

1. Baixe os *Database Tools*:  
   [https://www.mongodb.com/try/download/database-tools](https://www.mongodb.com/try/download/database-tools)  
   - Versão: 100.x ou superior  
   - Tipo: `.zip`

2. Extraia o conteúdo e mova para um local fixo:  
   Exemplo: `C:\Program Files\MongoDB\Tools\100\`

3. Verifique o executável:  
   `C:\Program Files\MongoDB\Tools\100\bin\mongoimport.exe`

> Opcional: adicione o caminho `bin` do Tools ao **Path do sistema** para facilitar o uso no terminal.

---

### 1.4. Instalar **us-accident.json**

1. Baixe *O json aqui*:
   [https://drive.google.com/file/d/1qVSJJ9lLFszbRCAit0Uoex_6oxqpe8fX/view?usp=drive_link]

## 🔄 2. Preparar os dados

Você deve possuir o arquivo original `us-accident.json`, contendo os dados integrados de acidentes, clima, localização e aeroportos.

### 2.1. Converter o JSON em duas coleções

Execute o script Python `converter_json.py` fornecido neste projeto para transformar o dataset original em dois arquivos prontos para importação no MongoDB:

- `accidents_mongo.json`  
- `airports_mongo.json`

> Esse script separa o conteúdo redundante (como informações do aeroporto) em uma coleção específica, mantendo o restante organizado por acidente.

---

## 📥 3. Importar os dados no MongoDB

### 3.1. Abrir o terminal (Prompt de Comando)

Certifique-se de estar na pasta onde estão os arquivos `accidents_mongo.json` e `airports_mongo.json`.

### 3.2. Importar a coleção **airports**

```cmd
"C:\Program Files\MongoDB\Tools\100\bin\mongoimport.exe" ^
  --db us_accidents_db ^
  --collection airports ^
  --file airports_mongo.json ^
  --jsonArray
```

### 3.3. Importar a coleção **accidents**

```cmd
"C:\Program Files\MongoDB\Tools\100\bin\mongoimport.exe" ^
  --db us_accidents_db ^
  --collection accidents ^
  --file accidents_mongo.json ^
  --jsonArray
```

---

### 🔍 4. Visualizar os dados com o Mongo Shell

Execute o MongoDB Shell:

```cmd
"C:\Program Files\MongoDB\Shell\bin\mongosh.exe"
```

No shell, digite:

```js
use us_accidents_db

db.airports.findOne()
db.accidents.findOne()
```

Você verá um documento de cada coleção.

---

### 🧠 5. Por que duas coleções? E por que NoSQL?

#### ✂️ Separar em duas coleções

No arquivo original, dados do aeroporto (nome, timezone) são repetidos em milhares de registros de acidentes. Separar isso em uma coleção `airports`:

- Evita redundância
- Facilita atualizações (ex: mudar nome do aeroporto em um único lugar)
- Deixa os documentos `accidents` mais limpos

Além disso, a separação por subdocumentos (como `Location`, `Weather`, `Road_Features`) melhora a legibilidade e organização.

#### 🆚 SQL vs NoSQL neste caso

**SQL (relacional):**

- Exige múltiplas tabelas com joins (acidentes, localização, clima, etc.)
- Relações precisam ser bem definidas (chaves estrangeiras)
- Mais rígido e verboso para consultas

**NoSQL (MongoDB):**

- Permite documentos aninhados (subdocumentos dentro de cada acidente)
- Os dados que são usados juntos, ficam armazenados juntos
- Consultas mais diretas e flexíveis
- Ótimo para leitura rápida e análise exploratória

Esse modelo é ideal quando há acesso frequente a dados agrupados, como o contexto completo de um acidente.

---

### 🏁 Resultado final

**Banco:** `us_accidents_db`  
**Coleções:**

- `accidents`: registros completos de acidentes
- `airports`: metadados únicos de aeroportos

Agora você pode fazer queries, análises, dashboards ou integrações usando MongoDB com dados mais organizados e otimizados.
