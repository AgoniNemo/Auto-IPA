#!/usr/bin/env bash

if [ $? -eq 0 ]
then
    echo "导出xcarchive成功！"
else
    echo "导出xcarchive失败！"
    exit 1
fi

plistName=$1
echo "修改plist文件：$plistName"

# 取出 method
method=$(/usr/libexec/PlistBuddy -c "Print :method" $plistName)

# 设置 method
/usr/libexec/PlistBuddy -c "Set :method "$2"" $plistName

# 取出 signingStyle
signingStyle=$(/usr/libexec/PlistBuddy -c "Print :signingStyle" $plistName)

echo $signingStyle

# 配置文件名称
configName=$(/usr/libexec/PlistBuddy -c "Print :provisioningProfiles:"$3"" $plistName)
echo "配置文件名称 $configName"

if [ $configName != "$4" ]
then
   # 修改配置文件名称
   /usr/libexec/PlistBuddy -c "Set :provisioningProfiles:"$3" "$4"" $plistName
fi

if [ $signingStyle = "automatic" ]
then
    echo '---证书自动管理---'
    if [ $method = "app-store" ] && [ $2 != "app-store" ]
    then

        # 删除 uploadBitcode
        /usr/libexec/PlistBuddy -c "Delete :uploadBitcode" $plistName

        # 删除 uploadSymbols
        /usr/libexec/PlistBuddy -c "Delete :uploadSymbols" $plistName

        # 先添加key值 compileBitcode
        /usr/libexec/PlistBuddy -c "Add :compileBitcode bool YES" $plistName

        # 先添加key值 thinning
        /usr/libexec/PlistBuddy -c "Add :thinning string <none>" $plistName
    
    elif [ $method != "app-store" ] && [ $2 = "app-store" ]
    then
        # 删除 thinning
        /usr/libexec/PlistBuddy -c "Delete :thinning" $plistName

        # 删除 compileBitcode
#        /usr/libexec/PlistBuddy -c "Delete :compileBitcode" $plistName

        # 先添加key值 uploadSymbols
        /usr/libexec/PlistBuddy -c "Add :uploadSymbols bool YES" $plistName

        # 先添加key值 uploadBitcode
        /usr/libexec/PlistBuddy -c "Add :uploadBitcode bool YES" $plistName
    else
        echo "只修改了method，其他不需要修改！"
    fi
else
    # 删除 provisioningProfiles
    /usr/libexec/PlistBuddy -c "Delete :provisioningProfiles" $plistName

    # 先添加key值 provisioningProfiles
    /usr/libexec/PlistBuddy -c "Add :provisioningProfiles dict" $plistName

    # 添加value值
    /usr/libexec/PlistBuddy -c "Add :provisioningProfiles:"$3" string "$4"" $plistName

    # 设置 signingCertificate
    /usr/libexec/PlistBuddy -c "Set :signingCertificate iPhone "$5"" $plistName
fi




