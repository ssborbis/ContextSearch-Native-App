# ContextSearch-Native-App
Native App for use with ContextSearch web-ext

This is a simple app written in both C and python that reads a requested file to base64 for webextensions native application processing.

## Windows
Grab the latest release and run the installer

The ContextSearch_installer.exe does the following

Creates folder C:\Program Files (x86)\ContextSearch with the following files

    ContextSearch.exe
    ContextSearch.json
    README.md
    uninstaller.exe

Adds the following key to the registry
HKLM\SOFTWARE\Mozilla\NativeMessagingHosts\ContextSearch

## Other OS
1. Download ContextSearch.c (or ContextSearch.py if using python) and ContextSearch.json
2. Compile ContextSearch.c with gcc or equivelent (skip if using ContextSearch.py)
2. Edit "path" key in ContextSearch.json to point to the binary or python script

### Linux
For global visibility, copy ContextSearch.json to:

* /usr/lib/mozilla/native-messaging-hosts/ContextSearch.json

or:

* /usr/lib64/mozilla/native-messaging-hosts/ContextSearch.json

For per-user visibility

* ~/.mozilla/native-messaging-hosts/ContextSearch.json

### Mac OS X
For global visibility, copy ContextSearch.json to:

* /Library/Application Support/Mozilla/NativeMessagingHosts/ContextSearch.json

For per-user visibility

* ~/Library/Application Support/Mozilla/NativeMessagingHosts/ContextSearch.json

