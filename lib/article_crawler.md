# 下載巴哈姆特文章內容
1. 需下載 wkhtmltopdf
2. 執行指令：`python aritcle_crawler.py 討論版編號 文章編號 刪除檔案`

# 變數解釋
刪除檔案：選擇是否刪除產生的 html 檔案，保留為0、刪除為1。預設保留 html 檔案。

# 抓取巴哈標頭的 script 細節
## bar
1. <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js"></script>
4. <script src="https://i2.bahamut.com.tw/js/plugins/js.cookie-2.1.4.js"></script>
6. <script src="https://i2.bahamut.com.tw/js/plugins/dialogify.min.js?v=1708584729"></script>
7. <script src="https://i2.bahamut.com.tw/js/user_login.js?v=1709623193"></script>
8. <script defer="" src="https://i2.bahamut.com.tw/js/notification_notice.js?v=1733301248"></script>
9. <script defer="" src="https://i2.bahamut.com.tw/js/BH_topBar_noegg.js?v=1733301248"></script>
10. <script defer="" src="https://i2.bahamut.com.tw/js/BH_mainmenu.js?v=1728375589"></script>
12. <script src="https://i2.bahamut.com.tw/js/util.js?v=1728288149"></script>
19. <script src="https://i2.bahamut.com.tw/js/signin_ad.js?v=1732498015"></script>
25. <script src="https://i2.bahamut.com.tw/js/plugins/popper_core-2.5.4.min.js?v=1610513978" type="text/javascript"></script>
26. <script src="https://i2.bahamut.com.tw/js/plugins/tippy-6.3.7.min.js?v=1663218249" type="text/javascript"></script>
32. <script src="https://i2.bahamut.com.tw/js/forum_lastBoard.js?v=1690959617" type="text/javascript"></script>
38. <script src="https://i2.bahamut.com.tw/JS/honorData.js?v=1731997000"></script>
39. <script src="https://i2.bahamut.com.tw/js/movetomobile.js"></script>
49. <script src="https://i2.bahamut.com.tw/js/forum_post.js?v=1733975140"></script>
50. <script src="https://i2.bahamut.com.tw/js/forum_common.js?v=1716448130"></script>
52. <script src="https://i2.bahamut.com.tw/js/forum_vote.js?v=1683002637"></script>
60. <script src="https://i2.bahamut.com.tw/js/plugins/sticker.js?v=1733991402"></script>
64. <script defer="" src="https://i2.bahamut.com.tw/js/creator.js?v=1728960765"></script>

## 抓取人物大頭貼
37. <script async="" src="https://i2.bahamut.com.tw/js/plugins/lazysizes-3.0.0.min.js"></script>

## 樓層移動
48. <script src="https://i2.bahamut.com.tw/js/forum_c.js?v=1732592887"></script>

## 右側長條廣告
69. <script async="async" src="https://securepubads.g.doubleclick.net/tag/js/gpt.js"></script>
70. <script>var googletag = googletag || {};googletag.cmd = googletag.cmd || [];</script>
71. <script>if (window.Cookies) {...}...</script>


--enable-local-file-access

article_title需要流程調整