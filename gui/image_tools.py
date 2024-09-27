#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PIL import Image


def resize_image(image: Image, max_width, max_height):
    """Resize the image to fit within the specified dimensions while maintaining aspect ratio."""
    width, height = image.size
    aspect_ratio = width / height

    if width > max_width:
        width = max_width
        height = int(width / aspect_ratio)
    if height > max_height:
        height = max_height
        width = int(height * aspect_ratio)

    return image.resize((width, height))


def load_image(image_path: str, normalize: bool, max_width=0, max_height=0):
    image = Image.open(image_path).convert('RGBA')  # Ensure the image is in RGBA format
    if max_width > 0 and max_height > 0:
        image = resize_image(image, max_width, max_height)
    width, height = image.size

    if not normalize:
        return image, width, height

    # Step 2: Convert image to a list of floats (normalized between 0.0 and 1.0)
    image_data = list(image.getdata())  # Get pixel data
    image_data = [item / 255 for pixel in image_data for item in pixel]  # Normalize data to [0.0, 1.0]
    return image_data, width, height
