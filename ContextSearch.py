#!/usr/bin/python3 -u

# Note that running python with the `-u` flag is required on Windows,
# in order to ensure that stdin and stdout are opened in binary, rather
# than text, mode.

import json
import sys
import struct
import os
import logging

__version__ = "2.19"

BINARY_URL = "https://raw.githubusercontent.com/ssborbis/ContextSearch-Native-App/master/ContextSearch.py"
VERSION_URL = "https://raw.githubusercontent.com/ssborbis/ContextSearch-Native-App/master/version.json"

logging.basicConfig(
    filename='python.log', 
    encoding='utf-8',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

# Read a message from stdin and decode it.
def get_message():
    raw_length = sys.stdin.buffer.read(4)

    if not raw_length:
        sys.exit(0)

    message_length = struct.unpack('=I', raw_length)[0]
    message = sys.stdin.buffer.read(message_length).decode("utf-8")
    return json.loads(message)

# Encode a message for transmission, given its content.
def encode_message(message_content):
    encoded_content = json.dumps(message_content).encode("utf-8")
    encoded_length = struct.pack('=I', len(encoded_content))
    #  use struct.pack("10s", bytes), to pack a string of the length of 10 characters
    return {'length': encoded_length, 'content': struct.pack(str(len(encoded_content))+"s",encoded_content)}

# Send an encoded message to stdout.
def send_message(encoded_message):
    sys.stdout.buffer.write(encoded_message['length'])
    sys.stdout.buffer.write(encoded_message['content'])
    sys.stdout.buffer.flush()

def check_for_update():
    import urllib.request
    response = urllib.request.urlopen(VERSION_URL)
    js = json.loads(response.read().decode("utf-8"))
    latest_version = js["version"]

    if ( float(latest_version) > float(__version__)):
        return latest_version
    else:
        return False

def update():
    import urllib.request
    response = urllib.request.urlopen(BINARY_URL)
    remote_script = response.read().decode("utf-8")

    with open(os.path.realpath(__file__), 'w') as f:
        f.write(remote_script);

def download(url, dest):
    import urllib.request
    import urllib.error
    import cgi

    remotefile = urllib.request.urlopen(url)

    content = remotefile.info()['Content-Disposition']

    if content:
        value, params = cgi.parse_header(content)
        filename = os.path.join(dest, params["filename"])
    else:
        filename = os.path.join(dest, os.path.basename(url))

    urllib.request.urlretrieve(url, filename)

    return filename

try:

    # receive nativeMessage
    message = get_message()

    if message.get("verify"):
        send_message(encode_message(True))
        sys.exit(0)

    elif message.get("version"):
        send_message(encode_message(__version__))
        sys.exit(0)

    elif message.get("checkForUpdate"):
        send_message(encode_message(check_for_update()))
        sys.exit(0)

    elif message.get("update"):
        update()
        send_message(encode_message(True))
        sys.exit(0)

    # use python to fetch remote content
    if message.get("downloadURL"):
        tmpdir = None

        if message.get("downloadFolder") and os.path.isdir(os.path.expanduser(message.get("downloadFolder"))):
            tmpdir = os.path.expanduser(message.get("downloadFolder"))
        else:
            import tempfile
            tmpdir = tempfile.gettempdir()

        filename = download(message.get("downloadURL"), tmpdir)
        message["path"] = message["path"].replace("{download_url}", filename)

    # execute shell command
    if message.get("path"):

        import subprocess

        cwd = message.get("cwd") or os.getcwd()
        cwd = os.path.expanduser(cwd)

        import shlex
        cmd = shlex.split(message["path"])

        if message["return_stdout"]:
            output = subprocess.check_output(message["path"], cwd=cwd, shell=True).decode()
            send_message(encode_message(output))
        else:

            if sys.platform == "win32":

                CREATE_NEW_PROCESS_GROUP = 0x00000200
                DETACHED_PROCESS = 0x00000008
                CREATE_NEW_CONSOLE = 0x00000010
                CREATE_BREAKAWAY_FROM_JOB = 0x01000000

                subprocess.run(message["path"], cwd=cwd, shell=True, creationflags=CREATE_BREAKAWAY_FROM_JOB )

            else:
                subprocess.run(message["path"], cwd=cwd, shell=True)
        
        sys.exit(0)

    # no valid requests
    send_message(encode_message(False))
    sys.exit(1)

except Exception as e:
    logging.error(e)