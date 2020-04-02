# _*_coding:utf-8_*_

import argparse
import ast
import time
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526.RunInstancesRequest import RunInstancesRequest
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest

RUNNING_STATUS = 'Running'
CHECK_INTERVAL = 3
CHECK_TIMEOUT = 180

# 1. 通过argparse命令行接口生成字典
# 2. 生成的字典添加到AliyunEcsExample初始化中
# 3. 通过 __init__ 初始化信息带入到run_instances函数中。run_instances得出instance_id
# 4. check_instance_status函数根据instance_id得出instance主机状态和IP

class AliyunEcsExample():
    """
    ast.literal 判断需要计算的内容是不是合法的python类型，
    如果是则进行运算，否则就不进行运算。
    """
    def __init__(self):
        params_dict = self.arg_parse()
        self.access_id = params_dict["access_id"]
        self.access_secret = params_dict["access_secret"]

        self.dry_run = params_dict["dry_run"]
        self.region_id = params_dict["region_id"]
        self.instance_type = params_dict["instance_type"]
        self.instance_charge_type = params_dict["instance_charge_type"]
        self.image_id = params_dict["image_id"]
        self.security_group_id = params_dict["security_group_id"]
        self.period_unit = params_dict["period_unit"]
        self.zone_id = params_dict["zone_id"]
        self.internet_charge_type = params_dict["internet_charge_type"]
        self.vswitch_id = params_dict["vswitch_id"]
        self.instance_name = params_dict["instance_name"]
        self.password = params_dict["password"]
        self.amount = params_dict["amount"]
        self.internet_max_bandwidth_out = params_dict["internet_max_bandwidth_out"]
        self.system_disk_size = params_dict["system_disk_size"]
        self.system_disk_category = params_dict["system_disk_category"]
        self.data_disks = ast.literal_eval(params_dict["data_disks"])
        self.tags = ast.literal_eval(params_dict["tags"])

        self.client = AcsClient(self.access_id, self.access_secret, self.region_id)



    def arg_parse(self):
        """
        vars 生成字典
        :return:
        """
        parser = argparse.ArgumentParser(description="Aliyun ECS 参数选项")
        parser.add_argument("--access_id", "-access_id", type=str, required=True, help="Aliyun ID")
        parser.add_argument("--access_secret", "-access_secret", type=str, required=True, help="Aliyun secret")
        parser.add_argument("--dry_run", "-dry_run", type=bool, default=False,
                            help="True:检查请求，不会创建实例; False:检查请求，通创建实例")
        parser.add_argument("--region_id", "-region_id", type=str, default="cn-beijing", help="实例所属的地域ID")
        parser.add_argument("--instance_type", "-instance_type", type=str, default="ecs.n4.xlarge",
                            help="实例资源规格")
        parser.add_argument("--instance_charge_type", "-instance_charge_type", type=str, default="PostPaid", help="按量付费")
        parser.add_argument("--image_id", "-image_id", type=str,
                            default="centos_7_04_64_20G_alibase_201701015.vhd", help="镜像ID")
        parser.add_argument("--security_group_id", "-security_group_id", type=str, default="sg-2ze6qstyvxjc7j7l8nam",
                            help="实例所属于的安全组ID,必选")
        parser.add_argument("--zone_id", "-zone_id", type=str, default="cn-beijing-a", help="实例所属的可用区编号")
        parser.add_argument("--internet_charge_type", "-internet_charge_type", type=str,
                            default="PayByTraffic", help="按使用流量计费")
        parser.add_argument("--period_unit", "-period_unit", type=str, default="Hourly", help="购买资源的时长")
        parser.add_argument("--vswitch_id", "-vswitch_id", type=str, default="vsw-2zee6z8dxh973ntb2zjjk",
                            help="虚拟交换机ID")
        parser.add_argument("--instance_name", "-instance_name", type=str, default="test-[1,2]", help="实例名称")
        parser.add_argument("--password", "-password", type=str, default="Test123$%#", help="实例密码")
        parser.add_argument("--amount", "-amount", type=int, default=1, help="指定创建ECS实例的数量")
        parser.add_argument("--internet_max_bandwidth_out", "-internet_max_bandwidth_out", type=int, default=0,
                            help="公网出口带宽最大值")
        parser.add_argument("--system_disk_size", "-system_disk_size", type=int, default=20, help="系统盘大小")
        parser.add_argument("--system_disk_category", "-system_disk_category", type=str,
                            default="cloud_efficiency", help="系统盘的磁盘种类")
        parser.add_argument("--data_disks", "-data_disks", type=str,
                            default="[{'Size': 100, 'Category': 'cloud_efficiency', 'Encrypted': 'false', 'DeleteWithInstance': True}]",
                            help="数据盘，默认100G")
        parser.add_argument("--tags", "-tags", type=str, default="[{'Key': 'business-types', 'Value': 'test'}]",
                            help="实例标签 business-types: test")
        args_options = parser.parse_args()
        params_dict = vars(args_options)
        return params_dict


    def run_instances(self):
        """
        调用ECS API
        instance_id得出的是列表
        :return:
        """
        request = RunInstancesRequest()
        request.set_DryRun(self.dry_run)

        request.set_InstanceType(self.instance_type)
        request.set_InstanceChargeType(self.instance_charge_type)
        request.set_ImageId(self.image_id)
        request.set_SecurityGroupId(self.security_group_id)
        request.set_ZoneId(self.zone_id)
        request.set_InternetChargeType(self.internet_charge_type)
        request.set_VSwitchId(self.vswitch_id)
        request.set_InstanceName(self.instance_name)
        request.set_Password(self.password)
        request.set_Amount(self.amount)
        request.set_InternetMaxBandwidthOut(self.internet_max_bandwidth_out)
        request.set_SystemDiskSize(self.system_disk_size)
        request.set_SystemDiskCategory(self.system_disk_category)
        request.set_DataDisks(self.data_disks)
        request.set_Tags(self.tags)

        body = self.client.do_action_with_exception(request)
        data = json.loads(body)
        instance_id = data['InstanceIdSets']['InstanceIdSet']
        print('Success Instance Create. InstanceId: {}'.format(' '.join(instance_id)))
        return instance_id

    def check_instance_status(self, instance_id):
        """
        获取instance_id 和 instance状态
        :return:
        """
        start = time.time()
        host_list = []

        while True:
            request = DescribeInstancesRequest()
            request.set_InstanceIds(json.dumps(instance_id))
            body = self.client.do_action_with_exception(request)
            data = json.loads(body)
            for instance in data['Instances']['Instance']:
                if RUNNING_STATUS in instance['Status']:
                    instance_id.remove(instance['InstanceId'])
                    print('Instance boot successfully: {}'.format(
                        instance['InstanceId']))
                    host_list.append({"host": instance['VpcAttributes']['PrivateIpAddress']['IpAddress'][0],
                                           "password": self.password, "hostname": instance['InstanceName']})

            if not instance_id:
                print('Instances all boot successfully')
                break

            # 大于3分钟退出
            if time.time() - start > CHECK_TIMEOUT:
                print('Instances boot failed within {timeout}s: {ids}'
                      .format(timeout=CHECK_TIMEOUT, ids=', '.join(instance_id)))
                break

            # 每三秒钟检查一次
            time.sleep(CHECK_INTERVAL)
            # 输出主机连接信息
        return host_list

    def run(self):
        ids = self.run_instances()
        print(ids)
        print(type(ids))
        return self.check_instance_status(ids)


if __name__ == '__main__':
    a = AliyunEcsExample().run()
    print(a)