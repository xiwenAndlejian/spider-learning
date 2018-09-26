# 爬取GitHub

从day1中我们已经可以爬取`GitHub`第一页搜索结果的内容了
现在我们来实现一下

- 多页结果获取
- 存入数据库中

## 分析网页

### URL

接着`day1`的内容，在浏览器的搜索结果页面点击下一页

获得当前页面`url`：https://github.com/search?l=Swift&o=desc&p=2&q=swift&s=stars&type=Repositories

**新增参数**`p`: 值=2，对应`page`页数

### XPath

没有新的数据需要获取，因此沿用`day1`内容

### 数据库存储

我选择`MongoDB`数据库

```python
client = pymongo.MongoClient("mongodb://127.0.0.1:27101/")
db = client['spider']
collection = db['GitHub']
# 直接存入 class 对象会抛出异常，需要将数组元素转为字典（dict）类型
collection.insert_many(list(map(lambda x: x.tostring(), repos)))
client.close()
```

[python实现](spider-github.py)

## 总结

### 数组合并

list1 = [1, 2]
list2 = [3, 4]

1. 覆盖原数组：

   ```python
   list1.extend(list2)
   # list1 = [1, 2, 3, 4]
   ```

1. 生成新数组

   ```python
   list3 = list1 + list2
   # list3 = [1, 2, 3, 4] 注意：此处list1，list2不变
   ```
