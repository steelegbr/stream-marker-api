"""
    Stream Marker API
    Copyright (C) 2022 Marc Steele
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import re
from logging import Logger
from struct import unpack
from typing import BinaryIO, List

SIZE_LENGTH_FIELD = 1
SIZE_CHUNK = 16


class Marker:
    text: str
    time: float


def _get_block_length(raw: BinaryIO, logger: Logger) -> int:
    # Read raw

    block_length_raw = raw.read(1)
    logger.debug(f"Raw block length is {block_length_raw}")

    # Unpack to something we can use

    (block_length,) = unpack("<B", block_length_raw)
    logger.info(f"Found block length {block_length}.")
    return block_length


def cleanup_field(original: str) -> str:
    matches = re.search(r"StreamTitle='(.*)';", original)
    if matches:
        return matches.group(1)
    return original


def extract_marker(
    raw: BinaryIO, block_length: int, time: int, logger: Logger
) -> Marker:
    # Create the marker

    marker = Marker()
    marker.time = time

    # Extract the string component

    bytes_to_read = block_length * 16
    raw_bytes = raw.read(bytes_to_read)
    logger.debug(f"Read {bytes_to_read} bytes")

    (raw_string,) = unpack(f"<{bytes_to_read}s", raw_bytes)
    logger.debug(f"Extracted raw string: {raw_string}")

    decoded_string = raw_string.decode()
    logger.debug(f"Decoded string: {decoded_string}")

    # Remove the cruft from the field

    marker.text = cleanup_field(decoded_string)

    # Pass the marker back

    logger.debug(f'Found marker "{marker.text}" at {marker.time} ms')
    return marker


def to_markers_and_compressed_audio(
    raw: BinaryIO, metadata_interval: int, bitrate: int, logger: Logger
) -> (List[Marker], bytes):
    markers = []
    compressed_audio = []
    bitrate_bps = bitrate * 1000
    ms_per_jump = 1000 / bitrate_bps * metadata_interval

    current_ms = ms_per_jump

    try:
        # Keep going to the end of the file

        while True:

            # Read and append the next audio block

            compressed_audio.append(raw.read(metadata_interval))
            current_ms += ms_per_jump

            # Block length

            block_length = _get_block_length(raw, logger)

            # Have we found a marker

            if block_length:
                markers.append(extract_marker(raw, block_length, current_ms, logger))

    except Exception as ex:
        logger.debug(f"Infinite loop crashed out: {ex}")

    return (markers, compressed_audio)
