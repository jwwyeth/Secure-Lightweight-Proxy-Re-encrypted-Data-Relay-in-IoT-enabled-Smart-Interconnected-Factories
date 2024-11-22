from ECC import EllipticCurve
import random
import time
from sympy import mod_inverse

def main():
    T_delta=2
    ec=EllipticCurve()
    SK_ORG,PK_ORG=ec.generate_keys()
    SK_DST,PK_DST=ec.generate_keys()
    rk=mod_inverse(SK_ORG,ec.q)*SK_DST
    #for visual use
    rk_str=str(rk)



    print(f"PK_ORG: \nx: {PK_ORG.x()}\ny: {PK_ORG.y()}")
    print(f"\nSK_ORG: {SK_ORG}")

    print(f"\nPK_DST: \nx: {PK_DST.x()}\ny: {PK_DST.y()}")
    print(f"\nSK_DST: {SK_DST}")

#POCDT1------------------------------------------
    r=random.randint(1,ec.q-1)
    TORG=time.time()
    m="hello world"
    M=ec.string_to_point(m)
    print(f"\nM: \nx: {M.x()}\ny: {M.y()}")

    CT=r*PK_ORG
    CM=r*ec.P+M
    print(f"\nCT: \nx: {CT.x()}\ny: {CT.y()}")

    print(f"\nCM: \nx: {CM.x()}\ny: {CM.y()}")
    print(f"\nSENDING TUPLE CORG AND TORG TO ES" )
#ES-----------------------------------------------

    TESORG=time.time()
    if(TESORG-TORG)<=T_delta:
        TPROXY=time.time()
        print(f"\nrk_ORG_TO_DST:\n",rk_str[:77],"\n",rk_str[77:])
        CT_prime=r*PK_ORG*rk
        CPROXY=(CT_prime,CM)
        print(f"\nCT_prime: \nx: {CT_prime.x()}\ny: {CT_prime.y()}")
        print("\nSENDING CPROXY tuple and TPROXY TO POCDT2")
        
#POCDT2-----------------------------------------
        TDSTPORXY=time.time()
    if(TDSTPORXY-TPROXY)<=T_delta:
        decrypted_M=CM+(-1*(mod_inverse(SK_DST,ec.q)*CT_prime))
        print(f"\nDecrypted M: \nx: {decrypted_M.x()}\ny: {decrypted_M.y()}\n")








main()