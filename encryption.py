from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
import base64

print ("To generate private key and public key")

random_generator = Random.new().read

rsa = RSA.generate(1024,random_generator)

private_pem = rsa.exportKey()
print(type(private_pem))
with open('master-private.pem','w') as f:
	f.write(private_pem.decode())

public_pem = rsa.publickey().exportKey()
with open('master-public.pem','w') as f:
	f.write(public_pem.decode())

print (private_pem)

print (public_pem)

print ("2 encrypto and decrypto")

message = 'hello ghost, this is a plian text'

print ("message: " + message)

#encryto
with open('master-public.pem') as f:
    key = f.read()
    print(bytes(key,'utf-8'))
    rsakey = RSA.importKey(key.encode())
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(message.encode()))
    print ("encrypt:")
    print (cipher_text)

#decryto
with open('master-private.pem') as f:
    key = f.read()
    rsakey = RSA.importKey(key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    text = cipher.decrypt(base64.b64decode(cipher_text), random_generator)

    print ("decrypt:")
    print ("message:" + text)

    assert text == message, 'decrypt falied'

#signature and verification
print ("3 signature and verification")

# signature
print ("signature")
with open('master-private.pem') as f:
    key = f.read()
    rsakey = RSA.importKey(key)
    signer = Signature_pkcs1_v1_5.new(rsakey)
    digest = SHA.new()
    digest.update(message)
    sign = signer.sign(digest)
    signature = base64.b64encode(sign)

print (signature)

print ("verfication")
with open('master-public.pem') as f:
    key = f.read()
    rsakey = RSA.importKey(key)
    verifier = Signature_pkcs1_v1_5.new(rsakey)
    digest = SHA.new()
    # Assumes the data is base64 encoded to begin with
    digest.update(message)
    is_verify = verifier.verify(digest, base64.b64decode(signature))

print (is_verify)
