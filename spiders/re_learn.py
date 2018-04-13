from functings.spider_function import *


url='http://huodong.ctrip.com/Activity-Booking-OnlineWebSite/Recommend/UserComments?id=2071349&productName=%25e5%25b9%25bf%25e5%25b7%259e%25e7%2599%25bd%25e4%25ba%2591%25e5%25b1%25b1%252b%25e9%25bb%2584%25e5%259f%2594%25e5%2586%259b%25e6%25a0%25a1%25e6%2597%25a7%25e5%259d%2580%25e7%25ba%25aa%25e5%25bf%25b5%25e9%25a6%2586%252b%25e8%25b6%258a%25e7%25a7%2580%25e5%2585%25ac%25e5%259b%25ad%252b%25e9%2599%2588%25e5%25ae%25b6%25e7%25a5%25a0%252b%25e7%258f%25a0%25e6%25b1%259f%25e5%25a4%259c%25e6%25b8%25b8%25e4%25b8%2580%25e6%2597%25a5%25e6%25b8%25b8%25e3%2580%2590%25e5%25b9%25bf%25e5%25b7%259e%25e6%259c%25ac%25e5%259c%25b0%25e7%25b2%25be%25e5%258d%258e%252b%25e5%2590%25ab%25e5%258d%2588%25e6%2599%259a%25e9%25a4%2590%25e3%2580%2591&pageSize=5&pageIndex=2'
html = gethtml(url)
with open('html.txt','w',encoding='utf8') as f:
    f.writelines(html)

