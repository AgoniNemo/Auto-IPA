# 获取当前路径
path=$(dirname $0)
path=${path/\./$(pwd)}
file="$path/file"

examineVersion(){
    xcodebuild -version | awk '/Xcode/ ' >> file

    nine_above=false

    version=""
    while read line
    do
        version=$line
        break
    done < file
    
    result=${version#* }

    if [ `echo $result | awk -v t1=9 '{print($1>t1)? "1":"0"}'` -eq "0" ]
    then
        nine_above=false
    else
        nine_above=true
    fi
    rm $file
}

# if [ nine_above == true ]
# then 
#      echo Xcode版本9.0以上
# else
#      echo Xcode版本小于9.0
# fi

