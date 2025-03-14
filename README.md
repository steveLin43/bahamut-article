# bahamut-article
## 目前功能
* [將指定的一般巴哈姆特文章下載成一個 PDF 檔(半完成品)](lib/article_crawler.md)
* [將指定的"只看此樓"的文章下載成一個 HTML 檔(半完成品)](lib/spec_crawler.md)
* [將指定的小屋文章下載成一個 HTML 檔(半完成品)](lib/house_crawler.md)

## 巴哈姆特文章分析
1. 直接將頁面轉成 PDF 檔案時，時常因為頁面 CSS 的關係導致樓層跳躍與遮蓋
2. 網址 Query 參數，bsn 是討論版編號、snA 是文章編號、last=1#down 代表最後一樓、sn 是指定樓層編號
3. C.php 是一般文章、Co.php 是指定樓層文章
4. 查看全部留言一樣需要打 api 獲得，snB 是留言串編號，再加上 bsn、returnHtml=1、next_snC=0 等資訊
5. 一頁20樓

### 兩個##代表之後會再優化
* [修正日誌](lib/revise_log.md)
