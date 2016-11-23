# -*- coding: utf-8 -*-
import json


def get_id_from_link(link):
    link = link.replace('/', '').replace('inmueble', '')
    return int(link)


def get_variants():
    core_url = 'https://www.idealista.com/'
    with open('../../variants.json', 'r') as f:
        return [core_url+url for url in json.loads(f.read())]