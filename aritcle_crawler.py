import crawler_detail
import os
import pdfkit
import requests
import sys
from bs4 import BeautifulSoup

# 常數區
baha_web_url:str = 'https://forum.gamer.com.tw/C.php'
general_headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
floor_num_per_page:int = 20 # 巴哈每頁20樓
dir_name:str = os.path.join(os.path.dirname(__file__), 'gen') # 檔案儲存位置

# 運作變數區
pages:int = 1 # 此篇文章共有幾頁
file_path_html = os.path.join(dir_name, 'test.html')
file_path_pdf = os.path.join(dir_name, 'test.pdf')

# 輸入參數區
bsn:int = 0
snA:int = 0
delete_html:bool = False

def set_bsn():
    global bsn
    if len(sys.argv) <= 1:
        raise Exception('請填入 bsn 參數')
    elif not sys.argv[1].isdigit():
        raise Exception('你難道不知道 bsn 只能填入數字嗎')
    else:
        bsn = int(sys.argv[1])

def set_snA():
    global snA
    if len(sys.argv) <= 2:
        raise Exception('請填入 snA 參數')
    elif not sys.argv[2].isdigit():
        raise Exception('你難道不知道 snA 只能填入數字嗎')
    else:
        snA = int(sys.argv[2])

def handle_not_necessary_para():
    global delete_html
    if (len(sys.argv) >= 4) and (sys.argv[3] == 1):
        delete_html = True

def set_file_name(title:str, page:int = 1) -> None:
    global file_path_html, file_path_pdf
    if(pages == 1):
        file_path_html = os.path.join(dir_name, f'{title}.html')
        file_path_pdf = os.path.join(dir_name, f'{title}.pdf')
    else:
        file_path_html = os.path.join(dir_name, f'{title} - 第{page}頁.html')
        file_path_pdf = os.path.join(dir_name, f'{title} - 第{page}頁.pdf')

# 計算該篇文章最大樓層數
def get_last_floor() -> int:
    url = f'{baha_web_url}?bsn={bsn}&snA={snA}&last=1#down'
    soup = BeautifulSoup(requests.get(url, headers = general_headers).text, 'html.parser')
    floors = soup.find_all('a', {'class': 'floor'})

    if not floors:
        print("未找到樓層資訊")
        return 0

    last_floor_text = floors[-1].text.strip()
    last_floor = ''.join(list(filter(str.isdigit,last_floor_text)))
    return int(last_floor)

# 取得 url 頁面內容
def get_request_content(page:int = 1) -> BeautifulSoup:
    url = f'{baha_web_url}?bsn={bsn}&snA={snA}&page={page}'
    return BeautifulSoup(requests.get(url, headers = general_headers).text, 'html.parser')

# 主程式第一部分: 創建儲存資料夾
def create_dir(directory_name:str = '') -> None:
    try:
        if directory_name == '':
            directory_name = dir_name
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
    except Exception as e:
        print(e)

# 主程式第二部分: 將文章內容儲存html檔案
def get_article_content() -> None:
    global pages
    str_list:list = []
    total_floors_num = get_last_floor()
    pages = (total_floors_num // floor_num_per_page) + 1
    page_number = 0
    try:
        for i in range(pages):
            page_number += 1
            # todo: 可以用 while + try catch + sleep 進行自動重試
            page_soup = get_request_content(page_number)
            
            # 第一圈額外處理 head
            if (page_number == 1):
                article_title = crawler_detail.get_baha_title(page_soup)
                str_list.append(crawler_detail.get_baha_head(page_soup))

            set_file_name(article_title, page_number)
            str_list.append(crawler_detail.get_content_by_page(page_soup))

            # 寫入檔案
            result = "\n".join(str_list)
            with open(file_path_html, 'a', encoding='utf-8') as file:
                file.write(result)
            str_list = str_list[:1]
            
            # 每頁都存成 pdf，避免檔案過大導致失敗
            if (page_number % 1) == 0 :
                save_pdf(file_path_pdf)
                if delete_html:
                    os.remove(file_path_html)
                break

        save_pdf(file_path_pdf)
        if delete_html:
            os.remove(file_path_html)
        str_list.clear()

    except Exception as e:
        print(f'在處理第{page_number}頁時出現錯誤')
        print(e)

# 保存成 pdf
# todo: 圖片目前沒有顯示，ProtocolUnknownError
def save_pdf(pdfFileName:str) -> None:
    options = {
        'page-size': 'A4',
        'margin-top': '0.2in',
        'margin-right': '0.3in',
        'margin-bottom': '0.1in',
        'margin-left': '0.3in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'no-outline': None,  # 防止 outline 過度優化導致圖片加載失敗
        'no-stop-slow-scripts': None,       # 等待 script 執行完成
        'load-error-handling': 'skip',  # 資源加載處理方式
        'load-media-error-handling': 'ignore',  # 忽略多媒體錯誤
        'javascript-delay': 60 * 1000,  # 等待秒數
    }

    pdfkit.from_file(file_path_html, pdfFileName, options=options)

def merge_pdf() -> None:
    a=1
    #todo

if __name__ == '__main__':
    doing = True
    # 參數順序: bsn、snA、刪除檔案838 6284
    try:
        set_bsn()
        set_snA()
        handle_not_necessary_para()
    except Exception as e:
        print('出現錯誤: ' + str(e))
        doing = False

    # 執行
    if (doing):
        try:
            create_dir()
            get_article_content()
            merge_pdf()
        except Exception as e:
            print('出現錯誤: ' + str(e))