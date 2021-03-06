# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #

import os, json, shutil,glob
import baseEx


# 安全的获取指定文件内的content,返回str。出错则返回None
def safeGetFileContentStr(fileName, isNeedPrint = False):
	if not baseEx.validateString(fileName):
		return None
	if not os.path.isfile(fileName):
		return None
	try:
		fileFp = open(fileName, "r+")
	except:
		if isNeedPrint:
			print "Error: open file %s error. " % fileName
		return None

	try:
		fileData = fileFp.read()
	except:
		if isNeedPrint:
			print "Error: open file %s error." % fileName
		fileFp.close()
		return None
	fileFp.close()
	return fileData


# 安全的获取指定文件内的content,并转换为json返回。出错则返回None
def safeGetFileContentJSON(fileName, isNeedPrint = False):
	retStr = safeGetFileContentStr(fileName, isNeedPrint)
	if not baseEx.validateString(retStr):
		if isNeedPrint:
			print "Error: file %s is empty." % fileName
		return None
	try:
		# 注意,json解析后,所有的 str类型都转换为了 Unicode类型
		ret = json.loads(retStr)
	except:
		if isNeedPrint:
			print "Error: json encode file %s error." % fileName
		return None
	return ret


def safeWriteFileContentStr(fileName, content, isNeedPrint = False):
	ret = True
	if not baseEx.validateString(content):
		return False

	try:
		writerFileFP = open(fileName, "w")
	except:
		if isNeedPrint:
			print "Error:writer open file %s error." % fileName
		return False

	try:
		writerFileFP.write(content)
	except:
		if isNeedPrint:
			print "Error: writer file %s error." % fileName
		ret = False
	finally:
		writerFileFP.close()
	return ret


def safeWriteFileContentJSON(fileName, obj, needFormat = True, isNeedPrint = False):
	try:
		if needFormat:
			contentJsonStr = json.dumps(obj, indent = 4)
		else:
			contentJsonStr = json.dumps(obj)
	except:
		if isNeedPrint:
			print "Error: writer file %s error." % fileName
		return ret

	if baseEx.validateString(contentJsonStr):
		return safeWriteFileContentStr(fileName, contentJsonStr, isNeedPrint)
	else:
		return False


# 清空文件夹,支持多层文件夹创建
def safeClearDir(dirPath):
	if not baseEx.validateString(dirPath):
		return False
	else:
		if os.path.isdir(dirPath):
			shutil.rmtree(dirPath)
		try:
			os.makedirs(dirPath)
		except:
			return False
		return True


# 如果存在那就不创建,否则就创建该文件夹.会递归创建路径中缺失的所有文件夹
def safeCreateDir(dirPath):
	if not baseEx.validateString(dirPath):
		return False
	else:
		if os.path.isdir(dirPath):
			return False
		try:
			os.makedirs(dirPath)
		except:
			return False
		return True


def safeRemovePath(path):
	if not baseEx.validateString(path):
		return False
	if os.path.isfile(path):
		os.remove(path)
		return True
	if os.path.isdir(path):
		shutil.rmtree(path)
		return True
	return False


def fileDirIsEmpty(sourceDir):
	if not os.path.isdir(sourceDir):
		return False
	fileList = os.listdir()
	if len(fileList) == 0:
		return True
	else:
		return False


# 文件夹复制操作
# targetDir必须是确切的路径
def safeMoveDir(sourceDir, targetDir):
	if not baseEx.validateString(sourceDir) or not baseEx.validateString(targetDir):
		return False
	if not os.path.isdir(sourceDir):
		return False
	if not os.path.exists(targetDir) or (os.path.isdir(targetDir) and fileDirIsEmpty(targetDir)):
		try:
			os.rename(sourceDir, targetDir)
		except:
			return False
		return True
	return False

# 允许覆盖目的地同名文件
# targetFile必须是确切的路径
def safeMoveFile( sourceFile,targetFile ):
	if not baseEx.validateString(sourceFile) or not baseEx.validateString(targetFile):
		return False
	if not os.path.isfile(sourceFile):
		return False
	if os.path.isdir(targetFile):
		return False
	try:
		os.rename(sourceFile,targetFile)
	except:
		return False
	return True

# 合并源文件夹到目标文件夹中
# 覆盖性合并
def mergeDirToDst(sourceDir,targetDir):
	if not baseEx.validateString(sourceDir) or not baseEx.validateString(targetDir):
		return False
	if not os.path.isdir(sourceDir):
		return False
	if os.path.isfile(targetDir):
		return False
	if not os.path.isdir(targetDir):
		os.mkdir(targetDir)
	for fileName in os.listdir(sourceDir):
		sourceName = sourceDir + "/" + fileName
		dstName = targetDir + "/" + fileName
		safeMoveFile(sourceName,dstName)
	return True

# 文件copy操作
# 要求必须写全路径名和文件名
# 覆盖性写入
def safeCopyFile(sourceFile,targetFile):
	if not baseEx.validateString(sourceFile) or not baseEx.validateString(targetFile):
		return False
	if not os.path.isfile(sourceFile):
		return False
	if os.path.isdir(targetFile):
		return False
	try:
		shutil.copyfile(sourceFile, targetFile)
	except:
		return False
	return True

# 文件copy到指定文件夹中
def safeCopyFileToDir(sourceFile,targetDir):
	if not baseEx.validateString(sourceFile) or not baseEx.validateString(targetDir):
		return False
	if not os.path.isfile(sourceFile):
		return False
	if not os.path.isdir(targetDir):
		return False
	try:
		shutil.copy(sourceFile,targetDir)
	except:
		return False
	return True

# 安全的copy文件夹到指定的位置,指定位置必须不能存在同名文件夹
def safeCopyDirToNewDir(sourceDir,targetDir):
	if not baseEx.validateString(sourceDir) or not baseEx.validateString(targetDir):
		return False
	if not os.path.exists(sourceDir):
		return False
	if os.path.exists(targetDir):
		return False
	try:
		shutil.copytree(sourceDir,targetDir)
	except:
		return False
	return True

# copy指定目录下所有文件到一个已存在的文件夹中,
# 覆盖性写入
def safeCopyDirToDir(sourceDir,targetDir):
	if not baseEx.validateString(sourceDir) or not baseEx.validateString(targetDir):
		return False
	if not os.path.exists(sourceDir):
		return False
	if os.path.isfile(targetDir):
		return False
	if not os.path.isdir(targetDir):
		os.makedirs(targetDir)
	for fileName in os.listdir(sourceDir):
		sourceName = sourceDir + "/" + fileName
		dstName = targetDir + "/" + fileName
		safeCopyFile(sourceName, dstName)
	return True

# 创建软链接文件,文件和文件夹通用
# 覆盖性写入
def safeSymbolLink(src,dst,isNeedCover = True):
	# 由于这里的路径必须是dst所在文件夹为基准的相对路径,所以不具备参考价值
	# if not os.path.exists(src):
	# 	return False
	if os.path.exists(dst):
		if isNeedCover:
			safeRemovePath(dst)
		else:
			return False
	os.symlink(src,dst)
	return True


# [非递归]返回指定文件夹下的所有文件夹,是否需要隐藏文件可以指定,是否需要路径可以指定
def getAllDirsInSpecialDir(specifyDirName ,needPathName = False, needHideElement = True):
	if not baseEx.validateString(specifyDirName):
		return None
	if not os.path.isdir(specifyDirName):
		return None
	resultList = []
	subLeafList = os.listdir(specifyDirName)
	for element in subLeafList:
		if os.path.isdir(specifyDirName + "/" + element):
			if element.find(".") == 0 and needHideElement:
				continue
			if needPathName:
				resultList.append(specifyDirName + "/" + element)
			else:
				resultList.append(element)
	return resultList

# [非递归]返回指定文件夹下的所有文件,是否需要隐藏文件可以指定,是否需要路径可以指定
def getAllFilesInSpecialDir(specifyDirName ,needPathName = False, needHideElement = True):
	if not baseEx.validateString(specifyDirName):
		return None
	if not os.path.isdir(specifyDirName):
		return None
	resultList = []
	subLeafList = os.listdir(specifyDirName)
	for element in subLeafList:
		if os.path.isfile(specifyDirName + "/" + element):
			if element.find(".") == 0 and needHideElement:
				continue
			if needPathName:
				resultList.append(specifyDirName + "/" + element)
			else:
				resultList.append(element)
	return resultList

def recursionGetAllDirInSpecialDir(specifyDirName ,needPathName = False, needHideElement = True):
	if not baseEx.validateString(specifyDirName):
		return None
	if not os.path.isdir(specifyDirName):
		return None
	resultList = []
	subLeafList = os.listdir(specifyDirName)
	for element in subLeafList:
		if os.path.isdir(specifyDirName + "/" + element):
			if element.find(".") == 0 and needHideElement:
				continue
			if needPathName:
				resultList.append(specifyDirName + "/" + element)
			else:
				resultList.append(element)
			subList = recursionGetAllDirInSpecialDir( specifyDirName + "/" + element,needPathName,needHideElement )
			resultList.extend(subList)
	return resultList

def recursionGetSpecialFilesInSpecialDir(specifyDirName ,formatStr ,needPathName = False, needHideElement = True):
	if not baseEx.validateString(specifyDirName):
		return None
	if not os.path.isdir(specifyDirName):
		return None
	subDirResultList = recursionGetAllDirInSpecialDir(specifyDirName,True)
	dirResultList = [specifyDirName]
	resultList = []
	if baseEx.validateList(subDirResultList):
		dirResultList.extend(subDirResultList)
	for element in dirResultList:
		sourceSubList = glob.glob(element + "/" + formatStr)
		subList = []
		if baseEx.validateList(sourceSubList):
			for filePath in sourceSubList:
				if not os.path.isfile(filePath):
					continue
				if needHideElement and os.path.basename(filePath)[0] == ".":
					continue
				if not needPathName:
					subList.append(os.path.basename(filePath))
				else:
					subList.append(filePath)
		resultList.extend(subList)
	return resultList


