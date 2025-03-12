import crawler_log
import json
import os
import requests
import time
from bs4 import BeautifulSoup

# 抓湯裡面的巴哈標題
def get_baha_title(soup:BeautifulSoup) -> str:
    try:
        title = soup.head.title.string
        result = title.split(' @')[0]
        return result
    except Exception:
        crawler_log.expected_log(42, 'get_baha_title 出錯。')
        raise

# 抓湯裡面的巴哈標頭
def get_baha_head(soup:BeautifulSoup) -> str:
    result_list:list = ['<head>']
    try:
        baha_head = soup.head

        meta_tags = baha_head.find_all('meta')
        meta_list = [0, 1, 7]
        for item in meta_list:
            result_list.append(str(meta_tags[item]))

        result_list.append(str(baha_head.title))

        link_tags = baha_head.find_all('link')
        # 如果背景主題為黑色，則會在 12 的位置多插入 <link>
        link_list = list(range(10)) + list(range(14, 33))
        for item in link_list:
            result_list.append(str(link_tags[item]))

        # 較重要的內容: bar、抓取人物大頭貼、樓層移動、右側長條廣告，細節請見文件
        script_tags = baha_head.find_all('script')
        script_list = [1, 4, 6, 7, 8, 9, 10, 12, 19, 25, 26, 32, 37, 38, 39, 48, 49, 50, 52, 60, 64]
        for item in script_list:
            result_list.append(str(script_tags[item]))

        result_list.append(str(baha_head.style))
        result_list.append('</meta></meta></meta></head>')

        return "\n".join(result_list)
    except Exception:
        crawler_log.expected_log(42, 'get_baha_head 出錯。')
        raise

# 抓一般文章的各樓內容
def get_content_by_page(soup:BeautifulSoup) -> str:
    result_list:list = ['<body>']
    try:
        baha_body = soup.body

        # 框架樣式
        result_list.append(handle_content_bar(baha_body))
        result_list.append(str(baha_body.find_all('script')[1]))
        result_list.append(str(baha_body.find('div', {'class': 'BH-menu'})))
        result_list.append('<div class="bh-banner" id="bh-banner"></div>')
        result_list.append('<div class="" id="BH-wrapper"><div id="BH-master"><div class="forum-ad_top"></div>')
        result_list.append('<!-- 框架樣式結束 -->')

        # 中心內容
        content = baha_body.find_all('section', {'class': 'c-section'})
        for item in content:
            if '<section class="c-section" id=' not in str(item): # 排除非內文的部分
                continue

            hide_comments = item.find_all('a', {'class': 'hide-reply is-hide'})
            if hide_comments:
                item = handle_morecomment(item)
            result_list.append(str(item))
            
        result_list.append('</div>') # BH-master
        result_list.append('<!-- 中心內容結束 -->')

        # 右側內容
        result_list.append(handle_content_right(baha_body))
        result_list.append('<!-- 右側內容結束 -->')

        # 最底下 footer
        #result_list.append(str(baha_body.find('br', {'class': 'clearfloat'})))

        result_list.append('</div></body>')

        return "\n".join(result_list)
    except Exception:
        crawler_log.expected_log(42, 'get_content_by_page 出錯。')
        raise

# 抓小屋創作的內容
def get_content_by_house(soup:BeautifulSoup) -> str:
    result_list:list = ['<body>']
    try:
        baha_body = soup.body

        ## 有空時會再精細篩檢
        '''
        # 框架樣式
        result_list.append(handle_content_bar(baha_body))
        result_list.append(str(baha_body.find_all('script')[1]))
        result_list.append(str(baha_body.find('div', {'class': 'BH-menu'})))
        result_list.append('<div class="bh-banner" id="bh-banner"></div>')
        result_list.append('<div class="" id="BH-wrapper"><div id="BH-master"><div class="forum-ad_top"></div>')
        result_list.append('<!-- 框架樣式結束 -->')

        # 中心內容
        content = baha_body.find_all('section', {'class': 'c-section'})
        for item in content:
            if '<section class="c-section" id=' not in str(item): # 排除非內文的部分
                continue

            hide_comments = item.find_all('a', {'class': 'hide-reply is-hide'})
            if hide_comments:
                item = handle_morecomment(item)
            #result_list.append(str(item))
        content = baha_body.find_all('div', {'class': 'article-content main'})
        for item in content:
            crawler_log.expected_log(10,f'{item}')
            result_list.append(str(item))
            
        result_list.append('</div>') # BH-master
        result_list.append('<!-- 中心內容結束 -->')

        # 右側內容
        #result_list.append(handle_content_right(baha_body))
        result_list.append('<!-- 右側內容結束 -->')

        # 最底下 footer
        #result_list.append(str(baha_body.find('br', {'class': 'clearfloat'})))

        result_list.append('</div></body>')

        return "\n".join(result_list)
        '''
        return str(baha_body)
    except Exception:
        crawler_log.expected_log(42, 'get_content_by_page 出錯。')
        raise

# 減少內文量，如果嫌麻煩或是出錯，可以直接 soup.body.find('div', {'class': 'TOP-bh'})
def handle_content_bar(soup_body:BeautifulSoup) -> str:
    content_bar_list:list = ['<div class="TOP-bh"><div class="TOP-data" id="BH-top-data">']
    content_bar_list.append('<div class="TOP-my"></div>')
    content_bar_list.append('<div class="TOP-msg" id="topBarMsg_more" style="display:none"></div>')
    content_bar_list.append('<script src="https://i2.bahamut.com.tw/js/forum_search.js" type="text/javascript"></script>')

    try:
        content_bar_list.append(str(soup_body.find('a', {'class': 'logo'})))
        content_bar_list.append(str(soup_body.find('div', {'class': 'header__search gcse-bar mobilehide'})))
        content_bar_list.append('</div></div>')

        return "\n".join(content_bar_list)

    except Exception:
        crawler_log.expected_log(42, 'handle_content_bar 出錯。')
        raise

# 減少內文量，如果嫌麻煩或是出錯，可以直接忽略
def handle_content_right(soup_body:BeautifulSoup) -> str:
    content_right_list:list = ['<div id="BH-slave">']
    try:
        # 板務人員
        content_right_list.append(str(soup_body.find('div', {'class': 'BH-rbox FM-rbox14'})))

        # 內文超連結 flySalve
        content_right_list.append(str(soup_body.style))
        content_right_list.append(str(soup_body.find_all('script', type='text/javascript')[-1]))

        # 向下滑動時的bar
        content_right_list.append('<div id="postInfo" style="display:none;"></div>')
        content_right_list.append('<template id="optionMenu"></template>')
        content_right_list.append('<template id="manageMenu"></template>')
        content_right_list.append('<div id="replyMenu" style="display:none;"></div>')
        content_right_list.append(str(soup_body.find('div', {'class': 'c-fixed--header'})))
        content_right_list.append('<script id="insertVideoTemplate" type="text/template"></script>')

        # 右下小功能
        content_right_list.append('<link href="https://i2.bahamut.com.tw/css/baha_quicktool.css" rel="stylesheet"/>')
        content_right_list.append(str(soup_body.find('div', {'class': 'baha_quicktool no-bottombar'})))
        content_right_list.append('<script src="https://i2.bahamut.com.tw/js/quicktool.js"></script>')

        content_right_list.append('</div>')
        return "\n".join(content_right_list)

    except Exception:
        crawler_log.expected_log(42, 'handle_content_right 出錯。')
        raise

# 抓取討論串中各樓的所有圖片
def download_pictures_from_soup(soup:BeautifulSoup, path:str, pic_title:str, number:int) -> int:
    content_list = soup.body.find_all('div', {'class': 'c-article__content'})
    pictures_list = []
    defective_nums = 0

    # 針對每則回覆進行提取
    for content in content_list:
        pictures_list += content.find_all('img', {'class': 'lazyload'})

    # 提取連結並下載
    for pic in pictures_list:
        try:
            pic_url = pic.get('data-src')

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
            response = requests.get(pic_url, headers=headers, timeout=10)
            response.raise_for_status() # 確保有正常取得圖片

            pic_name = os.path.join(path, f'{pic_title}-{number:02}.{file_extension}')
            with open(pic_name, "wb") as file:
                file.write(response.content)

            number += 1
            time.sleep(1)

        except Exception as e:
            crawler_log.unexpected_error()
            continue

    if defective_nums != 0:
        print('共有{defective_nums}張圖片沒有成功下載，請記得確認。')

    return number

# 取得更多內容的資料
def get_morecomment_content(bsn:int, snB:int) -> str:
    ## morecomment html conent (固定變數)=======================================================
    data_comment = {
        "bsn": bsn,
        "snB": snB,
        "sn": 1  # 變動值
    }
    second = '<button class="more tippy-reply-menu" type="button"><i class="material-icons"></i></button>'
    eighth = '<div class="buttonbar"><button class="gp" onclick="Forum.C.commentGp(this);" title="推一個！" type="button"><i class="material-icons"></i></button><a class="gp-count" data-gp="0" href="javascript:;"></a><button class="bp" onclick="Forum.C.commentBp(this);" title="我要噓…" type="button"><i class="material-icons"></i></button><a class="bp-count" data-bp="0" href="javascript:;"></a>'
    ## =========================================================================================

    time.sleep(1)
    url = f'https://forum.gamer.com.tw/ajax/moreCommend.php?bsn={bsn}&snB={snB}'
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        crawler_log.expected_log(44, json.dumps(response.json()))
        return ''
    comments = response.json()

    result = []
    for key, value in comments.items():
        if key == 'next_snC':
            continue
        ## morecomment html conent (變動變數)=======================================================
        data_comment['sn'] = value['sn']
        data_comment_str = json.dumps(data_comment)
        username = value['userid'].lower()
        
        # 處理訊息內容
        value_content = value['content']
        if (value['content'][0] == '[') and (']' in value['content']) and (':' in value['content']): #回覆對象 ex: [test123:測試321]訊息訊息訊息
            temp = value['content'].split(']')
            temp2 = temp[0].split(':')
            a_tag = f'<a target="_blank" href="https://home.gamer.com.tw/{temp2[0][1:]}">{temp2[1]}</a>'
            value_content = a_tag + temp[-1]

        if (value['content'][0] == '#') and ('# ' in value['content']) and (':' in value['content']): #回覆樓層 ex: #test123:測試321# 訊息訊息訊息
            temp = value['content'].split('# ')
            temp2 = temp[0].split(':')
            # 超連結沒必要所以單純賦予顏色
            #a_tag = f'<a href="javascript:Forum.C.openCommentDialog(838, 23194,3392104);">{temp2[1]}</a> ' 
            a_tag = f'<span style="color: rgb(17, 126, 150)">{temp2[0][1:]}</span> '
            value_content = a_tag + temp[-1]

        first = f'<div class="c-reply__item" data-comment=\'{data_comment_str}\' id="Commendcontent_{value['sn']}" name="comment_parent"><div>'
        third = f'<a class="reply-avatar user--sm" href="//home.gamer.com.tw/{username}" target="_blank"><img class="gamercard lazyload" data-gamercard-userid="{value['userid']}" data-src="https://avatar2.bahamut.com.tw/avataruserpic/{username[0]}/{username[1]}/{username}/{username}_s.png"/></a>'
        forth = f'<div class="reply-content"><a class="reply-content__user" href="//home.gamer.com.tw/{username}" target="_blank">{value['nick']}</a>'
        fifth = f'<article class="reply-content__article c-article"><span class="comment_content" data-formatted="yes"> {value_content}</span></article>'
        sixth = f'<div class="reply-content__footer"><div class="edittime" name="comment_floor" style="margin-right:6px;">B{value['floor']}</div>'
        seventh = f'<div class="edittime" data-tippy-content="留言時間 {value['wtime']}"> {value['wtime']}</div>'
        nineth = f'<button class="tag" onclick="Forum.C.replyToFloor({value['snB']}, {value['sn']}, {value['floor']});" type="button">回覆</button></div></div></div></div></div>'
        ## =========================================================================================
        result_value = first + second + third + forth + fifth + sixth + seventh + eighth + nineth
        result.append(result_value)

    connect_str = ''
    result.reverse()
    front = f'<div id="Commendlist_{snB}">'
    return front + connect_str.join(result) + '</div>'

def handle_morecomment(soup_content:BeautifulSoup) -> BeautifulSoup:
    # 尋找替換位置
    replaced = soup_content.find('div', {'class': 'c-post__footer c-reply'})

    # 產生替換內容
    new_content = '<div class="c-post__footer c-reply">'
    div_tag = soup_content.find('div', {'class': 'c-reply__item'})
    data_comment = div_tag['data-comment']
    comment_data = json.loads(data_comment)
    new_content += get_morecomment_content(comment_data['bsn'], comment_data['snB']) + '</div>'
    
    replaced.replace_with(BeautifulSoup(new_content, 'html.parser'))
    return soup_content

# 特定半形符號轉全形
def half_to_full(trans_str:str) -> str:
    halfwidth = "/\\*:?\"<>|"
    fullwidth = "／＼＊：？＂＜＞｜"

    translation_table = str.maketrans(halfwidth, fullwidth) # 映射表
    return trans_str.translate(translation_table)