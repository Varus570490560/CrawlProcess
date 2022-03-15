# CrawlProcess
这是一个简易的爬虫框架。主要实现的在数据爬取的过程中数据去重和爬虫并发的问题。
数据去重：依赖于mysql ，在connect_database.save()函数中以字典形式提交数据，以元组方式给出组合重复依赖键（需提前搭建mysql环境并且执行sql语句）
爬虫并发：将多个任务加入到muti_thread.task中（以元组形式，(fun,param1,param2,...)）,执行muti_thread_execute(),参数为开辟线程数
