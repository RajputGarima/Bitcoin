# Bitcoin

Implemented Bitcoin system with multi-transaction support which includes ensuring integrity of blocks(maintained using Merkle Trees), proof-of-work carried out by each node, digital signatures and the consensus protocol of Bitcoin. A node is implemented as a seperate thread and all nodes are assumed to be honest. Each node is assigned 5 wallets i.e. 5 pairs of <public key, private key>. <br />

There is a config file where the number of nodes to be present in the network can be chosen. You can also specify the arity of Merkle Tree, Nonce Size, Hash size and some more parameters of blockchain. <br />

To run the code, type - <br />
python3 Node.py


It prints out the log of transactions starting from the initial state of each node. All the transactions along with the state of all the nodes is printed upon addition of a new block to the blockchain. 
