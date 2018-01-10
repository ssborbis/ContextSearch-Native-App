!include "WordFunc.nsh"

# define installer name
OutFile "ContextSearch_installer.exe"
 
# set desktop as install directory
InstallDir $PROGRAMFILES\ContextSearch
 
# default section start
Section

SetDetailsView show
 
# define output path
SetOutPath $INSTDIR

# specify file to go in output path
File ContextSearch.exe
File README.md
 
# define uninstaller name
WriteUninstaller $INSTDIR\uninstaller.exe
SetRegView 64
WriteRegStr HKLM "SOFTWARE\Mozilla\NativeMessagingHosts\ContextSearch" '' '$INSTDIR\ContextSearch.json'

Var /GLOBAL modifiedInstDir
${WordReplace} $INSTDIR "\" "\\" "E+" $modifiedInstDir

FileOpen $0 $INSTDIR\ContextSearch.json w
FileWrite $0 '{$\n\
	"name": "ContextSearch",$\n\
	"description": "Sends base64 encoded search.json.mozlz4 file",$\n\
	"path": "$modifiedInstDir\\ContextSearch.exe",$\n\
	"type": "stdio",$\n\
	"allowed_extensions": [ "{5dd73bb9-e728-4d1e-990b-c77d8e03670f}" ]$\n\
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
SetRegView 64
DeleteRegKey HKLM "SOFTWARE\Mozilla\NativeMessagingHosts\ContextSearch"
 
# now delete installed file
RMDir /r $INSTDIR
 
SectionEnd