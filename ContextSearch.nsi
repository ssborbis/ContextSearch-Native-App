!include "WordFunc.nsh"

# define installer name
OutFile "ContextSearch_installer.exe"
 
# set desktop as install directory
InstallDir $APPDATA\ContextSearch
 
# default section start
Section
 
# define output path
SetOutPath $INSTDIR
 
# specify file to go in output path
File ContextSearch.exe
 
# define uninstaller name
WriteUninstaller $INSTDIR\uninstaller.exe
 
#HKEY_CURRENT_USER\SOFTWARE\Mozilla\NativeMessagingHosts\ContextSearch /ve /f /d 
WriteRegStr HKCU "SOFTWARE\Mozilla\NativeMessagingHosts\ContextSearch" '' '$APPDATA\ContextSearch\native.json'
Var /GLOBAL modifiedInstDir
${WordReplace} $INSTDIR "\" "\\" "E+" $modifiedInstDir
FileOpen $0 $INSTDIR\native.json w
FileWrite $0 '{$\r\
	"name": "ContextSearch",$\r\
	"description": "Sends base64 encoded search.json.mozlz4 file",$\r\
	"path": "$modifiedInstDir\\ContextSearch.exe",$\r\
	"type": "stdio",$\r\
	"allowed_extensions": [ "{5dd73bb9-e728-4d1e-990b-c77d8e03670f}" ]$\r\
}'
FileClose $0

#-------
# default section end
SectionEnd
 
# create a section to define what the uninstaller does.
# the section will always be named "Uninstall"
Section "Uninstall"
 
# Always delete uninstaller first
Delete $INSTDIR\uninstaller.exe
DeleteRegKey HKCU "SOFTWARE\Mozilla\NativeMessagingHosts\ContextSearch"
 
# now delete installed file
RMDir /r $INSTDIR
 
SectionEnd