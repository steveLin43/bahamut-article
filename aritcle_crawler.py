import common
import crawler_detail
import crawler_log
import os
import requests
import sys
from bs4 import BeautifulSoup

# 常數區
baha_web_url:str = 'https://forum.gamer.com.tw/C.php'
general_headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
floor_num_per_page:int = 20 # 巴哈每頁20樓
dir_name:str = os.path.join(os.path.dirname(__file__), 'gen') # 檔案儲存位置

# 輸入參數區
bsn:int = 0
snA:int = 0
delete_html:bool = False
delete_pdf:bool = False
no_picture:bool = True

# 參數順序: bsn、snA、是否刪除html檔案(d)、是否刪除PDF子文件(m)、是否不下載圖片(p)
def set_parameters():
    global bsn, snA
    if len(sys.argv) <= 1:
        raise Exception('請填入 bsn 參數')
    elif len(sys.argv) <= 2:
        raise Exception('請填入 snA 參數')

    bsn = common.set_para(sys.argv[1])
    snA = common.set_para(sys.argv[2])
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

# 計算該篇文章最大樓層數
def get_last_floor() -> int:
    url = f'{baha_web_url}?bsn={bsn}&snA={snA}&last=1#down'
    soup = BeautifulSoup(requests.get(url, headers = general_headers).text, 'html.parser')
    floors = soup.find_all('a', {'class': 'floor'})

    if not floors:
        crawler_log.expected_log(20)
        return 0

    last_floor_text = floors[-1].text.strip()
    last_floor = ''.join(list(filter(str.isdigit,last_floor_text)))
    return int(last_floor or '0') or 1

# 取得 url 頁面內容
def get_request_content(page:int = 1) -> BeautifulSoup:
    url = f'{baha_web_url}?bsn={bsn}&snA={snA}&page={page}'
    return BeautifulSoup(requests.get(url, headers = general_headers).text, 'html.parser')

# 將文章內容儲存html檔案
def get_article_content() -> None:
    file_path_html = os.path.join(dir_name, 'test.html')
    file_path_pdf = os.path.join(dir_name, 'test.pdf')
    file_path_pdf_final = os.path.join(dir_name, 'test_final.pdf')

    str_list:list = []
    pdf_list:list = []
    total_floors_num = get_last_floor()
    article_title:str = ''
    
    # 此文章共有幾頁
    pages = (total_floors_num // floor_num_per_page)
    if total_floors_num % floor_num_per_page != 0:
        pages += 1
    
    page_number = 0
    page_number_each = 1 # 讓程式每幾頁儲存一次
    picture_number = 1
    
    if total_floors_num == 0:
        print('無符合資料')
        crawler_log.expected_log(22)
        return
    
    try:
        for i in range(pages):
            page_number += 1
            page_soup = get_request_content(page_number)
            
            # 第一圈額外處理 head
            if (page_number == 1):
                article_title = crawler_detail.half_to_full(crawler_detail.get_baha_title(page_soup))
                str_list.append(crawler_detail.get_baha_head(page_soup))

            # 設定此次檔名
            file_path_html, file_path_pdf, file_path_pdf_final = common.set_file_name(article_title, dir_name, page_number, pages)

            str_list.append(crawler_detail.get_content_by_page(page_soup))
            if no_picture:
                picture_number = crawler_detail.download_pictures_from_soup(page_soup, dir_name, article_title, picture_number)

            # 寫入檔案
            result = "\n".join(str_list)
            #result = result.replace("https://i2.bahamut.com.tw/css", "../baha_doc/css") # 取得本地檔案
            #result = result.replace("https://i2.bahamut.com.tw/js", "../baha_doc/js") # 取得本地檔案
            with open(file_path_html, 'a', encoding='utf-8') as file:
                file.write(result)
            str_list = str_list[:1]
            
            # 分頁儲存避免檔案過大導致失敗
            if (page_number % page_number_each) == 0:
                #common.save_pdf(file_path_html, file_path_pdf)# 目前因 CSS 樣式過於複雜，導致 pdfkit 無法正常處理
                pdf_list.append(file_path_pdf)
                if delete_html:
                    os.remove(file_path_html)

        if (pages % page_number_each) != 0 :
            #common.save_pdf(file_path_html, file_path_pdf) # 目前因 CSS 樣式過於複雜，導致 pdfkit 無法正常處理
            pdf_list.append(file_path_pdf)
            if delete_html:
                os.remove(file_path_html)
        str_list.clear()

        #if len(file_path_pdf) > 1:
            #common.merge_pdf(pdf_list, file_path_pdf_final, delete_pdf)

    except Exception as e:
        crawler_log.expected_log(41, f'第{page_number}頁。')

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