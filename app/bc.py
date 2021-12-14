import datetime
import hashlib
import json


class BlockChain:
    def __init__(self):
        self.chain = []
        self.criar_block(proof=1, previous_hash='0')

    @property
    def previous_block(self):
        return self.chain[-1]

    @property
    def chain_length(self):
        return len(self.chain)

    def criar_block(self, proof: int, previous_hash: str):
        block = {
                'index': len(self.chain) + 1,
                'timestamp': str(datetime.datetime.today()),
                'proof': proof,
                'previous_hash': previous_hash
        }
        self.chain.append(block)
        return block

    def proof_of_work(self, previous_proof: int):
        new_proof = 1
        check_proof = False

        while not check_proof:
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == '00000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]

            if block['previous_hash'] != self.get_hash(block=previous_block):
                return False

            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2-previous_proof**2).encode()).hexdigest()

            if hash_operation[:4] == '00000':
                return False

            previous_block = block
            block_index += 1
        return True

    def get_hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
