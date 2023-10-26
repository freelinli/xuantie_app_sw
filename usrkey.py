# !/usr/bin/env python3
from ecdsa import ECDH, NIST384p, BRAINPOOLP384r1
from ecdsa import SigningKey, NIST384p
from Crypto.Cipher import AES
import hashlib, hmac
# pip install pycryptodome==3.17
# pip install pycryptodome==0.18.0

class UsrKey:
    def __init__(self):
        self.ecdh = ECDH(curve=NIST384p)
        self.sign_data = [110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110,
            110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110,
            110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110,
            110, 110, 110, 110, 110,110, 110]
    def ecdsa_sign_data_set(self, sign_data):
        self.sign_data = sign_data
        print(f"Sign data = {[b  for b in self.sign_data]}")

    def ecdsa_key(self):
        sk = SigningKey.generate(curve=NIST384p)
        vk = sk.verifying_key
        private_key = sk.to_string()
        signature = sk.sign(bytes(self.sign_data))
        remote_public_key = vk.to_string()
        # print(f"Signing key = {[b for b in private_key]}")
        # print(f"Verifying key = {[b for b in remote_public_key]}")
        assert vk.verify(signature, bytes(self.sign_data))
        return [private_key, remote_public_key, signature]

    def ecdh_ver(self, private_key, remote_public_key):
        self.ecdh.load_private_key_bytes(bytes(private_key))
        self.ecdh.load_received_public_key_bytes(bytes(remote_public_key))
        share_secret = self.ecdh.generate_sharedsecret_bytes()
        print(f"shared secret = {[b  for b in share_secret]}")
        return share_secret

    def hmac_encode(self, key, data):
        h = hmac.new(bytes(key), bytes(data), hashlib.sha256)
        # print(h.hexdigest())
        return h.digest()

    def aes_encode(self, aeskey, data, iv = [x for x in range(0, 16)]):
        obj = AES.new(bytes(aeskey), AES.MODE_CBC, bytes(iv))
        encrytext = obj.encrypt(bytes(data))
        print(f"aes_encode = {[hex(b)   for b in encrytext]}")
        return encrytext

    def aes_decode(self, aeskey, data, iv = [x for x in range(0, 16)]):
        obj = AES.new(bytes(aeskey), AES.MODE_CBC, bytes(iv))
        decrytext = obj.decrypt(bytes(data))
        print(f"aes_decode  = {[hex(b)  for b in decrytext]}")
        return decrytext

if __name__ == "__main__":
    hmac_data = [110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110,
            110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110,
            110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110,
            110, 110, 110, 110, 110,110, 110]
    key = UsrKey()
    ecdsa1 = key.ecdsa_key()
    ecdsa2 = key.ecdsa_key()
    share_secret1 = key.ecdh_ver(ecdsa1[0], ecdsa2[1])
    share_secret2 = key.ecdh_ver(ecdsa2[0], ecdsa1[1])
    assert share_secret1 == share_secret2
    hmac_sign_data = key.hmac_encode(ecdsa1[0], hmac_data)
    aes_encode_data = key.aes_encode(ecdsa1[0][0:32], hmac_sign_data[0:32])
    aes_decode_data = key.aes_decode(ecdsa1[0][0:32], aes_encode_data[0:32])
    assert aes_decode_data[0:32] == hmac_sign_data[0:32]
