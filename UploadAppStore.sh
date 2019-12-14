
#!/usr/bin/env bash

echo "username == $1" "password == $2"

altoolPath="/Applications/Xcode.app/Contents/Applications/Application Loader.app/Contents/Frameworks/ITunesSoftwareService.framework/Versions/A/Support/altool"
"$altoolPath" --validate-app -f $3 -u $1 -p $2

"$altoolPath" --upload-app -f $1 -u $1 -p $2