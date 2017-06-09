
### AutoBuild.py用法

+ 如果要用到fir上传，要先安装fir-cli
地址：https://github.com/FIRHQ/fir-cli

+ PS：这里要注意一点，因为Xcode8.3以后打包的ruby版本要为mac系统的默认版本，而fir-cli插件最低支持的版本为2.3.0，所以在脚本里用了rvm来做版本的切换，需要安装rvm（可以使用在终端命令rvm -v查看是不是安装了rvm）,如果安装了,最好下通过ruby -v命令查看下ruby的版本,如果高于2.0.0,需要在终端输入 rvm use system命令切换到系统版本（2.0.0版本）

+ 打开conf.ini，设置里面的证书名、描述文件、项目路径等。

+ 打开终端，运行命令 python 路径+AutoBuild.py(要去Xcode里把打勾的automatically manage signing去掉)

### 下面来说说怎么找到证书、描述文件
+ iPhone Developer: xxxxx@xxx.com (LJV3E98B44)就是了
+ 还可以右键-->显示简介，常用名称就是了
![image](http://upload-images.jianshu.io/upload_images/1610969-0976addfe850abc8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
+ 描述文件就有点麻烦了，先进入到下面的路径
> ~/Library/MobileDevice/Provisioning Profiles 这是描述文件的路径
+ 可以看到描述文件，如果你有多个项目建议你先copy一份放桌面，然后删除全部文件，在安装你从开发者中心下载的描述文件，这时，你在这个文件里就能看到描述文件名字了

### 错误：
- error: exportArchive: No applicable devices found.如果报错提示是这个,要在终端输入 rvm use system
