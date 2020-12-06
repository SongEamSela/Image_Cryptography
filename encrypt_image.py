# Import image processing standard library
from PIL import Image
# Import the pycrypto library, reference the aes encryption module, need to be installed through the pip command under cmd (installation is more troublesome)
from Crypto.Cipher import AES
import random
import string

# Randomly generate 16 strings composed of lowercase letters
def key_generator(size=16, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


filename = "input.jpg"

# Using a function to randomly generate a string of lowercase letters
# key = key_generator(16)
key = bytes("abc123456789qwer", 'utf-8')
iv = bytes("abc987654321qwer", 'utf-8')
print(key)
# AES encrypted plaintext space is an integer multiple of 16, which cannot be divided evenly, so it needs to be filled
# In the corresponding ascii, "\x00" means 0x00, the specific value is NULL, b means that it is expressed in bytes
def pad(data):
    return data + b"\x00" * (16 - len(data) % 16)


# Map the image data to RGB
def trans_format_RGB(data):
    # tuple: Immutable, ensure that data is not lost
    red, green, blue = tuple(map(lambda e: [data[i] for i in range(0, len(data)) if i % 3 == e], [0, 1, 2]))
    pixels = tuple(zip(red, green, blue))
    # print(pixels)
    return pixels

def encrypt_image_cbc(filename):
    # Open the bmp picture and convert it to RGB image
    im = Image.open(filename)
    value_vector = im.convert("RGB").tobytes()

    # Convert image data to pixel value bytes
    imlength = len(value_vector)

    # Perform pixel value mapping on the filled and encrypted data
    value_encrypt = trans_format_RGB(aes_cbc_encrypt(key, pad(value_vector))[:imlength])

    # Create a new object, store the corresponding value
    im2 = Image.new(im.mode, im.size)
    im2.putdata(value_encrypt)

    # Save the object as an image in the corresponding format
    # im2.save(filename_encrypted_cbc + "." + format, format)
    im2.save('enc_cbc.jpg')


# CBC encryption
def aes_cbc_encrypt(key, data, mode=AES.MODE_CBC):
    # IV is a random value
    # IV = bytes(key_generator(16), 'utf-8')
    IV= iv
    # IV = key_generator(16)
    aes = AES.new(key, mode, IV)
    new_data = aes.encrypt(data)
    return new_data

encrypt_image_cbc(filename)