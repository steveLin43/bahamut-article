import helper.common as common
import helper.crawler_other_web as crawler_other_web
import helper.crawler_log as crawler_log
import os
import requests
import sys
from bs4 import BeautifulSoup

# 常數區
web_url:str = 'https://kirokiro.cc/games'
general_headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
dir_name:str = os.path.join(os.path.dirname(__file__), 'gen') # 檔案儲存位置

# 輸入參數區
id:int = 0
delete_html:bool = False
no_picture:bool = True

# 參數順序: bsn、snA、是否刪除html檔案(d)、是否刪除PDF子文件(m)、是否不下載圖片(p)
def set_parameters():
    global id
    if len(sys.argv) <= 1:
        raise Exception('請填入 文章編號 參數')

    id = common.set_para(sys.argv[1])
    handle_not_necessary_para(2)

def handle_not_necessary_para(base_num:int):
    global delete_html, delete_pdf, no_picture
    if (len(sys.argv) >= base_num + 1):
        if 'd' in sys.argv[base_num:]:
            delete_html = True
        if 'p' in sys.argv[base_num:]:
            no_picture = False

# 取得 url 頁面內容
def get_request_content() -> BeautifulSoup:
    url = f'{web_url}/{id}'
    return BeautifulSoup(requests.get(url, headers = general_headers).text, 'html.parser')

# 將文章內容儲存html檔案
def get_article_content() -> None:
    file_path_html = os.path.join(dir_name, 'test.html')
    file_path_pdf = os.path.join(dir_name, 'test.pdf')

    str_list:list = []
    article_title:str = ''
    picture_number = 1
    
    try:
        web_soup = get_request_content()
        
        article_title = common.half_to_full(web_soup.body.find('h1', {'class': 'post-title entry-title'}).string)
        str_list.append(crawler_other_web.get_kiro_head(web_soup))

        # 設定此次檔名
        file_path_html, file_path_pdf, *rest = common.set_file_name(article_title, dir_name)

        content, pic_table = crawler_other_web.get_kiro_content(web_soup)
        str_list.append(content)
        if no_picture:
            picture_number = crawler_other_web.download_pictures_from_web(web_soup, dir_name, article_title, picture_number, 1 + pic_table)

        # 寫入檔案
        result = "\n".join(str_list)
        with open(file_path_html, 'a', encoding='utf-8') as file:
            file.write(result)
        str_list = str_list[:1]
        
        common.save_pdf(file_path_html, file_path_pdf)# 目前因 CSS 樣式過於複雜，導致 pdfkit 無法正常處理
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