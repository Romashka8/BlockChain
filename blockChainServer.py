from fastapi import FastAPI
from typing import Optional, Any, Dict
from hashlib import sha256
from ast import literal_eval
import uvicorn
import requests

from blockChain import Block, BlockChain

app = FastAPI()
MyBlockChain = BlockChain()
peers_list = []


# studying example
def check_peer(key: str):
    key_hashed = sha256()
    key_hashed.update(key.encode('utf-8'))
    key = key_hashed.hexdigest()
    with open('key.txt', 'r') as file:
        key_orig = file.readline().strip()
        if key_orig == key:
            return True
    return False


def send_updates(message: str, data: Optional[Any]):
    for i in peers_list:
        requests.post(f'http://{i[0]}:{i[1]}/updates', json={'Message': message, 'data': data})


@app.get('/', tags=['tech'])
def navigate_route():
    return {'Message': 'Welcome on our API!'}


@app.get('/blocks', tags=['blocks'])
def blocks():
    return [block for block in MyBlockChain.chain]


@app.post('/mine_block', tags=['blocks'])
# Valid data format:
# {"data": {"Name": "Roman"}}
def mine_block(data: Dict[Any, Any]):
    if data:
        new_block = Block(data=literal_eval(str(data["data"])))
        MyBlockChain.add_block(new_block)
        send_updates('Block added', str(repr(new_block)))
        send_updates('Current BlockChain', str(MyBlockChain.chain))
        return new_block
    return MyBlockChain.chain


@app.get('/peers', tags=['peers'])
def peers():
    return peers_list


@app.post('/add_peer', tags=['peers'])
# data format is - {'key': str, 'peer_data': Optional[list] = None}
# ATTENTION! Better use pydantic schemas for this kind of purposes!
def add_peer(data: Dict[Any, Any]):
    if data['key'] == 'CLOSED' and data['peer_data'] in peers_list:
        peers_list.remove(data['peer_data'])
        send_updates('Peer left', data['peer_data'])
    if check_peer(data['key']):
        if data['peer_data']:
            send_updates('Peer connected', data['peer_data'])
            peers_list.append(data['peer_data'])
    return peers_list


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.0', port=8000)
