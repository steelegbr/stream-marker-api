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

import ffmpeg
import re

from logging import Logger
from struct import unpack
from tempfile import NamedTemporaryFile
from typing import BinaryIO, List, Tuple, Union
from wave_chunk_parser.chunks import (
    CueChunk,
    CuePoint,
    FormatChunk,
    LabelChunk,
    ListChunk,
    RiffChunk,
)

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
    marker.time = round(time)

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
) -> Union[List[Marker], bytes]:
    markers = []
    compressed_audio = []
    bitrate_bps = bitrate * 1000
    ms_per_jump = 1000 * metadata_interval / bitrate_bps * 8

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

    return (markers, b"".join(compressed_audio))


def decompress_audio(compressed: bytes, logger: Logger) -> NamedTemporaryFile:
    temp_file_out = NamedTemporaryFile(suffix=".wav")
    with NamedTemporaryFile() as temp_file_in:

        # Write what we have to disk

        logger.debug(f"Writing to temp source file {temp_file_in.name}")
        temp_file_in.write(compressed)
        temp_file_in.flush()

        # Trigger FFMPEG

        logger.debug(f"Trigger FFMPEG to write to {temp_file_out.name}")
        ffmpeg_stderr, ffmpeg_stdout = (
            ffmpeg.input(temp_file_in.name)
            .output(temp_file_out.name)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )

        # Read in what we got

        logger.debug(f"FFMPEG STDERR: {ffmpeg_stderr}")
        logger.debug(f"FFMPEG STDOUT: {ffmpeg_stdout}")

        # Return the wave file

        temp_file_out.seek(0)
        decompressed_audio = temp_file_out.read()
        logger.debug("Successfully decompressed audio.")

    return temp_file_out


def decode_wave_file(file_handle: BinaryIO, logger: Logger) -> RiffChunk:
    logger.debug("Attempting to decode file")
    return RiffChunk.from_file(file_handle)


def marker_to_cue_point(index: int, marker: Marker, sample_rate: int) -> CuePoint:
    samples = sample_rate * marker.time // 1000
    return CuePoint(index, samples, RiffChunk.CHUNK_DATA, 0, 0, samples)


def markers_to_chunks(
    markers: List[Marker], format_chunk: FormatChunk, logger: Logger
) -> Tuple[CueChunk, ListChunk]:
    sample_rate = format_chunk.sample_rate
    logger.debug(f"Determined sample rate to be {sample_rate}Hz")

    cue_points = [
        marker_to_cue_point(index + 1, marker, sample_rate)
        for index, marker in enumerate(markers)
    ]
    logger.debug(f"Converted {len(cue_points)} cue points")

    labels = [
        LabelChunk(index + 1, marker.text) for index, marker in enumerate(markers)
    ]
    logger.debug(f"Converted {len(labels)} labels")

    return (CueChunk(cue_points), ListChunk(labels))


def append_cue_chunks(
    audio_file: RiffChunk, markers: List[Marker], logger: Logger
) -> bytes:
    logger.debug("Call into cue point append process")
    cue_chunk, list_chunk = markers_to_chunks(
        markers, audio_file.sub_chunks[RiffChunk.CHUNK_FORMAT], logger
    )

    audio_file.sub_chunks[RiffChunk.CHUNK_CUE] = cue_chunk
    audio_file.sub_chunks[RiffChunk.CHUNK_LIST] = list_chunk

    logger.debug("Attempting to encode the file for transmission")
    return audio_file.to_bytes()
