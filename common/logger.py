'''
Author: mengzonefire
Date: 2021-09-21 09:23:35
LastEditTime: 2022-03-03 13:32:27
LastEditors: mengzonefire
Description: log模块
'''
import os
import re
from common.const import getContext
from common.text import log_warning


def write_log(log_name, log_content):
    log_path = getContext('log_path')
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    file_path = re.sub(
        r'[:*?"<>|]', '', os.path.join(log_path, log_name+'.log')) # 去除路径内的非法字符
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(log_content)
        print(log_warning.format(file_path))
