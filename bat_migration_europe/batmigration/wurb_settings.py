#!/usr/bin/python3
# -*- coding:utf-8 -*-
#
# Copyright (c) 2022-present Arnold Andreasson
# License: MIT License (see LICENSE file or http://opensource.org/licenses/mit).

import pathlib
import logging


class WurbSettings:
    """ """

    def __init__(self):
        """ """
        self.logger = logging.getLogger("bat_migration")
        self.clear()

    def clear(self):
        """ """
        self.settings_dict = {}

    def get_settings_dict(self):
        """ """
        return self.settings_dict

    def get_value(self, key=""):
        """ """
        if key:
            value = self.settings_dict.get(key, "")
        return value

    def load_settings(self, directory_name=""):
        """ """
        self.clear()
        settings_path = pathlib.Path(directory_name, "wurb_rec_settings.txt")
        with settings_path.open("r") as file:
            rows = file.readlines()
        # Create dictionary.
        for row in rows:
            if "#" in row:
                parts = row.split("#")
                row = parts[0]
            if len(row) == 0:
                continue
            parts = row.split(":")
            key = parts[0].strip()
            value = parts[1].strip()
            if (len(key) > 0) and (len(value) > 0):
                self.settings_dict[key] = str(value)
