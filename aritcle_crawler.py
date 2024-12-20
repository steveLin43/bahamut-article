import requests
import pdfkit
import os
import crawler_detail
from bs4 import BeautifulSoup

bsn:int = 0
snA:int = 0
baha_web_url:str = 'https://forum.gamer.com.tw/C.php'
general_headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
floor_num_per_page:int = 20 # 巴哈每頁20樓
dir_name:str = os.path.join(os.path.dirname(__file__), 'gen') # 檔案儲存位置
temp_file_path = os.path.join(dir_name, 'test.html')


def set_bsn(num = None) -> bool:
    global bsn
    if(num == None or (not isinstance(num, int))):
        return False
    else:
        bsn = int(num)
    return True

def set_snA(num = None) -> bool:
    global snA
    if(num == None or (not isinstance(num, int))):
        return False
    else:
        snA = int(num)
    return True

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
# todo:留言未展開
# todo:轉為 PDF 檔時常因時間不足而未讀取完CSS，ProtocolUnknownError
def get_article_content() -> None:
    str_list:list = []
    total_floors_num = get_last_floor()
    pages = (total_floors_num // floor_num_per_page) + 1
    page_number = 0
    try: 
        for i in range(pages):
            page_number += 1
            # todo: 判斷標頭只取一次或是每次都取
            # todo: 可以用 while + try catch + sleep 進行自動重試，但由於目前是直接寫入檔案因此須改結構
            page_soup = get_request_content(page_number)
            article_title = crawler_detail.get_baha_title(page_soup)
            str_list.append(crawler_detail.get_baha_head(page_soup))
            str_list.append(crawler_detail.get_content_by_page(page_soup))
            # 寫入檔案
            result = "\n".join(str_list)
            with open(temp_file_path, 'a', encoding='utf-8') as file:
                file.write(result)
            str_list.clear()
            
            # 每頁都存成 pdf，避免檔案過大導致失敗
            if (page_number % 1) == 0 :
                save_pdf(f'gen/{article_title} - 第{page_number}頁.pdf')
                #os.remove(temp_file_path)
                break

        save_pdf(f'gen/{article_title} - 第{page_number}頁.pdf')
        #os.remove(temp_file_path)
        str_list.clear()

    except Exception as e:
        print(f'在處理第{page_number}頁時出現錯誤')
        print(e)

# 保存成 pdf
def save_pdf(filename = 'gen/testpdf.pdf') -> None: # todo: file_name 為 pdf文件名，要換掉
    options = {
        'page-size': 'Letter',
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
        'outline-depth': 10,
        'no-stop-slow-scripts': '',       # 等待 script 執行完成
        'load-error-handling': 'skip',  # 資源加載處理方式
        'javascript-delay': 10*60 * 1000,  # 等待秒數
    }

    pdfkit.from_file(temp_file_path, filename, options=options)

def merge_pdf() -> None:
    a=1
    #todo

if __name__ == '__main__':
    # todo: 用 sys.argv[n] 將輸入參數化
    resbsn = set_bsn(838)
    ressnA = set_snA(6824)
    try:
        if (resbsn and ressnA):
            create_dir()
            get_article_content()
            #merge_pdf()
        else:
            print('輸入參數錯誤')
    except Exception as e:
        print('出現錯誤: ' + e)