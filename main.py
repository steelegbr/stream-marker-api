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

from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()


@app.post("/")
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
    return {"filename": stream.filename}
