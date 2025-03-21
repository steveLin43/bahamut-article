# bahamut-article
有些攻略網站的資訊可能會隨著網站關閉而消逝，為了避免這個狀況，因此創建這個下載專案。
目前攻略網站以巴哈姆特為最大宗，因此會由此拓展。
另外目前大多數網站的 CSS 都過於複雜，導致 PyPDF2 基本上都無法正常運作，除非只取文字內容或是額外許多的處理。

## 目前功能
### 巴哈姆特
* [將指定的一般巴哈姆特文章下載成一個 PDF 檔(半完成品)](lib/article_crawler.md)
* [將指定的"只看此樓"的文章下載成一個 HTML 檔(半完成品)](lib/spec_crawler.md)
* [將指定的小屋文章下載成一個 HTML 檔(半完成品)](lib/house_crawler.md)
* [將指定的精華文章下載成一個 HTML 檔(半完成品)](lib/star_crawler.md)

### 其他網站與小功能
* [奇樂奇樂(下載成一個 PDF 檔)](lib/kirokiro_crawler.md)
* [將指定目錄的 PDF 檔合成為一個 PDF 檔](lib/small_tool.md#將指定目錄的-PDF-檔合成為一個-PDF-檔)

## 巴哈姆特文章分析
1. 直接將頁面轉成 PDF 檔案時，時常因為頁面 CSS 的關係導致樓層跳躍與遮蓋
2. 網址 Query 參數，bsn 是討論版編號、snA 是文章編號、last=1#down 代表最後一樓、sn 是指定樓層編號
3. C.php 是一般文章、Co.php 是指定樓層文章、artwork.php 是小屋文章、G2.php 是精華文章
4. 查看全部留言一樣需要打 api 獲得，snB 是留言串編號，再加上 bsn、returnHtml=1、next_snC=0 等資訊
5. 一頁20樓

### 兩個##代表之後會再優化
* [修正日誌](lib/revise_log.md)
* 未來預計調整1:將巴哈姆特相關功能統合成一個，利用參數或是每個網址找一遍的方式結合
* 未來預計調整2:將常用參數拉成 config
