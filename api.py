# We’re going to use the Python Flask Framework. 
# It’s a micro-framework and it makes it easy to map endpoints to Python functions. 
# This allows us talk to our blockchain over the web using HTTP requests.
# We’ll create three methods:

#   /transactions/new - to create a new transaction to a block
#   /mine - to tell our server to mine a new block.
#   /chain - to return the full Blockchain

# Our server will form a single node in our blockchain network. 

from uuid import uuid4
from flask import Flask, jsonify
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
    return "We'll mine a new Block"
  
@app.route('/transactions/new', methods=['POST']) 
#Create the /transactions/new endpoint, which is a POST request, since we’ll be sending data to it
def new_transaction():
    return "We'll add a new transaction"

@app.route('/chain', methods=['GET'])
#Create the /chain endpoint, which returns the full Blockchain
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

# Runs the server on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
