from blockChain import Block, BlockChain
from time import time

MyBlockchain = BlockChain()
MyBlockchain.add_block(Block(time(), {'Name': 'Roman', 'Balance': 10000000000000}))
print(MyBlockchain)
print(MyBlockchain.is_valid())
