# We’re going to use the Python Flask Framework. 
# It’s a micro-framework and it makes it easy to map endpoints to Python functions. 
# This allows us talk to our blockchain over the web using HTTP requests.
# We’ll create three methods:

#   /transactions/new - to create a new transaction to a block
#   /mine - to tell our server to mine a new block.
#   /chain - to return the full Blockchain

# Our server will form a single node in our blockchain network. 

from uuid import uuid4
from flask import Flask, jsonify, request
from blockchain import Blockchain

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node. Create a random name for our node
node_identifier = str(uuid4()).replace('-', '') 

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET']) 
# Create the /mine endpoint, which is a GET request
def mine():
    # Our mining endpoint is where the magic happens, and it’s easy. It has to do three things:
    #   - Calculate the Proof of Work
    #   - Reward the miner (us) by adding a transaction granting us 1 coin
    #   - Forge the new Block by adding it to the chain
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    #Note that the recipient of the mined block is the address of our node. 
    #And most of what we’ve done here is just interact with the methods on our Blockchain class. 
    #At this point, we’re done, and can start interacting with our blockchain.
    return jsonify(response), 200
  
@app.route('/transactions/new', methods=['POST']) 
#Create the /transactions/new endpoint, which is a POST request, since we’ll be sending data to it
def new_transaction():
    #Obtain data request
    values = request.get_json()
    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
#Create the /chain endpoint, which returns the full Blockchain
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

# Before we can implement a Consensus Algorithm, we need a way 
# to let a node know about neighbouring nodes on the network. 
# Each node on our network should keep a registry of other nodes on the network. 
# Thus, we’ll need some more endpoints:
#   - /nodes/register - to accept a list of new nodes in the form of URLs.
#   - /nodes/resolve - to implement our Consensus Algorithm,
#                      which resolves any conflicts—to ensure a node has the correct chain.
# Let’s register the two endpoints to our API, 
# one for adding neighbouring nodes and the another for resolving conflicts:
# At this point you can grab a different machine if you like, and spin up different nodes on your network. 
# Or spin up processes using different ports on the same machine. I spun up another node on my machine, 
# on a different port, and registered it with my current node. Thus, I have two nodes:
#   -   http://localhost:5000
#   -   http://localhost:5001

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

# Runs the server on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
