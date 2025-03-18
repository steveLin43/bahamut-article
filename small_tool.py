import helper.common as common
import helper.crawler_log as crawler_log
import os
import sys
from PyPDF2 import PdfWriter

# 將指定目錄的 PDF 檔合成為一個 PDF 檔
def __merge_files_into_1pdf(output_name:str = 'test.pdf', dir_name:str = 'C:\\testDir', same_pre:str = '') -> None:
    # 參數設定
    output_name = '輸出檔名.pdf'
    dir_name = 'C:\\Users\\資料夾路徑'
    same_pre = '需要刪除的前墜文字'

    output_pdf = os.path.join(dir_name, output_name)
    pdf_writer = PdfWriter()
    page_number = 0 # 目前頁數
    
    try:
        # 先取得資料夾下的所有 PDF 檔案與標題
        pdf_files_names = [f for f in os.listdir(dir_name) if f.lower().endswith('.pdf')]
        pdf_files_path = [os.path.join(dir_name, f) for f in pdf_files_names]
        chapter_titles = common.pdf_titles_filter(pdf_files_names, same_pre)
        
        # 整理 PDF 檔案
        for i in range(len(pdf_files_path)):
            pdf_writer, add_num = common.pdf_add_pdf(chapter_titles[i], pdf_writer, pdf_files_path[i], page_number)
            page_number += add_num

        with open(output_pdf, "wb") as out_file:
            pdf_writer.write(out_file)

    except Exception as e:
        crawler_log.expected_log(41)

if __name__ == '__main__':
    doing = True
    try:
        crawler_log.expected_log(10, str(sys.argv))
        common.create_dir()
        if 'mergeAll' in sys.argv:
            __merge_files_into_1pdf()
        else:
            print('執行完畢')
    except Exception as e:
        crawler_log.expected_log(0, 'Unknown')
        print('執行出錯導致失敗')