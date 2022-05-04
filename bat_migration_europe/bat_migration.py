#!/usr/bin/python3
# -*- coding:utf-8 -*-
#
# Copyright (c) 2022-present Arnold Andreasson
# License: MIT License (see LICENSE file or http://opensource.org/licenses/mit).

import pathlib
import logging
import bat_migration_europe


class BatMigration:
    """ """

    def __init__(self):
        """ """
        self.export_events = bat_migration_europe.BatMigrationEvents()
        self.export_metadata = bat_migration_europe.BatMigrationMetadata()
        self.wurb_settings = bat_migration_europe.WurbSettings()
        #
        self.metadata_file = "Metadata_table.csv"

    def setup(self, export_config_file, metadata_config_file):
        """ """
        # Load config.
        self.export_events.load_config(export_config_file)
        self.export_metadata.load_config(metadata_config_file)

    def scan_sampling_events(self):
        """ """
        self.export_events.scan_directories()

    def save_metadata(self):
        """ """
        target_path = pathlib.Path(self.export_events.target_directory)
        if not target_path.exists():
            target_path.mkdir(parents=True)
        self.export_metadata.save_metadata(
            metadata_dir=self.export_events.target_directory,
            metadata_file=self.metadata_file,
            source_metadata=self.export_events.sampling_events_list,
        )

    def move_ta_files(self):
        """ """
        try:
            root_dir_path = pathlib.Path(self.export_events.source_directory)
            for ta_file in root_dir_path.glob("**/txt/*.ta"):
                source_location = str(ta_file)
                target_location = source_location.replace(
                    self.export_events.source_directory,
                    self.export_events.target_directory,
                )
                if "/txt/" in target_location:
                    target_location = target_location.replace("txt/", "")
                    target_path = pathlib.Path(target_location)
                    # Create parend directory.
                    target_file_parent = target_path.parent
                    if not target_file_parent.exists():
                        target_file_parent.mkdir(parents=True)
                    # Move file.
                    ta_file.replace(target_path)
        except Exception as e:
            print("Exception: ", e)

    # def delete_wav_files(self):
    #     """ """
    #     try:
    #         root_dir_path = pathlib.Path(self.export_events.export_directory)
    #         for ta_file in root_dir_path.glob("**/*.wav"):
    #             ta_file.unlink()
    #     except Exception as e:
    #         print("Exception: ", e)

    def setup_logging(self, log_file_name):
        """ """
        # Remove old logfile, if exists.
        logfile_path = pathlib.Path(log_file_name)
        if logfile_path.exists():
            logfile_path.unlink()
        # New logfile, and console logging.
        logger = logging.getLogger("bat_migration")
        logger.setLevel(logging.DEBUG)
        # Remove old handlers.
        while logger.hasHandlers():
            logger.removeHandler(logger.handlers[0])
        # To file.
        file_handler = logging.FileHandler(log_file_name)
        file_handler.setLevel(logging.DEBUG)
        # Console logging.
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        # Create formatter and add to the handlers.
        formatter = logging.Formatter("%(asctime)s %(levelname)s : %(message)s")
        file_handler.setFormatter(formatter)
        formatter = logging.Formatter("%(message)s")
        console_handler.setFormatter(formatter)
        # Add filter to console to avoid huge error lists.
        class ConsoleFilter(logging.Filter):
            def filter(self, record):
                return record.levelno in [logging.INFO, logging.WARNING]
                # return record.levelno in [logging.DEBUG, logging.INFO, logging.WARNING]

        # Connect filter class.
        console_handler.addFilter(ConsoleFilter())
        # Add handlers to the loggers.
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
