from ECC import EllipticCurve
import random
import time
from sympy import mod_inverse
import socket
import pickle
import json
from ecdsa.ellipticcurve import PointJacobi
from ecdsa import SECP256k1

def dict_to_point(data):
    return PointJacobi(curve = SECP256k1.curve,x=data['x'], y=data['y'], z=data.get('z', 1))  # Default z to 1 if not provided


def point_to_dict(point):
    """Convert a PointJacobi object to a dictionary."""
    return {'x': point.x(), 'y': point.y()}  # Adjust based on the actual attributes of PointJacobi


def setup():
    PORT=5050
    HEADER=64
    FORMAT='utf-8'
    SERVER=socket.gethostbyname(socket.gethostname())
    #print(socket.gethostbyname(socket.gethostname()))
    ADDR=(SERVER,PORT)

    machine=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    machine.connect(ADDR)
    print('Edge Server')
    


    # Convert the JSON string back to a Python dictionary
    TA_starterset=( json.loads(machine.recv(4096).decode('utf-8')))
    #print (TA_starterset)

    rk=TA_starterset['rk']
    rk_str=str(rk)

    print(f"\nrk_ORG_to_DST:\n",rk_str[:77],"\n",rk_str[77:])
    return rk
def main():
    rk=setup()
    deltat=2

    DT1_ES_PORT=8080
    HEADER=64
    FORMAT='utf-8'
    SERVER=socket.gethostbyname(socket.gethostname())
    #print(socket.gethostbyname(socket.gethostname()))
    ADDR=(SERVER,DT1_ES_PORT)

    machine=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    machine.connect(ADDR)

    

    CORG=( json.loads(machine.recv(4096).decode('utf-8')))
    print("\n Received data from PoC-DT1")
    TESORG=time.time()
    #print (CORG)


    CT=CORG['CT']
    CT=dict_to_point(CT)  
    CM=CORG['CM']
    CM=dict_to_point(CM)
    TORG=CORG['TORG']
    hM_str=str(CORG['hM'])
    if((TESORG-TORG)<deltat):
        print("\n|T_ES_ORG - T_ORG| is less than  Delta_T")
        port = 7070
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((socket.gethostbyname(socket.gethostname()), port))
        server.listen()

        conn, addr = server.accept()

        TPROXY=time.time()
        CT_prime=CT*rk
        CProxy={'CT_prime':point_to_dict(CT_prime),
                'CM':CORG['CM'],
                'hM':CORG['hM'],
                'TPROXY':TPROXY
        }
        print("\nCalculating CT'")

        print(f"\nCT' = \nx: {CT_prime.x()}\ny: {CT_prime.y()}")

        print(f"\nC_Proxy = (" )
        print(f"\n\tCT' = \n\tx: {CT_prime.x()}\n\ty: {CT_prime.y()}")

        print(f"\n\tCM = \n\tx: {CM.x()}\n\ty: {CM.y()}")
        print(f"\n\thM = \n\t",hM_str[:77],"\n\t",hM_str[77:],"\n\t)")

        print("\nSending C_PROXY and T_PROXY TO POCDT2")
        condensed=(json.dumps(CProxy)).encode('utf-8')
        conn.sendall(condensed)
        conn.close()

  
   

main()