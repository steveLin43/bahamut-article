from . import common
from . import crawler_log
import json
import os
import requests
import time
from bs4 import BeautifulSoup

# 抓奇樂表頭 (僅剩設定版型的功能)
def get_kiro_head(soup:BeautifulSoup) -> str:
    head_list:list = ['<head>']
    try:
        head_list.append('<meta charset="UTF-8">')
        head_list.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        head_list.append('<style> .main-content { padding-left: 80px;} </style>')
        head_list.append('</head>')

        return "\n".join(head_list)
    except Exception:
        crawler_log.expected_log(42, 'get_kiro_head 出錯。')
        raise

# 抓奇樂內容
# 輸出參數1：文章內容
# 輸出參數2：是否有圖片在表格內。0代表圖片都在文章內，1代表有圖片在表格內。
def get_kiro_content(soup:BeautifulSoup) -> tuple:
    result_list:list = ['<body><br>']
    kiro_picture_table = 0 # 這網站的圖片網址在文章中以及在表格中的標籤不同
    try:
        # 中心內容
        main_content = soup.body.find('article', {'id': 'the-post'})

        # 處理超連結
        result_list.append('<div class="main-content tie-col-md-8 tie-col-xs-12" role="main">')
        for item in main_content.find_all('img', {'decoding': 'async'}):
            data_src = item.get('data-src')
            data_lazy_src = item.get('data-lazy-src')
            
            if data_src is not None: # 代表圖片在文章內
                item['src'] = 'https:' + data_src
            elif data_lazy_src is not None: # 圖片在表格內
                kiro_picture_table = 1
                item['src'] = 'https:' + item['data-lazy-src']
            else: # 圖片在表格內的附加產物
                item['src'] = 'https:' + item['src']
        
        # 移除 header 與 footer
        delete_list = []
        delete_list.append(main_content.find('nav', {'id': 'breadcrumb'}))
        delete_list.append(main_content.find('span', {'class': 'post-cat-wrap'}))
        delete_list.append(main_content.find('div', {'class': 'share-buttons share-buttons-bottom'}))
        delete_list.append(main_content.find('a', {'data-type': 'post'}))
        for delete_item in delete_list:
            if delete_item is not None:
                delete_item.decompose()

        result_list.append(str(main_content))
        result_list.append('</div></body>')
        
        return "\n".join(result_list), kiro_picture_table

    except Exception:
        crawler_log.expected_log(42, 'get_kiro_content 出錯。')
        raise

# 抓取各種文章中的所有圖片
# soup:     網站內容
# path:     檔案路徑
# pic_title:檔案標題
# number:   圖片編號
# web_type: 網站種類
def download_pictures_from_web(soup:BeautifulSoup, path:str, pic_title:str, number:int, web_type: int) -> int:
    if web_type == 1: # kirokiro，且圖片都在文章內
        pictures_list = soup.body.find_all('img', {'decoding': 'async'})
        picture_tag = 'data-src'
    elif web_type == 1: # kirokiro，且有圖片在表格內
        pictures_list = soup.body.find_all('img', {'decoding': 'async'})
        picture_tag = 'data-lazy-src'

    else:
        crawler_log.expected_log(40, f'download_pictures_from_web 輸入的 web_type：{web_type}')
        return 0

    return common.download_pictures(pictures_list, number, path, pic_title, picture_tag, True)
