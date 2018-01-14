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

<code>HKLM\SOFTWARE\Mozilla\NativeMessagingHosts\ContextSearch</code>

## Other OS

### Using ContextSearch C binary 
##### Step 1
Download ContextSearch.c and ContextSearch.json
##### Step 2
Compile ContextSearch.c with gcc or an equivelent compiler and output to the desired location

<code>gcc ContextSearch.c -o /home/mclovin/bin/ContextSearch</code>
##### Step 3
Edit the "path" key in ContextSearch.json to point to the binary.  For example. if you compiled ContextSearch to  /home/mclovin/bin your ContextSearch.json would look like:

```javascript
{
"name": "ContextSearch",
"description": "Sends base64 encoded search.json.mozlz4 file",
"path": "/home/mclovin/bin/ContextSearch",
"type": "stdio",
"allowed_extensions": [ "{5dd73bb9-e728-4d1e-990b-c77d8e03670f}" ]
}
```

### Using Python 
##### Step 1
Download ContextSearch.py and ContextSearch.json
##### Step 2
Make ContextSearch.py executable and move to desired location

<code>chmod +x ContextSearch.py && mv ContextSearch.py /home/mclovin/bin</code>
##### Step 3
Edit "path" key in ContextSearch.json to point to the python script.  For example. if you moved ContextSearch.py to  /home/mclovin/bin your ContextSearch.json would look like:

```javascript
{
"name": "ContextSearch",
"description": "Sends base64 encoded search.json.mozlz4 file",
"path": "/home/mclovin/bin/ContextSearch.py",
"type": "stdio",
"allowed_extensions": [ "{5dd73bb9-e728-4d1e-990b-c77d8e03670f}" ]
}
```

##### Step 4
Move ContextSearch.json to the location required by the Firefox NativeMessaging API

###### Linux
* ~/.mozilla/native-messaging-hosts/ContextSearch.json

###### Mac OS X
* ~/Library/Application Support/Mozilla/NativeMessagingHosts/ContextSearch.json

