# _*_coding:utf-8_*_

import argparse
import os
import oss2


class AliyunOss(object):
    FILE_LIST = []

    def __init__(self, args):
        self.access_id = args.access_id
        self.access_secret = args.access_secret

        self.upload_dir = args.upload_dir
        self.bucket = args.bucket

        self.OssAuth = oss2.Auth(self.access_id, self.access_secret)
        self.OssBucket = oss2.Bucket(self.OssAuth, 'oss-cn-beijing.aliyuncs.com', self.bucket)

    def UploadFiles(self, dir):
        files = os.listdir(dir)
        for file in files:
            file_path = dir + "/" + file
            if os.path.isdir(file_path):
                self.UploadFiles(file_path)
            else:
                AliyunOss.FILE_LIST.append(file_path)

    def UploadName(self):
        self.UploadFiles(self.upload_dir)
        upload_list = []
        for file in AliyunOss.FILE_LIST:
            up_list = file.split(self.upload_dir)[1].replace('/', '', 1)
            upload_list.append(up_list)
        return upload_list

    def OssApi(self, name, file):
        self.OssBucket.put_object_from_file(name, file)

    def UploadOss(self):
        names = self.UploadName()
        # print(names)
        files = AliyunOss.FILE_LIST
        oss_dict = dict(zip(names, files))
        for key in oss_dict:
            self.OssApi(key, oss_dict[key])


def arg_parse():
    parser = argparse.ArgumentParser(description="Aliyun OSS 参数选项")
    parser.add_argument("--access_id", "-access_id", type=str, required=True, help="Aliyun ID")
    parser.add_argument("--access_secret", "-access_secret", type=str, required=True, help="Aliyun secret")
    parser.add_argument("--upload_dir", "-upload_dir", type=str, required=True, help="上传目录")
    parser.add_argument("--bucket", "-bucket", type=str, default="mrfresh", help="选择bucket")
    args_options = parser.parse_args()
    return args_options


if __name__ == '__main__':
    args = arg_parse()
    aliyun_oss = AliyunOss(args)
    aliyun_oss.UploadOss()