
# 加载rvm
if [[ -s "$HOME/.rvm/scripts/rvm" ]]
  then
  source "$HOME/.rvm/scripts/rvm"

elif [[ -s "/usr/local/rvm/scripts/rvm" ]]
  then
  source "/usr/local/rvm/scripts/rvm"
else
  printf "找不到rvm!\n"
fi


if [ -e "$1" ]
  then
   echo "正在上传!";
 else
   printf "找不到上传文件!错误路径："$1"\n"
   exit 1
fi


# 切换ruby版本
rvm use 2.3.0

fir p "$1"
rvm use system
open https://fir.im/apps
