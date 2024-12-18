# bahamut-article
## 目前功能
* 將指定的巴哈姆特文章下載成一個 PDF 檔(製作中)

## 巴哈姆特文章分析
1. 直接將頁面轉成 PDF 檔案時，時常因為頁面 CSS 的關係導致樓層跳躍與遮蓋
2. 網址 Query 參數，bsn 是討論版編號、snA 是文章編號、last=1#down 代表最後一樓
3. 一頁20樓

# 下載巴哈姆特文章內容
1. 需下載 wkhtmltopdf
2. 執行指令：`python aritcle_crawler.py`
3. 預設保留 html 檔案