#!/usr/bin/python
# coding=utf-8


import argparse
import json
import logging
import re
import sys
from sys import argv
from os.path import exists
import time
import os
import os.path
import shutil


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


def convert_to_products(total_file_list):
    map = {}
    product_list = []
    for filename in total_file_list:
        if ".txt" not in filename or ".crdownload" in filename:
            continue
        filename = filename.replace(".txt", "")
        if "_" not in filename:
            continue
        last_index = len(filename) - filename[::-1].index("_") - 1
        product_name = filename[0:last_index]
        time = filename[last_index+1:len(filename)]
        if not map.__contains__(product_name):
            map[product_name] = []
        map[product_name].append(int(time))
    for name in map:
        product_list.append(Product(name, map[name]))
    return product_list

def output_files(origin_path,product_list, output_path):
    for product in product_list:
        for product_time in product.time_list:
            product_name = product.name
            path = get_product_target(output_path, product_name, product_time)
            origin_file_path = origin_path + "/" + product_name + "_" + str(product_time) + ".txt"
            if not exists(path) :
                os.makedirs(path)
            shutil.copy(origin_file_path, path)


def get_product_target(output_path, product_name, product_time):
    time_array = time.strftime("%m-%d-%H-%M", time.localtime(product_time/1000)).split("-")
    return output_path + "/" + product_name + "/" + time_array[0] + "/" + time_array[1] + "/" + time_array[2]


def collect_all_file(origin_path, output_path):
    total_file_list = listDir(origin_path)
    product_list = convert_to_products(total_file_list)
    output_files(origin_path, product_list, output_path)


class Product:
    def __init__(self, name, time_list):
        self.name = name
        self.time_list = time_list


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser('collect_data')
    parser.add_argument('--origin', help='[origin file path]', required=True)
    parser.add_argument('--target', help='[report file alias]', required=True)
    args = parser.parse_args()

    print("start collect")
    collect_all_file(args.origin, args.target)
    # collect_all_file("/Users/nalecyxu/Downloads/nft_origin", "/Users/nalecyxu/Downloads/nft_target")

