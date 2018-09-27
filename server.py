#!/usr/local/bin/python3
# /-*- coding:utf-8 -*-
'''
name: zzq
last_edited: 18-09-25
功能：
    购物系统的服务端
    根据连接上的客户端发送的信息，回复不同的信息
    客户端退出时，服务端自动保存信息
    1.验证管理员还是用户，新用户注册，还是游客
        管理员登录：a.提供用户信息 b.更改用户信息 c.提供仓库信息
            d.更改仓库信息 e.提供利润信息 f.修改管理员信息
        新用户注册：a.添加用户信息
        游客：a.提供仓库信息
        用户：a.提供商品列表 b.修改商品列表，用户信息 c.查看用户信息
            d.修改用户信息 e.修改用户信息 f.修改用户信息 g.查看用户信息

    2.技术分析：
    socket tcp 套接字
    多进程并发
    信息的传输
    将信息读取出来封装到类里
    将信息存储到数据库中
'''

import os
import sys
from multiprocessing import *
from socket import *
import traceback
import pymongo


# 将用户信息保存在Client类中
class Client(object):
    def __init__(self, account, password, name, address,
                 vip=0, money=0, shopping_list=None):
        self.__account = account
        self.__pd = password
        self.__name = name
        self.__addr = address
        self.__vip = vip
        self.__money = money
        self.__shopping_list = shopping_list

    def get_account(self):
        return self.__account

    def get_pd(self):
        return self.__pd

    def get_name(self):
        return self.__name

    def get_addr(self):
        return self.__addr

    def get_vip(self):
        return self.__vip

    def get_money(self):
        return self.__money

    def get_shopping_list(self):
        return self.__shopping_list


# 将仓库中商品信息保存在Inventory类中
class Inventory(object):

    def __init__(self, name, cost, price, count):
        self.__name = name
        self.__cost = cost
        self.__price = price
        self.__count = count

    def get_name(self):
        return self.__name

    def get_cost(self):
        return self.__cost

    def get_price(self):
        return self.__price

    def get_count(self):
        return self.__count


# 将服务端系统功能写在类里
class shopping_sys(object):

    def __init__(self, c):
        self.__c = c


# 根据客户端传来的信息，判断是admin还是老用户，新用户，游客
def func(c):
    ftp = shopping_sys(c)
    while 1:
        data = c.recv(1024).decode()
        if not data or data == 'quit':
            c.close()
            sys.exit('客户端已退出')
        elif data[0] == 'C':
            ftp.check_file()
        elif data[0] == 'D':
            filename = data[1:]
            ftp.send_file(filename)
        elif data[0] == 'U':
            filename = data[1:]
            ftp.get_file(filename)


# 创建套接字，绑定，接收客户端，每接收一个客户端，创建一个新的进程
def main():
    HOST = ''
    PORT = 8888
    ADDR = (HOST, PORT)
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(8)
    while 1:
        try:
            c, addr = s.accept()
        except KeyboardInterrupt:
            print('服务端退出')
            break
        except Exception as e:
            traceback.print_exc()
            continue
        p = Process(target=func, args=(c,))
        p.daemon = 1
        p.start()


if __name__ == "__main__":
    main()
