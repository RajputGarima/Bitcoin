# Bitcoin


Implemented a bitcoin system with 'n' number of nodes where 'n' is adjustable. There are 'n' independent threads in the system and the network between these nodes is assumed to be fully connected. A node can perform any number of transactions and the node that wins in the **proof-of-work** and satisfies **consensus requirements** finally gets to create a block which is added to the immutable block chain. <br />

To maintain integrity of the blocks, **Merkle tree** of all the transactions present in the block is created. The tree stores hash pointers at each level. A block also stores hash pointer of the previous block in the chain. This ensures any tampering with a transaction or a block leads to disturbance in the hash values along the complete chain which can not go undetected. <br />

Each node is given 5 wallets i.e. 5 pairs of *<publicKey, privateKey>* to give **Multi-Transaction support.** 


There is a config file *(config.py)* that allows adjusting the hyper-parameters of the Blockchain like number of nodes in the network, arity of Merkle tree, Nonce size, Hash size etc. <br />

To run the code, type - <br />
> python3 Node.py

It prints out the log of transactions starting from the initial state of each node. All the transactions along with the state of all the nodes is printed upon addition of a new block to the blockchain. <br />

The code runs infinitely as a bitcoin system is supposed to do. Random transactions would keep taking place and the nodes winning hash puzzle will keep on adding blocks to the block chain. To view the logs after addition of 1-2 blocks in the block chain, force quit the program *"Ctrl + C"* after 2 minutes of execution. 



Refer to REPORT.pdf for detailed implementation.
