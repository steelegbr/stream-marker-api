"""
    Shoutcast Metadata Client
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

import click
import json
import signal
from halo import Halo
from os.path import exists
from requests import get, post
from requests.exceptions import HTTPError
from uuid import uuid4


@click.group()
def interface():
    pass


@Halo(text="Capturing audio... press CTRL-C to stop...", spinner="dots")
def capture_audio(capture_file_name: str, metadata_file_name: str, url: str):
    with open(capture_file_name, "wb") as output_file:

        # Request the audio

        headers = {"Icy-MetaData": "1"}

        with get(url, headers=headers, stream=True) as response:

            # Make sure we're connected properly

            response.raise_for_status()

            # Write out the metadata

            metadata = {
                "metadata_interval": response.headers.get("icy-metaint"),
                "bitrate": response.headers.get("icy-br"),
            }

            with open(metadata_file_name, "w") as metadata_file:
                json.dump(metadata, metadata_file)

            # Stream the audio to disk (with a stop action)
            # Capture SIGINT

            signal.signal(signal.SIGINT, signal.default_int_handler)

            try:
                while True:
                    output_file.write(response.raw.read(1000))
            except KeyboardInterrupt:
                pass


@click.command()
@click.option("--url", required=True, help="URL of the stream to capture")
def capture(url: str):
    id = uuid4()
    capture_file_name = f"{id}.capture"
    metadata_file_name = f"{id}.json"
    print(f"Writing to file {capture_file_name} from {url}...")
    print(f"Storing metadata to {metadata_file_name}")

    try:
        capture_audio(capture_file_name, metadata_file_name, url)
        print(f"Capture successfully completed.")
    except HTTPError as e:
        print(f"Failed to capture audio - HTTP error - {e}")


@click.command()
@click.option(
    "--uuid", required=True, help="UUID of the audio capture you wish to convert"
)
@click.option("--api", required=True, help="URL of the conversion API")
def convert(uuid: str, api: str):
    capture_file_name = f"{uuid}.capture"
    metadata_file_name = f"{uuid}.json"
    converted_file_name = f"{uuid}.wav"

    # Check the files exist

    if not (exists(capture_file_name) and exists(metadata_file_name)):
        print(f"Failed to find both files for capture {uuid}.")
        return

    # Read in the metadata

    with open(metadata_file_name, "r") as metadata_file:
        metadata = json.load(metadata_file)

    # Perform the conversion

    spinner = Halo(text="Converting audio...")
    spinner.start()

    with open(capture_file_name, "rb") as capture_file:
        files = {"stream": capture_file}

        response = post(api, data=metadata, files=files)

        try:
            response.raise_for_status()
            with open(converted_file_name, "wb") as converted_file:
                for chunk in response.iter_content(1000):
                    converted_file.write(chunk)
            print(f"Output file {converted_file_name} successfully written.")
        except HTTPError as e:
            print(f"Failed to convert audio - HTTP error - {e}")

    spinner.stop()


interface.add_command(capture)
interface.add_command(convert)

if __name__ == "__main__":
    interface()
