from flask import jsonify

from app import app
from app.bc import BlockChain

blockchain = BlockChain()


@app.route('/', methods=['GET'])
def index():
    return jsonify(
            message='Lista de rotas disponiveis:',
            routes={
                    'route1': 'http://127.0.0.1:8000/mine-block',
                    'route2': 'http://127.0.0.1:8000/get-chain',
                    'route3': 'http://127.0.0.1:8000/validate-chain'
            }
    )


@app.route('/mine-block', methods=['GET'])
def mine():
    previous_block = blockchain.previous_block
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.get_hash(previous_block)
    block = blockchain.criar_block(proof, previous_hash)

    return jsonify(
            index=block['index'],
            proof=block['proof'],
            message='Um bloco foi minado',
            timestamp=block['timestamp'],
            previous_hash=block['previous_hash']
    )


@app.route('/get-chain', methods=['GET'])
def get_chain():
    return jsonify(
            chain=blockchain.chain,
            lenght=blockchain.chain_length
    )


@app.route('/validate-chain', methods=['GET'])
def validate_chain():
    valid = blockchain.chain_valid(blockchain.chain)

    if valid:
        return jsonify(message='BlockChain valido.')
    else:
        return jsonify(message='BlockChain invalido.')
