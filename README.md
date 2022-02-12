# ContextSearch-Native-App
Native App for use with ContextSearch web-ext

This is a simple app written python that launches external applications from ContextSearch web-ext.

This app only runs when called by ContextSearch web-ext.  It does not run when the browser is closed or when ContextSearch web-ext is not installed.

## Linux / MacOS

### Using Python 
##### Step 1
Download ContextSearch.py and contextsearch_webext.json
##### Step 2
Make ContextSearch.py executable and move to desired location ( where <i>mclovin</i> is your user name )

<code>
    mkdir /home/mclovin/bin
    chmod +x ContextSearch.py && mv ContextSearch.py /home/mclovin/bin
</code>
##### Step 3
Edit "path" key in contextsearch_webext.json to point to the python script.  For example. if you moved ContextSearch.py to  /home/mclovin/bin your contextsearch_webext.json would look like:

```javascript
{
"name": "contextsearch_webext",
"description": "Launch applications from ContextSearch-webext",
"path": "/home/mclovin/bin/ContextSearch.py",
"type": "stdio",
"allowed_extensions": [ "{5dd73bb9-e728-4d1e-990b-c77d8e03670f}" ]
}
```

##### Step 4
Move contextsearch_webext.json to the location required by the browser's NativeMessaging API

###### Linux
Firefox: ~/.mozilla/native-messaging-hosts/contextsearch_webext.json
Google Chrome: ~/.config/google-chrome/NativeMessagingHosts/contextsearch_webext.json
Chromium: ~/.config/chromium/NativeMessagingHosts/contextsearch_webext.json

###### Mac OS X
Firefox: ~/Library/Application Support/Mozilla/NativeMessagingHosts/contextsearch_webext.json
Google Chrome: ~/Library/Application Support/Google/Chrome/NativeMessagingHosts/contextsearch_webext.json
Chromium: ~/Library/Application Support/Chromium/NativeMessagingHosts/contextsearch_webext.json

