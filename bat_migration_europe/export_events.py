#!/usr/bin/python3
# -*- coding:utf-8 -*-
#
# Copyright (c) 2022-present Arnold Andreasson
# License: MIT License (see LICENSE file or http://opensource.org/licenses/mit).

import pathlib
import dateutil.parser
import datetime
import yaml
import logging
import bat_migration_europe


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
        self.source_directory = ""
        self.target_directory = ""

    def load_config(self, config_file):
        """ """
        # Load config from yaml-file.
        config_path = pathlib.Path(config_file)
        with config_path.open("r") as file:
            self.metadata_config = yaml.load(file, Loader=yaml.FullLoader)
        # Load source/target directories and staticMetadata.
        self.source_directory = self.metadata_config.get("sourceDirectory", {})
        self.target_directory = self.metadata_config.get("targetDirectory", {})
        self.static_metadata = self.metadata_config.get("staticMetadata", {})

    def scan_directories(self):
        """ """
        try:
            root_dir_path = pathlib.Path(self.source_directory)
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
                            # End date: add one day.
                            end_date_datetime = dateutil.parser.parse(event_date)
                            end_date_datetime += datetime.timedelta(days=1)
                            metadata_dict["event_end_date"] = str(
                                end_date_datetime.date()
                            )
                            # Add static metadata.
                            for key, value in self.static_metadata.items():
                                metadata_dict[key] = str(value)
                            # Add wurb settings metadata.
                            settings_dict = self.read_wurb_settings(event_date)
                            for key, value in settings_dict.items():
                                metadata_dict[key] = str(value)
                            # Append to metadata list.
                            self.sampling_events_list.append(metadata_dict)
        except Exception as e:
            self.logger.error("Exception when scanning directories: " + str(e))

    def read_wurb_settings(self, event_date):
        """ """
        settings_dict = {}
        try:
            settings = bat_migration_europe.WurbSettings()
            settings.load_settings(self.event_path)
            settings_dict = settings.get_settings_dict()
            # Translate keys.
            latitude_dd = settings_dict.get("latitude_dd", "")
            longitude_dd = settings_dict.get("longitude_dd", "")
            settings_dict["decimal_latitude"] = latitude_dd
            settings_dict["decimal_longitude"] = longitude_dd

            start_event = settings_dict.get("scheduler_start_event", "")
            start_adjust = settings_dict.get("scheduler_start_adjust", "")
            stop_event = settings_dict.get("scheduler_stop_event", "")
            stop_adjust = settings_dict.get("scheduler_stop_adjust", "")

            # Calculate start/stop time from sunset/sunrise. TODO.
            try:
                solartime_dict = bat_migration_europe.get_solartime_data(
                    event_date,
                    latitude_dd,
                    longitude_dd,
                    start_event,
                    start_adjust,
                    stop_event,
                    stop_adjust,
                )
                settings_dict["event_start_time"] = solartime_dict.get(
                    "start_time", "ERROR"
                )
                settings_dict["event_end_time"] = solartime_dict.get(
                    "end_time", "ERROR"
                )

            except Exception as e:
                print("EXCEPTION Sun: ", e)
                settings_dict["event_start_time"] = "ERROR"  # TODO.
                settings_dict["event_end_time"] = "ERROR"  # TODO.
        except Exception as e:
            self.logger.error("Exception when reading WURB settings: " + str(e))
        #
        return settings_dict
