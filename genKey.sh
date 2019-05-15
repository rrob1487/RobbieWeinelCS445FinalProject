#!/bin/bash
# Alice generates her private key
openssl ecparam -name secp256k1 -genkey -noout -out data_priv_key.pem &> /dev/null
# Alice extracts her public key from her private key
openssl ec -in data_priv_key.pem -pubout -out data_pub_key.pem &> /dev/null

#Generating Shared Symmetric Key
openssl pkeyutl -derive -inkey data_priv_key.pem -peerkey test_pub_key.pem -out data_shared_secret.bin &> /dev/null