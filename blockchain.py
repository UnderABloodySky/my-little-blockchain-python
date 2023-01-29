import hashlib
import json
from time import time
import requests
from urllib.parse import urlparse

# Our Blockchain class is responsible for managing the chain. 
# It will store transactions and have some helper methods for adding new blocks to the chain. 
class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # Create the genesis block
        self.nodes = set()
        self.new_block(previous_hash=1, proof=100)

    # After new_transaction() adds a transaction to the list.
    # It returns the index of the block which the transaction will be added to—the next one to be mined. 
    # This will be useful later on, to the user submitting the transaction.

    def new_transaction(self, sender, recipient, amount):
        
        #Creates a new transaction to go into the next mined Block
        # :param sender: <str> Address of the Sender
        # :param recipient: <str> Address of the Recipient
        # :param amount: <int> Amount
        # :return: <int> The index of the Block that will hold this transaction

        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        }

        self.current_transactions.append(transaction)
        return self.last_block['index'] + 1
    
    # When our Blockchain is instantiated we’ll need to seed it with a genesis block—a block with no predecessors. 
    # We’ll also need to add a “proof” to our genesis block which is the result of mining (or proof of work). 
    # In addition to creating the genesis block in our constructor, we’ll also flesh out the methods for new_block(), new_transaction() and hash()

    def new_block(self, proof, previous_hash=None):
        # Create a new Block in the Blockchain
        # param proof: <int> The proof given by the Proof of Work algorithm
        # param previous_hash: (Optional) <str> Hash of previous Block
        # return: <dict> New Block
        
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        # Creates a SHA-256 hash of a Block
        # param block: <dict> Block
        # return: <str>
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
# Understanding Proof of Work: A Proof of Work algorithm (PoW) is how new Blocks are created or mined on the blockchain. 
# The goal of PoW is to discover a number which solves a problem. The number must be difficult to find but easy to verify—computationally speaking—by anyone on the network. 
# This is the core idea behind Proof of Work.
# A Proof of Work algorithm (PoW) is how new Blocks are created or mined on the blockchain. 
# The goal of PoW is to discover a number which solves a problem. 
# The number must be difficult to find but easy to verify—computationally speaking—by anyone on the network. 
# This is the core idea behind Proof of Work.
# Let’s implement a similar algorithm for our blockchain. Our rule will be similar to the example above:

#      <  Find a number p that when hashed with the previous block’s solution a hash with 4 leading 0s is produced.  >

    def proof_of_work(self, last_proof):
        # Simple Proof of Work Algorithm:
        #  - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
        #  - p is the previous proof, and p' is the new proof
        #  :param last_proof: <int>
        #  return: <int>
        
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        # Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        # :param last_proof: <int> Previous Proof
        # :param proof: <int> Current Proof
        #:return: <bool> True if correct, False if not.
        
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


    # We’ve got a basic Blockchain that accepts transactions and allows us to mine new Blocks. 
    # But the whole point of Blockchains is that they should be decentralized. 
    # And if they’re decentralized, how on earth do we ensure that they all reflect the same chain? 
    # This is called the problem of Consensus, and we’ll have to implement a Consensus Algorithm 
    # if we want more than one node in our network.
    # Before we can implement a Consensus Algorithm, we need a way to let a node know about neighbouring nodes on the network. 
    # Each node on our network should keep a registry of other nodes on the network. 
    # We’ll need to modify our Blockchain’s constructor and provide a method for registering nodes:
    
    def register_node(self, address):
        # Add a new node to the list of nodes
        #   :param address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
        #   :return: None
        
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        # This method is responsible for checking if a chain is valid by looping through each block 
        # and verifying both the hash and the proof.
        # Determine if a given blockchain is valid
        #   :param chain: <list> A blockchain
        #   :return: <bool> True if valid, False if not
        
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        # This is a method which loops through all our neighbouring nodes, 
        # downloads their chains and verifies them using the above method. 
        # If a valid chain is found, whose length is greater than ours, we replace ours.
        # This is our Consensus Algorithm, it resolves conflicts
        # y replacing our chain with the longest one in the network.
        #    :return: <bool> True if our chain was replaced, False if not

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False