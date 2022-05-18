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

import logging
from converter import (
    append_cue_chunks,
    decode_wave_file,
    decompress_audio,
    to_markers_and_compressed_audio,
)
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import StreamingResponse
from io import BytesIO

# Logging

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)

# Launch FastAPI

app = FastAPI()

# API endpoints


@app.post("/api/")
async def convert_file(
    stream: UploadFile = File(..., title="A captured stream to extract markers from"),
    metadata_interval: int = Form(
        ..., ge=1, title="The icy-metaint value from Shoutcast"
    ),
    bitrate: int = Form(..., ge=16, title="Stream bitrate in kbps"),
    encoding: str = Form(
        ..., regex="^audio\/\w+$", title="Content-Type headed for the stream"
    ),
):
    markers, compressed_audio = to_markers_and_compressed_audio(
        stream.file, metadata_interval, bitrate, logger
    )

    decompressed_audio_file = decompress_audio(compressed_audio, logger)
    decoded_audio_file = decode_wave_file(decompressed_audio_file, logger)
    complete_audio_file = append_cue_chunks(decoded_audio_file, markers, logger)

    logger.debug("Returning audio file to user")
    return StreamingResponse(BytesIO(complete_audio_file), media_type="audio/wav")
