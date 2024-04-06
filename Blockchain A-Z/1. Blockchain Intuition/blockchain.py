# -*- coding: utf-8 -*-
"""
Creating a Blockchain
"""
import datetime
import hashlib
import json
from flask import Flask, jsonify

class Blockchain:
    def __init__(self):
        self.chain=[]
        self.create_block(proof=1, previous_hash='0')
        
    def create_block(self,proof,previous_hash):
        block={ 'index': len(self.chain)+1,
               'timestamp': str(datetime.datetime.now()),
               'proof' : proof,
               'previous_hash' : previous_hash} 
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    
    def proof_of_work(self,previous_proof):
        new_proof=1
        check_proof=False
        while(check_proof is False):
            hash_value=hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_value[:4]=='0000':
                check_proof=True
            else:
                new_proof+=1
                
        return new_proof
            
    
    def hash(self,block):
        encoded_block=json.dumps(block).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        previous_block=chain[0]
        current_block_index=1
        while current_block_index<len(chain):
            current_block=chain[current_block_index]
            previous_hash=hash(previous_block)
            current_block_prev_hash=current_block['previous_hash']
            if(previous_hash!=current_block_prev_hash):
                return False
            
            previous_proof=previous_block['proof']
            current_prrof=current_block['proof']
            hash_value=hashlib.sha256(str(current_prrof**2 - previous_proof**2).encode()).hexdigest()
            if(hash_value[:4]!='0000'):
                return False
            previous_block=current_block
            current_block_index+=1
        return True
  
    
# Mining our Blockchain
# create a flask web app
app= Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
# create a blockchain object
blockchain=Blockchain() 

@app.route('/',methods=['GET'])
def hello_world():
    return 'hello world'

@app.route('/mine_block',methods=['GET'])
def mine_block():
    previous_block=blockchain.get_previous_block()
    previous_hash=blockchain.hash(previous_block)
    print(previous_hash)
    previous_proof=previous_block['proof']
    proof=blockchain.proof_of_work(previous_proof)
    block=blockchain.create_block(proof, previous_hash)
    print(block['previous_hash'])
    response={
        'message' : 'Congratulation you just mined one block!',
        'index' : block['index'],
        'timestamp' : block['timestamp'],
        'previous_hash': block['previous_hash'],
        'proof': block['proof']}
    return jsonify(response) , 200
 
@app.route('/get_chain',methods=['GET'])
def get_chain():
    response={
        'chain' : blockchain.chain,
        'length': len(blockchain.chain)}
    return jsonify(response) , 200

@app.route('/is_valid',methods=['GET'])
def is_valid():
    return blockchain.is_chain_valid(blockchain.chain),200

if __name__=="__main__":
    app.run(debug=True)