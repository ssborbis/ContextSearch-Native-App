!include "WordFunc.nsh"
!include LogicLib.nsh

Function CopyToClipboard
Exch $0 ;input string
Push $1
Push $2
System::Call 'user32::OpenClipboard(i 0)'
System::Call 'user32::EmptyClipboard()'
StrLen $1 $0
IntOp $1 $1 + 1
System::Call 'kernel32::GlobalAlloc(i 2, i r1) i.r1'
System::Call 'kernel32::GlobalLock(i r1) i.r2'
System::Call 'kernel32::lstrcpyA(i r2, t r0)'
System::Call 'kernel32::GlobalUnlock(i r1)'
System::Call 'user32::SetClipboardData(i 1, i r1)'
System::Call 'user32::CloseClipboard()'
Pop $2
Pop $1
Pop $0
FunctionEnd

# define installer name
OutFile "ContextSearch_installer.exe"
 
# set desktop as install directory
InstallDir $PROGRAMFILES\ContextSearch
Name "ContextSearch Native App"
 
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
WriteRegStr HKLM "SOFTWARE\Mozilla\NativeMessagingHosts\ContextSearch" '' '$INSTDIR\ContextSearch.json'
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

# read Firefox profile.ini and look for the default profile
Var /GLOBAL i
${ForEach} $i 0 9 + 1
	ReadINIStr $0 $APPDATA\Mozilla\Firefox\profiles.ini Profile$i Default
	${If} $0 == "1"
		${ExitFor}
	${EndIf}
${Next}

ReadINIStr $0 $APPDATA\Mozilla\Firefox\profiles.ini Profile$i Path
ReadINIStr $1 $APPDATA\Mozilla\Firefox\profiles.ini Profile$i IsRelative

${If} $0 != ""

	${If} $1 == "1"
		StrCpy $0 "$APPDATA\Mozilla\Firefox\$0"
	${EndIf}
	
	Push "$0" ;input > copy to clipboard
	Call CopyToClipboard

	MessageBox MB_OK "The following profile path has been copied to the clipboard. If this is the profile you wish to use with ContextSearch, paste it to ContextSearch Options->Search Engines->Automatic->Path$\r$\n$\r$\n$0 $\r$\n$\r$\nYou can open about:profiles in the Firefox address bar to find the path to your current profile path if this is incorrect"

${EndIf}

#-------
# default section end
SectionEnd
 
# create a section to define what the uninstaller does.
# the section will always be named "Uninstall"
Section "Uninstall"
 
# Always delete uninstaller first
Delete $INSTDIR\uninstaller.exe
DeleteRegKey HKLM "SOFTWARE\Mozilla\NativeMessagingHosts\ContextSearch"
SetRegView 64
DeleteRegKey HKLM "SOFTWARE\Mozilla\NativeMessagingHosts\ContextSearch"
 
# now delete installed file
RMDir /r $INSTDIR
 
SectionEnd