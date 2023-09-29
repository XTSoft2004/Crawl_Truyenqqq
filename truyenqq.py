import requests #Request
from PIL import Image #Download Image
from io import BytesIO
import os
import re

Path_Local = os.getcwd()


def Check_Name(name):
        ans = ""
        for x in name:
            if x >= ' ' and x <= '/' or x >= ':' and x <= '@':
                x = '-'
            ans += x

        return ans


class Truyen_QQ:
             
    def Download_Image(self,link,name_manga,name_chapter):
        host = link.split('/')[2] # Lấy host của link request ( vì web nhiều link chứa ảnh khác nhau nên host sẽ khác nhau )

        namefile = link.split('/')[5];
        namefile = re.match(r'^([^?]+)', namefile).group(1) # Xử lý tên bị thừa để tách ra tên file

        name_chapter = Check_Name(name_chapter) # Thay đổi các kí tự đặc biệt mà tên folder không được đặt
        name_manga = Check_Name(name_manga)
        Path_Download = f"{Path_Local}\\{name_manga}\\{name_chapter}" #Set Folder chứa các ảnh được download vào

        if not os.path.exists(Path_Download): # Kiểm tra xem đã tồn tại folder ảnh chưa nếu chưa sẽ tạo folder mới
            os.makedirs(Path_Download)

        header = {
            'Accept':'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'vi',
            'Host':host,
            'Referer':'https://truyenqqq.vn/',
            'Sec-Ch-Ua':'"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'Sec-Ch-Ua-Mobile':'?0',
            'Sec-Ch-Ua-Platform':'"Windows"',
            'Sec-Fetch-Mode':'no-cors',
            'Sec-Fetch-Site':'cross-site',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43'
          }

        x = requests.get(link,headers=header) # Request GET

        if(x.status_code == 200):
            image_content = x.content
            # Create an image object from the content
            img = Image.open(BytesIO(image_content))
            # Save the image to your local system
            img.save(f"{Path_Download}\\{namefile}")
            print(f"Download Success {namefile} !!!!")
        else:
            print(f"Download Fail {namefile} !!!!")
            
    def Get_Link_Chapter(self,link_mange):
        Link_Chapter = []
        
        result = requests.get(link_mange)

        if(result.status_code == 200): 
            content = result.text
            match = re.findall(r'<a target="_self" class="" href="(.*?)</a>', content)
            if match.count != 0:
                for x in match:

                    link, name_chapter = x.split('">')
                    Manga = {}
                    Manga["Link"] = link
                    Manga["Name"]= name_chapter
                    Link_Chapter.append(Manga)

                return Link_Chapter
            else:
                print("Không có chapter nào !!!")
                return None
        else:
            print("Không thể lấy chapter !!!")
            return None
        
    def Get_Image_Mange(seft,link_chapter):
        Image_Chapter = []

        result = requests.get(link_chapter)
        
        if(result.status_code == 200): 
            content = result.text
            match = re.findall(r'<img class="lazy" src="(.*?)"', content)
            if match.count != 0:
                for x in match:
                    Image_Chapter.append(x)

                return Image_Chapter
            else:
                print("Không có image nào trong chapter !!!")
                return None
        else:
            print("Không thể lấy imgae được !!!")
            return None
        
    def Get_Name_Manga(seft,link_manga):    
        result = requests.get(link_manga)

        if(result.status_code == 200): 
            content = result.text
            match = re.findall(r'<span itemprop="name">(.*?)</span>', content)
            return match[1]
        else:
            return None