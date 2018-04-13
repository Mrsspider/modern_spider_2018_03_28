import requests


def test_ip(iplist=[]):
    '''没有参数，输出可用[ip:port,...]列表'''
    with open('settings/n_proxy.txt','r',encoding='utf-8') as f:
        iplist = f.read()
    iplist = iplist.split(',')
    iplist = list(set(iplist))
    print(iplist)
    print(len(iplist))
    n = 0
    prolist=[]
    for ip in iplist:
        try:
            # ip = ip[:-1]
            url = 'http://2017.ip138.com/ic.asp'
            pro = {'http':ip,'https':ip,}
            head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
            response = requests.get(url,proxies=pro,headers=head,timeout=3)
            test_num = response.status_code
            if test_num == 200:
                print(ip)
                prolist.append(ip+',')
                print(response.content.decode('gb2312'))
                n+=1
                print(n)

        except Exception as e:
            e = {'test_ip':e}
            print(e)
            with open('logbook/logbook.txt','a',encoding='utf-8') as f:
                f.writelines(str(e))
            continue
    # with open('settings/n_proxy.txt', 'a', encoding='utf-8') as f:
    #     f.writelines(prolist)
test_ip()