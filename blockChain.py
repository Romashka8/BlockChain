import time
import json
from typing import Optional, Any
from hashlib import sha256


class Block:
    def __init__(self, timestamp: Optional[float] = None, data: Optional[Any] = None):
        self.index = 1
        self.previous_hash = None
        self.timestamp = timestamp or time.time()
        self.timestamp = str(self.timestamp)
        self.data = [] if data is None else data
        self.difficulty = 4
        # NONCE - number that can only be used once
        self.nonce = 0
        self.hash = self.get_hash()

    def __repr__(self):
        return json.dumps({'index': self.index, 'previous_hash': self.previous_hash,
                           'timestamp': self.timestamp, 'data': self.data,
                           'difficulty': self.difficulty, 'nonce': self.nonce,
                           'hash': self.hash})

    def get_hash(self) -> str:
        hashed = sha256()
        # sha256().update(data) - data must be bytes-like object
        # this is the reason why we use str().encode('utf-8')
        # str().encode('utf-8') -> bytes
        hashed.update(str(self.previous_hash).encode('utf-8'))
        hashed.update(str(self.timestamp).encode('utf-8'))
        hashed.update(str(self.data).encode('utf-8'))
        hashed.update(str(self.nonce).encode('utf-8'))
        return hashed.hexdigest()

    # 'Proof-of-work algorith realisation'
    def mine(self, difficulty: int):
        # while hash do not begin from two sign num
        # who has quantity of prime numbers <= num
        # quantity = difficulty * 2
        while Block().sieve_of_eratosthenes(int(self.hash[:2], 16)) != difficulty * 2:
            # getting new hash
            self.nonce += 1
            self.hash = self.get_hash()

    # count with sieve of Eratosthenes how much prime numbers(except 1) in numbers that <= num
    @staticmethod
    def sieve_of_eratosthenes(num):
        nums = [i for i in range(2, num)]
        for i in range(num - 2):
            if nums[i] != 0:
                j = i + nums[i]
                while j < len(nums):
                    nums[j] = 0
                    j += nums[i]
        return len(nums) - nums.count(0)


class BlockChain:
    def __init__(self):
        self.chain = [Block(time.time())]
        # mine even first block
        self.chain[0].mine(Block().difficulty)

    def __repr__(self) -> str:
        # for beautiful output
        return json.dumps([{'index': item.index, 'previous_hash': item.previous_hash,
                            'timestamp': item.timestamp, 'data': item.data,
                            'difficulty': item.difficulty, 'nonce': item.nonce,
                            'hash': item.hash} for item in self.chain])

    def get_last_block(self) -> Block:
        return self.chain[len(self.chain) - 1]

    def add_block(self, block: Block):
        block.previous_hash = self.get_last_block().hash
        # updating hash
        block.hash = block.get_hash()
        block.mine(Block().difficulty)
        block.index = len(self.chain) + 1
        self.chain.append(block)

    def is_valid(self) -> bool:
        # starting from 1 because we have no blocks before 0-indexed block
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # checking BlockChain hashes
            if current_block.hash != current_block.get_hash() or \
                    previous_block.hash != current_block.previous_hash:
                return False

        return True
