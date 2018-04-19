#!/usr/bin/env bash

source './version.sh'

examineVersion

# 加载rvm
if [ $nine_above == true ]
then 
     if [[ -s "$HOME/.rvm/scripts/rvm" ]]
        then
        source "$HOME/.rvm/scripts/rvm"
    elif [[ -s "/usr/local/rvm/scripts/rvm" ]]
        then
        source "/usr/local/rvm/scripts/rvm"
    else
        printf "找不到rvm!\n"
    fi
fi


if [ -e "$1" ]
 then
  echo "======正在上传!======";
else
  printf "找不到上传文件!错误路径："$1"\n"
  exit 1
fi

# 切换ruby版本
if [ $nine_above == true ]
then 
    #  rvm use 2.3.0
     echo "fir使用的ruby版本必须为2.3.0以上!"
fi

# 上传ipa
fir p $1 -T $2

if [ $nine_above == true ]
then 
     rvm use system
fi

open https://fir.im/apps

