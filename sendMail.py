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
import ConfigParser

def get_path():
    path = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isfile(path):
        path =  os.path.dirname(path)
    return path;

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

# 发邮件
def send_mail():
    cf = ConfigParser.ConfigParser()
    cf.read('%s/conf.ini' % get_path())

    from_addr = cf.get('Mail', 'from_addr')
    password = cf.get('Mail', 'password')
    smtp_server = cf.get('Mail', 'smtp_server')

    to_addrs = cf.get('Mail', 'to_addrs').split(',')
    sendText = cf.get('Mail', 'text')

    if len(sendText) is 0:
        text = "iOS测试项目于" + time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) + " 已经打包完毕，请前往 https://fir.im/ 下载测试！"
    else:
        text = sendText
        pass

    print(from_addr,password,smtp_server,to_addrs,type(to_addrs),text)

    msg = MIMEText(text, 'plain', 'utf-8')
    msg['From'] = _format_addr('自动打包系统 <%s>' % from_addr)
    # '%s' % ','.join([_format_addr('<%s>' % to_addr)for to_addr in to_addrs]) _format_addr('xx测试人员 <%s>' % to_addr)
    print('新的 <%s>' % ','.join([_format_addr('<%s>' % to_addr)for to_addr in to_addrs]));
    print('xx测试人员 <%s>' % to_addr);
    msg['To'] = 'xx测试人员 <%s>' % ','.join([_format_addr('<%s>' % to_addr)for to_addr in to_addrs])
    msg['Subject'] = Header('iOS客户端打包完成', 'utf-8').encode()
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
