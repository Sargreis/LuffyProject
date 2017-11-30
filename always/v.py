#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2017/11/29

import redis

conn = redis.Redis(host='172.96.192.80',port=6379,password='luffy')

# conn.hset('luffy_car',1,"asdfds")
# val = conn.hget('luffy_car',1)
# conn.hdel('luffy_car',1)

print(val)
