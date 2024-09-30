# -*- coding: utf-8 -*-
from ast import If
import os
import sys
import time
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import sendMail
import configparser

# 发邮件
def send_mail():
    sendMail.send_mail()

# 上传到蒲公英
def uploadPGYer(path,apiKey,updateDescription=''):
    os.popen("curl -F 'file=@%s' -F '_api_key=%s' -F 'updateDescription=%s' https://www.pgyer.com/apiv2/app/upload"%(path,apiKey,updateDescription)).read()
    os.system("open https://www.pgyer.com/my")

# 导出ipa
def exportIPA(xcarchivePath,plistPath,exportPath):
    export = 'xcodebuild -exportArchive -archivePath %s -exportOptionsPlist %s -exportPath %s -allowProvisioningUpdates' %(xcarchivePath,plistPath,exportPath)
    print(export)
    os.system(export)

# 导出xcarchive
def build_project(conf):
    bundleID=conf['BundleID']
    sign=conf['SIGN_IDENTITY']
    pName=conf['PROVISIONING_PROFILE_NAME']
    plistPath=conf['PlistPath']
    timeName = time.strftime('%Y年%m月%d日-%H-%M-%S',time.localtime(time.time()))
    
    xcworkPath = '%s/%s.xcworkspace' %(conf['project_path'],conf['workspace_Name'])
    xcarchivePath = '%s/%s/%s_%s.xcarchive' %(conf['targerIPA_path'],timeName,conf['ProjectName'],conf['type'])
    
    scheme = conf['ProjectName']
    
    # 判断是个人账号还是公司账号
    isTeam = (len(conf['teamID']) > 0)

    # 导出xcarchive
    build = 'xcodebuild -workspace %s -scheme %s -configuration %s -archivePath %s clean archive build' %(xcworkPath,scheme,conf['configuration'],xcarchivePath)
    
    if ((conf['automatic'] == str(False)) & bool(1-isTeam)):
        string = ' CODE_SIGN_IDENTITY="%s" PROVISIONING_PROFILE="%s" PRODUCT_BUNDLE_IDENTIFIER="%s"'%(sign,pName,bundleID)
        build = build + string

    build = build + ' || exit 1'
    os.system(build)
    print(build)

    # 自动生成的plist文件名
    p = 'TeamExportOptionsPlist.plist' if (isTeam) else 'ExportOptionsPlist.plist'
    print ("plist文件名:%s"%p)
    # 导出plist文件
    needCreatePlist = conf['needCreatePlist']
    if (needCreatePlist == str(True)):
        #l = ["ad-hoc","app-store-connect","enterprise","development","app-store-connect"]
        try:
            s=sign.split(':',1)[0].split(' ')[1]
        except IOError:
            print("Error: conf.ini文件里的 SIGN_IDENTITY 参数错误!")
        
        path = '%s/%s' % (get_path(),p)
        print(path)
        if os.path.isfile(path):
            replist = './revise_plist.sh %s %s %s %s %s' % (p,conf["BundleType"],bundleID,conf['ProvisioningProfiles'],s)
            print("修改 %s" % replist)
            os.system(replist)
        else:
            t = '_team' if (isTeam) else ''
            
            os.system('chmod u+x %s/revise%s_plist.sh'%(get_path(),t))
            os.system('chmod u+x %s/create%s_plist.sh'%(get_path(),t))
            print('plist文件不存在，开始创建plist文件！')
            explist = './create%s_plist.sh %s' % (t,conf["BundleType"])
            if (isTeam):
                explist = '%s %s %s %s %s %s'%(explist,conf['teamID'],bundleID,conf['ProvisioningProfiles'],conf['enableCompileBitcode'].lower(),conf['compileBitcode'].lower())
            else:
                explist = "%s %s %s %s %s %s"%(explist,bundleID,conf['ProvisioningProfiles'],s,conf['enableCompileBitcode'].lower(),conf['compileBitcode'].lower())
            print(explist)
            os.system(explist)

    plistName = p if (needCreatePlist == str(True)) else  plistPath
    print ("--%s--"%(plistName))

    plistp = '%s/%s'%(get_path(),plistName)
    exportp = '%s/%s'%(conf['targerIPA_path'],timeName)
    # 导出ipa
    exportIPA(xcarchivePath,plistp,exportp)
    type = conf['type']
    
    if(type == 'AppStore'):
        os.system('chmod  u+x ./BundleVersion.sh')
        project_path = '%s/%s'%(conf['project_path'],conf['workspace_Name'])
        shell = './BundleVersion.sh %s %s %s %s' % (project_path,scheme,conf['VersionReleaseUuid'],conf['VersionDebugUuid'])
        print(shell)
        os.system(shell)
    
    if (conf['needSendMail'] == str(True)):
        # 发邮件
        send_mail()
        pass

    name = conf['ProjectName']
    dirPath = '%s/%s/%s' %(conf['targerIPA_path'],timeName,name)
    filePath = '%s.ipa' %(dirPath)
    print('===filePath %s==='%(name))

    if (conf['index'] == 0 or conf['index'] == 3):
        if (conf['uploadFir'] == str(True)):
            os.system('chmod  u+x %s/UploadIPA.sh'%(get_path()))
            os.system('bash %s/UploadIPA.sh %s %s'%(get_path(),filePath,conf['FIRToken']))
        
        if (conf['uploadPGYer'] == str(True)):
            uploadPGYer(filePath,conf['APIKey'],'版本更新')

        if (conf['uploadCustom'] == str(True)):
            os.system('chmod  u+x %s/CustomUpload.sh'%(get_path()))
            os.system('bash %s/CustomUpload.sh %s'%(get_path(),filePath))

    else:
        if conf['index'] == 1:
            userName = conf['loaderUserName']
            password = conf['loaderPassword']
            print('====userName====%s %s %s %s'%(userName,len(userName), len(password),dirPath))
            if len(userName) > 0 and len(password) > 0:
                os.system('chmod  u+x %s/UploadAppStore.sh'%(get_path()))
                os.system('bash %s/UploadAppStore.sh %s %s %s'%(get_path(),userName,password))
            else:
                os.system('open %s'%(dirPath))
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
    cf = configparser.ConfigParser()
    cf.read('%s/conf.ini' % get_path())
    
    conf = {
        'project_path':cf.get('conf', 'project_path'),
        'workspace_Name':cf.get('conf', 'Workspace_Name'),
        'targerIPA_path':cf.get('conf', 'targerIPA_path'),
        'configuration':cf.get('conf', 'Configuration')
        }
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
    conf['loaderUserName'] = cf.get('AppStore','loaderUserName')
    conf['loaderPassword'] = cf.get('AppStore','loaderPassword')
    
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
        conf['BundleType'] = cf.get(key,'BundleType')
        conf['BundleID'] = cf.get(key,'BundleID')
        conf['SIGN_IDENTITY'] = cf.get(key,'SIGN_IDENTITY')
        conf['PROVISIONING_PROFILE_NAME'] = cf.get(key,'PROVISIONING_PROFILE_NAME')
        conf['PlistPath'] = cf.get(key,'PlistPath')
        conf['VersionReleaseUuid'] = cf.get(key,'VersionReleaseUuid')
        conf['VersionDebugUuid'] = cf.get(key,'VersionDebugUuid')
        build_project(conf)
    else:
        print("无效序号!")



def main():
    # 从conf.ini文件中得到数据并开始编译导出
    get_build_project_data()


# 执行
main()
