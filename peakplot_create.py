#!/usr/bin/python3
# -*- coding:utf-8 -*-
#
# Copyright (c) 2022-present Arnold Andreasson
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib
from re import A
import yaml
import matplotlib
import matplotlib.figure

# from scipy import signal
# from scipy.io import wavfile
# import numpy
import datetime
import dateutil.parser


class PeakPlotGenerator:
    """ """

    def __init__(self):
        """ """
        self.source_directory = ""
        self.target_directory = ""
        self.source_file_list = []
        self.plot_list = []
        self.plot_data = []

    def load_config(self, config_file="peakplot_config.yaml"):
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
        wav_files = list(source_path.glob("**/*.wav"))
        for wav_file in wav_files:
            self.source_file_list.append(str(wav_file))
        print("DEBUG: source length:", len(self.source_file_list))

    def build_plot_list(self):
        """ """
        for wav_file in self.source_file_list:
            parent_name = str(pathlib.Path(wav_file).parent.name)
            if parent_name not in self.plot_list:
                self.plot_list.append(parent_name)
        print("DEBUG: target length:", len(self.plot_list))

    def extract_data(self):
        """ """
        for wav_file in self.source_file_list:
            wav_path = pathlib.Path(wav_file)
            parent_name = str(wav_path.parent.name)
            wav_name = wav_path.stem
            file_parts = wav_name.split("_")
            if len(file_parts) >= 5:
                prefix = file_parts[0]
                time = file_parts[1]
                position = file_parts[2]
                wav_type = file_parts[3]
                peak = file_parts[4]
                peak_parts = peak.split("-")
                peak_khz = peak_parts[0]
                peak_dbfs = peak_parts[1]
                peak_khz = peak_khz.replace("kHz", "")
                peak_dbfs = str(int(peak_dbfs.replace("dB", "")) * -1.0)

                data_row = [parent_name, time, position, peak_khz, peak_dbfs]
                self.plot_data.append(data_row)

    def cleanup(self):
        """ """
        # wav_files = list(pathlib.Path(self.source_directory).glob("**/*.wav"))
        # wav_files = [str(file.name) for file in wav_files]
        # spectrogram_files = list(pathlib.Path(self.target_directory).glob("**/*_SPECTROGRAM.jpg"))
        # for spectrogram_file in spectrogram_files:
        #     target_file_name = spectrogram_file.name
        #     target_file_name = target_file_name.replace("_SPECTROGRAM.jpg", ".wav")
        #     if target_file_name not in wav_files:
        #         spectrogram_file.unlink() # Remove file.
        #         print("Wav file is missing, spectrogram deleted: ", str(spectrogram_file.name))

    def create_plots(self):
        """ """
        try:
            for plot_name in sorted(self.plot_list):

                # Plot figure.
                matplotlib.rcParams.update({"font.size": 6})
                figure = matplotlib.figure.Figure(figsize=(10, 2), dpi=500)
                ax1 = figure.add_subplot(111)

                x = [
                    dateutil.parser.parse(x[1].split("+")[0])
                    for x in self.plot_data
                    if x[0] == plot_name
                ]
                y = [float(x[3]) for x in self.plot_data if x[0] == plot_name]

                plot_name_parts = plot_name.split("_")
                plot_place = plot_name_parts[0]
                plot_date = dateutil.parser.parse(plot_name_parts[1])
                start_datetime = plot_date + datetime.timedelta(hours=18)
                end_datetime = plot_date + datetime.timedelta(hours=30)

                # Create scatter plot.
                ax1.scatter(x, y, marker=".", color='blue', s=5)

                # Title and labels.
                title = plot_name.replace("_", " ")
                if len(x) == 1:
                    title += "     (One sound file recorded.)"
                else:
                    title += "     (" + str(len(x)) + " sound files recorded.)"
                ax1.set_title(title, fontsize=8)
                ax1.set_ylabel("Peak frequency (kHz)")
                ax1.set_ylim((0, 100))
                # ax1.set_xlabel("Time")
                ax1.set_xlim((start_datetime, end_datetime))
                xfmt = matplotlib.dates.DateFormatter("%H:%M")
                ax1.xaxis.set_major_formatter(xfmt)
                ax1.xaxis.set_major_locator(
                    matplotlib.dates.HourLocator(byhour=None, interval=1)
                )
                ax1.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(10))

                # Grid.
                ax1.minorticks_on()
                ax1.grid(which="major", linestyle="-", linewidth="0.5", alpha=0.5)
                ax1.grid(which="minor", linestyle="-", linewidth="0.4", alpha=0.2)
                ax1.tick_params(
                    which="both", top="off", left="off", right="off", bottom="off"
                )

                # Save.
                figure.tight_layout()
                target_path = pathlib.Path(
                    self.target_directory, plot_place, plot_name + "_PEAKS.png"
                )
                if not target_path.parent.exists():
                    target_path.parent.mkdir(parents=True)
                figure.savefig(str(target_path))

        except Exception as e:
            print("EXCEPTION in create_plots: ", e)


# MAIN.
if __name__ == "__main__":
    """ """
    generator = PeakPlotGenerator()
    generator.load_config()
    generator.build_source_file_list()
    generator.build_plot_list()
    generator.extract_data()
    generator.create_plots()
    generator.cleanup()
