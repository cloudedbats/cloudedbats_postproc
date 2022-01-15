#!/usr/bin/python3
# -*- coding:utf-8 -*-
#
# Copyright (c) 2022-present Arnold Andreasson
# License: MIT License (see LICENSE file or http://opensource.org/licenses/mit).

import pathlib
import yaml
import logging
import batmigration


class BatMigrationEvents:
    """ """

    def __init__(self):
        """ """
        self.clear()

    def clear(self):
        """ """
        self.sampling_night_dir = ""
        self.sampling_nights_list = []
        self.static_metadata = {}

    def get_static_metadata(self):
        """ """
        return self.static_metadata

    def load_config(self, config_file):
        """ """
        # Load config from yaml-file.
        config_path = pathlib.Path(config_file)
        with open(config_path) as file:
            self.metadata_config = yaml.load(file, Loader=yaml.FullLoader)

        # Load "staticMetadata".
        self.static_metadata = self.metadata_config.get("staticMetadata", {})



        # For test.
        self.sampling_night_dir = (
            "/Users/arnold/Documents/bats2022/se-o-1_2021/Furulund_2021-05-30"
        )



    def scan_directories(self):
        """ """
        settings = batmigration.WurbSettings()
        settings.load_settings(self.sampling_night_dir)
        settings_dict = settings.get_settings_dict()
        self.sampling_nights_list.append(settings_dict)

        # Dummy metadata.
        settings_dict["monitoring_site_name"] = "Furulund-1"
        settings_dict["monitoring_event"] = "Furulund-1_2021-06-01"
        settings_dict["event_start_date"] = "2021-06-01"
        settings_dict["event_end_date"] = "2021-06-01"
        settings_dict["event_start_time"] = "20:10"
        settings_dict["event_end_time"] = "05:30"
        # Translate.
        settings_dict["decimal_latitude"] = settings_dict.get("latitude_dd","")
        settings_dict["decimal_longitude"] = settings_dict.get("longitude_dd","")

        # Merge directories.
        for key, value in self.static_metadata.items():
            settings_dict[key] = str(value)
