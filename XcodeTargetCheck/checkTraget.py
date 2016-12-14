# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #

# 邮件相关头文件
import smtplib
from email.mime.text import MIMEText
# 本地文件操作
import CJFKit,time,commands,sys

reload(sys)
sys.setdefaultencoding('utf-8')

# 执行git仓库更新
# 校验target是否存在
# 拉取git最近的git更新记录
# 发送邮件通知

#---------------------------------- 全局变量区域 ---------------------------------

# 监测间隔
global_check_time = 580						# 时间间隔，second
global_git_log_time = 20					# git 拉取记录的时间，min

# 邮箱全局变量配置区域
global_mail_host = "smtp.163.com"            # 使用的邮箱的smtp服务器地址，这里是163的smtp地址
global_mail_user = "xxxxxxx"                 # 用户名
global_mail_pass = "xxxxxxx"                 # 密码,网易规定必须使用授权码
global_mail_postfix = "163.com"              # 邮箱的后缀，网易就是163.com
global_mail_user_name = "xxx"

# 接收方邮件全局配置
global_mail_receive_list = ["asdadadad@163.com","asdqfrgvtef@163.com"]		# 此处仅为示例

# 本地文件记录全局变量配置区域
global_log_dirName = "./CheckScriptLog"

# 项目配置文件path
global_pbxproj_path = "xxx.xcodeproj/project.pbxproj"			#相对路径
global_project_path = "/Users/chengjianfeng/Desktop/xxxxx"		#绝对路径

# 带中文的target必须将str标为 Unicode,以下均为示例
global_target_list = ["CJFTest","CJFTestWatch","CJFTestWatchExtension",u"今日Extension"]

#---------------------------------- 全局函数区域 ---------------------------------

def send_mail(to_list, sub, content):
	global global_mail_host
	global global_mail_user
	global global_mail_pass
	global global_mail_postfix
	global global_mail_user_name

	# 常规项配置内容
	mail_host = global_mail_host
	mail_user = global_mail_user
	mail_pass = global_mail_pass
	mail_postfix = global_mail_postfix
	mail_user_name = global_mail_user_name

	# 邮件发送代码
	me = mail_user_name + "<" + mail_user + "@" + mail_postfix + ">"
	msg = MIMEText(content, _subtype = 'plain',_charset = 'utf-8')
	if not isinstance(sub,unicode):
		sub = unicode(sub)
	msg['Subject'] = sub
	msg['From'] = me
	msg['To'] = ";".join(to_list)                		# 将收件人列表以‘；’分隔
	msg["Accept-Language"]="zh-CN"
	msg["Accept-Charset"]="ISO-8859-1,utf-8"
	try:
		server = smtplib.SMTP()
		server.connect(mail_host)                        # 连接服务器
		server.login(mail_user, mail_pass)               # 登录操作
		server.sendmail(me, to_list, msg.as_string())
		server.close()
		return True
	except Exception, e:
		print "邮件发送失败：%s" % (str(e))
		return False

#---------------------------------- 全局类定义区域 ---------------------------------


#---------------------------------- 正式代码区域 ---------------------------------

if __name__ == "__main__":
	if not CJFKit.validateList(global_target_list):
		print "警告:暂无崩溃监控对象"
		exit(-1)

	print "开始监控target程序"
	CJFKit.safeCreateDir(global_log_dirName)

	while True:
		cmd_git_update = "cd " + global_project_path + " && " + "git pull"
		cmd_git_log = "cd " + global_project_path + " && " + 'git log --since "' + str(global_git_log_time) + ' minutes ago"'

		commands.getoutput(cmd_git_update)

		nowTimeStr = CJFKit.getNowTimeStr()
		check_fail_list = []
		project = CJFKit.XcodeProject.Load(global_project_path + "/" + global_pbxproj_path )
		for targetName in global_target_list:
			targetObj = project.get_target_by_name(targetName)
			if not targetObj:
				check_fail_list.append(targetName)

		if not CJFKit.validateList(check_fail_list):
			print "%s:target校验正常" % (nowTimeStr)
			time.sleep(global_check_time)
		else:
			logStr = commands.getoutput(cmd_git_log)
			if CJFKit.validateString(logStr):
				logStr = CJFKit.getNowTimeStr() + u":发生校验不合格事件。\n被误删的tragte为:" + ",".join(check_fail_list) + u"\n\ngit提交日志如下:\n" + "--------------------------------------------\n\n" + logStr + u"\n\n--------------------------------------------\n" 
			else:
				logStr = CJFKit.getNowTimeStr() + u":发生校验不合格事件。\n被误删的tragte为:" + ",".join(check_fail_list)

			# 邮件通知
			for receiver_address in global_mail_receive_list:
				mail_subject = u"代码target校验不合格告警"
				mail_conetnt = logStr
				sendSuc = send_mail(mailto_list1, mail_subject, mail_conetnt)
				if sendSuc:
				print "%s:发生 %s 被误删情况,已经成功向 %s 发送邮件通知" % (nowTimeStr,",".join(check_fail_list),receiver_address)
			else:
				print "%s:发生 %s 被误删情况,向 %s 发送邮件通知失败" % (nowTimeStr,",".join(check_fail_list),receiver_address)

			# 写入日志
			writerSuc = CJFKit.safeWriteFileContentStr(global_log_dirName + "/" + CJFKit.getValidateFileNameByNowStr() ,logStr)
			if writerSuc:
				print "%s:发生 %s 被误删情况,已经成功写入log" % (nowTimeStr,",".join(check_fail_list))
			else:
				print "%s:发生 %s 被误删情况,写入log失败" % (nowTimeStr,",".join(check_fail_list))
			break

	print "监控target程序执行结束"
