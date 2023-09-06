import pytest
import utils
import re

test_data = [('1234', 'd0d3e1c6-b5bd-496a-8fd6-175538930b24.static.developer.xxx.com'),
             ('1234', 'd9166bd9-c771-46b3-8be1-dcb46ba3edb1.static.developer.xxx.com'),
             ('1234', 'dcea45e4-d922-489b-a903-c45763a84bfe.static.developer.xxx.com'),
             ('5678', 'homepage.yyy.com'),
             ('5678', 'tusxiz0wvh0j.sub.yyy.com'),            
             ('5678', 'sub.yyy.com')]

test_data_list = []
for elem in test_data:
    test_data_list.append(elem[1])

good_data = test_data_list[:3]

def test_get_data():
    data_processor = utils.DataProcessor('domains')
    data_processor.process_data()

    res = [domain for domain in test_data_list if re.match(data_processor.regex['1234'], domain)]

    assert res == good_data