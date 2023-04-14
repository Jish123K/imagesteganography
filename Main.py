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

    merge.add_argument
('--image2', required=True, help='Image2 path')
extract = subparser.add_parser('extract')

extract.add_argument('--image', required=True, help='Image path')

extract.add_argument('--output', required=True, help='Output path')

args = parser.parse_args()

if args.command == 'merge':

    img1 = cv2.imread(args.image1)

    img2 = cv2.imread(args.image2)

    # Convert the images to grayscale

    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Resize the images to have the same shape

    img1_resized = cv2.resize(img1_gray, img2_gray.shape[::-1])

    img2_resized = img2_gray

    # Merge the images

    merged_image = merge_images(img1_resized, img2_resized)

    # Save the merged image

    cv2.imwrite(args.output, merged_image)

elif args.command == 'extract':

    img = cv2.imread(args.image)

    # Convert the image to grayscale

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Extract the hidden image

    extracted_image = extract_image(img_gray)

    # Save the extracted image

    cv2.imwrite(args.output, extracted_image)


merge.add_argument('--output', required=True, help='Output path')
