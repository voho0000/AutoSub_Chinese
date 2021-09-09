#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime


def get_timestamp_string(timedelta, format):
    """Convert the timedelta into something that can be used by a subtitle file.

    Args:
        timedelta : timedelta timestmap
        format : subtitle format
    """
    sep = '.' if format == "vtt" else ','
    # timedelta may be eg, '0:00:14'
    if '.' in str(timedelta):
        timestamp = "0" + str(timedelta).split(".")[0] + sep + str(timedelta).split(".")[-1][:3]
    else:
        timestamp = "0" + str(timedelta) + sep + "000"
    return timestamp


def write_to_file(file_handle, inferred_text, line_count, limits, vtt, cues):
    """Write the inferred text to SRT file
    Follows a specific format for SRT files

    Args:
        file_handle : SRT file handle
        inferred_text : text to be written
        line_count : subtitle line count 
        limits : starting and ending times for text
    """

    from_dur = get_timestamp_string(datetime.timedelta(seconds=float(limits[0])), format)
    to_dur = get_timestamp_string(datetime.timedelta(seconds=float(limits[1])), format)

    if not vtt:    
        file_handle.write(str(line_count) + "\n")
        file_handle.write(from_dur + " --> " + to_dur + "\n")
        file_handle.write(inferred_text + "\n\n")
    else:
        file_handle.write(from_dur + " --> " + to_dur + "  align:start position:0%\n")
        file_handle.write(inferred_text + "\n")
        
        words = [f"<c> {x}</c>" for x in inferred_text.split(" ")]
        cue_tags = [f"<{str(datetime.timedelta(seconds=cue))}>" for cue in cues]
        words_cues_mixed = [val for pair in zip(cue_tags, words) for val in pair][1:]
        file_handle.write(''.join(words_cues_mixed) + "\n\n")
