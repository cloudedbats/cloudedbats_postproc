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
        self.logger = logging.getLogger("bat_migration")
        self.clear()

    def clear(self):
        """ """
        self.sampling_events_list = []
        self.static_metadata = {}
        self.export_directory = ""

    def load_config(self, config_file):
        """ """
        # Load config from yaml-file.
        config_path = pathlib.Path(config_file)
        with config_path.open("r") as file:
            self.metadata_config = yaml.load(file, Loader=yaml.FullLoader)
        # Load "exportDirectory" and "staticMetadata".
        self.export_directory = self.metadata_config.get("exportDirectory", {})
        self.static_metadata = self.metadata_config.get("staticMetadata", {})

    def scan_directories(self):
        """ """
        try:
            root_dir_path = pathlib.Path(self.export_directory)
            for site_path in sorted(root_dir_path.iterdir()):
                if site_path.is_dir():
                    self.site_name = site_path.name
                    self.logger.info("- Processing site: " + self.site_name)
                    for event_path in sorted(site_path.iterdir()):
                        if event_path.is_dir():
                            self.event_name = event_path.name
                            self.event_path = event_path
                            self.logger.info("- Processing event: " + self.event_name)
                            # Metadata.
                            metadata_dict = {}
                            # From event name.
                            metadata_dict["monitoring_site"] = self.site_name
                            metadata_dict["monitoring_event"] = self.event_name
                            parts = self.event_name.split("_")
                            event_date = parts[1]
                            metadata_dict["event_start_date"] = event_date
                            metadata_dict["event_end_date"] = event_date
                            # Add static metadata.
                            for key, value in self.static_metadata.items():
                                metadata_dict[key] = str(value)
                            # Add wurb settings metadata.
                            settings_dict = self.read_wurb_settings()
                            for key, value in settings_dict.items():
                                metadata_dict[key] = str(value)
                            # Append to metadata list.
                            self.sampling_events_list.append(metadata_dict)
        except Exception as e:
            self.logger.error("Exception when scanning directories: " + str(e))

    def read_wurb_settings(self):
        """ """
        settings_dict = {}
        try:
            settings = batmigration.WurbSettings()
            settings.load_settings(self.event_path)
            settings_dict = settings.get_settings_dict()
            # Translate keys.
            settings_dict["decimal_latitude"] = settings_dict.get("latitude_dd", "")
            settings_dict["decimal_longitude"] = settings_dict.get("longitude_dd", "")

            # Calculate start/stop time from sunset/sunrise. TODO.
            settings_dict["event_start_time"] = "20:00"  # TODO.
            settings_dict["event_end_time"] = "06:00"  # TODO.
        except Exception as e:
            self.logger.error("Exception when reading WURB settings: " + str(e))
        #
        return settings_dict
