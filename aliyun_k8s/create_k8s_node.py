#!/usr/bin/env python
#coding=utf-8
# 添加节点

import argparse
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException


class k8s_cluster(object):
    def __init__(self, args):
        self.access_id = args.access_id
        self.access_secret = args.access_secret
        self.count = args.count
        self.key_pair = args.key_pair
        self.tag_key = args.tag_key
        self.tag_value = args.tag_value
        self.worker_data_disk = args.worker_data_disk


    def create(self):
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_method('POST')
        request.set_protocol_type('https')  # https | http
        request.set_domain('cs.cn-beijing.aliyuncs.com')
        request.set_version('2015-12-15')

        request.add_query_param('RegionId', "cn-beijing")
        request.add_header('Content-Type', 'application/json')
        request.set_uri_pattern('/api/v2/clusters/c970e25147efc4f9e98b4b1b73c9822a7')


        body = {
            "count": self.count,
            "worker_data_disk": self.worker_data_disk,
            "key_pair": self.key_pair,
            "worker_instance_types": ["ecs.g5.6xlarge"],
            "worker_instance_charge_type": "PostPaid",
            "vswitch_ids": ["vsw-2ze7mbfg62o3dqfv6rbkz"],
            "tags": [{"key":self.tag_key,"value":self.tag_value}]
        }

        request.set_content(json.dumps(body))

        client = AcsClient(self.access_id, self.access_secret, 'cn-beijing')

        try:
            response = client.do_action_with_exception(request)
            print(str(response, encoding='utf-8'))
        except ServerException as e:
            print(e)
        except ClientException as e:
            print(e)


def arg_parse():
    parser = argparse.ArgumentParser(description="Aliyun OSS 参数选项")
    parser.add_argument("--access_id", "-access_id", type=str, required=True, help="Aliyun ID")
    parser.add_argument("--access_secret", "-access_secret", type=str, required=True, help="Aliyun secret")
    parser.add_argument("--count", "-count", type=int, required=False, help="count")
    parser.add_argument("--key_pair", "-key_pair", type=str, required=False, help="key_pair")
    parser.add_argument("--worker_data_disk", "-worker_data_disk", type=bool, required=False, help="tag_key")
    parser.add_argument("--tag_key", "-tag_key", type=str, required=False, help="tag_key")
    parser.add_argument("--tag_value", "-tag_value", type=str, required=False, help="tag_value")

    args_options = parser.parse_args()
    return args_options

if __name__ == '__main__':
    args = arg_parse()
    k8s = k8s_cluster(args)
    k8s.create()