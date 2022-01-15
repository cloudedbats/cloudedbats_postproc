#!/usr/bin/python3
# -*- coding:utf-8 -*-
#
# Copyright (c) 2022-present Arnold Andreasson
# License: MIT License (see LICENSE file or http://opensource.org/licenses/mit).

import pathlib
import logging
import batmigration


class BatMigration:
    """ """

    def __init__(self):
        """ """
        self.export_events = batmigration.BatMigrationEvents()
        self.export_metadata = batmigration.BatMigrationMetadata()
        self.wurb_settings = batmigration.WurbSettings()
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
        self.export_metadata.save_metadata(
            metadata_dir=self.export_events.export_directory,
            metadata_file=self.metadata_file,
            source_metadata=self.export_events.sampling_events_list,
        )

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


# Main.
if __name__ == "__main__":
    """ """
    # Config files.
    export_config_file = "export_events_config.yaml"
    metadata_config_file = "metadata_config.yaml"

    # Create export.
    bat_migration = BatMigration()
    bat_migration.setup_logging("bat_migration_log.txt")
    logger = logging.getLogger("bat_migration")
    logger.info("\nMetadata generation started.")
    bat_migration.setup(export_config_file, metadata_config_file)
    bat_migration.scan_sampling_events()
    bat_migration.save_metadata()
    logger.info("Metadata generation finished.\n")
