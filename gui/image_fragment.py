#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ImageFragment:
    def __init__(self, fragment, row, column):
        self.fragment = fragment
        self.row = row
        self.column = column
        self.name = f"{row}_{column}"
