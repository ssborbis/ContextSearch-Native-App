## ContextSearch-Native-App
Native App for use with ContextSearch web-ext

This is a simple app written python that launches external applications from ContextSearch web-ext.

This app only runs when called by ContextSearch web-ext.  It does not run when the browser is closed or when ContextSearch web-ext is not installed.

### Requires Python 3
Be sure to install [Python 3](https://www.python.org/downloads/) before using the native app

---

## Using the Installer ( easy way )
Download and run <a href="https://raw.githubusercontent.com/ssborbis/ContextSearch-Native-App/master/install.py" download>install.py</a>

```
python3 install.py
```

To uninstall
```
python3 install.py --uninstall
```

---


## Manual Install ( not-so-easy way )

### Windows

##### Step 1
Download ContextSearch.py and contextsearch_webext.json

##### Step 2
Move files to desired location ( where <i>mclovin</i> is your user name )

```
mkdir "C:\Users\mclovin\AppData\Roaming\ContextSearch-webext"
move ContextSearch.py "C:\Users\mclovin\AppData\Roaming\ContextSearch-webext"
move contextsearch_webext.json "C:\Users\mclovin\AppData\Roaming\ContextSearch-webext"
```

and update your registry

Chrome
```
REG ADD "HKCU\Software\Google\Chrome\NativeMessagingHosts\contextsearch_webext" /ve /t REG_SZ /d "C:\Users\mclovin\AppData\Roaming\ContextSearch-webext\contextsearch_webext.json" /f
```

Firefox
```
REG ADD "HKCU\Software\Mozilla\NativeMessagingHosts\contextsearch_webext" /ve /t REG_SZ /d "C:\Users\mclovin\AppData\Roaming\ContextSearch-webext\contextsearch_webext.json" /f
```

##### Step 3
Edit "path" key in contextsearch_webext.json to point to the python script.  For example. if you moved ContextSearch.py to  "C:\Users\mclovin\AppData\Roaming\ContextSearch-webext" your contextsearch_webext.json would look like:

```javascript
{
    "name": "contextsearch_webext",
    "description": "Launch applications from ContextSearch-webext",
    "path": "C:\\Users\\mclovin\\AppData\\Roaming\\ContextSearch-webext\\ContextSearch.py",
    "type": "stdio",
    "allowed_extensions": [ "{5dd73bb9-e728-4d1e-990b-c77d8e03670f}" ]
}
```

Chrome requires a slightly different manifest.json

```javascript
{
    "name": "contextsearch_webext",
    "description": "Launches external application",
    "path": "C:\\Users\\mclovin\\AppData\\Roaming\\ContextSearch-webext\\ContextSearch.py",
    "type": "stdio",
    "allowed_origins": [ 
        "chrome-extension://lnojieghgnojlhmnfpmeidigmjpkppep/",
        "chrome-extension://ddippghibegbgpjcaaijbacfhjjeafjh/"
    ]
}
```

<br>
<b>Windows does not always recognize `ContextSearch.py` as an executable, and may not work unless called from a `.bat` file.</b>

##### Step 4 ( if necessary )
Create a new file named `ContextSearch.bat` in the `C:\Users\mclovin\AppData\Roaming\ContextSearch-webext` folder with the following content
```
@echo off
C:\Users\MYNAME\AppData\Local\Programs\Python\Python309\python.exe ContextSearch.py
```

change the Python path to wherever your python.exe is installed

##### Step 5 ( if necessary )
Change the `path` in `contextsearch_webext.json` to `"path": "C:\\Users\\mclovin\\AppData\\Roaming\\ContextSearch-webext\\ContextSearch.bat"`

---

### Linux / MacOS

##### Step 1
Download ContextSearch.py and contextsearch_webext.json

##### Step 2
Make ContextSearch.py executable and move to desired location ( where <i>mclovin</i> is your user name )

```
mkdir /home/mclovin/bin
chmod +x ContextSearch.py && mv ContextSearch.py /home/mclovin/bin
```

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

Chrome requires a slightly different manifest.json

```javascript
{
    "name": "contextsearch_webext",
    "description": "Launches external application",
    "path": "/home/mike/bin/ContextSearch.py",
    "type": "stdio",
    "allowed_origins": [ 
        "chrome-extension://lnojieghgnojlhmnfpmeidigmjpkppep/",
        "chrome-extension://ddippghibegbgpjcaaijbacfhjjeafjh/"
    ]
}
```

##### Step 4
Move contextsearch_webext.json to the location required by the browser's NativeMessaging API

###### Linux
* Firefox: 
```
~/.mozilla/native-messaging-hosts/contextsearch_webext.json
```
* Google Chrome: 
```
~/.config/google-chrome/NativeMessagingHosts/contextsearch_webext.json
```
* Chromium: 
```
~/.config/chromium/NativeMessagingHosts/contextsearch_webext.json
```

###### Mac OS X
* Firefox: 
```
~/Library/Application Support/Mozilla/NativeMessagingHosts/contextsearch_webext.json
```
* Google Chrome: 
```
~/Library/Application Support/Google/Chrome/NativeMessagingHosts/contextsearch_webext.json
```
* Chromium: 
```
~/Library/Application Support/Chromium/NativeMessagingHosts/contextsearch_webext.json
```

