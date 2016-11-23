import json

with open('data.json', 'r') as f:
    items = json.loads(f.read())
    urls = [item['url'].replace('https://www.idealista.com/alquiler-viviendas/', '') for item in items]
    with open('urls.json', 'w+') as fw:
        fw.write(json.dumps(urls))