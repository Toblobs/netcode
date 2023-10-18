# Synergy Netcode Framework
# Hosted on @Toblobs GitHub

from .package_installer import install as get_package

get_package('cryptography')
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding

## Useful Websites:

# https://www.techtarget.com/searchsecurity/definition/RSA#:~:text=RSA%20is%20a%20type%20of,is%20used%20to%20decrypt%20it.
# https://en.wikipedia.org/wiki/Public-key_cryptography
# https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/

# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#signing
# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#verification

class Crypt:

    """
       <class '__main__.Crypt'>
       
       A class that uses the 'cryptography' library to perform simple assymmetric encryption
       and decryption on data that needs to be sent securely accross the network.

       Parameters:
       @self | Reference to this Crypt object.

       Instance Variables:
       self.private_key | The private key, which is kept secret, and used to decrypt messages.
       self.public_key | The public key, which others can use to encrypt messages.
       self.private_serialized | The private key serialized to bytes.
       self.public_serialized | The public key serialized to bytes.
       self.padding_method | The method of padding used that fills the data with other junk.
       self.algorithm | The algorithm used when encrypting and decrypting.
       self.max_length | The max length of the padding.
       
    """

    def __init__(self):

        self.private_key = None
        self.public_key = None

        self.private_serialized = None
        self.public_serialized = None
        
        self.padding_method = padding.MGF1(algorithm = hashes.SHA256())
        self.algorithm = hashes.SHA256()

        self.max_length = padding.PSS.MAX_LENGTH


    def create_keys(self):

        """Creates the keys for this Crypt object using the instance variables padding_method
           and algorithm."""

        self.private_key = rsa.generate_private_key(public_exponent = 65537,
                                                    key_size = 2048,
                                                    backend = default_backend())

        self.public_key = self.private_key.public_key()

        self.private_serialized = self.private_key.private_bytes(encoding = serialization.Encoding.PEM,
                                                                 format = serialization.PrivateFormat.PKCS8,
                                                                 encryption_algorithm = serialization.NoEncryption())

        self.public_serialized = self.public_key.public_bytes(encoding = serialization.Encoding.PEM,
                                                              format = serialization.PublicFormat.SubjectPublicKeyInfo)
                                    

    def encrypt_message(self, plain:bytes, pu_key):

        """Encrypts some plaintext, using our instance variables.

           Parameters:
           @plain | The plain text that we want to encrypt. Must be bytes.
           @pu_key | The public key supplied from source."""

        ciphertext = pu_key.encrypt(plain, padding.OAEP(mgf = self.padding_method,
                                                        algorithm = self.algorithm,
                                                        label = None))

        return ciphertext

    def decrypt_message(self, cipher:bytes):

        """Encrypts some plaintext, using our instance variables.

           Parameters:
           @cipher | The cipher text that we want to decrypt. Must be bytes."""

        plaintext = self.private_key.decrypt(cipher, padding.OAEP(mgf = self.padding_method,
                                                                  algorithm = self.algorithm,
                                                                  label = None))

        return plaintext


    def deserialize_pu_key(self, pu_key):

        """Docs to be added."""

        return serialization.load_pem_public_key(pu_key, backend = default_backend) 
        
    def create_signature(self, message:bytes):

        """Creates the signature for a message using the instance varibales padding_method
           and algorithm.

           Paramters:
           @message | The message we want to sign. Must be bytes."""

        signature = self.private_key.sign(message, padding.PSS(self.padding_method,
                                         salt_length = self.max_length), self.algorithm)

        return signature


    def verify_signature(self, plain:bytes, signature, pu_key):

        """Verifies the identity of a signature on a message, using our instance variables.

           Parameters:
           @plain | The plain text supplied from the source we are checking. Must be bytes.
           @signature | The signature supplied from the source we are checking.
           @pu_key | The public key supplied from source."""

        try:

            pu_key.verify(signature,
                          plain,
                          padding.PSS(mgf = self.padding_method, salt_length = self.max_length),
                          self.algorithm)

            return True 

        except InvalidSignature:

            return False

    
    def setup(self):

        """Setup method, used by other objects."""

        self.create_keys()

    
### Example

#c = Crypt()
#c.setup()

#d = Crypt()
#d.setup()

#mess = b'This, my friends, is an encrypted message.'

# We want to send message from C -> D
# C encrypts using D's public key and then D decrypts using their private key

#encrypted = c.encrypt_message(plain = mess, pu_key = d.public_key)
#plainbytes = d.decrypt_message(encrypted)


#print(encrypted)
#print(plainbytes)















        

    
