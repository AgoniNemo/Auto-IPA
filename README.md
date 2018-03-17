
## 前言
这是用Python+xcodebuild写的脚本打包工具，支持上传fir,打包完成后多邮件发送

### 环境

- Xcode8.3+  
- ruby 2.3.0（需要上传到fir-cli的ruby最低版本，如果不需要上传，使用默认的就好）
- rvm 1.29.1+
- 项目使用CocoaPods生成

### AutoBuild.py用法

+ 在使用前先把ruby -v 在终端看到下ruby的版本，如果大于2.0.0，需要在终端中运行命令rvm use system（如果没有安装rvm点[这里](https://ruby-china.org/wiki/rvm-guide)）

+ 如果要用到fir上传，要先安装[fir-cli](https://github.com/FIRHQ/fir-cli),并且使用fir login + token命令登录（具体用法可以在下载地址查看）

+ 打开conf.ini，设置里面的证书名、描述文件、项目路径等。

+ 打开终端，运行命令 python 路径+AutoBuild.py(要去Xcode里把打勾的automatically manage signing去掉，还有Signing里的证书与配置文件的设置都要去掉，比如：Code Signing identity与Provisioning Profile等等)

### 下面来说说怎么找到证书、描述文件
+ iPhone Developer: xxxxx@xxx.com (LJV3E98B44)就是了

+ 还可以右键-->显示简介，常用名称就是了
![image](http://upload-images.jianshu.io/upload_images/1610969-0976addfe850abc8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

+ 描述文件就有点麻烦了，先进入到下面的路径

> ~/Library/MobileDevice/Provisioning Profiles 这是描述文件的路径

+ 可以看到描述文件，如果你有多个项目建议你先copy一份放桌面，然后删除全部文件，在安装你从开发者中心下载的描述文件，这时，你在这个文件里就能看到描述文件名字了

```
# 来说下conf.ini的配置
# 工程名字(Target名字，比如：XL)
Project_Name = XL

# workspace的名字（这个是工作空间，使用CocoaPods生成的，一般是与工程名字一样，以xcworkspace为后缀名）
Workspace_Name = XL

# 配置环境，Release或者Debug,默认release
Configuration = Release

# 是否需要发邮件,邮件配置在下面修改,False或者True,默认False
needSendMail = False

# 是否需要上传ipa到fir,False或者True,默认False
needUpload = False

# 是否自动创建plist文件,False或者True,默认True,如果设置为False则使用参数PlistPath的配置文件
needCreatePlist = True

# 项目根目录(比如你的项目CocoaPods文件在/Users/AG/Documents/ios/XXXXXX/XL.xcworkspace)
project_path = /Users/AG/Documents/ios/XXXXXX

# 打包后ipa存储目录
targerIPA_path = /Users/AG/Documents/ipa

# 配置文件名（比如配置文件为：AdHoc.mobileprovision）
provisioningProfiles = AdHoc
```

### 邮箱设置
+ 特别说明下qq的授权码以及开启SMTP服务点[这里](http://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256)


```
# 发送的邮箱账号
from_addr = 1180777777@qq.com

# 发送的邮箱授权码或者密码(一些邮箱登录比如 QQ 邮箱需要 SSL 认证)
password = wsfqivulmhxjbgdc

# 是否需要 SSL 认证(QQ，163等邮箱需要 SSL 认证)
smtp_SSL = True

# SMTP 服务器地址
smtp_server = smtp.qq.com

# SMTP 服务器端口(如果smtp_SSL=True可不管，qq的是465或者587，之前为25)
smtp_port = 25

# 收件人地址,有多个要用逗号隔开
to_addrs = XES168880@163.com,371988888@qq.com

# 发送内容（可不填）
text = 哈哈

```

### 错误：
- error: exportArchive: No applicable devices found.如果报错提示是这个,要在终端输入 rvm use system

- Provisioning profile "描述文件" doesn't include signing certificate "证书".Code signing is required for product type 'Application' in SDK 'iOS 10.3' 这个错误就是你的描述文件与证书不一致造成的，正确配置好就行了。
