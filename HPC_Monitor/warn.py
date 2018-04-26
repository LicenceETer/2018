#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

HOST = "jt-mail"
SUBJECT = u" "
TO = "test@qq.com"
FROM = "test@gmail.com"

def addimg(src,imgid):
    fp = open(src,'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID',imgid)
    return msgImage
    pass

msg = MIMEMultipart('related')
msgtext = sys.argv[1]
msg.attach(msgtext)
msg.attach(addimg("/python/HPC_Monitor/HPC_Status.png","status"))

msg['Subject'] = SUBJECT
