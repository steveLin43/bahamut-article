import helper.common as common
import helper.crawler_baha as crawler_baha
import helper.crawler_log as crawler_log
import os
import requests
import sys
from bs4 import BeautifulSoup

# 常數區
baha_web_url:str = 'https://forum.gamer.com.tw/G2.php'
general_headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
dir_name:str = os.path.join(os.path.dirname(__file__), 'gen') # 檔案儲存位置

# 輸入參數區
bsn:int = 0
sn:int = 0
delete_html:bool = False
delete_pdf:bool = False
no_picture:bool = True

# 參數順序: snA、是否刪除html檔案(d)、是否刪除PDF子文件(m)、是否不下載圖片(p)
def set_parameters():
    global bsn, sn
    if len(sys.argv) <= 1:
        raise Exception('請填入 bsn 參數')
    elif len(sys.argv) <= 2:
        raise Exception('請填入 sn 參數')

    bsn = common.set_para(sys.argv[1])
    sn = common.set_para(sys.argv[2])
    handle_not_necessary_para(3)

def handle_not_necessary_para(base_num:int):
    global delete_html, delete_pdf, no_picture
    if (len(sys.argv) >= base_num + 1):
        if 'd' in sys.argv[base_num:]:
            delete_html = True
        if 'm' in sys.argv[base_num:]:
            delete_pdf = True
        if 'p' in sys.argv[base_num:]:
            no_picture = False

# 取得 url 頁面內容
def get_request_content() -> BeautifulSoup:
    url = f'{baha_web_url}?bsn={bsn}&sn={sn}'
    return BeautifulSoup(requests.get(url, headers = general_headers).text, 'html.parser')

# 將文章內容儲存html檔案
def get_article_content() -> None:
    file_path_html = os.path.join(dir_name, 'test.html')
    file_path_pdf = os.path.join(dir_name, 'test.pdf')

    str_list:list = []
    pdf_list:list = []
    article_title:str = ''
    picture_number = 1
    
    try:
        soup = get_request_content()
        if not soup:
            print('無符合資料')
            crawler_log.expected_log(22)
            return

        # 處理 head
        article_title = common.half_to_full(crawler_baha.get_baha_title(soup))
        str_list.append(str(soup.head)) ##??? 有空時會再精細篩檢

        # 設定此次檔名
        file_path_html, file_path_pdf, file_path_pdf_final = common.set_file_name(article_title, dir_name)
        str_list.append(crawler_baha.get_content_by_house(soup))
        if no_picture:
            picture_number = crawler_baha.download_pictures_from_soup(soup, dir_name, article_title, picture_number, 3)

        # 寫入檔案
        result = "\n".join(str_list)
        #result = result.replace("https://i2.bahamut.com.tw/css", "../baha_doc/css") # 取得本地檔案
        #result = result.replace("https://i2.bahamut.com.tw/js", "../baha_doc/js") # 取得本地檔案
        with open(file_path_html, 'a', encoding='utf-8') as file:
            file.write(result)
        str_list = str_list[:1]
            
        #common.pdf_saved(file_path_html, file_path_pdf)# 目前因 CSS 樣式過於複雜，導致 pdfkit 無法正常處理
        pdf_list.append(file_path_pdf)
        if delete_html:
            os.remove(file_path_html)
        str_list.clear()

    except Exception as e:
        crawler_log.expected_log(41)

if __name__ == '__main__':
    doing = True
    try:
        crawler_log.expected_log(10, str(sys.argv))
        set_parameters()
    except Exception as e:
        crawler_log.expected_log(40)
        print('參數錯誤導致失敗')
        doing = False

    # 執行
    if (doing):
        try:
            common.create_dir()
            get_article_content()
        except Exception as e:
            crawler_log.expected_log(0, 'Unknown')
            print('執行出錯導致失敗')