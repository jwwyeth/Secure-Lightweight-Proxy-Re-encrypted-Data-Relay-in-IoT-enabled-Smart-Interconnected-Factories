from ECC import EllipticCurve 
from sympy import mod_inverse
import json
import socket

def point_to_dict(point):
    """Convert a PointJacobi object to a dictionary."""
    return {'x': point.x(), 'y': point.y()}  # Adjust based on the actual attributes of PointJacobi


def main():

    port = 5050
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((socket.gethostbyname(socket.gethostname()), port))
    server.listen()


    T_delta=2
    ec=EllipticCurve()
    SK_ORG,PK_ORG=ec.generate_keys()
    SK_DST,PK_DST=ec.generate_keys()
    rk=mod_inverse(SK_ORG,ec.q)*SK_DST
    P,q=ec.get_P_q()
    #print(P)

#POCDT1
    conn, addr = server.accept()
    POCDT1_TUPLE={'P':point_to_dict(P),
                  'q':q,
                  'PK_ORG':point_to_dict(PK_ORG),
                  'SK_ORG':SK_ORG}
    
    print(POCDT1_TUPLE)
    condensed=(json.dumps(POCDT1_TUPLE)).encode('utf-8')
    conn.sendall(condensed)
    conn.close()


    #ES
    conn, addr = server.accept()
    ES_TUPLE={'rk':rk }
    
    print(ES_TUPLE)
    condensed=(json.dumps(ES_TUPLE)).encode('utf-8')
    conn.sendall(condensed)
    conn.close()

#POCDT2
    conn, addr = server.accept()
    POCDT2_TUPLE={'P':point_to_dict(P),
                  'q':q,
                  'PK_DST':point_to_dict(PK_DST),
                  'SK_DST':SK_DST}
    
    print(POCDT2_TUPLE)
    condensed=(json.dumps(POCDT2_TUPLE)).encode('utf-8')
    conn.sendall(condensed)
    conn.close()


    



main()