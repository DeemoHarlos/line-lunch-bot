import json
import csv
import re
import os


def getData():
    with open('data/data.json', 'r', encoding = 'utf-8') as jsonFile: 
        data = json.load(jsonFile)
    return data 

def setData(data):
    with open('data/data.json', 'w', encoding = 'utf-8') as jsonFile: 
        json.dump(data, jsonFile)

def checkAuthority(userId):
    data = getData()
    return True

def hasRestaurant():
    restaurant_path = 'data/restaurant/' + data['restaurant'] + '.csv'
    if os.path.isfile(restaurant_path):
        return True
    else:
        return False

def getRestaurant():
    data = getData()
    return data['restaurant']

def setRestaurant(restaurant):
    data = getData()
    data['restaurant'] = restaurant
    setData(data)

def getMenu(restaurant):
    if hasRestaurant(restaurant):
        with open(restaurant_path, newline = '', encoding = 'utf-8') as menuFile:
            menu = list(csv.reader(menuFile))
            return menu
    else:
        return []
    

def printMenu(restaurant):
    if hasRestaurant(restaurant):
        with  open(restaurant_path, newline = '', encoding = 'utf-8') as menuFile:
            menu = list(csv.reader(menuFile))        
        reply = ''
        for food in menu:
            reply += ( food[0] + '. ' + food[1] + ' ' + food[2] + '\n' )
        return reply
    else:           
        return '查無此餐廳'

def addOrder(user_name, orders):
    f = open('data/order.csv', 'a+', encoding = 'utf-8')         
    orders = orders.split('/')     
    for order in orders:
        f.write(user_name + ',' + order + '\n')     
    f.close()          
    return '收到'
    
def getOrder():
    with open('data/order.csv', newline = '', encoding = 'utf-8') as orderFile:
        orders = list(csv.reader(orderFile))
    return orders

def countOrder(orders):
    foods = {}
    for order in orders:
        if order[1] in foods:
            foods[order[1]] += 1
        else:
            foods[order[1]] = 1
    return foods

def printStatistic(foods, menu):
    reply = ''
    total = 0
    total_price = 0
    # if database has restaurant's menu 
    if menu:
        # print items, numbers, total numbers, total price, etc.               
        for food in foods:
            food_name = menu[int(food)][1] if food.isnumeric() else food
            food_price = menu[int(food)][2] if food.isnumeric() else 0
            reply += ( food_name + ' ' + str(foods[food]) + '份\n')
            total += foods[food]
            total_price += ( int(food_price) * foods[food] )    
        reply += ( '共' + str(total) + '份' + str(total_price) + '元' )
    else:             
        for food in foods:
            reply += ( food + ' ' + str(foods[food]) + '份\n')
            total += foods[food] 
        reply += ( '共' + str(total) + '份' )
    return reply
    
def printDetail(orders, menu):
    order_no = 1
    reply = ''
    if menu:               
        # print order detail
        for order in orders:
            food_name = menu[int(order[1])][1]
            food_price = menu[int(order[1])][2]
            reply += ( str(order_no) + '. ' + order[0] + '/' + food_name + '/' + food_price + '元\n' )
            order_no += 1      
    else:
        for order in orders:
            reply += ( str(order_no) + '. ' + order[0] + '/' + order[1] + '\n' )
            order_no += 1
    return reply