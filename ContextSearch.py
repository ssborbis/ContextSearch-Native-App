#!/usr/bin/python3 -u

# Note that running python with the `-u` flag is required on Windows,
# in order to ensure that stdin and stdout are opened in binary, rather
# than text, mode.

import json
import sys
import struct
import os
import subprocess
import urllib.request

__version__ = "2.11"

BINARY_URL = "https://raw.githubusercontent.com/ssborbis/ContextSearch-Native-App/master/ContextSearch.py"
VERSION_URL = "https://raw.githubusercontent.com/ssborbis/ContextSearch-Native-App/master/version.json"

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
    response = urllib.request.urlopen(VERSION_URL)
    js = json.loads(response.read().decode("utf-8"))
    latest_version = js["version"]

    if ( float(latest_version) > float(__version__)):
        return latest_version
    else:
        return False

def update():
    response = urllib.request.urlopen(BINARY_URL)
    remote_script = response.read().decode("utf-8")

    with open(os.path.realpath(__file__), 'w') as f:
        f.write(remote_script);

message = get_message()

if not message.get("verify") is None:
    send_message(encode_message(True))
    sys.exit(0)

if not message.get("version") is None:
    send_message(encode_message(__version__))
    sys.exit(0)

if not message.get("checkForUpdate") is None:
    send_message(encode_message(check_for_update()))
    sys.exit(0)

if not message.get("update") is None:
    update()
    send_message(encode_message(True))
    sys.exit(0)

if not message.get("path") is None:

    cwd = message.get("cwd") or "."
    cwd = os.path.expanduser(cwd)

    if message["return_stdout"] is True:
        output = subprocess.check_output(message["path"], cwd=cwd, shell=True).decode()
        send_message(encode_message(output))
    else:
        import shlex
        cmd = shlex.split(message["path"])
        subprocess.Popen(cmd, cwd=cwd)

        send_message(encode_message(True))
    
    sys.exit(0)

send_message(encode_message(False))
sys.exit(1)