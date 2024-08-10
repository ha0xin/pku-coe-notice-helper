'''获取并聚合信息，制作消息'''
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup


class Notice:
    '''通知基类'''
    def __init__(self, title, link, date, content):
        self.title = title
        self.link = link
        self.date = date
        self.content = content

    def __str__(self):
        return f"Title: {self.title}\nLink: {self.link}\nDate: {self.date}\nContent: {self.content}\n"

    def __repr__(self):
        return f"Title: {self.title}\nLink: {self.link}\nDate: {self.date}\nContent: {self.content}\n"

class DeanNotice(Notice):
    '''教务部公告'''
    def __init__(self, title, link, date, content):
        super().__init__(title, link, date, content)
        self.department = "教务部"

    def message(self):
        '''将公告转换为消息'''
        message = f"【教务部】{self.title}\n时间：{self.date}\n链接：{self.link}\n"
        return message

class SchoolNotice(Notice):
    '''学校和部门公告'''
    def __init__(self, title, link, date, content, department, id):
        super().__init__(title, link, date, content)
        self.department = department
        self.id = id

    def __str__(self):
        base_str = super().__str__()
        return base_str + f"Department: {self.department}\nID: {self.id}\n"
    
    def message(self):
        '''将公告转换为消息'''
        message = f"【{self.department}】{self.title}\n时间：{self.date}\n链接：{self.link}\n"
        return message

class COENotice(Notice):
    '''工学院公告'''
    def __init__(self, title, link, date, content, label):
        super().__init__(title, link, date, content)
        self.label = label
        self.department = f"COE-{label}"

    def __str__(self):
        base_str = super().__str__()
        return base_str + f"Label: {self.label}\n"
    
    def message(self):
        '''将公告转换为消息'''
        message = f"【{self.department}】{self.title}\n时间：{self.date}\n链接：{self.link}\n"
        return message

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200",
    "sec-ch-ua": '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"'
}

dean_prefix = "https://dean.pku.edu.cn/web/"
coe_prefix = "https://www.coe.pku.edu.cn"
school_prefix = "https://portal.pku.edu.cn/portal2017/#/schoolNoticeDetail/"

def get_dean_notices():
    '''获取教务部公告'''
    url = 'https://dean.pku.edu.cn/web/notice.php'
    response = requests.get(url, headers=headers, timeout=10)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    notice_boxes = soup.find_all('div', class_='notice_item')

    notices = []
    for notice_box in notice_boxes:
        date = notice_box.find('span').get_text()
        # 将形如 “2023-04-24” 的日期转换为datetime对象
        date = datetime.strptime(date, "%Y-%m-%d")
        link = notice_box.find('a')['href']
        link = dean_prefix + link
        title = notice_box.find('a').get_text()
        
        notice = DeanNotice(title, link, date, "")
        notices.append(notice)

    return notices

def get_dept_notices():
    '''获取单位公告'''
    url = 'https://portal.pku.edu.cn/portal2017/notice/retrAllDeptNotice.do'
    data = {
        "keyword": "ALL",
        "limit": 20,
        "start": 0
    }
    response = requests.post(url, headers=headers, data=data, timeout=10)
    body = response.json()
    items = body['rows']

    # blacklist = ["讣告", "招标", "废标", "竞争性磋商", "招聘"]

    notices = []
    for item in items:
        title = item['Title']
        # if any(keyword in title for keyword in blacklist):
        #     continue
        time = item['Time']
        # 将形如2023-08-09 10:34:12的时间转换为datetime对象
        time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        department = item['Department']
        id = item['Number']
        link = school_prefix + id
        notice = SchoolNotice(title, link, time, "", department, id)
        notices.append(notice)

    return notices

def get_school_notices():
    '''获取学校公告'''
    url = 'https://portal.pku.edu.cn/portal2017/notice/retrAllSchoolNotice.do'
    #  https://portal.pku.edu.cn/portal2017/notice/retrAllSchoolNotice.do?keyword=ALL&limit=20&start=0
    data = {
        "keyword": "ALL",
        "limit": 20,
        "start": 0
    }
    response = requests.post(url, headers=headers, data=data, timeout=10)
    body = response.json()
    items = body['rows']

    notices = []
    for item in items:
        title = item['Title']
        time = item['Time']
        # 将形如2023-08-09 10:34:12的时间转换为datetime对象
        time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        department = item['Department']
        id = item['Number']
        link = school_prefix + id
        notice = SchoolNotice(title, link, time, "", department, id)
        notices.append(notice)

    return notices

def get_school_notice_detail_by_id(id):
    '''获取学校公告详情'''
    url = 'https://portal.pku.edu.cn/portal2017/notice/getSchoolNoticeDetailById.do'
    data = {
        "id": id
    }
    response = requests.post(url, headers=headers, data=data, timeout=10)
    body = response.json()
    print(body)

def get_coe_notices():
    '''获取工学院学院公告'''
    # url = "https://www.coe.pku.edu.cn/announcements/college_notice.html"
    url = "https://www.coe.pku.edu.cn/announcements/college_notice/p/1.html"
    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = 'utf-8' # 解决中文乱码问题
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    
    items = soup.select('.li')

    notices = []
    for item in items:
        # 提取标签
        label = item.select_one('.label').text
        # 提取标题
        title = item.select_one('.t a').text
        title = title.replace('\n', '').replace('\r', '') # 去除标题中的回车换行
        # 提取链接
        link = item.select_one('.t a')['href']
        link = coe_prefix + link
        # 提取日期
        date = item.select_one('.date').text
        # 将形如 “2023.07.02” 的日期转换为datetime对象
        date = datetime.strptime(date, "%Y.%m.%d")
        notice = COENotice(title, link, date, "", label)
        notices.append(notice)
    
    return notices

def get_coe_undergraduates_notices():
    '''获取工学院本科生通知'''
    # url = "https://www.coe.pku.edu.cn/undergraduates/notice.html"
    url = "https://www.coe.pku.edu.cn/undergraduates/notice/p/1.html"
    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = 'utf-8' # 解决中文乱码问题
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    items = soup.select('.li')

    notices = []
    for item in items:
        # 提取标签
        label = item.select_one('.label').text
        # 提取标题
        title = item.select_one('.t a').text
        title = title.replace('\n', '').replace('\r', '') # 去除标题中的回车换行
        # 提取链接
        link = item.select_one('.t a')['href']
        link = coe_prefix + link
        # 提取日期
        date = item.select_one('.date').text
        # 将形如 “2023.07.02” 的日期转换为datetime对象
        date = datetime.strptime(date, "%Y.%m.%d")
        notice = COENotice(title, link, date, "", label)
        notices.append(notice)

    return notices

def aggregate_notices():
    '''获取所有公告'''
    notices = []
    notices.extend(get_school_notices())
    notices.extend(get_dept_notices())
    notices.extend(get_dean_notices())
    notices.extend(get_coe_notices())
    # notices.extend(get_coe_undergraduates_notices())
    
    # 获取当前脚本的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    blacklist_path = os.path.join(script_dir, "blacklist.txt")
    
    with open(blacklist_path, "r", encoding='utf-8') as f:
        blacklist = f.readlines()
        blacklist = [line.strip() for line in blacklist]
    
    notices = [notice for notice in notices if all(keyword not in notice.title for keyword in blacklist)]
    
    return notices

def save_notices(notices):
    '''保存公告标题到文件'''
    with open("notices.txt", "a", encoding='utf-8') as f:
        for notice in notices:
            f.write(notice.title + "\n")

def read_saved_notices():
    '''读取已保存的公告标题'''
    try:
        with open("notices.txt", "r", encoding='utf-8') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]
            return lines
    except FileNotFoundError:
        return []
    
def filter_notices(notices):
    '''过滤已保存的公告'''
    saved_notices = read_saved_notices()
    filtered_notices = []
    for notice in notices:
        if notice.title not in saved_notices:
            filtered_notices.append(notice)
    return filtered_notices

def make_wechat_message():
    '''生成微信消息'''
    notices = aggregate_notices()
    notices = filter_notices(notices)
    notices = sorted(notices, key=lambda notice: notice.date, reverse=True)
    length = len(notices)
    departments = set([notice.department for notice in notices])
    if len(departments) > 5:
        dept_str = "、".join(list(departments)[:5]) + "等"
    else:
        dept_str = "、".join(departments)
    
    if length == 0:
        return None, None, length, None
    if length == 1:
        summary = f"【{notices[0].department}】{notices[0].title}"
    else: # length > 1
        summary = f"新增来自【{dept_str}】的【{length}】条通知"
    link = notices[0].link
    message = f"新增来自【{dept_str}】的{length}条通知：\n"
    num = 1
    for notice in notices:
        num_str = f"【{num}】"
        message += num_str.center(40,"-") + "\n" + notice.message()
        num += 1
    save_notices(notices)
    return summary, message, length, link
