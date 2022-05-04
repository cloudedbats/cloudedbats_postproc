#!/usr/bin/python3
# -*- coding:utf-8 -*-
#
# Copyright (c) 2022-present Arnold Andreasson
# License: MIT License (see LICENSE file or http://opensource.org/licenses/mit).

import pathlib
import yaml
import logging


class BatMigrationMetadata:
    """ """

    def __init__(self):
        """ """
        self.logger = logging.getLogger("bat_migration")
        self.metadata_config = {}
        self.column_delimiter = "\t"
        self.row_delimiter = "\n"
        self.export_key_list = []
        self.export_columns_dict = {}

    def load_config(self, config_file):
        """ """
        # Load config from yaml-file.
        config_path = pathlib.Path(config_file)
        with config_path.open("r") as file:
            self.metadata_config = yaml.load(file, Loader=yaml.FullLoader)
        # Load "columnDelimiter" and "rowDelimiter".
        self.column_delimiter = self.metadata_config.get(
            "columnDelimiter", self.column_delimiter
        )
        self.row_delimiter = self.metadata_config.get(
            "rowDelimiter", self.row_delimiter
        )
        # Load "exportMetadataColumns".
        export_columns = self.metadata_config.get("exportMetadataColumns", "")
        # Create both header and dictionary for easy access.
        self.export_key_list = []
        self.export_columns_dict = {}
        for column_dict in export_columns:
            # Add first key.
            key = list(column_dict.keys())[0]
            value = column_dict.get(key, "")
            self.export_key_list.append(str(key))
            self.export_columns_dict[key] = value

    def save_metadata(
        self, metadata_dir="", metadata_file="Metadata_table.csv", source_metadata=[]
    ):
        """ """
        self.logger.info("- Writing to metadata file: " + metadata_file)
        row_counter = 0
        # Open metadata file.
        metadata_path = pathlib.Path(metadata_dir, metadata_file)
        with metadata_path.open("w", encoding="utf8") as file:
            # Write header row.
            header = self.export_key_list
            file.write(self.column_delimiter.join(header) + self.row_delimiter)
            # Create rows.
            for row_dict in source_metadata:
                out_row = []
                # Map internally and externally used keys.
                for key in header:
                    column_dict = self.export_columns_dict.get(key, {})
                    value = ""
                    if "text" in column_dict:
                        value = column_dict.get("text", "")
                    elif "sourceKey" in column_dict:
                        source_key = column_dict.get("sourceKey", "")
                        value = row_dict.get(source_key, "")
                    # Check default.
                    if len(str(value)) == 0:
                        value = column_dict.get("default", "")
                    # Add to out_row.
                    if str(value).lower() == "none":
                        out_row.append("")
                    else:
                        out_row.append(str(value))
                # Write row.
                file.write(self.column_delimiter.join(out_row) + self.row_delimiter)
                row_counter += 1
        # Done.
        self.logger.info("- Number of rows in metadata: " + str(row_counter))
