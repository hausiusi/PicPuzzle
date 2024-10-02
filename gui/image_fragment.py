#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ImageFragment:
    def __init__(self, fragment, row, column, dims):
        self.fragment = fragment
        self.row = row
        self.column = column
        self.dims = dims
        self.name = f"{row}_{column}"

    def __str__(self):
        return f"POS:({self.name}) DIMS:{self.dims}"
