# Bitcoin

Implemented Bitcoin system with multi-transaction support which includes ensuring integrity of blocks(maintained using Merkle Trees), proof-of-work carried out by each node, digital signatures and the consensus protocol of Bitcoin. A node is implemented as a seperate thread and all nodes are assumed to be honest. Each node is assigned 5 wallets i.e. 5 pairs of <public key, private key>.

To run the code, type -
python3 Node.py


It prints out the log of transactions starting from the initial state of each node. All the transactions along with the state of all the nodes is printed upon addition of a new block to the blockchain. 
