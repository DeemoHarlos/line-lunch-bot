# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 15:50:24 2021

@author: jacky
"""

import json
import csv
import os

restaurant_folder = 'data/restaurant/'
data_path = 'data/data.json'
order_path = 'data/order.csv'
detail_path = 'static/detail.txt'
# detail_url = 'https://eatwhat-in-ncu.herokuapp.com/detail'

# return data in data.json
def getData():
    with open(data_path, 'r', encoding = 'utf-8') as jsonFile:
        data = json.load(jsonFile)
    return data

# edit data in data.json
def setData(data):
    with open(data_path, 'w', encoding = 'utf-8') as jsonFile:
        json.dump(data, jsonFile)

# return today's restaurant
def getRestaurant():
    data = getData()
    return data['restaurant']

# set today's restaurant
def setRestaurant(restaurant):
    data = getData()
    data['restaurant'] = restaurant
    setData(data)

# get a restaurant's menu
def getMenu(restaurant):
    with open(restaurant_folder + restaurant + '.csv', newline = '', encoding = 'utf-8') as menuFile:
        menu = list(csv.reader(menuFile))
        return menu

# print a restaurant's menu
def printMenu(restaurant):
    reply = ''
    menu = getMenu(restaurant)
    for food in menu:
        # no. / name / price
        reply += ( food[0] + '. ' + food[1] + ' ' + food[2] + '\n' )
    return reply

# check if user's input is valid
def checkValidity(order):
    menu = getMenu(getRestaurant())
    if order.isnumeric():
        if int(order) > 0 and int(order) < len(menu):
            return True
    return False

# add order(s) into order.csv
def addOrder(user_id, orders):
    orders = orders.split('/')
    with open(order_path, 'a+', encoding = 'utf-8') as orderFile:
        for order in orders:
            # validate parameter
            if order.isnumeric():
                orderFile.write(user_id + ',' + order + '\n')
            else:
                return '請依照格式輸入'
    return '收到'

# cancel and remove order(s) from order.csv
def cancelOrder(user_id, cancel_orders):
    orders = getOrder()
    os.remove(order_path)
    # if user does input parameters, cancel particular orders
    if cancel_orders:
        cancel_orders = cancel_orders.split('/')
        for order in orders:
            if order[0] != user_id:
                addOrder(order[0], order[1])
            elif order[1] not in cancel_orders:
                addOrder(order[0], order[1])
    # if user does not input parameters, cancel all the orders that match user_id
    else:
        for order in orders:
            if order[0] != user_id:
                addOrder(order[0], order[1])
    return '取消訂單'

# return orders
def getOrder():
    with open(order_path, newline = '', encoding = 'utf-8') as orderFile:
        orders = list(csv.reader(orderFile))
    return orders

# count number of each items via dict
def countOrder(orders):
    foods = {}
    for order in orders:
        foods[order[1]] = foods[order[1]] + 1 if order[1] in foods else 1
    return foods

# print each items' number, total number, and price
def printStatistic(foods, menu):
    reply = ''
    total = 0
    total_price = 0
    for food in foods:
        try:
            food_name = menu[int(food)][1]
            food_price = menu[int(food)][2]
            reply += ( food_name + ' ' + str(foods[food]) + '份\n')
            total += foods[food]
            total_price += ( int(food_price) * foods[food] )
        except:
            reply += '查無資料\n'
    reply += ( '共' + str(total) + '份' + str(total_price) + '元' )
    return reply

# write orders into detail.txt which is loaded by detail.html and show to the users
def showDetailAsHtml(line_bot_api, orders, menu, domain_name):
    if os.path.isfile(detail_path):
        os.remove(detail_path)
    order_no = 1
    for order in orders:
        try:
            user_name = line_bot_api.get_profile(order[0]).display_name
        except:
            user_name = order[0]
        food_name = menu[int(order[1])][1]
        food_price = menu[int(order[1])][2]
        with open(detail_path, 'a+', encoding = 'utf-8') as detailFile:
            detailFile.write( str(order_no) + '. ' + user_name + ' / ' + food_name + ' / ' + food_price + '元\n' )
        order_no += 1
    return domain_name + 'detail'

# print orders via line bot
def printDetail(line_bot_api, orders, menu):
    order_no = 1
    reply = ''
    for order in orders:
        try:
            user_name = line_bot_api.get_profile(order[0]).display_name
        except:
            user_name = order[0]
        food_name = menu[int(order[1])][1]
        food_price = menu[int(order[1])][2]
        reply += ( str(order_no) + '. ' + user_name + '/' + food_name + '/' + food_price + '元\n' )
        order_no += 1
    return reply

# remove unnecessary files
def clear():
    if os.path.isfile(order_path):
        os.remove(order_path)
    if os.path.isfile(detail_path):
        os.remove(detail_path)

