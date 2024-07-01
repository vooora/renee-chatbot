# Renee Medical Chatbot

<img width="1440" alt="image" src="https://github.com/srivantv/renee-chatbot/assets/126191857/37ae6e68-62ef-4f98-9b6d-f6fcc6c62646">

<img width="1434" alt="image" src="https://github.com/srivantv/renee-chatbot/assets/126191857/cf0c91fa-a072-4625-8e93-0cca05a3e46a">

# Instructions

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
### Setting up .env file
Add your open ai api key to the .env file as given. 
```
OPENAI_API_KEY=you_openai_api_key
```
Change the model accordingly in the .env file
```
MODEL_NAME=your_model_name
```

### Running server
Create vector database
```
python ingest.py
```
Run main
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
