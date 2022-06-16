'''
Author: mengzonefire
Date: 2021-09-24 21:04:29
LastEditTime: 2022-05-13 13:40:01
LastEditors: mengzonefire
Description: 任务类基类
'''
from abc import abstractmethod
from common.text import task_finish
from common.tools import downloadFile, saveText
from common.const import getContext

class Task(object):
    # config = {}  # 任务配置列表， 即const.context

    def __init__(self):
        self.dataList = {  # 自定义爬取数据结构
            'picList': {},  # DATA: {serverFileName: {url: , twtId: }}
            'gifList': {},  # DATA: ↑
            'vidList': {},  # DATA: ↑
            'textList': {},  # DATA: {twtId: textContent}
        }

    @abstractmethod
    def getDataList(self):
        raise NotImplemented

    def start(self):
        self.getDataList()

        taskList = ['picList', 'gifList', 'vidList']

        # 判断getContext('args').mode下载模式
        if getContext('args').mode:
            if getContext('args').mode == 'pic':
                taskList = ['picList']
            elif getContext('args').mode == 'gif':
                taskList = ['gifList']
            elif getContext('args').mode == 'video':
                taskList = ['vidList']
            elif getContext('args').mode == 'text':
                taskList = []    
            elif getContext('args').mode == 'media':
                taskList = ['picList','vidList']
            else:
                taskList = ['picList', 'gifList', 'vidList']

        for key in taskList:
            for serverFileName in self.dataList[key]:
                url = self.dataList[key][serverFileName]['url']
                fileName = '{}_{}_{}'.format(
                    self.userName, self.dataList[key][serverFileName]['twtId'], serverFileName)
                downloadFile(url, fileName, self.savePath)

        # 只有mode不存在或者text模式下才会执行
        if not getContext('args').mode or getContext('args').mode == 'text':
            for twtId in self.dataList['textList']:
                content = self.dataList['textList'][twtId]
                fileName = '{}_{}.txt'.format(
                    self.userName, twtId)
                saveText(content, fileName, self.savePath)

        print(task_finish.format(self.savePath))
