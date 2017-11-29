from django.test import TestCase

d = {
    "1": {
        "name": "zzz",
        "img": "/static/imgs/a.png",
        "selected_policy_id": "1",
        "policy_list": [
            {"id": "1", "name": "1month", "price": "9.9"},
            {"id": "2", "name": "2month", "price": "19.9"}
        ]
    }
}

d1 = {
    '1': {
        'name': 'xxx',
        'img': '/sdf/klo',
        'policy_id': '1',
        'policy_list': [
            {'a': '11'},
            {'b': '22'}
        ]
    }
}

d2 = {"1": {"a": "11", "b": [{"aa": "111"}, {"bb": "222"}]}}

# from django_redis import get_redis_connection
#
# conn = get_redis_connection('default')
#
# print(conn.hget('luffy_car',1))


# dict = {'1': {'a': '11'}, '2': {'b': '22'}}
# print(list(dict.keys()),type(list(dict.keys())))
# id_list = [k for k in dict.keys()]
# id = '1'
# if id in id_list:
#     dict.pop(id)
#
# print(dict)

