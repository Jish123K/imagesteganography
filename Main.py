import argparse

import base64

import io

import os

import random

from PIL import Image

from cryptography.fernet import Fernet

from pysteg import lsb

class Steganography:

    def __init__(self, key):

        self.key = key

        self.cipher_suite = Fernet(self.key)

    def _compress(self, data):

        """Compress data using gzip.

        :param data: Data to be compressed.

        :return: Compressed data.

        """

        import gzip

        compressed_data = io.BytesIO()

        with gzip.GzipFile(fileobj=compressed_data, mode='wb') as f:

            f.write(data)

        return compressed_data.getvalue()

    def _decompress(self, data):

        """Decompress data using gzip.

        :param data: Compressed data.

        :return: Decompressed data.

        """

        import gzip

        compressed_data = io.BytesIO(data)

        with gzip.GzipFile(fileobj=compressed_data, mode='rb') as f:

            decompressed_data = f.read()

        return decompressed_data

    def encrypt(self, data):

        """Encrypt data using AES.

        :param data: Data to be encrypted.

        :return: Encrypted data.

        """

        data_bytes = data.encode('utf-8')

        compressed_data = self._compress(data_bytes)

        encrypted_data = self.cipher_suite.encrypt(compressed_data)

        return encrypted_data

    def decrypt(self, data):

        """Decrypt data using AES.

        :param data: Encrypted data.

        :return: Decrypted data.

        """

        decompressed_data = self.cipher_suite.decrypt(data)

        data_bytes = self._decompress(decompressed_data)

        decrypted_data = data_bytes.decode('utf-8')

        return decrypted_data

    def merge(self, image1_path, image2_path, output_path):

        """Merge image2 into image1.

        :param image1_path: First image.

        :param image2_path: Second image.

        :param output_path: Output path for merged image.

        """

        image1 = Image.open(image1_path)

        image2 = Image.open(image2_path)

        if image2.size[0] > image1.size[0] or image2.size[1] > image1.size[1]:

            raise ValueError('Image 2 should be smaller than Image 1!')

        data = input("Enter message to hide: ")

        encrypted_data = self.encrypt(data)

        steg = lsb.hide(image1, encrypted_data)

        steg.save(output_path)

    def unmerge(self, image_path, output_path):

        """Unmerge an image.

        :param image_path: The input image.

        :param output_path: Output path for unmerged image.

        """

        image = Image.open(image_path)

        data = lsb.reveal(image)

        decrypted_data = self.decrypt(data)

        with open(output_path, 'wb') as f:

            f.write(decrypted_data)

def generate_key():

    """Generate a random encryption key."""

    return Fernet.generate_key()

def main():

    parser = argparse.ArgumentParser(description='Steganography')

    subparser = parser.add_subparsers(dest='command')

    merge = subparser.add_parser('merge')

    merge.add_argument('--image1', required=True, help='Image1 path')

    merge.add_argument('--image2', required=True, help='Image2 path')

    merge.add_argument('--output', required=True, help='Output path')

    extract = subparser.add_parser('extract')

    extract.add_argument('--image', required=True, help='Image path')

    extract.add_argument('--output', required=True, help='Output path')

    args = parser.parse_args()

    if args.command == 'merge':

        # Load images

        image1 = Image.open(args.image1)

        image2 = Image.open(args.image2)

        # Check if image2 is smaller than image1

        if image2.size[0] > image1.size[0] or image2.size[1] > image1.size[1]:

            raise ValueError('Image 2 should be smaller than Image 1!')

        # Get user input message

        message = input("Enter message to hide: ")

        # Encrypt message

        steg = Steganography(generate_key())

        encrypted_data = steg.encrypt(message)

        # Hide encrypted message in image1

        steg_image = lsb.hide(image1, encrypted_data)

        

        # Merge image2 and steganographic image

        merged_image = Image.new('RGB', (image1.size[0], image1.size[1] + image2.size[1]))

        merged_image.paste(steg_image, (0, 0))

        merged_image.paste(image2, (0, steg_image.size[1]))

        # Save merged image

        merged_image.save(args.output)

    elif args.command == 'extract':

        # Load image

        image = Image.open(args.image)

        # Extract steganographic data

        steg_data = lsb.reveal(image)

        # Decrypt steganographic data

        steg = Steganography(generate_key())

        decrypted_data = steg.decrypt(steg_data)

        # Write decrypted data to output file

        with open(args.output, 'w') as f:

            f.write(decrypted_data)


    
