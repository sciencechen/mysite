import os


# 要同时执行，否则执行的每一条命令是作用在当前目录下，
# 所以要cd转跳的瞬间（os.system前半句还未执行完的瞬间）
# 把python run.py执行完
scrapy = '人工智能'
mode = "root"
cmd = 'cd C:/chenjimiao/project/python/aiTeacherPlan/project/crawler/ && scrapy crawl baidu_spider -a keyword='+scrapy+' -a mode='+mode
os.system(cmd)
