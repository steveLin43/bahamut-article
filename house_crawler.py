import helper.common as common
import helper.crawler_baha as crawler_baha
import helper.crawler_log as crawler_log
import os
import requests
import sys
from bs4 import BeautifulSoup

# 常數區
baha_web_url:str = 'https://home.gamer.com.tw/artwork.php'
general_headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
                   'cookie':'_ga=GA1.1.595568408.1724040688; cf_clearance=XNKWw7iHbgTMd7CX1VgiaxUSi3sQv76OzZpiqsG8EJQ-1739523021-1.2.1.1-F8uNhsxFrc3MAUsIoGNGIgWSitCKRETmQaVZhLT6WD.djm0mXoHzpimRlrKbold7XWtPZPJNfAygLna8cj5ugd_M5d3Js3P4lwZyPZ_7yRhD9YZYFw1oD2me3DF7BseBJyQWb0650bJ8mDYyFiEH6kk96Vzz8HNeRvcCrFdLMmIVClbOjNxXDyo9RQftGU8YCnf6tAxORzQ_MnEkiOsnA7Af9oM2qBIC.KC9Zzv9Zw2yCcNG3YiF3D7nJj6DWH.6FooD4v1DdMgukAbBE5IsAyhABaUKoAveXwJIGralkE8qFdrPyWOGNxVYqSdg6RkdX0p8uPsI6HDHvGb6KKvPrg; ckBahamutCsrfToken=15b28d567fa64978; ckBH_lastBoard=[[%2226479%22%2C%22Let%20It%20Die%22]%2C[%2226497%22%2C%22Walkr%20-%20%E5%8F%A3%E8%A2%8B%E8%A3%A1%E7%9A%84%E9%8A%80%E6%B2%B3%E5%86%92%E9%9A%AA%22]%2C[%229558%22%2C%22%E5%B0%81%E9%AD%94%E7%8D%B5%E4%BA%BA(Bright%20Shadow)%22]%2C[%2260404%22%2C%22%E5%B7%B4%E5%93%88%E5%A7%86%E7%89%B9%E7%AB%99%E5%8B%99%E4%B8%AD%E5%BF%83%22]%2C[%2260292%22%2C%22%E7%A8%8B%E5%BC%8F%E8%A8%AD%E8%A8%88%E6%9D%BF%22]%2C[%2271458%22%2C%22%E5%B9%BB%E7%8D%B8%E5%B8%95%E9%AD%AF%22]%2C[%2220172%22%2C%22Terraria%22]%2C[%2233203%22%2C%22%E9%AD%94%E5%A5%B3%E4%B9%8B%E6%B3%89%20%E7%B3%BB%E5%88%97%22]%2C[%225786%22%2C%22%E9%AD%94%E7%89%A9%E7%8D%B5%E4%BA%BA%20%E7%B3%BB%E5%88%97%22]%2C[%2229016%22%2C%22%E6%AD%90%E7%B1%B3%E5%8A%A0%E8%BF%B7%E5%AE%AE%22]]; buap_modr=p014%20p001; buap_puoo=p202%20p102; ckHOME_visitor=233398280304193537; home_show_type=1; __gads=ID=5b18cd76d1b6c0f1:T=1724040688:RT=1741686348:S=ALNI_MajSztBPPxY2J4ZY2288Zl-LNbyGA; __gpi=UID=00000ec4cbe13c63:T=1724040688:RT=1741686348:S=ALNI_MZv54BhfAbXARpTrtYbrY9tMNTnZQ; __eoi=ID=e6a229caf010767c:T=1739950717:RT=1741686348:S=AA-AfjbUiuyU2DAFLZt-jd7rsWzJ; _ga_2Q21791Y9D=GS1.1.1741684885.98.1.1741686347.57.0.0; FCNEC=%5B%5B%22AKsRol8amP-vMRrETGmtL_h_oY98G013JlfpphcTFPFhaFfFfkv4nFUh3Z8qnd2S1YYGQ9Nwgq5B8G9e9i_CUG82gIv58OdN05RA2oThAyMW6TlBR0BqdEDZQOX6C-B9DXsj8IgcSdMv__Uu2g0aXkXWjmpm1ESxOA%3D%3D%22%5D%5D'}
dir_name:str = os.path.join(os.path.dirname(__file__), 'gen') # 檔案儲存位置

# 輸入參數區
sn:int = 0
delete_html:bool = False
delete_pdf:bool = False
no_picture:bool = True

# 參數順序: snA、是否刪除html檔案(d)、是否刪除PDF子文件(m)、是否不下載圖片(p)
def set_parameters():
    global sn
    if len(sys.argv) <= 1:
        raise Exception('請填入 sn 參數')

    sn = common.set_para(sys.argv[1])
    handle_not_necessary_para(2)

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
    url = f'{baha_web_url}?sn={sn}'
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
            picture_number = crawler_baha.download_pictures_from_soup(soup, dir_name, article_title, picture_number, 2)

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