<<<<<<< HEAD
# Our Blockchain class is responsible for managing the chain. 
# It will store transactions and have some helper methods for adding new blocks to the chain. 
=======
    # Our Blockchain class is responsible for managing the chain. 
    # It will store transactions and have some helper methods for adding new blocks to the chain. 
>>>>>>> 9a2cabd645cbeaf23e15b67181e2148a391704c4


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

<<<<<<< HEAD
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
=======
>>>>>>> 9a2cabd645cbeaf23e15b67181e2148a391704c4
