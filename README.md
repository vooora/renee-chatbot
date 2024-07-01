# Renee Medical Chatbot

<img width="1440" alt="image" src="https://github.com/srivantv/renee-chatbot/assets/126191857/37ae6e68-62ef-4f98-9b6d-f6fcc6c62646">

<img width="1434" alt="image" src="https://github.com/srivantv/renee-chatbot/assets/126191857/cf0c91fa-a072-4625-8e93-0cca05a3e46a">

# Follow the instructions in order to use the chatbot

Ensure you are using python 3.11 in order to run the chatbot

## Server

```
cd server
```
### Setting up

Create environment
```
python -m venv myenv
```
Activate Environment
```
source myenv/bin/activate
```
Install requirements
```
pip install -r requirements.txt
```
### Running server
1. Create vector database
```
python ingest.py
```
2. Run main
```
python main.py
```

## Client
Start another terminal and follow while letting your server run.

```
cd client
```
### Setting up

```
npm install
```

### Running client

```
npm start
```
