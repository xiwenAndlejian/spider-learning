import requests
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
        print(self.__dict__)


keyWorld = 'swift'
language = 'Swift'
URL = ('https://github.com/search?l=%s&o=desc&q=%s&s=stars&type=Repositories&p=5' % (language, keyWorld))

session = requests.session()
response = session.get(URL)

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
    repo.summary = repo_html.xpath('.//p[contains(@class,"d-inline-block")]')[0].text_content().strip()
    # 由于标签包含许多空格以及\n，需要去除
    repo.tag_list = list(map(lambda x: x.strip(), repo_html.xpath('.//a[contains(@class,"topic-tag")]/text()')))
    repo.license = repo_html.xpath('.//div[@class="d-flex flex-wrap"]//p[position()=1]')[0].text.strip()
    repo.lastUpdateTime = repo_html.xpath('.//div[@class="d-flex flex-wrap"]//relative-time/@datetime')[0]
    repo.language = repo_html.xpath('.//span[@class="repo-language-color"]/parent::div[1]')[0].text_content().strip()
    repo.star_num = repo_html.xpath('.//a[@class="muted-link"]')[0].text_content().strip()
    repo_list.append(repo)

# 输出爬取结果
for repo in repo_list:
    repo.tostring()
