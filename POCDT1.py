import random
import time
import socket
import json
from ecdsa.ellipticcurve import PointJacobi
from ecdsa import SECP256k1
import hashlib



def dict_to_point(data):
    return PointJacobi(curve = SECP256k1.curve,x=data['x'], y=data['y'], z=data.get('z', 1))  # Default z to 1 if not provided

def point_to_dict(point):
    """Convert a PointJacobi object to a dictionary."""
    return {'x': point.x(), 'y': point.y()} 


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
    print('PoC-DT_Org')

    

    # Convert the JSON string back to a Python dictionary
    TA_starterset=( json.loads(machine.recv(4096).decode('utf-8')))
    #print(TA_starterset)
    P=TA_starterset['P']
    P=dict_to_point(P)

    PK_ORG=TA_starterset['PK_ORG']
    PK_ORG=dict_to_point(PK_ORG)

    SK_ORG=TA_starterset['SK_ORG']
    q=TA_starterset['q']

    return P,PK_ORG,SK_ORG,q


def string_to_point(m_str,P,q):
        # Convert the string to bytes
        byte_str = m_str.encode()
        
        # Convert bytes to an integer
        point_int = int.from_bytes(byte_str, byteorder='big')
        
        # Use modulo to get a number in the range of the curve order
        point_int = point_int % q

        # Generate the point on the curve
        point = point_int * P
        return point


def main():
    P,PK_ORG,SK_ORG,q=setup()
    print(f"\nPK_ORG = \nx: {PK_ORG.x()}\ny: {PK_ORG.y()}")
    print(f"\nsk_ORG = \n{SK_ORG}")
    deltat=2
    r=random.randint(1,q-1)
    TORG=time.time()
    m="hello world"
    M=string_to_point(m,P,q)
    print('\nEncoding m as a point M on curve E')
    print('\nChoosing random secret and taking timestamp T_ORG')

    hM=hash_data(M.x(),M.y())
    CT=r*PK_ORG
    CM=r*P+M
    print('\nHashing M to calculate value hM')
    print('\nCalculating CT')
    print('\nCalculating CM')


    ''' 
    print(f"\nM = \nx: {M.x()}\ny: {M.y()}")
    print(f"\nCT = \nx: {CT.x()}\ny: {CT.y()}")

    print(f"\nCM = \nx: {CM.x()}\ny: {CM.y()}")
    '''
    print(f"\nC_Org = (" )
    print(f"\n\tCT = \n\tx: {CT.x()}\n\ty: {CT.y()}")

    print(f"\n\tCM = \n\tx: {CM.x()}\n\ty: {CM.y()}")
    hM_str=str(hM)
    print(f"\n\thM = \n\t",hM_str[:77],"\n\t",hM_str[77:],"\n\t)")


    port = 8080
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((socket.gethostbyname(socket.gethostname()), port))
    server.listen()

    conn, addr = server.accept()

    CORG_TUPLE={'CT':point_to_dict(CT),
                'CM':point_to_dict(CM),
                "hM":hM,
                'TORG':TORG}
    
    condensed=(json.dumps(CORG_TUPLE)).encode('utf-8')
    conn.sendall(condensed)
    conn.close()
    print('\nSending C_Org, T_ORG to Edge Server')


main()