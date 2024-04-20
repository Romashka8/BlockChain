import json
from fastapi import FastAPI
from typing import Any, Dict
from colorama import init
from colorama import Fore, Style
import requests
import sys
import os

app = FastAPI()
# initialize colorama for color terminal output
init(autoreset=True)


@app.get('/', tags=['tech'])
def navigate_route():
    return {'Message': 'Welcome on our API!'}


# send updates on this url
@app.post('/updates', tags=['tech'])
def updates(data: Dict[Any, Any]):
    print(Fore.GREEN + data['Message'].upper() + ':')
    if data['Message'] == 'Current BlockChain':
        blocks = json.loads(f"{data['data']}")
        [print(i) for i in blocks]
    elif data['Message'] == 'Peer connected':
        print(data['data'])
        print(Fore.GREEN + 'ALL PEERS IN NET:')
        curr_peers = requests.get('http://127.0.0.0:8000/peers').json()
        curr_peers.append(data['data'])
        [print(i) for i in curr_peers]
    elif data['Message'] == 'Peer left':
        print(data['data'])
        print(Fore.GREEN + 'ALL PEERS IN NET:')
        curr_peers = requests.get('http://127.0.0.0:8000/peers').json()
        [print(i) for i in curr_peers]
    else:
        print(data['data'])
    return data


# example CORRECT json data:
# {"Name": "Roman"}
@app.post('/mine_block', tags=['blocks'])
def mine_block(data: Any):
    requests.post(f'http://127.0.0.0:8000/mine_block', json={'data': data})
    return data


if __name__ == '__main__':
    # 127.0.0.1, 8001 - for example
    host, port = sys.argv[1], int(sys.argv[2])
    print(Fore.GREEN + 'INFO:    ', 'Uvicorn running on',
          Style.DIM + Fore.CYAN + f'http://{host}:{port}',
          '(Press CTRL+C to quit)')
    print(Fore.GREEN + 'CURRENT BLOCKCHAIN:')
    [print(i) for i in requests.get('http://127.0.0.0:8000/blocks').json()]
    requests.post('http://127.0.0.0:8000/add_peer', json={'key': 'simple_key', 'peer_data': [host, port]})
    # running server through terminal
    # --log-level critical - hide all uvicorn logs
    os.system(f'uvicorn clientServer:app --host {host} --port {port} --log-level critical')
    requests.post('http://127.0.0.0:8000/add_peer', json={'key': 'CLOSED', 'peer_data': [host, port]})
