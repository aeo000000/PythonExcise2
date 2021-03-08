
import base64
import os;
import urllib.request as  req
import requests

# url = r'https://rss.srss.xyz/link/4afkj7ttdewYXj3t?mu=2'

# 对文字解码，解码时，长度应是4的倍数，不足的几个就加几个 = 。
def base64_str(str0):
    lll = len(str0)%4
    if lll != 0:
        str0 = str0 + '='*(4-lll)
    # bytes转成string ，可以用str(bytes,encoding = "utf-8") ,也可以  bytesStr.decode("utf-8")
    return base64.b64decode(str0).decode("utf-8")


def vmess2Clash(oneVmessDic):
    '''输入一条vmess的字典，转换成clash字典，输出为clash规则的一串字符 '''
    key1 = {"ps": "name" ,"host" : "server" ,  "id" : "uuid", "aid":"alterId" , "net":"network", "path": "ws-path" , "port": "port"}
    key2 = { "tls": "true" , "type": "vmess", "cipher": "auto"}
    key3 = {"ws-headers":"{{Host: {}}}"}
    strNew = {}
    for an in key1:
        strNew[ key1[an]  ]  = oneVmessDic[an]

    for an in key2:
        strNew[an] = key2[an]
    if oneVmessDic["add"]:
        strNew["ws-headers"] = key3["ws-headers"].format(oneVmessDic["add"])
    # print(strNew)

    str3 = "{" + ', '.join('%s: %s' %(k,v) for k,v in strNew.items())  + "}"
    str3 = str3.replace('\\/','/')
    return str3




# 输出
def clashTxt(names , clashLst,fileDir):
    ''' 输入两个字典：服务器名称表 服务器完整字典表，最后整合成一个string,并写到文件fileDir中'''
    names = [' '*6 + '- '+ a for a in names]
    nameStr = '\n'.join(names) 
    clashLst = [' '*2 + '- '+ a for a in clashLst]
    clashStr = '\n'.join(clashLst) 
    string = '''port: 7890
socks-port: 7891
allow-lan: true
mode: Rule
log-level: info
external-controller: 127.0.0.1:9090
proxies:
{0}
proxy-groups:
  - name: 🚀 节点选择
    type: select
    proxies:
      - ♻️ 自动选择
      - DIRECT
{1}
  - name: ♻️ 自动选择
    type: url-test
    url: http://www.gstatic.com/generate_204
    interval: 300
    tolerance: 50
    proxies:
{1}
rules:
  - MATCH,🚀 节点选择
'''
    # print(string.format(clashStr,nameStr))
    string2 = string.format(clashStr,nameStr)
    # fileDir = 'f:/23456.yml'
    fo = open(fileDir,'w',encoding='utf-8')
    fo.write(string2)
    fo.close


def main():

    url_dirs = [{'url': 'https://rss.srss.xyz/link/4afkj7ttdewYXj3t?' , 'dir':'C:/Users/zlj/.config/clash/profiles/1609481918404.yml'},  #009
                {'url': 'https://rss.srss.xyz/link/JEwXOzcJOLWXUqeR?' , 'dir':'C:/Users/zlj/.config/clash/profiles/1609481997013.yml'}]

    params = {'mu' : '2'}
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
    for urlDir in url_dirs:
        # 自动对params进行编码,然后自动和url进行拼接,去发请求
        res = requests.get(urlDir['url'],params=params,headers=headers)
        res.encoding = 'utf-8'
        str00 = res.text
        strAll = base64_str(str00)
        strLst = strAll.split("\n")
        vmessLst = []
        for vmess in strLst:
            string_temp = {}
            vmess = base64_str(vmess[8:])
            # print('---{}---'.format(vmess))
            if vmess.startswith('{'):
                exec("str2 = " + vmess,None,string_temp)
                vmessLst.append(string_temp["str2"])
        # print(vmessLst)
        # 所有名称
        nameLst = [ a['ps'].replace('\\/','/') for a in vmessLst]
        # print(nameLst)
        clashLst = [ vmess2Clash(a) for a in vmessLst ]
        # print(clashLst)
        clashTxt(nameLst , clashLst,urlDir['dir'])



if __name__ == "__main__":
    main()


# 出现这个问题的最主要原因还是在于本地仓库和远程仓库实际上是独立的两个仓库。假如我之前是直接clone的方式在本地建立起远程github仓库的克隆本地仓库就不会有这问题了。

# 查阅了一下资料，发现可以在pull命令后紧接着使用--allow-unrelated-history选项来解决问题（该选项可以合并两个独立启动仓库的历史）。
# ————————————————
# 版权声明：本文为CSDN博主「铁乐与猫」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/u012145252/article/details/80628451

# git pull PythonExcise2 main --allow-unrelated-histories

# git push PythonExcise2 main:main
# 直接强行推送过去更新
# git push -f origin master
# git push -f PythonExcise2 main:main     -f为强制更新