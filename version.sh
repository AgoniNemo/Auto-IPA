#!/usr/bin/env bash

examineVersion(){
    v=$(xcodebuild -version | awk '/Xcode/ ')
    length=${#v}
    result=${v:6:$length}
    nine_above=false
  
    if [ `echo $result | awk -v t1=9 '{print($1>t1)? "1":"0"}'` -eq "0" ]
    then
        nine_above=false
    else
        nine_above=true
    fi
}

# if [ nine_above == true ]
# then 
#      echo Xcode版本9.0以上
# else
#      echo Xcode版本小于9.0
# fi

