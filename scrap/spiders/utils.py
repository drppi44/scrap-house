# -*- coding: utf-8 -*-


def get_id_from_link(link):
    link = link.replace('/', '').replace('inmueble', '')
    return int(link)
