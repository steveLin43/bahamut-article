import logging
import os
from datetime import datetime

now = datetime.now()
date = now.strftime('%Y-%m-%d')
dir_name:str = os.path.join(os.path.dirname(__file__), 'log')
log_name = os.path.join(dir_name, f'{date}.log')

if not os.path.exists(dir_name):
    os.makedirs(dir_name)

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, filename=log_name, filemode='a', format=FORMAT, encoding='utf-8')

log_message_map:dict = {
    0: 'test log',
    # debug    10
    10: '輸入參數資訊：',
    # info     20
    20: '未找到樓層資訊。',
    21: '可能是網址或是網路錯誤。',
    # warning  30
    # error    40
    40: '參數錯誤導致失敗。',
    41: '處理頁面時出現錯誤。',
    42: 'crawler_detail 出現錯誤。',
    43: '處理圖片時出現錯誤。',
    44: '打 API 時非正常回應。',
    # critical 50
}


def unexpected_error():
    logging.error("Catch an unexpected exception.", exc_info=True)

def expected_log(log_number:int = 0, addition_msg:str = ''):
    map_message = log_message_map.get(log_number, 'Unknown')
    message = f'{map_message} {addition_msg}'
    
    if message == 'Unknown':
        logging.error("Catch an unknown exception.", exc_info=True)
    elif log_number < 20:
        logging.debug(message)
    elif log_number < 30:
        logging.info(message)
    elif log_number < 40:
        logging.warning(message)
    elif log_number < 50:
        logging.error(message, exc_info=True)
    else:
        logging.critical(message, exc_info=True)
