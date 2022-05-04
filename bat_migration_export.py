#!/usr/bin/python3
# -*- coding:utf-8 -*-
#
# Copyright (c) 2022-present Arnold Andreasson
# License: MIT License (see LICENSE file or http://opensource.org/licenses/mit).

import logging
import bat_migration_europe


# Main.
if __name__ == "__main__":
    """ """
    # Config files.
    export_config_file = "bat_migration_config.yaml"
    metadata_config_file = "bat_migration_europe/metadata_config.yaml"

    # Create export.
    bat_migration = bat_migration_europe.BatMigration()
    bat_migration.setup_logging("bat_migration_europe_log.txt")
    logger = logging.getLogger("bat_migration")
    logger.info("\nMetadata generation started.")
    bat_migration.setup(export_config_file, metadata_config_file)
    bat_migration.scan_sampling_events()
    bat_migration.save_metadata()
    bat_migration.move_ta_files()
    # bat_migration.delete_wav_files()
    logger.info("Metadata generation finished.\n")
