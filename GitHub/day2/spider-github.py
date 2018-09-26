import requests
import pymongo
from lxml import html


class GithubRepo:

    name = ''
    author = ''
    summary = ''
    tag_list = []
    license = ''
    lastUpdateTime = ''
    language = ''
    star_num = 0

    def tostring(self):
        return self.__dict__


def page_info(key_world, language, page):
    url = ('https://github.com/search?l=%s&o=desc&q=%s&s=stars&type=Repositories&p=%d' % (language, key_world, page))

    session = requests.session()
    response = session.get(url)

    tree = html.fromstring(response.text)
    repo_list = []
    # 仓库列表
    repo_html_list = tree.xpath('//ul[@class="repo-list"]/child::*')
    for repo_html in repo_html_list:
        repo = GithubRepo()
        # 注意这里的. 表示从当前元素下获取子元素，如果没有，则会从全局html中获取
        repo.name = repo_html.xpath('.//h3/a/@href')[0].split('/')[2]
        repo.author = repo_html.xpath('.//h3/a/@href')[0].split('/')[1]
        # text属性只包含了当前节点的text，而没有包含子节点的，因此需要使用text_content()方法
        # summary 并非必定存在字段，因此需要非空判断
        if repo_html.xpath('.//p[contains(@class,"d-inline-block")]'):
            repo.summary = repo_html.xpath('.//p[contains(@class,"d-inline-block")]')[0].text_content().strip()
        # 由于标签包含许多空格以及\n，需要去除
        repo.tag_list = list(map(lambda x: x.strip(), repo_html.xpath('.//a[contains(@class,"topic-tag")]/text()')))
        repo.license = repo_html.xpath('.//div[@class="d-flex flex-wrap"]//p[position()=1]')[0].text.strip()
        repo.lastUpdateTime = repo_html.xpath('.//div[@class="d-flex flex-wrap"]//relative-time/@datetime')[0]
        repo.language = repo_html.xpath('.//span[@class="repo-language-color"]/parent::div[1]')[0].text_content().strip()
        repo.star_num = repo_html.xpath('.//a[@class="muted-link"]')[0].text_content().strip()
        repo_list.append(repo)

    # 返回爬取结果
    return repo_list


keyWorld = 'swift'
language = 'Swift'
# 最大页数
max_page = 10

repos = []
# 注意这里分页是从1开始，第0页数据与第一页相同（负数同理）
for i in range(1, max_page + 1):
    repos.extend(page_info(keyWorld, language, i))


client = pymongo.MongoClient("mongodb://127.0.0.1:27101/")
db = client['spider']
collection = db['GitHub']
# 直接存入 class 对象会抛出异常，需要将数组元素转为字典（dict）类型
collection.insert_many(list(map(lambda x: x.tostring(), repos)))
client.close()
