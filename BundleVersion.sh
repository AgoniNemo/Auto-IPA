#!/usr/bin/env bash

path="${1}/Info.plist"

# 取出 CFBundleVersion
version=$(/usr/libexec/PlistBuddy -c 'Print :CFBundleVersion' $path)
echo $version
version=$[version+1]

echo $version

# 设置 CFBundleVersion
/usr/libexec/PlistBuddy -c "Set :CFBundleVersion "$version"" $path

# 查看 CFBundleVersion
version=$(/usr/libexec/PlistBuddy -c 'Print :CFBundleVersion' $path)
echo $version
