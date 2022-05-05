#!/usr/bin/python3
# -*- coding:utf-8 -*-
#
# Copyright (c) 2022-present Arnold Andreasson
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib
import yaml
import matplotlib
import matplotlib.figure
from scipy import signal
from scipy.io import wavfile
import numpy

class SpectrogramGenerator():
    """ """
    def __init__(self):
        """ """
        self.source_directory = ""
        self.target_directory = ""
        self.source_file_list = []
        self.target_file_list = []

    def load_config(self, config_file="spectrograms_config.yaml"):
        """ """
        config_path = pathlib.Path(config_file)
        with open(config_path) as file:
            config_dict = yaml.load(file, Loader=yaml.FullLoader)

        if "sourceDirectory" in config_dict:
            self.source_directory = config_dict["sourceDirectory"]
        if "targetDirectory" in config_dict:
            self.target_directory = config_dict["targetDirectory"]

    def build_source_file_list(self):
        """ """
        source_path = pathlib.Path(self.source_directory)
        wav_files = list(source_path.glob('**/*.wav'))
        for wav_file in wav_files:
            self.source_file_list.append(str(wav_file))
            # print("DEBUG: wav:", str(wav_file))
        print("DEBUG: source length:", len(self.source_file_list))

    def build_target_file_list(self):
        """ """
        target_path = pathlib.Path(self.target_directory)
        wav_files = list(target_path.glob('**/*.jpg'))
        for wav_file in wav_files:
            self.target_file_list.append(str(wav_file))
            # print("DEBUG: wav:", str(wav_file))
        print("DEBUG: target length:", len(self.target_file_list))

    def cleanup(self):
        """ """
        wav_files = list(pathlib.Path(self.source_directory).glob("**/*.wav"))
        wav_files = [str(file.name) for file in wav_files]
        spectrogram_files = list(pathlib.Path(self.target_directory).glob("**/*_SPECTROGRAM.jpg"))
        for spectrogram_file in spectrogram_files:
            target_file_name = spectrogram_file.name
            target_file_name = target_file_name.replace("_SPECTROGRAM.jpg", ".wav")
            if target_file_name not in wav_files:
                spectrogram_file.unlink() # Remove file.
                print("Wav file is missing, spectrogram deleted: ", str(spectrogram_file.name))
        
    def get_target_path(self, source_path):
        """ """
        target_path = str(source_path)
        target_path = target_path.replace(self.source_directory, self.target_directory)
        target_path = target_path.replace(".wav", "_SPECTROGRAM.jpg")
        return target_path

    def create_spectrogram(self, source_path, target_path):
        """ """
        # print("DEBUG. Source: ", source_path)
        # print("DEBUG. Target: ", target_path)
        if pathlib.Path(target_path).exists():
            print("Already done. Skipped.")
            return

        try:
            sample_rate, samples = wavfile.read(source_path)
            # Change from time expanded, TE, to full scan, FS.
            if sample_rate < 90000:
                sample_rate *= 10

            #Calculate spectrogram.
            frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate, window="blackmanharris", nperseg=1024, noverlap=768)
            # From Hz to kHz.
            frequencies = frequencies / 1000.0

            # Plot figure.
            matplotlib.rcParams.update({'font.size': 6})
            figure = matplotlib.figure.Figure(
                figsize=(10,3), 
                dpi=500)
            ax1 = figure.add_subplot(111)
            # Fix colours, use logarithmic scale.
            ax1.pcolormesh(times, frequencies, numpy.log(spectrogram))
            # Title and labels.
            ax1.set_title('File: ' + str(pathlib.Path(source_path).name), fontsize=8)
            ax1.set_ylabel('Frequency (kHz)')
            ax1.set_xlabel('Time (s)')
            ax1.set_ylim((0,100))
            # Grid.
            ax1.minorticks_on()
            ax1.grid(which='major', linestyle='-', linewidth='0.5', alpha=0.7)
            ax1.grid(which='minor', linestyle='-', linewidth='0.5', alpha=0.3)
            ax1.tick_params(which='both', top='off', left='off', right='off', bottom='off')
            # Save.
            figure.tight_layout()
            figure.savefig(target_path)
        except Exception as e:
            print("EXCEPTION in create_spectrogram: ", e)

# MAIN.
if __name__ == "__main__":
    """ """
    generator = SpectrogramGenerator()
    generator.load_config()
    generator.build_source_file_list()
    # generator.build_target_file_list()
    for source_file in sorted(generator.source_file_list):
        target_file = generator.get_target_path(source_file)
        # Create if not exists.
        target_dir = pathlib.Path(target_file).parents[0]
        print("Processing:", source_file)
        if not target_dir.exists():
            target_dir.mkdir(parents=True)
        # Create spectrogram.
        generator.create_spectrogram(source_file, target_file)
    # Remove spectrograms with no corresponding wav files.
    generator.cleanup()

