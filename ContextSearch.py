#!/usr/bin/python -u

# Note that running python with the `-u` flag is required on Windows,
# in order to ensure that stdin and stdout are opened in binary, rather
# than text, mode.

import json
import sys
import struct
import base64
import os
import time

# Read a message from stdin and decode it.
def get_message():
    raw_length = sys.stdin.read(4)
    if not raw_length:
        sys.exit(0)
    message_length = struct.unpack('@I', raw_length)[0]
    message = sys.stdin.read(message_length)
    return json.loads(message)

# Encode a message for transmission, given its content.
def encode_message(message_content):
    encoded_content = json.dumps(message_content)
    encoded_length = struct.pack('@I', len(encoded_content))
    return {'length': encoded_length, 'content': encoded_content}


# Send an encoded message to stdout.
def send_message(encoded_message):
    sys.stdout.write(encoded_message['length'])
    sys.stdout.write(encoded_message['content'])
    sys.stdout.flush()

message = get_message()
message_json = json.loads(message)

if '!@!@' in message_json:
    mod_time = os.path.getmtime(message_json['!@!@'])
    send_message(encode_message({"last_mod": time.ctime(mod_time), "base64": ""}))
    sys.exit(0)

with open(message_json['path'], "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

mod_time = os.path.getmtime(message_json['path'])
send_message(encode_message({"last_mod": time.ctime(mod_time), "base64": encoded_string}))