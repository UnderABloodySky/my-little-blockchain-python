import hashlib
import json
from time import time

# Our Blockchain class is responsible for managing the chain. 
# It will store transactions and have some helper methods for adding new blocks to the chain. 
class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        
    def new_block(self):
        # Creates a new Block and adds it to the chain
        pass
    
    def new_transaction(self):
        # Adds a new transaction to the list of transactions
        pass
    
    @staticmethod
    def hash(block):
        # Hashes a Block
        pass

    @property
    def last_block(self):
        # Returns the last Block in the chain
        pass

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





