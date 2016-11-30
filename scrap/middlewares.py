from itertools import cycle


class ProxyMiddleware(object):
    def __init__(self):
        self.proxies_list = cycle([
            'https://5.189.182.40:1455',
            'http://5.189.135.39:3128',
            'http://5.196.218.190:8080',
            'http://176.31.107.113:4444',
            'http://37.57.179.2:8080',
            'http://5.135.164.181:3128', ])

    def process_request(self, request, spider):

        request.meta['proxy'] = self.proxies_list.next()
        print(request.meta['proxy'])
