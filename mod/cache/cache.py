#!/usr/bin/zsh python
# -*- coding:utf-8 -*-

from cachetools import TTLCache

cache = TTLCache(maxsize=50,ttl=300)