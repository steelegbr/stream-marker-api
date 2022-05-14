# Stream Marker API

A simple REST API for taking a Shoutcast stream sample and converting it to a wave file with cue markers. This can then be used to adjust the metadata timing. While less important for now playing, getting the timing spot on is important for ad injection.

Calls to the API require the bitrate (in kbps), the ICY metadata offset and the stream sample file.

## Capturing a sample

cURL can be used to capture the required data. In the following command, shoutcast.blob is the captured stream data:

    curl -v https://live.solidradio.co.uk/solid -H "Icy-MetaData: 1" -o shoutcast.blob

Note that custom request header. Without it, we just get the AAC/MP3 data. We also need a few response headers to help us:

    < HTTP/1.1 200 OK
    < Server: nginx/1.18.0 (Ubuntu)
    < Date: Sat, 14 May 2022 17:33:05 GMT
    < Content-Type: audio/aacp
    < Transfer-Encoding: chunked
    < Connection: keep-alive
    < icy-notice1: <BR>This stream requires <a href="http://www.winamp.com">Winamp</a><BR>
    < icy-notice2: Shoutcast DNAS/posix(linux x64) v2.6.1.777<BR>
    < Accept-Ranges: none
    < Access-Control-Allow-Origin: *
    < Cache-Control: no-cache,no-store,must-revalidate,max-age=0
    < icy-name: Solid Radio UK
    < icy-genre: Pop/Rock
    < icy-br: 128
    < icy-sr: 44100
    < icy-url: https://www.solidradio.co.uk/
    < icy-pub: 1
    < icy-metaint: 16384
    < X-Clacks-Overhead: GNU Terry Pratchett

Specifically, we're interested in:
* icy-metaint - the offset in bytes between ICY metadata blocks.
* icy-br - the bitrate in kbps.
* icy-sr - sample rate in Hz. Not necessary for decoding but useful.
* Content-Type - in this case AAC+, which is a little misleading. In reality it's classic AAC with SBR disabled.

## ICY Metadata Blocks

A metadata block contains at least one byte. This first byte is the length of the rest of the block in multiples of 16 bytes. Thanks to [Johan Montelius](https://people.kth.se/~johanmon/dse/casty.pdf) for that useful snippet of information.

Now playing information is encoded