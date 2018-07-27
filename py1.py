import requests
import urllib
import urllib.parse
import re
import urllib.request
import time
import os.path


class netbian():
    imgName=""
    imgNameUrlEncoding=""
    pagecount=1;#图片页数
    time=1#间隔时间
    netbianUrl=""#请求地址
    netbianHostUrl="http://www.netbian.com"#主机地址
    netbianAD1="http://img.netbian.com/file/2017/0713/bb096e7fc133ddfbe1d409cf9340800b.jpg"#页面无用图片1

    def __init__(self,keyboard,pagecount):
        self.imgName=keyboard
        self.pagecount=pagecount
        keyboard=urllib.parse.quote(keyboard,"/",encoding="gbk")
        self.imgNameUrlEncoding=keyboard

    def removeRepeat(self,li):#删除重复的list
        li=list(set(li))
        for i in li:
            if i==self.netbianAD1:
                li.remove(self.netbianAD1)
        return li

    def getHtml(self,url):
        page=requests.get(url)
        page.encoding=page.apparent_encoding
        if page.status_code==200:
            print("页面获取成功！")
        else:
            print("页面获取失败！\r"+page.status_code)

        return page.text

    def getImageUrl(self,page):
        p=r"/desk/[0-9]*.htm"#正则匹配链接
        s = re.findall(p,page)
        return s

    def getImageUrl1(self,page1):
        p=r"/desk/[0-9]*-{1,}[0-9]*x[0-9]*.htm"#正则匹配图片url
        s=re.findall(p,page1)
        return s

    def getImageUrl2(self,page2):
        p=r"http://\w*.\w*.\w*./file/[0-9]*/[0-9]*\w*.\w*.jpg"#正则匹配图片下载地址
        s=re.findall(p,page2)
        return s

    def start(self):
        for cou in range(self.pagecount):
            self.netbianUrl = "http://www.netbian.com/e/sch/index.php?page="+str(cou)+"&keyboard=" + self.imgNameUrlEncoding + "&totalnum=85"
            page = bian.getHtml(self.netbianUrl)  # 获取图片url的html
            t = self.getImageUrl(page)  # 图片url数组
            rr = self.removeRepeat(t)  # 去重后的图片url数组
            for i in range(len(rr)):
                page1 = self.getHtml(self.netbianHostUrl + rr[i])
                img = self.getImageUrl1(page1)
                rr1 = self.removeRepeat(img)
                print("rr1-------------"+str(rr1))
                for j in range(len(rr1)):
                    page2 = self.getHtml(self.netbianHostUrl + rr1[j])
                    imgurl = self.getImageUrl2(page2)
                    rr2 = self.removeRepeat(imgurl)
                    print("从" + str(rr2) + "保存图片")
                    time.sleep(self.time)
                    if not os.path.exists(os.getcwd()+"\\image"):
                        os.mkdir(os.getcwd()+"\\image")
                    try:
                        if os.path.exists(os.getcwd()+"\\" + self.imgName + str(cou)+str(i)+str(j) + ".jpg"):#如果存在这张图片就跳过
                            print("当前图片已存在，跳过！")
                            continue
                        urllib.request.urlretrieve(rr2[0], os.getcwd()+"\\image\\" + self.imgName + str(cou)+str(i)+str(j) + ".jpg")
                        print(str(rr2) + "第"+str(cou+1)+"页,第"+str(i+1)+"张图片保存完成！")
                    except Exception as e:
                        print("保存失败！出现异常：" + str(e))

if __name__ == "__main__":
    bian=netbian("猫",6)#第一个要搜索的图片名，第二个参数为下载页数
    bian.start()
