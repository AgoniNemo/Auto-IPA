# -*- coding: utf-8 -*-
import os
import sys
import time
import hashlib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import sendMail
import ConfigParser


# 发邮件
def send_mail():
    sendMail.send_mail();

# 导出xcarchive,ipa
def build_project(conf,bundleID,sign,pName,plistPath):

    timeName = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

    xcworkPath = '%s/%s.xcworkspace' %(conf['project_path'],conf['workspace_Name'])
    xcarchivePath = '%s/%s/%s_%s.xcarchive' %(conf['targerIPA_path'],timeName,conf['project_name'],conf['type'])

    # 导出xcarchive
    build = 'xcodebuild -workspace %s -scheme %s -configuration %s -archivePath %s clean archive build CODE_SIGN_IDENTITY="%s" PROVISIONING_PROFILE="%s" PRODUCT_BUNDLE_IDENTIFIER="%s"' %(xcworkPath,conf['project_name'],conf['configuration'],xcarchivePath,sign,pName,bundleID)
    # print(build)
    os.system(build)

    # 自动生成的plist文件名
    p = 'ExportOptionsPlist.plist'

    # 导出plist文件
    needCreatePlist = conf['needCreatePlist']
    if (needCreatePlist == str(True)):
        l = ["ad-hoc","app-store","enterprise","development"]
        try:
            s=sign.split(':',1)[0].split(' ')[1]
        except IOError:
            print "Error: conf.ini文件里的 SIGN_IDENTITY 参数错误!"

        path = '%s/%s' % (get_path(),p)
        if os.path.isfile(path):
            replist = './revise_plist.sh %s %s %s %s' % (l[conf["index"]],bundleID,conf['provisioningProfiles'],s)
            os.system(replist)
        else:
            os.system('chmod u+x %s/revise_plist.sh'%(get_path()))
            os.system('chmod u+x %s/create_plist.sh'%(get_path()))
            os.system('chmod u+x %s/version.sh'%(get_path()))
            print 'plist文件不存在，开始创建plist文件！'
            explist = './create_plist.sh %s %s %s %s' % (l[conf["index"]],bundleID,conf['provisioningProfiles'],s)
            print explist
            os.system(explist)

    plistName = p if (needCreatePlist == str(True)) else  plistPath
    print plistName

    # 导出ipa
    export = 'xcodebuild  -exportArchive -archivePath %s -exportOptionsPlist %s/%s -exportPath %s/%s -allowProvisioningUpdates' %(xcarchivePath,get_path(),plistName,conf['targerIPA_path'],timeName)
    print(export)
    os.system(export)

    if (conf['needSendMail'] == str(True)):
        # 发邮件
        send_mail()
        pass

    filePath = '%s/%s' %(conf['targerIPA_path'],timeName)
    if conf['index'] is 0 or conf['index'] is 3 and (conf['needUpload'] == str(True)):
        uploadIPA = '%s/%s.ipa' % (filePath,conf['project_name'])
        os.system('chmod  u+x %s/UploadIPA.sh'%(get_path()))
        os.system('bash %s/UploadIPA.sh %s'%(get_path(),uploadIPA))
        pass
    else:
        os.system('open %s'%(filePath))



def get_path():
    path = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isfile(path):
        path =  os.path.dirname(path)
    return path;

def get_build_project_data():
    cf = ConfigParser.ConfigParser()
    cf.read('%s/conf.ini' % get_path())

    conf ={'project_path':cf.get('conf', 'project_path'),'project_name':cf.get('conf', 'Project_Name'),'workspace_Name':cf.get('conf', 'Workspace_Name'),'targerIPA_path':cf.get('conf', 'targerIPA_path'),'configuration':cf.get('conf', 'Configuration')}
    conf['needSendMail']=cf.getboolean('conf', 'needSendMail');
    conf['needUpload'] = cf.get('conf','needUpload');
    conf['needCreatePlist'] = cf.get('conf','needCreatePlist');

    # sh_path = '%s/rvm.sh' % get_path()
    # os.system('chmod  u+x %s'%(sh_path))
    # os.system('bash %s 1'%(sh_path))

    list = ["AdHoc","AppStore","Enterprise","Development"]

    print "~~~~~~~~~~~~选择打包方式(输入序号)~~~~~~~~~~~~~~~"
    for idx, val in enumerate(list):
        print("		 %s %s" % (idx, val))

    index = input("请输入序号: ");

    if index < 4:
        key = list[index];
        conf['type'] = key;
        conf['index'] = index;
        conf['provisioningProfiles'] = cf.get(key,'provisioningProfiles');

        build_project(conf,cf.get(key,'BundleID'),cf.get(key,'SIGN_IDENTITY'),cf.get(key,'PROVISIONING_PROFILE_NAME'),cf.get(key,'PlistPath'))
    else:
        print("无效序号!")



def main():
    # 从conf.ini文件中得到数据并开始编译导出
    get_build_project_data();


# 执行
main()
