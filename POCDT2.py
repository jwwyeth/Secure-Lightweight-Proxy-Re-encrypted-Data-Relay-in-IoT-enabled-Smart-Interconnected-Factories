from ECC import EllipticCurve
import random
import time
from sympy import mod_inverse
import socket
import pickle
import json
from ecdsa.ellipticcurve import PointJacobi
from ecdsa import SECP256k1
import hashlib

def dict_to_point(data):
    return PointJacobi(curve = SECP256k1.curve,x=data['x'], y=data['y'], z=data.get('z', 1))  # Default z to 1 if not provided


def point_to_dict(point):
    """Convert a PointJacobi object to a dictionary."""
    return {'x': point.x(), 'y': point.y()}  # Adjust based on the actual attributes of PointJacobi

def hash_data(*args):
        string=''.join(str(arg) for arg in args)
        return hashlib.sha512(string.encode()).hexdigest()


def setup():
    PORT=5050
    HEADER=64
    FORMAT='utf-8'
    SERVER=socket.gethostbyname(socket.gethostname())
    #print(socket.gethostbyname(socket.gethostname()))
    ADDR=(SERVER,PORT)

    machine=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    machine.connect(ADDR)
    print('Poc-DT_DST')

    

    # Convert the JSON string back to a Python dictionary
    TA_starterset=( json.loads(machine.recv(4096).decode('utf-8')))
    #print (TA_starterset)

    P=TA_starterset['P']
    P=dict_to_point(P)

    PK_DST=TA_starterset['PK_DST']
    PK_DST=dict_to_point(PK_DST)

    SK_DST=TA_starterset['SK_DST']
    q=TA_starterset['q']
    return P,PK_DST,SK_DST,q

def main():
    P,PK_DST,SK_DST,q=setup()


    print(f"\nPK_DST =\nx: {PK_DST.x()}\ny: {PK_DST.y()}")
    print(f"\nSK_DST =\n{SK_DST}")


    deltat=2
    ES_POCDT2_PORT=7070
    HEADER=64
    FORMAT='utf-8'
    SERVER=socket.gethostbyname(socket.gethostname())
    #print(socket.gethostbyname(socket.gethostname()))
    ADDR=(SERVER,ES_POCDT2_PORT)

    machine=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    machine.connect(ADDR)
    CProxy=( json.loads(machine.recv(4096).decode('utf-8')))
    print("\nReceived data from Edge Server")
    TDSTPROXY=time.time()
    CT_prime=CProxy['CT_prime']
    CT_prime=dict_to_point(CT_prime)    

    CM=CProxy['CM']
    CM=dict_to_point(CM) 
    hM=CProxy['hM']
    TProxy=CProxy['TPROXY']
    if((TDSTPROXY-TProxy)<deltat):
        print("\n|T_DST_PROXY - T_PROXY| is less than  Delta_T")

        print("\nDecrypting M ")
        decrypted_M=CM+(-1*(mod_inverse(SK_DST,q)*CT_prime))
        print(f"\nDecrypted M= \nx: {decrypted_M.x()}\ny: {decrypted_M.y()}\n")
    if (hash_data(decrypted_M.x(),decrypted_M.y())) ==hM:
        print(f"\nHashed value of decrypted M is equivalent to hM")





    

main()