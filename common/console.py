'''
Author: mengzonefire
Date: 2021-09-21 09:20:19
LastEditTime: 2022-03-03 02:45:01
LastEditors: mengzonefire
Description: 
'''
import os
from task.singlePageTask import SinglePageTask
from task.userMediaTask import UserMediaTask
from typing import List
from common.text import *
from common.const import *
from common.tools import get_token, getHeader, getUserId, saveEnv


def cmdMode():
    url_list = []
    print(input_ask)
    while True:
        temp = input()
        if not temp:
            break
        if '//t.co/' in temp or '//twitter.com/' in temp:
            url_list.append(temp)
        else:
            cmdCommand(temp)
            return
    if url_list:
        startCrawl(url_list)

    if input(continue_ask):
        cmdMode()


def startCrawl(url_list: List):
    dl_path = getContext('dl_path')
    if not os.path.exists(dl_path):
        os.mkdir(dl_path)

    for page_url in url_list:
        print('\n正在提取: {}'.format(page_url))
        urlHandler(page_url)


def urlHandler(url: str):
    # userHomePage
    user_link = p_user_link.findall(url)
    if user_link:
        userName = user_link[0]
        userId = getUserId(userName)
        if userId:
            UserMediaTask(userName, userId).start()
        return

    # SinglePage
    twt_link = p_twt_link.findall(url)
    if twt_link:
        userName = twt_link[0][0]
        twtId = twt_link[0][1]
        SinglePageTask(userName, twtId).start()
        return

def followHandler(url: str):
    # userHomePage
    user_link = p_user_link.findall(url)
    if user_link:
        userName = user_link[0]
        userId = getUserId(userName)
        if userId:
            # 用户关注列表
            getUserFollowing(userId)
        return


# 获取用户关注列表用户ID
def getUserFollowing(id: str):
    response = getContext('globalSession').get(
            userFollowersApi, params={'variables': userFollowersApiPar.format(id, 99), 'features': userFollowersApiPar2}, proxies=getContext(
                'proxy'), headers=getContext('headers'))
    if response.status_code != 200:
        print(http_warning.format('FollowingTask.getDataList',
            response.status_code, getHttpText(response.status_code)))
        return 
    pageContent = response.text
    # 匹配出用户ID和用户名
    userNameList = p_user_name.findall(pageContent)
    userIdList = p_user_id.findall(pageContent)
    # 遍历用户ID列表index，开始UserMediaTask
    for index in range(len(userIdList)):
        userName = userNameList[index]
        userId = userIdList[index]
        print('\n开始: {}({})'.format(userName, userId))
        UserMediaTask(userName, userId).start()


def cmdCommand(command):
    if command == 'exit':
        return
    elif command == 'set cookie':
        headers = getContext("headers")
        cookie = input(input_cookie_ask).strip()
        if cookie:
            token = get_token(cookie)
            if token:
                headers['x-csrf-token'] = token
                headers['Cookie'] = cookie
                print(cookie_success)
            else:
                print(cookie_warning)
        else:
            headers['Cookie'] = ''  # 清除cookie
            getHeader()  # 重新获取游客token
            print(cookie_purge_success)
        setContext('headers', headers)
        saveEnv()
    else:
        print(input_warning)
    cmdMode()
