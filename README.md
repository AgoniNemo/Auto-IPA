
### AutoBuild.py用法

+ 如果要用到fir上传，要先安装fir-cli
地址：https://github.com/FIRHQ/fir-cli

+ PS：这里要注意一点，因为Xcode8.3以后打包的ruby版本要为mac系统的默认版本，而fir-cli插件最低支持的版本为2.3.0，所以在脚本里用了rvm来做版本的切换，需要安装rvm（可以使用在终端命令rvm -v查看是不是安装了rvm）,如果安装了,最好下通过ruby -v命令查看下ruby的版本,如果高于2.0.0,需要在终端输入 rvm use system命令切换到系统版本（2.0.0版本）

+ 打开conf.ini，设置里面的证书名、描述文件、项目路径等。

+ 打开终端，运行命令 python 路径+AutoBuild.py(要去Xcode里把打勾的automatically manage signing去掉)


### 错误：
- error: exportArchive: No applicable devices found.如果报错提示是这个,要在终端输入 rvm use system
