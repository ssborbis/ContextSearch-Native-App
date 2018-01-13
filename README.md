# ContextSearch-Native-App
Native App for use with ContextSearch web-ext

This is a simple app written in both C and python that reads a requested file to base64 for webextensions processing.

## Windows
Grab the latest release and run the installer

The ContextSearch_installer.exe does the following

Creates folder C:\Program Files (x86)\ContextSearch with the following files

    ContextSearch.exe
    ContextSearch.json
    README.md
    uninstaller.exe

Adds the following key to the registry
- HKLM\SOFTWARE\Mozilla\NativeMessagingHosts\ContextSearch

## Other OS
1. Download ContextSearch.c (or ContextSearch.py if using python) and ContextSearch.json
2. Compile ContextSearch.c with gcc or equivelent (e.g. <code> gcc ContextSearch.c -o ContextSearch</code>) 
    OR 
   <code>chmod+x ContextSearch.py</code> if using python under Linux
2. Edit "path" key in ContextSearch.json to point to the binary or python script.  For example. if you installed ContextSearch.py to  /home/mclovin/bin your ContextSearch.json would look like:
```javascript
{
"name": "ContextSearch",
"description": "Sends base64 encoded search.json.mozlz4 file",
"path": "/home/mclovin/bin/ContextSearch.py",
"type": "stdio",
"allowed_extensions": [ "{5dd73bb9-e728-4d1e-990b-c77d8e03670f}" ]
}
```
### Linux
For global visibility, copy ContextSearch.json to:

* /usr/lib/mozilla/native-messaging-hosts/ContextSearch.json

or:

* /usr/lib64/mozilla/native-messaging-hosts/ContextSearch.json

For per-user visibility <b>!preferred method per user feedback</b>

* ~/.mozilla/native-messaging-hosts/ContextSearch.json

### Mac OS X
For global visibility, copy ContextSearch.json to:

* /Library/Application Support/Mozilla/NativeMessagingHosts/ContextSearch.json

For per-user visibility

* ~/Library/Application Support/Mozilla/NativeMessagingHosts/ContextSearch.json

