import os
import re
import json

curpath = os.getcwd()
datapath = curpath + "/androidx-class-mapping.csv"
count = 0

skips = ["/.git/", "/.gradle/", "/.idea/", "/build/generated/", "/build/intermediates/", "/build/kotlin/",
         "/build/outputs/", "/build/tmp/"]
fileSuffix = [".java", ".kt", ".gradle", ".xml", ".pro", ".txt", ".cfg"]



def getMapData():
    result = []
    table = {}
    for line in iter(open(datapath,encoding='utf-8')):
        temp = line.split(',')
        table = {}
        table["from"] = temp[0]
        table["to"] = temp[1].rstrip('\n')
        result.append(table)
    return result[1:]


def isSupportMigrate(path):
    for dir in skips:
        if (path.__contains__(dir)):
            return False
    for file in fileSuffix:
        if (path.__contains__(file)):
            return True
    return False


def skipDir(path):
    for dir in skips:
        if (path.__contains__(dir)):
            return True
    return False


def getAllFiles(path):
    files = []
    dirs = os.listdir(path)
    for filepath in dirs:
        if (os.path.isdir(path + "/" + filepath) and not skipDir(path + "/" + filepath)):
            print("Scanning " + path + "/" + filepath)
            for file in getAllFiles(path + "/" + filepath):
                if (isSupportMigrate(file)):
                    files.append(file)
        elif (isSupportMigrate(path + "/" + filepath)):
            files.append(path + "/" + filepath)
    return files


def replaceAndroidX(line, configs):
    for config in configs:
        if ("from" in config and line.__contains__(config["from"])):
            line = line.replace(config["from"], config["to"])
    return line


def replaceSupport(file, configs):
    content = ""
    needReWrite = False
    print('dealWith:'+file)
    for line in iter(open(file,encoding='utf-8')):
        if (line.__contains__("android.support") or line.__contains__("android.arch") or line.__contains__(
                "android.databinding") or line.__contains__("android.test")):
            needReWrite = True
            content = content + replaceAndroidX(line, configs)
        else:
            content = content + line
    if (needReWrite):
        global count
        count += 1
        print("Migrating " + file)
        fo = open(file, "w",encoding='utf-8')
        fo.write(content)
        fo.close


def main():
    configs = getMapData()
    configs.sort(reverse=True, key=lambda x:x['from'])
    files = getAllFiles(curpath)
    for file in files:
        replaceSupport(file, configs)
    print("Total migrate files=" + str(count))


main()
