from . import crawler_log
import os
import requests
import time
import pdfkit
from PyPDF2 import PdfReader, PdfWriter

def set_para(input_para):
    if not input_para.isdigit():
        raise Exception('你難道不知道只能填入數字嗎')
    return int(input_para)

def create_dir(directory_name:str = '') -> None:
    default = os.path.join(os.path.dirname(__file__), 'gen')
    try:
        if directory_name == '':
            directory_name = default
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
    except Exception as e:
        print('創建儲存資料夾時失敗')
        crawler_log.unexpected_error()
        raise

# 特定半形符號轉全形
def half_to_full(trans_str:str) -> str:
    halfwidth = "/\\*:?\"<>|"
    fullwidth = "／＼＊：？＂＜＞｜"

    translation_table = str.maketrans(halfwidth, fullwidth) # 映射表
    return trans_str.translate(translation_table)

# 處理每份文件名稱
def set_file_name(title:str, dir_name:str = '', page:int = 1, total_pages:int = 1) -> None:
    file_path_pdf_final = ''
    if(total_pages == 1):
        file_path_html = os.path.join(dir_name, f'{title}.html')
        file_path_pdf = os.path.join(dir_name, f'{title}.pdf')
    else:
        file_path_html = os.path.join(dir_name, f'{title}-第{page}頁.html')
        file_path_pdf = os.path.join(dir_name, f'{title}-第{page}頁.pdf')
        file_path_pdf_final = os.path.join(dir_name, f'{title}.pdf')
    return file_path_html, file_path_pdf, file_path_pdf_final

# 保存成 pdf
def save_pdf(file_path:str, pdfFileName:str) -> None:
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
        'enable-local-file-access': None,
    }

    pdfkit.from_file(file_path, pdfFileName, options=options)

def merge_pdf(pdf_list:list, output_name:str, delete_pdf:bool = False) -> None:
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

# 下載圖片
# pl:           待下載的圖片列表
# total_nums:   目前下載圖片數量(編號用)
# path:         檔案路徑
# pic_title:    檔案標題
# pic_tag:      html 的 element 名稱
def download_pictures(pl:list, total_nums:int, path:str, pic_title:str, pic_tag:str) -> int:
    defective_nums = 0
    for pic in pl:
        try:
            pic_url = pic.get(pic_tag)

            if not pic_url:
                crawler_log.expected_log(43, f'{pic_url} 無效的圖片URL')
                defective_nums += 1
                continue

            file_extension = pic_url.split('.')[-1].lower() # 統一轉為小寫
            if file_extension not in ['jpg', 'jpeg', 'png', 'gif']:
                crawler_log.expected_log(43, f'{pic_url}：不支持的圖片格式 {file_extension}')
                defective_nums += 1
                continue

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(pic_url, headers=headers, timeout = 10)
            response.raise_for_status() # 確保有正常取得圖片

            pic_name = os.path.join(path, f'{pic_title}-{total_nums:02}.{file_extension}')
            with open(pic_name, "wb") as file:
                file.write(response.content)

            total_nums += 1
            time.sleep(1)

        except Exception as e:
            crawler_log.unexpected_error()
            continue

    if defective_nums != 0:
        print(f'共有{defective_nums}張圖片沒有成功下載，請記得確認。')

    return total_nums
