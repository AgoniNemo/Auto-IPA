#!/usr/bin/env bash

path="$1.xcworkspace"
projectPath="$1.xcodeproj/project.pbxproj"
version_release_uuid="$3"
version_debug_uuid="$4"

version=$(xcodebuild -workspace "$path" -scheme "$2" -showBuildSettings | grep CURRENT_PROJECT_VERSION | tr -d 'CURRENT_PROJECT_VERSION = ')
version=$((version + 1))
/usr/libexec/PlistBuddy -c "Set :objects:${version_release_uuid}:buildSettings:CURRENT_PROJECT_VERSION ${version}" "${projectPath}"
/usr/libexec/PlistBuddy -c "Set :objects:${version_debug_uuid}:buildSettings:CURRENT_PROJECT_VERSION ${version}" "${projectPath}"

# 查看 CFBundleVersion
version=$(xcodebuild -workspace "$path" -scheme "$2" -showBuildSettings | grep CURRENT_PROJECT_VERSION | tr -d 'CURRENT_PROJECT_VERSION = ')
echo $version
