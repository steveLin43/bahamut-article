# 下載"小屋創作"的文章內容
1. 使用時須加入 cookie 的值，否則會導轉到舊版頁面，目前寫死在 house_crawler.py 第12行。
~~需下載 wkhtmltopdf~~ 由於巴哈的 CSS 樣式過於複雜，導致 pdfkit 無法正常處理
2. 暫時預設不產生 PDF 檔案，僅產生 html 檔案
2. 執行指令範例：`python house_crawler.py 文章編號 刪除html檔案 刪除PDF子文件 不下載圖片`
3. 編號以後的參數不必按照順序

# 變數解釋
刪除html檔案(d)：選擇是否刪除產生的 html 檔案，預設保留，如果要刪除則輸入d。
刪除PDF子文件(m)：選擇是否刪除產生的 PDF 子檔案，預設保留，如果要刪除則輸入m。
不下載圖片(p)：選擇是否不下載討論串中的圖片，預設下載，如果不下載則輸入p。