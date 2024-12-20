from bs4 import BeautifulSoup

# 抓湯裡面的巴哈標題
def get_baha_title(soup:BeautifulSoup) -> str:
    try:
        title = soup.head.title.string
        result = title.split(' @')[0]
        return result
    except Exception as e:
        print(f'get_baha_title 出現錯誤: {e}')
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

        # 較重要的內容: bar(1 4 6 9 10 32 53)、抓取人物大頭貼(37)、樓層移動(48)、右側長條廣告(69-71)
        script_tags = baha_head.find_all('script')
        script_list = [1, 4, 6, 9, 10, 32, 37, 48, 53]
        for item in script_list:
            result_list.append(str(script_tags[item]))

        result_list.append(str(baha_head.style))
        result_list.append('</head>')

        return "\n".join(result_list)
    except Exception as e:
        print(f'get_baha_head 出現錯誤: {e}')
        raise

# 抓湯裡面的各樓內容
def get_content_by_page(soup:BeautifulSoup) -> str:
    # todo: 圖片目前沒有顯示
    try:
        """
        # 此方法會省略script內容，需要額外拉出來
        content = soup.find_all('div', {'class': 'c-section__main c-post'})
        for item in content:
            # todo: 加入一些條件，將內容調整得更美觀
            str_list.append(str(item))
        """
        # 暫時先全部取
        baha_content = soup.body
        return str(baha_content)

    except Exception as e:
        print(f'get_content_by_page 出現錯誤: {e}')
        raise