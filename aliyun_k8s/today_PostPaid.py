# #!/usr/bin/env python
# #coding=utf-8

import datetime
import json
import os
import sys
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from aliyun_k8s.conf import setting

scale_nodes_list = []

client = AcsClient(setting.ACCESS_ID, setting.ACCESS_SECRET, 'cn-beijing')

request = CommonRequest()
request.set_accept_format('json')
request.set_method('GET')
request.set_protocol_type('https') # https | http
request.set_domain('cs.cn-beijing.aliyuncs.com')
request.set_version('2015-12-15')

request.add_query_param('RegionId', "cn-beijing")
request.add_query_param('pageSize', "100")
request.add_query_param('pageNumber', "1")
request.add_header('Content-Type', 'application/json')
request.set_uri_pattern('/clusters/c970e25147efc4f9e98b4b1b73c9822a7/nodes')
body = '''{}'''
request.set_content(json.dumps(body))

try:
    response = client.do_action_with_exception(request)

    str_instace_dict = (str(response, encoding = 'utf-8'))
    json_instance_dict = json.loads(str_instace_dict)

    for instance in json_instance_dict['nodes']:
        # print(instance)
        if instance['instance_charge_type'] == "PostPaid" and instance['instance_type_family'] == "ecs.g5":
            if str(datetime.date.today()) in instance['creation_time']:
                scale_nodes_list.append(instance['node_name'])

    print(scale_nodes_list)
except ServerException as e:
    print(e)
except ClientException as e:
    print(e)
