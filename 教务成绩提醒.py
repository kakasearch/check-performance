#获取课程代码，已获取完毕
#写一个下载器，功能：自定义headers,cookie,session,不要重复下载，多线程下载
#获取全部文件的下载url
#传递给下载器，修改保存代码，从url获取文件后缀



import swjtu_jw_login
import requests
import re,os
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


with open('./users_configs.txt',encoding='utf-8')as f:
	usrs  = f.readlines()
user = []
for f in usrs:
	user.append(tuple([x.replace('\n','') for x in f.split(',')]))



#
def send_email(receivers,subject='test',content='测试内容'):
    sender = 'yxtk2019@163.com'#
    passWord = 'USWCJWITXRUQPGKL'
    mail_host = 'smtp.163.com'
    #receivers是邮件接收人，用列表保存，可以添加多个
    

    #设置email信息
    msg = MIMEMultipart()
    #邮件主题
    msg['Subject'] = subject#input(u'请输入邮件主题：')
    #发送方信息
    msg['From'] = sender
    #邮件正文是MIMEText:
    msg_content = content#input(u'请输入邮件主内容:')
    msg.attach(MIMEText(msg_content, 'plain', 'utf-8'))
    try:
        s = smtplib.SMTP_SSL(mail_host, 465)
        s.set_debuglevel(1)
        s.login(sender,passWord)
        #给receivers列表中的联系人逐个发送邮件
        for item in receivers:
            msg['To'] = to = item
            s.sendmail(sender,to,msg.as_string())
            print('Success!')
        s.quit()
        print ("All emails have been sent over!")
        return True
    except smtplib.SMTPException as e:
        print ("Falied,%s",e)
        return False

def check(username,password,email_):
	login = swjtu_jw_login.login(username,password)
	session = login.session

	####查看成绩
	headers={
	            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
	            'Accept-Encoding': 'gzip, deflate',
	            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
	            'Cache-Control': 'max-age=0',
	            'Connection': 'keep-alive',
	            #'Cookie': `JSESSIONID=${Sid}; username=${username}`,//SESSIONID和学号
	            'Host': 'jwc.swjtu.edu.cn',
	            'Upgrade-Insecure-Requests': '1',
	            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
	        }


	chengji_url = 'http://jwc.swjtu.edu.cn/vatuu/StudentScoreInfoAction?setAction=studentScoreQuery&viewType=studentScore&orderType=submitDate&orderValue=desc'

	r = session.get(chengji_url,headers=headers)

	trs = re.findall(r'<tr>.*?</tr>',r.text.replace('\t','').replace('  ','').replace('\n',''))
	path = './成绩记录_'+username+'.txt'
	try:
		with open(path,'r',encoding='utf-8')as f:
			has_data = f.read()
			first_run = 0
	except:
		has_data = ''
		first_run = 1
	for tr in trs[5:]:
		tds = re.findall(r'<td >(.*?)</td>',tr)
		name = tds[2]
		total = ''.join(re.findall(r'\S',tds[5]))
		end = tds[6]
		mid = tds[7]
		cj_str ='科目： '+name+'\n'+'总成绩： '+total+'\n'+'期末成绩： '+end+'\n'+'期中成绩： '+mid+'\n'
		#检查
		if cj_str not in has_data:
			if not first_run:
				send_email(receivers = [email_],subject='教务网成绩跟新提醒',content=cj_str)
			with open(path,'a+',encoding='utf-8')as f:
				f.write(cj_str+'\n')



for username,password,email_ in user:
	print('开始检查',username)
	check(username,password,email_)

