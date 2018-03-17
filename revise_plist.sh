#!/usr/bin/env bash

echo $1

# 设置 method
/usr/libexec/PlistBuddy -c "Set :method "$1"" ExportOptionsPlist.plist

# 删除 provisioningProfiles
/usr/libexec/PlistBuddy -c "Delete :provisioningProfiles" ExportOptionsPlist.plist

# 先添加key值 provisioningProfiles
/usr/libexec/PlistBuddy -c "Add :provisioningProfiles dict" ExportOptionsPlist.plist

# 添加value值
/usr/libexec/PlistBuddy -c "Add :provisioningProfiles:"$2" string "$3"" ExportOptionsPlist.plist

# 设置 signingCertificate
/usr/libexec/PlistBuddy -c "Set :signingCertificate iPhone "$4"" ExportOptionsPlist.plist