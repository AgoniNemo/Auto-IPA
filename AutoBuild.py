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
    sendMail.send_mail()

# 上传到蒲公英
def uploadPGYer(path,apiKey,updateDescription=''):
    os.popen("curl -F 'file=@%s' -F '_api_key=%s' -F 'updateDescription=%s' https://www.pgyer.com/apiv2/app/upload"%(path,apiKey,updateDescription))
    os.system("open https://www.pgyer.com/my")

# 导出ipa
def exportIPA(xcarchivePath,plistPath,exportPath):
    export = 'xcodebuild -exportArchive -archivePath %s -exportOptionsPlist %s -exportPath %s -allowProvisioningUpdates' %(xcarchivePath,plistPath,exportPath)
    print(export)
    os.system(export)

# 导出xcarchive
def build_project(conf,bundleID,sign,pName,plistPath):
    
    timeName = time.strftime('%Y年%m月%d日-%H-%M-%S',time.localtime(time.time()))
    
    xcworkPath = '%s/%s.xcworkspace' %(conf['project_path'],conf['workspace_Name'])
    xcarchivePath = '%s/%s/%s_%s.xcarchive' %(conf['targerIPA_path'],timeName,conf['ProjectName'],conf['type'])
    
    scheme = conf['ProjectName']
    
    # 导出xcarchive
    build = 'xcodebuild -workspace %s -scheme %s -configuration %s -archivePath %s clean archive build' %(xcworkPath,scheme,conf['configuration'],xcarchivePath)
    
    if (conf['automatic'] == str(False)):
        string = ' CODE_SIGN_IDENTITY="%s" PROVISIONING_PROFILE="%s" PRODUCT_BUNDLE_IDENTIFIER="%s"'%(sign,pName,bundleID)
        build = build + string

    build = build + ' || exit 1'
    os.system(build)
    print(build)

    # 自动生成的plist文件名
    p = 'TeamExportOptionsPlist.plist' if (conf['automatic'] == str(True)) else 'ExportOptionsPlist.plist'
    print ("plist文件名:%s"%p)
    # 导出plist文件
    needCreatePlist = conf['needCreatePlist']
    if (needCreatePlist == str(True)):
        l = ["ad-hoc","app-store","enterprise","development"]
        try:
            s=sign.split(':',1)[0].split(' ')[1]
        except IOError:
            print("Error: conf.ini文件里的 SIGN_IDENTITY 参数错误!")
        
        path = '%s/%s' % (get_path(),p)
        print(path)
        if os.path.isfile(path):
            replist = './revise_plist.sh %s %s %s %s %s' % (p,l[conf["index"]],bundleID,conf['ProvisioningProfiles'],s)
            print("修改 %s" % replist)
            os.system(replist)
        else:
            t = '_team' if (conf['automatic'] == str(True)) else ''
            
            os.system('chmod u+x %s/revise%s_plist.sh'%(get_path(),t))
            os.system('chmod u+x %s/create%s_plist.sh'%(get_path(),t))
            print('plist文件不存在，开始创建plist文件！')
            explist = './create%s_plist.sh %s' % (t,l[conf["index"]])
            if (conf['automatic'] == str(True)):
                explist = '%s %s %s %s %s %s'%(explist,conf['teamID'],bundleID,conf['ProvisioningProfiles'],conf['enableCompileBitcode'].lower(),conf['compileBitcode'].lower())
            else:
                explist = "%s %s %s %s %s %s"%(explist,bundleID,conf['ProvisioningProfiles'],s,conf['enableCompileBitcode'].lower(),conf['compileBitcode'].lower())
            print(explist)
            os.system(explist)

    plistName = p if (needCreatePlist == str(True)) else  plistPath
    print ("--%s--"%(plistName))

    # 导出ipa
    # export = 'xcodebuild  -exportArchive -archivePath %s -exportOptionsPlist %s/%s -exportPath %s/%s -allowProvisioningUpdates' %(xcarchivePath,get_path(),plistName,conf['targerIPA_path'],timeName)
    # print(export)
    # os.system(export)

    plistp = '%s/%s'%(get_path(),plistName)
    exportp = '%s/%s'%(conf['targerIPA_path'],timeName)
    # 导出ipa
    exportIPA(xcarchivePath,plistp,exportp)
    
    if(conf['type'] == 'AppStore'):
        os.system('chmod  u+x ./BundleVersion.sh')
        os.system('./BundleVersion.sh %s'%(conf['plist_path']))
    
    if (conf['needSendMail'] == str(True)):
        # 发邮件
        send_mail()
        pass

    filePath = '%s/%s' %(conf['targerIPA_path'],timeName)
    if (conf['index'] is 0 or conf['index'] is 3):
        name = conf['ProjectName']
        print('===%s==='%(name))
        
        uploadIPA = '%s/%s.ipa' % (filePath,name)
        
        if (conf['uploadFir'] == str(True)):
            os.system('chmod  u+x %s/UploadIPA.sh'%(get_path()))
            os.system('bash %s/UploadIPA.sh %s %s'%(get_path(),uploadIPA,conf['FIRToken']))
        
        if (conf['uploadPGYer'] == str(True)):
            uploadPGYer(uploadIPA,conf['APIKey'],'版本更新')

        if (conf['uploadCustom'] == str(True)):
            os.system('chmod  u+x %s/CustomUpload.sh'%(get_path()))
            os.system('bash %s/CustomUpload.sh %s'%(get_path(),uploadIPA))

    else:
        os.system('open %s'%(filePath))

# 获取当前路径
def get_path():
    path = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isfile(path):
        path =  os.path.dirname(path)
    return path

# 读取配置文件
def get_build_project_data():
    cf = ConfigParser.ConfigParser()
    cf.read('%s/conf.ini' % get_path())
    
    conf ={'project_path':cf.get('conf', 'project_path'),'workspace_Name':cf.get('conf', 'Workspace_Name'),'targerIPA_path':cf.get('conf', 'targerIPA_path'),'configuration':cf.get('conf', 'Configuration')}
    conf['needSendMail']=cf.getboolean('conf', 'needSendMail')
    conf['needCreatePlist'] = cf.get('conf','needCreatePlist')
    conf['teamID'] = cf.get('conf','teamID')
    conf['APIKey'] = cf.get('conf','APIKey')
    conf['FIRToken'] = cf.get('conf','FIRToken')
    conf['automatic'] = cf.get('conf','automatic')
    conf['uploadFir'] = cf.get('conf','uploadFir')
    conf['uploadPGYer'] = cf.get('conf','uploadPGYer')
    conf['uploadCustom'] = cf.get('conf','uploadCustom')
    conf['plist_path'] = cf.get('conf','plist_path')
    conf['enableCompileBitcode'] = cf.get('InfoPlist','enableCompileBitcode')
    conf['compileBitcode'] = cf.get('InfoPlist','compileBitcode')
    
    # sh_path = '%s/rvm.sh' % get_path()
    # os.system('chmod  u+x %s'%(sh_path))
    # os.system('bash %s 1'%(sh_path))
    
    list = ["AdHoc","AppStore","Enterprise","Development"]
    
    print("~~~~~~~~~~~~选择打包方式(输入序号)~~~~~~~~~~~~~~~")
    for idx, val in enumerate(list):
        print("      %s %s" % (idx, val))

    index = 4

    if len(sys.argv) > 1:
        index = int(sys.argv[1])
        pass
    else:
        index = input("请输入序号: ")
        pass

    if index < 4:
        key = list[index]
        conf['type'] = key
        conf['index'] = index
        conf['ProvisioningProfiles'] = cf.get(key,'ProvisioningProfiles')
        conf['ProjectName'] = cf.get(key,'ProjectName')
        
        build_project(conf,cf.get(key,'BundleID'),cf.get(key,'SIGN_IDENTITY'),cf.get(key,'PROVISIONING_PROFILE_NAME'),cf.get(key,'PlistPath'))
    else:
        print("无效序号!")



def main():
    # 从conf.ini文件中得到数据并开始编译导出
    get_build_project_data()


# 执行
main()
