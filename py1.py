import requests
import urllib
import urllib.parse
import re
import urllib.request
import time
import os.path


class netbian():
    imgName=""
    imgNameUrlEncoding=""#图片名的URL编码
    pageCount=1#获取图片页数
    intervalTime=0.4#获取图片间隔时间(s)
    netbianHostUrl="http://www.netbian.com"#主机地址
    netbianNotSave="http://img.netbian.com/file/2017/0713/bb096e7fc133ddfbe1d409cf9340800b.jpg"#不保存的图片

    def __init__(self,keyboard,pageCount):
        self.imgName=keyboard
        self.pageCount=pageCount
        self.imgNameUrlEncoding=urllib.parse.quote(keyboard,"/",encoding="gbk")

    def removeRepeat(self,list_old):
        list_old=list(set(list_old))
        for i in list_old:#删除集合中指定的不保存的图片URL
            if i==self.netbianNotSave:
                list_old.remove(self.netbianNotSave)
        return list_old

    def getHtml(self,url):
        page=requests.get(url)
        page.encoding=page.apparent_encoding
        # if page.status_code==200:
        #     print("页面获取成功！")
        # else:
        #     print("页面获取失败！\r"+page.status_code)

        return page.text

    def getImageUrl(self,page):
        urlList=r"/desk/[0-9]*.htm"
        imgUrl = re.findall(urlList,page)
        return imgUrl

    def getImageUrl1(self,page1):
        urlList=r"/desk/[0-9]*-{1,}[0-9]*x[0-9]*.htm"
        imgUrl=re.findall(urlList,page1)
        return imgUrl

    def getImageUrl2(self,page2):
        urlList=r"http://\w*.\w*.\w*./file/[0-9]*/[0-9]*\w*.\w*.jpg"
        imgUrl=re.findall(urlList,page2)
        return imgUrl

    def start(self):
        imageSaveCount=0#成功保存的图片数量
        for cou in range(self.pageCount):
            netbianUrl = "http://www.netbian.com/e/sch/index.php?page="+str(cou)+"&keyboard=" + self.imgNameUrlEncoding + "&totalnum=85"

            page = bian.getHtml(netbianUrl)  # 获取第一个页面
            imgUrl = self.getImageUrl(page)  # 获取第一个页面的第一个URL
            imgUrlrr = self.removeRepeat(imgUrl)  # 去重

            for i in range(len(imgUrlrr)):
                page1 = self.getHtml(self.netbianHostUrl + imgUrlrr[i])# 获取第二个页面
                imgUrl1 = self.getImageUrl1(page1)# 获取第二个页面的第一个URL
                imgUrl1rr1 = self.removeRepeat(imgUrl1)# 去重

                for j in range(len(imgUrl1rr1)):
                    page2 = self.getHtml(self.netbianHostUrl + imgUrl1rr1[j]) # 获取第三个页面
                    imgUrl2 = self.getImageUrl2(page2)# 获取第三个页面的第一个URL
                    imgUrl2rr2 = self.removeRepeat(imgUrl2) # 去重

                    print("当前图片:" + str(imgUrl2rr2))

                    if len(imgUrl2rr2)==0:
                        print("当前集合没有数据,取消保存")
                        continue

                    time.sleep(self.intervalTime)

                    if not os.path.exists(os.getcwd()+"\\image"):#当前路径是否存在image文件夹
                        os.mkdir(os.getcwd()+"\\image")

                    try:
                        imagePathAndName=os.getcwd()+"\\image\\" + self.imgName + str(cou)+str(i) + ".jpg"#即将保存的图片
                        if os.path.exists(imagePathAndName):
                            print("当前图片已存在，跳过！")
                            continue
                        
                        urllib.request.urlretrieve(imgUrl2rr2[0],imagePathAndName)
                        print("第"+str(cou+1)+"页,第"+str(i+1)+"张图片保存完成！")
                        imageSaveCount=imageSaveCount+1
                    except Exception as e:
                        print("第"+str(cou+1)+"页,第"+str(i+1)+"张图片保存失败！\r\n异常信息:" + str(e))
        print("ヾﾉ≧∀≦)o 共保存了"+str(imageSaveCount)+"张图片！")

if __name__ == "__main__":
    bian=netbian("猫",10)#参数说明(要搜索的图片名，页数)
    bian.start()
