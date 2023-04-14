import argparse

from steganography.steganography import Steganography

from cryptography.fernet import Fernet

import io

from PIL import Image

import numpy as np

class ImageSteganography:

    def __init__(self, key=None):

        if key is None:

            key = Fernet.generate_key()

        self.key = key

        self.cipher = Fernet(key)

    def encrypt(self, data):

        return self.cipher.encrypt(data)

    def decrypt(self, data):

        return self.cipher.decrypt(data)

    def merge(self, image1_path, image2_path, output_path, secret_message):

        secret_message = self.encrypt(secret_message.encode())

        steganography = Steganography(image1_path)

        steganography.hide(output_path, secret_message, auto_convert_rgb=True)

        image1 = Image.open(image1_path).convert("RGBA")

        image2 = Image.open(image2_path).convert("RGBA")

        # Resize image2 to the size of image1

        image2 = image2.resize(image1.size)

        image2_arr = np.array(image2)

        # Extract the alpha channel from image1

        alpha = np.array(image1)[:, :, 3].reshape(image1.size[1], image1.size[0], 1)

        # Merge the alpha channel with image2

        image2_arr = np.concatenate((image2_arr, alpha), axis=2)

        merged_image = Image.fromarray(image2_arr, mode='RGBA')

        merged_image.save(output_path)

    def unmerge(self, image_path):

        steganography = Steganography(image_path)

        secret_message = steganography.retrieve(auto_convert_rgb=True)

        return self.decrypt(secret_message).decode()

def main():

    parser = argparse.ArgumentParser(description='Image Steganography')

    subparser = parser.add_subparsers(dest='command')

    merge = subparser.add_parser('merge')

    merge.add_argument('--image1', required=True, help='Image1 path')

    merge.add_argument('--image2', required=True, help='Image2 path')

    merge.add_argument('--output', required=True, help='Output path')

    merge.add_argument('--message', required=True, help='Secret message')

    unmerge = subparser.add_parser('unmerge')

    unmerge.add_argument('--image', required=True, help='Image path')

    args = parser.parse_args()

    steganography = ImageSteganography()

    if args.command == 'merge':

        steganography.merge(args.image1, args.image2, args.output, args.message)

        print(f"Image merged successfully with key: {steganography.key.decode()}")

    elif args.command == 'unmerge':

        message = steganography.unmerge(args.image)

        print(f"Secret message retrieved: {message}")

if __name__ == '__main__':

    main()

