import requests #Request
from PIL import Image #Download Image
from io import BytesIO
import os
from truyenqq import Truyen_QQ # Tham chiếu từ class Truyen_QQ

str = input("Nhập link truyện muốn tải ở trang  https://truyenqqq.vn/  :  ")

Manga = Truyen_QQ()
Link_Chapter = Manga.Get_Link_Chapter(str)
Name_Manga = Manga.Get_Name_Manga(str)
print(f"Đang download manga {Name_Manga} ......")
for x in Link_Chapter:
    _link_chapter = x["Link"]
    _name_chapter = x["Name"]
    print(f"Đang tải ảnh {_name_chapter} ....")
    Image_Manga = Manga.Get_Image_Mange(_link_chapter)

    for image in Image_Manga:
        Manga.Download_Image(image,Name_Manga,_name_chapter)

    print(f"Đã tải xong hết ảnh ở {_name_chapter}")