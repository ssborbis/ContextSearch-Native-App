#!/usr/bin/python3 -u

import os
import sys
import json
import copy
import stat
import urllib.request

manifest_template = {
    "name": "contextsearch_webext",
    "description": "Launches external application",
    "type": "stdio"
}

manifest_file           = "contextsearch_webext.json"
binary_file             = "ContextSearch.py"
bat_file                = "ContextSearch.bat"
browsers_file           = "browsers.json"
windows_install_path    = "~\\AppData\\Roaming\\ContextSearch-webext\\"
nix_install_path        = "~/ContextSearch-webext/"
install_global          = False
repository_path         = "https://raw.githubusercontent.com/ssborbis/ContextSearch-Native-App/master/"

def loadLocalThenRemote(local_path, remote_path):
    try:
        if os.path.exists(local_path):
            return open(local_path).read()
        else:
            print(local_path, "No local file. Fetching remote ...")
            response = urllib.request.urlopen(remote_path)
            return response.read().decode("utf-8")
    except Exception as e:
        print("Cannot load", local_path, " - aborting install")
        sys.exit(1)

def loadBrowsers():
    return json.loads(loadLocalThenRemote(browsers_file, repository_path + browsers_file))

def loadBinary():
    return loadLocalThenRemote(binary_file, repository_path + binary_file)

def installRegistryKey(key, manifest_path):
    cmd = 'REG ADD %s /ve /t REG_SZ /d "%s" /f' % ( key, manifest_path )
    print(cmd)
    os.system(cmd)

def uninstallRegistryKey(key):
    cmd = 'REG DELETE %s /va /f' % ( key )
    print(cmd)
    os.system(cmd)

def installBinary(path):

    try:
        os.mkdir(path)
    except OSError as error:
        pass

    if not os.path.isdir(path):
        print("Unable to create directory", path)
        return

    try:
        with open(os.path.join(path, binary_file), "w" ) as f:
            f.write(loadBinary())  
    except OSError as error:
        print(error)
        sys.exit(1)

    try:
        st = os.stat(os.path.join(path, binary_file))
        os.chmod(os.path.join(path, binary_file), st.st_mode | stat.S_IEXEC)
    except OSError as error:
        print(error)

def installManifest(platform):
    for b in loadBrowsers():
        print()
        path = os.path.expanduser(b["platforms"][platform]["user_config_path"])
        path_browser_specific = os.path.join(path, b["name"])
        parent_path = os.path.abspath(os.path.join(path, os.pardir)) 
        if os.path.isdir(parent_path):
            print('Installing for', b["name"])
            print()

            try:
                os.mkdir(path)
            except OSError as error:
                pass

            if platform == "windows":
                if not os.path.isdir(path):
                    continue

                try:
                    os.mkdir(path_browser_specific)
                except OSError as error:
                    pass

                if not os.path.isdir(path_browser_specific):
                    continue

            manifest = copy.deepcopy(manifest_template)
            manifest.update(b["manifest"])

            if platform == "windows":
                manifest_path = os.path.join(path_browser_specific, manifest_file)
            else:
                manifest_path = os.path.join(path, manifest_file)

            if platform == "windows":
                manifest["path"] = os.path.join(os.path.expanduser(windows_install_path), bat_file)
            else:
                manifest["path"] = os.path.join(os.path.expanduser(nix_install_path), binary_file)

            try:
                print(manifest_path)
                print()
                with open( manifest_path, 'w', encoding='utf-8') as f:
                    json.dump(manifest, f, ensure_ascii=False, indent=4)
                f.close()

            except OSError as error:
                print(error)

        if platform == "windows":
            for key in b["platforms"][platform]["registry_keys_user"]:
                installRegistryKey(key, manifest_path)

def getPlatform():
    if sys.platform == "linux" or sys.platform == "linux2":
        return "linux"

    elif sys.platform == "darwin":
        return "macOS"

    elif sys.platform == "win32":
        return "windows"

if len(sys.argv) == 2 and sys.argv[1] == "--uninstall":

    print("Removing ContextSearch web-ext Native App")

    if getPlatform() == "windows":
        # remove registry keys
        for b in loadBrowsers():
            for key in b["platforms"]["windows"]["registry_keys_user"]:
                print("removing registry key", key)
                uninstallRegistryKey(key)

        # remove app folder
        app_folder = os.path.expanduser(windows_install_path)
        try:
            import shutil
            shutil.rmtree(app_folder)
        except OSError as e:
            print("Error: %s : %s" % (app_folder, e.strerror))

    else:
         # remove manifests
        for b in loadBrowsers():
            delete_path = os.path.expanduser(b["platforms"][getPlatform()]["user_config_path"] + manifest_file)

            if os.path.exists(delete_path):
                os.remove(delete_path)

        # remove app folder
        app_folder = os.path.expanduser(nix_install_path)
        try:
            import shutil
            shutil.rmtree(app_folder)
        except OSError as e:
            print("Error: %s : %s" % (app_folder, e.strerror))
    sys.exit(0)

if getPlatform() == "linux":
    installManifest("linux")
    installBinary(os.path.expanduser(nix_install_path))

elif getPlatform() == "macOS":
    installManifest("macOS")
    installBinary(os.path.expanduser(nix_install_path))

elif getPlatform() == "windows":
    installManifest("windows")
    installBinary(os.path.expanduser(windows_install_path))

    path = os.path.expanduser(windows_install_path)
    bat_path = os.path.join(path, bat_file)
    with open( bat_path, 'w' ) as f:
        f.write("@echo off\r\n")
        f.write("\"" + sys.executable + "\" -u " + binary_file + "\r\n")

sys.exit(0)
