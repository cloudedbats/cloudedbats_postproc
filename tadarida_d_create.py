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
        self.base_dir = ""
        # Work.
        self.dir_list = []

    def load_config(self, config_file="tadarida_d_config.yaml"):
        """ """
        config_path = pathlib.Path(config_file)
        with open(config_path) as file:
            config_dict = yaml.load(file, Loader=yaml.FullLoader)

        if "pathToTadatridaD" in config_dict:
            self.tadatrida_d = config_dict["pathToTadatridaD"]
        if "baseDirectory" in config_dict:
            self.base_dir = config_dict["baseDirectory"]

    def build_dir_list(self):
        """ """
        self.dir_list = []
        base_dir_path = pathlib.Path(self.base_dir)
        # tmp_dir_list = [f for f in base_dir_path.iterdir() if f.is_dir()]
        tmp_dir_list = [f for f in base_dir_path.glob("**/") if f.is_dir()]
        # Only use directories containing wav files.
        for tmp_dir in tmp_dir_list:
            wav_files = list(pathlib.Path(tmp_dir).glob("*.wav"))
            if len(wav_files) > 0:
                self.dir_list.append(str(tmp_dir))

    def generate_ta(self):
        """ """
        for wav_dir in sorted(self.dir_list):
            print("\nDEBUG: Generates TA files for: ", wav_dir)
            list_files = subprocess.run([self.tadatrida_d, wav_dir])
            print("Finished with exit code: %d" % list_files.returncode)

    def cleanup(self):
        """ """
        for wav_dir in sorted(self.dir_list):
            wav_files = list(pathlib.Path(wav_dir).glob("*.wav"))
            wav_files = [str(file.name) for file in wav_files]
            ta_files = list(pathlib.Path(wav_dir).glob("**/*.ta"))
            for ta_file in ta_files:
                ta_file_name = ta_file.name
                ta_file_name = ta_file_name.replace(".ta", ".wav")
                if ta_file_name not in wav_files:
                    ta_file.unlink() # Remove file.
                    print("Wav file is missing, TA deleted: ", str(ta_file.name))


# MAIN.
if __name__ == "__main__":
    """ """
    generator = GeneratorTadaridaD()
    generator.load_config()
    generator.build_dir_list()
    # Run Tadarida-D.
    # generator.generate_ta()
    # Remove ta-files with no corresponding wav files.
    generator.cleanup()
