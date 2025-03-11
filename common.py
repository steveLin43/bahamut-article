import crawler_log
import os
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


