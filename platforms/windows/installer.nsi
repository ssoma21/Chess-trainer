; Run from dist/windows:  makensis -DVERSION=1.1 installer.nsi
Unicode true
!ifndef VERSION
  !define VERSION "1.1"
!endif
Name "Chess Trainer"
OutFile "ChessTrainer-Setup.exe"
InstallDir "$LOCALAPPDATA\Programs\Chess Trainer"
RequestExecutionLevel user
SetCompressor /SOLID lzma
Icon "icon.ico"
UninstallIcon "icon.ico"
Page instfiles
UninstPage instfiles
Section "Install"
  SetOutPath "$INSTDIR"
  File /r "app\*"
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  CreateShortcut "$DESKTOP\Chess Trainer.lnk" "$INSTDIR\ChessTrainer.exe" "" "$INSTDIR\icon.ico"
  CreateDirectory "$SMPROGRAMS\Chess Trainer"
  CreateShortcut "$SMPROGRAMS\Chess Trainer\Chess Trainer.lnk" "$INSTDIR\ChessTrainer.exe" "" "$INSTDIR\icon.ico"
  CreateShortcut "$SMPROGRAMS\Chess Trainer\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ChessTrainer" "DisplayName" "Chess Trainer"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ChessTrainer" "DisplayVersion" "${VERSION}"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ChessTrainer" "UninstallString" '"$INSTDIR\Uninstall.exe"'
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ChessTrainer" "DisplayIcon" "$INSTDIR\icon.ico"
  Exec '"$INSTDIR\ChessTrainer.exe"'
SectionEnd
Section "Uninstall"
  Delete "$DESKTOP\Chess Trainer.lnk"
  RMDir /r "$SMPROGRAMS\Chess Trainer"
  RMDir /r "$INSTDIR"
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ChessTrainer"
SectionEnd
