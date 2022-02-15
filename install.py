#!/usr/bin/python3 -u

import os
import sys
import json
import shutil
import copy

manifest_template = {
    "name": "contextsearch_webext",
    "description": "Launches external application",
    "type": "stdio"
}

manifest_file = "contextsearch_webext.json"
binary_file = "ContextSearch.py"
use_bat_file = True

browsers = json.load(open('browsers.json'))

def installRegistryKeys(key, manifest_path):
    cmd = "REG ADD " + key + " /ve /t REG_SZ /d \"" + manifest_path + "\" /f"
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
        shutil.copyfile(binary_file, os.path.join(path, binary_file))
    except OSError as error:
        print(error)

def installManifest(platform):
    for b in browsers:
        print()
        path = os.path.expanduser(b["platforms"][platform]["user_config_path"])
        path_browser_specific = os.path.join(path, b["name"])
        parent_path = os.path.abspath(os.path.join(path, os.pardir)) 
        if os.path.isdir(parent_path):
            print('Found', b["name"])
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
                manifest["path"] = os.path.join(os.path.expanduser("~/AppData/roaming/ContextSearch-webext/"), "ContextSearch.bat")
            else:
                manifest["path"] = os.path.join(os.path.expanduser("~/ContextSearch-webext/"), binary_file)

            try:
                print("Installing manifest -> ", manifest_path)
                print()
                with open( manifest_path, 'w', encoding='utf-8') as f:
                    json.dump(manifest, f, ensure_ascii=False, indent=4)
                f.close()

            except OSError as error:
                print(error)

        if platform == "windows":
            for key in b["platforms"][platform]["registry_keys"]:
                installRegistryKeys(key, manifest_path)

if sys.platform == "linux" or sys.platform == "linux2":
    # linux
    installManifest("linux")
    installBinary(os.path.expanduser("~/ContextSearch-webext/"))

    sys.exit(0)

elif sys.platform == "darwin":
    # OS X
    installManifest("macOS")
    installBinary(os.path.expanduser("~/ContextSearch-webext/"))

    sys.exit(0)

elif sys.platform == "win32":
	# windows
    installManifest("windows")
    installBinary(os.path.expanduser("~/AppData/roaming/ContextSearch-webext/"))

    if use_bat_file:
        path = os.path.expanduser("~\\AppData\\Roaming\\ContextSearch-webext\\")
        bat_path = os.path.join(path, "ContextSearch.bat")
        with open( bat_path, 'w' ) as f:
            f.write("@echo off\r\n")
            f.write("\"" + sys.executable + "\" -u " + binary_file + "\r\n")
        f.close()

    sys.exit(0)



