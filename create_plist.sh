#!/usr/bin/env bash

# 获取当前路径
path=$(dirname $0)
path=${path/\./$(pwd)}
file="{$path}/ExportOptionsPlist"

source './create_xml.sh'
source './version.sh'

# 设置文件权限
chmod u+x ./create_xml.sh

examineVersion

put_head 'xml version="1.0" encoding="UTF-8"'
put '!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"'
tag_start 'plist version="1.0"'
tag_start 'dict'

if [ $nine_above == true ]
then
    put_key 'key' 'compileBitcode'
    tag_value 'false'
fi
put_key 'key' 'method'
put_key 'string' ${1}

if [ $nine_above == false ]
then
    tag_end 'dict'
    tag_end 'plist'
    exit 1
fi
put_key 'key' 'provisioningProfiles'
tag_start 'dict'
put_key 'key' ${2}
put_key 'string' ${3}
tag_end 'dict'
put_key 'key' 'signingCertificate'
put_key 'string' "iPhone ${4}"
put_key 'key' 'signingStyle'
put_key 'string' 'manual'
put_key 'key' 'stripSwiftSymbols'
tag_value 'true'
tag_end 'dict'
tag_end 'plist'

