#!/usr/bin/python3
# -*- coding:utf-8 -*-
#
# Copyright (c) 2022-present Arnold Andreasson
# License: MIT License (see LICENSE file or http://opensource.org/licenses/mit).

import pathlib
import yaml
import subprocess


class GeneratorTadaridaD:
    """ """

    def __init__(self):
        """ """
        # Config.
        self.tadatrida_d = ""
        self.source_dir_list = ""
        # Work.
        self.sound_dir_list = []
        self.not_processed_dir_list = []

    def load_config(self, config_file="tadarida_d_config.yaml"):
        """Load YAML"""
        config_path = pathlib.Path(config_file)
        with open(config_path) as file:
            config_dict = yaml.load(file, Loader=yaml.FullLoader)
        if "pathToTadatridaD" in config_dict:
            self.tadatrida_d = config_dict["pathToTadatridaD"]
        if "sourceDirList" in config_dict:
            self.source_dir_list = config_dict["sourceDirList"]
        print("")
        print("Path to Tadarida-D: ", self.tadatrida_d)
        print("")

    def build_dir_list(self):
        """Create a list of all directories containing wave files."""
        self.sound_dir_list = []
        for source_dir in self.source_dir_list:
            dir_counter = 0
            source_dir_list_path = pathlib.Path(source_dir)
            tmp_dir_list = [f for f in source_dir_list_path.glob("**/") if f.is_dir()]
            # Only use directories containing wav files.
            for tmp_dir in tmp_dir_list:
                wav_files = list(pathlib.Path(tmp_dir).glob("*.wav"))
                if len(wav_files) > 0:
                    dir_counter += 1
                    self.sound_dir_list.append(str(tmp_dir))
            print(
                "Directories with sound files: ", source_dir, " number: ", dir_counter
            )
        print("")

    def check_dir_list(self):
        """ """
        self.not_processed_dir_list = []
        for wav_dir in sorted(self.sound_dir_list):
            wav_dir_path = pathlib.Path(wav_dir)
            wave_file_list = [f.stem for f in wav_dir_path.glob("*.wav")]
            ta_file_list = [f.stem for f in wav_dir_path.glob("txt/*.ta")]
            # Add to dir list for processing.
            if len(ta_file_list) == 0:
                self.not_processed_dir_list.append(wav_dir)
            else:
                # Log problematic directories.
                is_generated_and_equal = False
                if len(wave_file_list) == len(ta_file_list):
                    if sorted(wave_file_list) == sorted(ta_file_list):
                        is_generated_and_equal = True
                if not is_generated_and_equal:
                    print(
                        "Wave and TA differ: ",
                        wav_dir,
                        " Count wave: ",
                        len(wave_file_list),
                        " TA: ",
                        len(ta_file_list),
                    )
        print("")

    def generate_ta(self):
        """ """
        for wav_dir in sorted(self.not_processed_dir_list):
            print("\nDEBUG: Generates TA files for: ", wav_dir)
            list_files = subprocess.run([self.tadatrida_d, wav_dir])
            print("Finished with exit code: %d" % list_files.returncode)

    # def cleanup(self):
    #     """ Remove ta-files with no corresponding wav files. """
    #     for wav_dir in sorted(self.sound_dir_list):
    #         wav_files = list(pathlib.Path(wav_dir).glob("*.wav"))
    #         wav_files = [str(file.name) for file in wav_files]
    #         ta_files = list(pathlib.Path(wav_dir).glob("**/*.ta"))
    #         for ta_file in ta_files:
    #             ta_file_name = ta_file.name
    #             ta_file_name = ta_file_name.replace(".ta", ".wav")
    #             if ta_file_name not in wav_files:
    #                 ta_file.unlink() # Remove file.
    #                 print("Wav file is missing, TA deleted: ", str(ta_file.name))


# MAIN.
if __name__ == "__main__":
    """ """
    generator = GeneratorTadaridaD()
    generator.load_config()
    generator.build_dir_list()

    # Check if already generated in directory.
    generator.check_dir_list()

    # Run Tadarida-D.
    # generator.generate_ta()

    # Remove ta-files with no corresponding wav files.
    # generator.cleanup()
