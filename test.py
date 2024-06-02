def getip():
    with open('ipdaili.txt') as f
        iplist = f.readlines()
        proxy = iplist[random.randint(0, len(iplist) - 1)]
        proxy = proxy.replace('\n', "")
        proxies = {
            'http': 'http://' + str(proxy)
        }
    return proxies
