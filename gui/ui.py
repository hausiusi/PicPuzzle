#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random

import dearpygui.dearpygui as dpg
from gui.image_tools import load_image, resize_image
from gui.drag_drop import DragDrop
from gui.image_fragment import ImageFragment
from PIL import Image

group_textures = {}  # Save all textures of the puzzle to delete them easily later
payload_buffer = ""  # Buffer to use in drag and drop. This is the drag object


# Callbacks
def resize_window():
    # Get viewport dimensions
    viewport_width = dpg.get_viewport_width()
    viewport_height = dpg.get_viewport_height()

    if dpg.get_item_info("PuzzleWindow") is not None:
        dpg.get_item_rect_size("PuzzleWindow")

        # Resize the window
        dpg.configure_item("PuzzleWindow", width=viewport_width, height=viewport_height - 30)
        dpg.get_item_rect_size("PuzzleWindow")


def on_start():
    resize_window()


def create_puzzle_callback(sender):
    print(f"Selected on {sender}. Creating the puzzle")
    create_puzzle(sender)


def delete_group_and_textures(group_tag):
    # Delete the group of image buttons
    if dpg.does_item_exist(group_tag):
        dpg.delete_item(group_tag)

    # Delete the textures related to the group
    if group_tag in group_textures:
        for texture in group_textures[group_tag]:
            if dpg.does_item_exist(texture):
                dpg.delete_item(texture)

        # Remove the group from the dictionary after deletion
        del group_textures[group_tag]


def create_clickable_image(image_data, width, height, image_tag, texture_tag):
    with dpg.texture_registry():
        texture_id = dpg.add_static_texture(width, height, image_data, tag=texture_tag)

    # Add the image with drag and drop functionality
    img_btn = dpg.add_image_button(texture_id, tag=image_tag, payload_type="image_payload",
                                   callback=create_puzzle_callback)
    return img_btn


def list_files_in_directory(directory):
    try:
        files = [os.path.join(directory, f) for f in os.listdir(directory) if
                 os.path.isfile(os.path.join(directory, f))]
        return files
    except FileNotFoundError:
        return None
    except Exception as e:
        return str(e)


def align_right(item, right_margin=20):
    # Get the item's width (assumes it's an image or widget where width is known)
    item_width = dpg.get_item_width(item)

    # Get the current window width (viewport or parent window size)
    viewport_width = dpg.get_viewport_width()

    # Calculate x position to align item to the right
    x_pos = viewport_width - item_width - right_margin

    # Set the item position with calculated x and fixed y position (for this example, y=50)
    dpg.set_item_pos(item, pos=(x_pos, 50))  # y-pos is set to 50 for this example


def create_choice_list():
    img_id = 0
    for file in list_files_in_directory("data/img"):
        print(file)
        img, w, h = load_image(file, True, 100, 100)
        created_img = create_clickable_image(img, w, h, f"{file}", f"ImageTexture{img_id}")
        dpg.set_item_pos(created_img, [670, 20 + 103 * img_id])
        img_id += 1


def check_solve_progress(dd: DragDrop):
    total = len(dd.draggable_items)
    matching = 0
    for item in dd.draggable_items:
        user_data: ImageFragment = dpg.get_item_user_data(item)
        pos = str(item).split('-')[1]
        if pos == user_data.name:
            matching += 1

    solved = matching / total
    print(f"{solved * 100}%")
    dpg.set_value("ProgressBar", solved)


def create_puzzle(sender):
    path = sender
    image = Image.open(path)
    # Get the dimensions of the image
    image_width, image_height = image.size

    # Define the number of rows and columns (3x3 grid)
    rows = 3
    cols = 3

    # Calculate the width and height of each segment
    segment_width = image_width // cols
    segment_height = image_height // rows

    delete_group_and_textures("PuzzleGroup")
    dd = DragDrop(group_textures, check_solve_progress)

    image_fragments = []
    with dpg.group(tag="PuzzleGroup", parent="PuzzleWindow"):
        for row in range(rows):
            for col in range(cols):
                # Calculate the cropping box for each part (left, upper, right, lower)
                left = row * segment_width
                upper = col * segment_height
                right = left + segment_width
                lower = upper + segment_height

                # Crop the image
                cropped_image = image.crop((left, upper, right, lower))
                cropped_image = resize_image(cropped_image, 100, 100)
                width, height = cropped_image.size
                # cropped_image.save(f"img{row}_{col}_{(left, upper, right, lower)}.jpg")
                cropped_image = cropped_image.convert("RGBA")
                image_data = list(cropped_image.getdata())  # Get pixel data
                image_data = [item / 255 for pixel in image_data for item in pixel]  # Normalize data to [0.0, 1.0]
                image_fragments.append(ImageFragment(image_data, row, col, (left, upper, right, lower)))
                random.shuffle(image_fragments)

        x, y = 0, 0
        for frag in image_fragments:
            created_img = dd.create_draggable_image(
                frag,
                width,
                height,
                f"PuzzleBox-{x}_{y}",
                f"PuzzleBoxTexture-{frag.name}",
                parent="PuzzleGroup")
            dpg.set_item_pos(created_img, [20 + width * x, 80 + height * y])

            if x < rows - 1:
                x += 1
            else:
                x = 0
                y += 1


def load_and_run():
    # Create Dear PyGui context
    dpg.create_context()

    print(f"DPG version {dpg.get_dearpygui_version()}")

    # Create a window
    with dpg.window(label="", tag="PuzzleWindow", width=400, height=300, no_close=True,
                    no_collapse=True):
        create_choice_list()

        dpg.add_progress_bar(label="Progress", tag="ProgressBar", width=300, default_value=0, pos=(30, 500))

    # Setup and show viewport
    dpg.create_viewport(title="Picture puzzle", width=800, height=600)
    dpg.set_viewport_resize_callback(resize_window)  # Auto-resize when viewport changes
    dpg.set_start_callback(on_start)  # Ensure window is resized on start

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()

    # Clean up
    dpg.destroy_context()
