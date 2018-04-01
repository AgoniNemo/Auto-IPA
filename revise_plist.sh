#!/usr/bin/env bash

# 取出 method
method=$(/usr/libexec/PlistBuddy -c "Print :method" ExportOptionsPlist.plist)

# 设置 method
/usr/libexec/PlistBuddy -c "Set :method "$1"" ExportOptionsPlist.plist

# 取出 signingStyle
signingStyle=$(/usr/libexec/PlistBuddy -c "Print :signingStyle" ExportOptionsPlist.plist)

echo $signingStyle

if [ $signingStyle = "automatic" ]
then
    echo '---'
    if [ $method = "app-store" ] && [ $1 != "app-store" ]
    then

        # 删除 uploadBitcode
        /usr/libexec/PlistBuddy -c "Delete :uploadBitcode" ExportOptionsPlist.plist

        # 删除 uploadSymbols
        /usr/libexec/PlistBuddy -c "Delete :uploadSymbols" ExportOptionsPlist.plist

        # 先添加key值 compileBitcode
        /usr/libexec/PlistBuddy -c "Add :compileBitcode bool YES" ExportOptionsPlist.plist

        # 先添加key值 thinning
        /usr/libexec/PlistBuddy -c "Add :thinning string <none>" ExportOptionsPlist.plist
    
    elif [ $method != "app-store" ] && [ $1 = "app-store" ]
    then
        # 删除 thinning
        /usr/libexec/PlistBuddy -c "Delete :thinning" ExportOptionsPlist.plist

        # 删除 compileBitcode
        /usr/libexec/PlistBuddy -c "Delete :compileBitcode" ExportOptionsPlist.plist

        # 先添加key值 uploadSymbols
        /usr/libexec/PlistBuddy -c "Add :uploadSymbols bool YES" ExportOptionsPlist.plist

        # 先添加key值 uploadBitcode
        /usr/libexec/PlistBuddy -c "Add :uploadBitcode bool YES" ExportOptionsPlist.plist
    else
        echo "error!!!"
    fi
else
    echo '3333'
    # 删除 provisioningProfiles
    /usr/libexec/PlistBuddy -c "Delete :provisioningProfiles" ExportOptionsPlist.plist

    # 先添加key值 provisioningProfiles
    /usr/libexec/PlistBuddy -c "Add :provisioningProfiles dict" ExportOptionsPlist.plist

    # 添加value值
    /usr/libexec/PlistBuddy -c "Add :provisioningProfiles:"$3" string "$4"" ExportOptionsPlist.plist

    # 设置 signingCertificate
    /usr/libexec/PlistBuddy -c "Set :signingCertificate iPhone "$5"" ExportOptionsPlist.plist
fi