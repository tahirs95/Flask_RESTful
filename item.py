import sqlite3
from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

items =[]

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required = True,
        help= "This field cannot be left blank."
    )
    # parser.add_argument('name',
    #     type=str,
    #     required = True,
    #     help= "This field cannot be left blank."
    # )
    
    @jwt_required()
    def get(self, name):
        # # for item in items:
        # #     if item['name'] == name:
        # #         return item
        # item = next(filter(lambda x : x["name"] == name, items), None) #next is used to fetch from first item else use "list"
        # return {"item":item}, 200 if item is not None else 404

        item = self.find_by_name(name)
        if item:
           return item 
        return {"message":"Item not found"}, 404

    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items where name=?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item':{'name':row[0],'price':row[1]}}

    def post(self,name):
        
        # if next(filter(lambda x : x["name"] == name, items), None):
        if self.find_by_name(name):
            return({"message":"An item with name {} already exists.".format(name)})

        data = Item.parser.parse_args()
        # data = request.get_json()
        #force=True, silent=True
        item = {"name":name, "price":data["price"]}
        try:
            self.insert(item)
        except:
            return({"message":"An error occurred in inserting the item."}), 500 #internal server error
        # items.append(item)
        return item, 201

    @classmethod
    def insert(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"
        result = cursor.execute(query,(item['name'],item['price']))
        connection.commit()
        connection.close()
    
    @classmethod
    def update(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        result = cursor.execute(query,(item['price'],item['name']))
        connection.commit()
        connection.close()



    def delete(self, name):
        # global items
        # items = list(filter(lambda x: x["name"] != name, items))
        if self.find_by_name(name):
            # return({"message":"An item with name {} already exists.".format(name)})
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "DELETE FROM items WHERE name=?"
            result = cursor.execute(query,(name,))
            connection.commit()
            connection.close()
            return {"message":"Item deleted"}
        else:
            return({"message":"Item not found."})

    def put(self, name):
        data = Item.parser.parse_args()
        # data = request.get_json()
        # item = next(filter(lambda x: x["name"] == name, items), None)
        item = self.find_by_name(name)
        updated_item = {"name":name, "price":data['price']}
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return({"message":"An error occurred inserting the item"}), 500
        else:
            try:
                self.update(updated_item)
            except:
                return({"message":"An error occurred updating the item"}), 500
        return updated_item


    
class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({"name":row[0],"price":row[1]})
        connection.close()
        return {"items":items}