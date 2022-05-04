#!/usr/bin/python3
# -*- coding:utf-8 -*-
#
# Copyright (c) 2022-present Arnold Andreasson
# License: MIT License (see LICENSE file or http://opensource.org/licenses/mit).

# import datetime
import dateutil.parser
import datetime
import bat_migration_europe


def get_solartime_data(
    event_date,
    latitude_dd,
    longitude_dd,
    start_event,
    start_adjust_minutes,
    stop_event,
    stop_adjust_minutes,
):
    """ """
    start_end_dict = {}
    try:
        solartime = bat_migration_europe.SolarTime()
        if (latitude_dd == 0.0) or (longitude_dd == 0.0):
            return None
        # Get sun info for current day and position.
        sampling_date_datetime = dateutil.parser.parse(event_date)
        date_local = sampling_date_datetime.date()
        latitude_short = round(float(latitude_dd), 2)
        longitude_short = round(float(longitude_dd), 2)
        solartime_dict = solartime.sun_utc(date_local, latitude_short, longitude_short)

        sunset_utc = solartime_dict.get("sunset", None)
        sunrise_utc = solartime_dict.get("sunrise", None)
        sunset_local = sunset_utc.astimezone()
        sunrise_local = sunrise_utc.astimezone()

        # Dates.
        start_end_dict["start_date"] = str(date_local)
        start_end_dict["end_date"] = str(date_local + datetime.timedelta(days=1))
        # Time.
        start_adj = datetime.timedelta(minutes=int(float(start_adjust_minutes)))
        stop_adj = datetime.timedelta(minutes=int(float(stop_adjust_minutes)))
        # start_time = sunset_utc + start_adj
        # stop_time = sunrise_utc + stop_adj
        start_time = sunset_local + start_adj
        stop_time = sunrise_local + stop_adj
        start_end_dict["start_time"] = str(start_time.time())
        start_end_dict["end_time"] = str(stop_time.time())
    except Exception as e:
        print("EXCEPTION: Solartime: ", e)

    print("DEBUG: ", start_end_dict)

    return start_end_dict
