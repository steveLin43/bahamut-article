import crawler_detail
import crawler_log
import os
import pdfkit
import requests
import sys
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader, PdfWriter

# 常數區
baha_web_url:str = 'https://forum.gamer.com.tw/C.php'
general_headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
floor_num_per_page:int = 20 # 巴哈每頁20樓
dir_name:str = os.path.join(os.path.dirname(__file__), 'gen') # 檔案儲存位置

# 運作變數區
pages:int = 1 # 此篇文章共有幾頁
file_path_html = os.path.join(dir_name, 'test.html')
file_path_pdf = os.path.join(dir_name, 'test.pdf')
file_path_pdf_final = os.path.join(dir_name, 'test_final.pdf')

# 輸入參數區
bsn:int = 0
snA:int = 0
delete_html:bool = False
delete_pdf:bool = False
no_picture:bool = False

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
    global delete_html, delete_pdf, no_picture
    if (len(sys.argv) >= 4):
        if 'd' in sys.argv[3:]:
            delete_html = True
        if 'm' in sys.argv[3:]:
            delete_pdf = True
        if 'p' in sys.argv[3:]:
            no_picture = True

# 處理每份文件名稱
def set_file_name(title:str, page:int = 1) -> None:
    global file_path_html, file_path_pdf, file_path_pdf_final
    if(pages == 1):
        file_path_html = os.path.join(dir_name, f'{title}.html')
        file_path_pdf = os.path.join(dir_name, f'{title}.pdf')
    else:
        file_path_html = os.path.join(dir_name, f'{title} - 第{page}頁.html')
        file_path_pdf = os.path.join(dir_name, f'{title} - 第{page}頁.pdf')
        file_path_pdf_final = os.path.join(dir_name, f'{title}.pdf')

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
        print('創建儲存資料夾時失敗')
        crawler_log.unexpected_error()
        raise

# 主程式第二部分: 將文章內容儲存html檔案
def get_article_content() -> None:
    global pages
    str_list:list = []
    pdf_list:list = []
    total_floors_num = get_last_floor()
    article_title:str = ''
    pages = (total_floors_num // floor_num_per_page) + 1
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
                article_title = crawler_detail.get_baha_title(page_soup)
                str_list.append(crawler_detail.get_baha_head(page_soup))

            set_file_name(article_title, page_number)
            str_list.append(crawler_detail.get_content_by_page(page_soup))
            if no_picture:
                picture_number = crawler_detail.download_pictures_from_soup(page_soup, dir_name, article_title, picture_number)

            # 寫入檔案
            result = "\n".join(str_list)
            with open(file_path_html, 'a', encoding='utf-8') as file:
                file.write(result)
            str_list = str_list[:1]
            
            # 分頁儲存避免檔案過大導致失敗
            if (page_number % page_number_each) == 0:
                save_pdf(file_path_pdf)
                pdf_list.append(file_path_pdf)
                if delete_html:
                    os.remove(file_path_html)
                break #todo:測試用

        if (pages % page_number_each) != 0 :
            save_pdf(file_path_pdf)
            pdf_list.append(file_path_pdf)
            if delete_html:
                os.remove(file_path_html)
        str_list.clear()

        if len(file_path_pdf) > 1:
            merge_pdf(pdf_list, file_path_pdf_final)

    except Exception as e:
        crawler_log.expected_log(41, f'第{page_number}頁。')

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

def merge_pdf(pdf_list:list, output_name:str) -> None:
    pagenum = 0
    pdf_output = PdfWriter()

    for pdf in pdf_list:
        pdf_input = PdfReader(open(pdf, 'rb'))

        page_count = len(pdf_input.pages)
        for i in range(page_count):
            pdf_output.add_page(pdf_input.pages[i])
        pagenum += page_count

    # 合併
    pdf_output.write(open(output_name, 'wb'))
    # 删除所有PDF子文件
    if delete_pdf:
        for item in pdf_list:
            os.remove(item)

if __name__ == '__main__':
    doing = True
    # 參數順序: bsn、snA、是否刪除html檔案(d)、是否刪除PDF子文件(m)、是否不刪除圖片(p)
    try:
        crawler_log.expected_log(10, str(sys.argv))
        set_bsn()
        set_snA()
        handle_not_necessary_para()
    except Exception as e:
        crawler_log.expected_log(40)
        print('參數錯誤導致失敗')
        doing = False

    # 執行
    if (doing):
        try:
            create_dir()
            get_article_content()
        except Exception as e:
            print('執行出錯導致失敗')