#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dearpygui.dearpygui as dpg
from gui.image_fragment import ImageFragment


class DragDrop:
    def __init__(self, group_textures, drag_drop_finished):
        self._drag_object = None
        self._drag_texture = None
        self.group_textures = group_textures
        self.drag_drop_finished = drag_drop_finished
        self.draggable_items = []

    def _drag_callback(self, sender):
        self._drag_object = sender
        self._drag_texture = dpg.get_item_configuration(sender)["texture_tag"]
        # print(f"Dragging from {dpg.get_item_configuration(sender)['user_data']}")

    def _drop_callback(self, sender):
        usr_data_tg: ImageFragment = dpg.get_item_configuration(sender)["user_data"]
        usr_data_src: ImageFragment = dpg.get_item_configuration(self._drag_object)["user_data"]
        print(
            f"Dropped from {self._drag_object} into {sender} src {usr_data_src}, dst {usr_data_tg}")
        dpg.configure_item(self._drag_object, texture_tag=dpg.get_item_configuration(sender)["texture_tag"],
                           user_data=usr_data_tg)
        dpg.configure_item(sender, texture_tag=self._drag_texture, user_data=usr_data_src)
        self.drag_drop_finished(self)

    def create_draggable_image(self, image_fragment: ImageFragment, width, height, image_tag, texture_tag, parent):
        if dpg.does_item_exist(parent):
            if not dpg.does_item_exist(texture_tag):
                with dpg.texture_registry():
                    texture_tag = dpg.add_static_texture(width, height, image_fragment.fragment, tag=texture_tag)

            if parent not in self.group_textures:
                self.group_textures[parent] = []
            self.group_textures[parent].append(texture_tag)

            # Add the image with drag and drop functionality
            img_btn = dpg.add_image_button(texture_tag, tag=image_tag,
                                           payload_type="image_payload",
                                           user_data=image_fragment,
                                           drag_callback=self._drag_callback,
                                           drop_callback=self._drop_callback)

            self.draggable_items.append(img_btn)
            with dpg.drag_payload(parent=img_btn, payload_type="image_payload"):
                dpg.add_text("Dragging...")  # This will be displayed during dragging
            return img_btn

        return None
