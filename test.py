import urllib
import json
import time

result = []

with open('data.json', 'r') as f:
    data = json.loads(f.read())
    urls = [_['url'] for _ in data]
    for url in urls:
        try:
            if urllib.urlopen(url).getcode() == 200:
                result.append({'url': url, 'status': 'ok'})
            else:
                result.append({'url': url, 'status': 'fail', 'type': 404})
        except UnicodeError:
            result.append({'url': url, 'status': 'fail', 'type': 'unicodeError'})
        time.sleep(2)

with open('urls.json', 'w+') as f:
    data = json.dumps(result)
    f.write(data)
