from ecdsa import SECP256k1
import random

class EllipticCurve:
    def __init__(self):
        self.curve = SECP256k1
        self.P = self.curve.generator  # Generator point
        self.q = self.curve.order

    

    def generate_keys(self):
        SK = random.randint(1, self.q - 1)
        PK = SK * self.P
        return SK, PK
    
    def get_P_q(self):
        return self.P, self.q