import os
import smtplib
#import mandrill

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import COMMASPACE,formatdate
from email import encoders

g_cap_mail="CAP@thomsonreuters.com"

def send_mail(fro, to, subject, text, files=[]):
    #assert type(server) == dict 
    assert type(to) == list
    assert type(files) == list
    
    msg = MIMEMultipart('alternative')
    
    msg['Subject'] = subject
    msg['From'] = 'CAP_team@thomsonreuters.com' # Your from name and email address
    msg['To'] = ','.join(to)
    #print msg['To']
    msg['Date'] = formatdate(localtime=True)
    msg.attach(MIMEText(text, 'html', 'utf-8'))
    
    for file in files:
        data = open(file, 'rb')
        part = MIMEBase('application', 'octet-stream') #'octet-stream': binary data 
        part.set_payload(data.read()) 
        data.close()
        encoders.encode_base64(part) 
        part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file)) 
        msg.attach(part)
        
    s = smtplib.SMTP('10.80.81.132', 25)    
    #s.login(username, password)
    s.sendmail(fro, to, msg.as_string())
    s.quit()
    
    ''' mandrill web api way
    try:
        mandrill_client = mandrill.Mandrill('ElZncQlS9DXqotj0TMjuJA')
        #to = ['chao.xie@thomsonreuters.com', 'yang.yang@thomsonreuters.com']
        raw_message = msg.as_string()
        #print raw_message
        result = mandrill_client.messages.send_raw(raw_message, from_email=None, from_name='Chao Xie', to=None, async=False, ip_pool='Main Pool', send_at=None, return_path_domain=None)

    except mandrill.Error, e:
        # Mandrill errors are thrown as exceptions
        print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
        # A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'    
        raise
    '''
    
if __name__ == "__main__":
    fro = 'chao.xie@thomsonreuters.com'
    to1 = ['chao.xie@thomsonreuters.com','yingjie.liu@thomsonreuters.com','liang.zhang1@thomsonreuters.com']#"chao.xie@thomsonreuters.com", "yingjie.liu@thomsonreuters.com", "liang.zhang1@thomsonreuters.com"]
    to = ['chao.xie@thomsonreuters.com']
    subject = "Python email test"
    text = '<b>HTML content</b><br><a href="http://www.baidu.com">baidu</a>'
    files = ['C:\Users\u0147926\Pictures\DATA_ART_Wallpaper_WallPaper_12_1680x1050.jpg', 'E:\work\CAP\CAP\publish.py']
    send_mail(fro, to, subject, text, files)
