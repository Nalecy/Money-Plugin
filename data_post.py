#!/usr/bin/python
# coding=utf-8


import argparse
import json
import logging
import re
from sys import argv
from os.path import exists
import time
import os
import os.path
import shutil
import requests

product_list = []


def readFile(path):
    fo = open(path, "r")
    content = fo.read()
    fo.close()
    return content


def readBrandFile(brand_path):
    fo = open(brand_path, "r")
    content = fo.read()
    fo.close()
    return json.loads(content)


def writeFile(target_path, src_content):
    fo = open(target_path, "w")
    fo.write(src_content)
    fo.close()


def listDir(origin_path):
    return os.listdir(origin_path)


last_content = ""


def post_data_core(product_data):
    global last_content
    content = build_post_content(product_data)
    print(content)
    print(last_content)
    if content == "":
        print("null?")
        return
    if last_content == content:
        print("same, ignore")
        return
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/f0f47031-b071-4e40-8cfb-953523b475d5"
    data = ("{\"msg_type\":\"text\",\"content\":{\"text\":\"" + content + "\"}}").encode('utf-8')
    headers = {"Content-Type": "application/json"}
    print(requests.post(url=url, data=data, headers=headers).text)
    last_content = content


def build_post_content(product_data):
    content = ""
    for product in product_data:
        array = product_data[product].split(",")
        content += product + ":" + array[0] + "," + array[1] + "," + array[2] + "\\n"
    return content


def data_post(target_root_path):
    global product_list
    product_list = listDir(target_root_path)
    product_data = {}
    for product_name in product_list:
        if product_name == ".DS_Store":
            continue
        target_path = get_target_path(target_root_path, product_name)
        if not exists(target_path):
            continue
        target_file_path = target_path + "/" + find_newest_file(target_path)
        product_data[product_name] = readFile(target_file_path)
    post_data_core(product_data)


def get_target_path(root_path, product_name):
    time_array = time.strftime("%m-%d-%H-%M", time.localtime(time.time())).split("-")
    target_path = root_path + "/" + product_name + "/" + time_array[0] + "/" + time_array[1] + "/" + time_array[
        2]
    return target_path


def find_newest_file(target_path):
    filenames = listDir(target_path)
    product_name = ""
    product_times = []
    for filename in filenames:
        if ".txt" not in filename:
            continue
        if "_" not in filename:
            continue
        filename = filename.replace(".txt", "")
        last_index = len(filename) - filename[::-1].index("_") - 1
        product_name = filename[0:last_index]
        product_time = int(filename[last_index + 1:len(filename)])
        product_times.append(product_time)
    sorted_time = sorted(product_times, key=lambda x: x, reverse=True)
    print(sorted_time[0])
    return product_name + "_" + str(sorted_time[0]) + ".txt"


def get_time_from_filename(filename):
    filename = filename.replace(".txt", "")
    last_index = len(filename) - filename[::-1].index("_") - 1
    time = filename[last_index + 1:len(filename)]
    return time


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser('collect_data')
    parser.add_argument('--target', help='[report file alias]', required=True)
    args = parser.parse_args()
    while True:
        time.sleep(5)
        # data_post("/Users/nalecyxu/Downloads/nft_target")
        data_post(args.target)
