import psycopg2
import MongoDB_vs_PostGreSQL.package.config as config
import datetime
import pymongo


class Model:
    __slots__ = 'mongoConn'

    def __init__(self):
        self.mongoConn = connectToDataBase()

        # self.cur = self.connectionString.cursor()

    def getProductsById(self, id):
        config.numberOfOperations += 1

        collection = self.mongoConn['products']

        query = {'_id': id}

        product = collection.find_one(query)

        if not product:
            print("Please enter a valid ID")
            return

        return product

    def Auth(self, username, password):
        config.numberOfOperations += 1

        collection = self.mongoConn['users']
        query = {'username': username, "password": password}
        user = collection.find_one(query)

        if not user:
            print("Invalid username or password")
            return

        return user

    def updateStockLevel(self, id, stock):

        config.numberOfOperations += 1

        collection = self.mongoConn['products']
        updateCriteria = {"_id": id}
        newvalues = {"$set": {"stock": stock}}

        collection.update_one(updateCriteria, newvalues)


    def addProduct(self, Id, name, description, price, initialStock):
        try:
            config.numberOfOperations += 1
            collection = self.mongoConn['products']

            myQuery = {'_id': Id, 'name': name, 'description': description, 'price': price,
                       'stock': initialStock}

            idStored = collection.insert_one(myQuery)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Error in adding product")

            return False

        return True

    def getProductandReviews(self, productId):
        config.numberOfOperations += 1
        collection = self.mongoConn['products']
        # query = "Select id as productId, name as productName, p.description as productDescription, " \
        #        "price as productPrice, stock as stockLeft, " \
        #        "username as username, rating as productRating, pr.description as review " \
        #        "from Products as p join ProductReviews as pr on p.id = pr.product_id where p.id = %s"

        query = [{'$match': {"_id": productId}},
                 {'$lookup': {"from": 'reviews', 'localField': '_id', 'foreignField': "productId", 'as': "Review"}},
                 {'$project': {'_id': 0, 'Review._id': 0}}]

        rows = collection.aggregate(query)
        reviews = []


        if not rows:
            print("No reviews found")
            return []
        return list(rows)

    def reviewExists(self, username, productId):
        config.numberOfOperations += 1

        collection = self.mongoConn['reviews']
        query = {'username': username, "productId": productId}
        rows = collection.find_one(query)

        if not rows:
            return False
        else:
            return True

    def postReview(self, username, password, productId, rating, reviewText):
        try:
            config.numberOfOperations += 1
            user = self.Auth(username, password)
            if not user:
                print("Invalid User")
                return False
            if self.reviewExists(username, productId):
                print("Review already exists")
                return False

            collection = self.mongoConn['reviews']

            myQuery = {'username': username, 'productId': productId, 'rating': rating,
                       'description': reviewText}

            collection.insert_one(myQuery)

            return True

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("error in posting your review")
            return False

    def getAverageUserRating(self, username):
        config.numberOfOperations += 1
        collection = self.mongoConn['reviews']
        groupBy = 'username'
        ref = "rating"

        query = [{"$match": {'username': username}},
                 {"$group": {
                     "_id": groupBy,
                     "Average": {
                         "$avg": "$"+ref
                     }
                 }
                 }]

        avg = collection.aggregate(query)
        avg = list(avg)
        store = None
        for i in avg:
            store = i["Average"]

        '''Get final value from tuple'''
        if not avg:
            print('Not Ratings found')
            return []


        # for r in row:
        #    store = r
        if not store:
            return 0

        return int(store)


    def insertOrder(self, username, time, productsOrdered):

        collection = self.mongoConn['orders']

        myQuery = {'username': username, 'createdAt': time, 'productsOrdered': productsOrdered}

        collection.insert_one(myQuery)

    # TODO: Insert rollback statements
    def SubmitOrder(self, username, password, listOfProductsAndQuantities, time):
        try:
            config.numberOfOperations += 1

            user = self.Auth(username, password)  # Authenticate User

            if not user:
                print("Invalid User")
                return

            # orderId = self.insertIntoOrderTable(time)

            verifiedProductDict = []
            for productId, quantity in listOfProductsAndQuantities.items():
                config.totalOrders += 1

                product = self.getProductsById(productId)  # Get product by Id

                if not product:
                    print("Sorry this product does not exist")
                    continue

                stock = product['stock']
                if stock <= 0:
                    #print("Sorry, that item is out of stock")
                    config.negativeStockCount += 1
                    continue

                # TODO : remove this count
                if stock < quantity:
                    #print("Sorry, you have exceeded the number of items present in stock")
                    # config.negativeStockCount += 1
                    continue

                newStock = stock - quantity
                self.updateStockLevel(productId, newStock)

                newDict = {}
                Map = {}
                Map['productId'] = productId
                Map['quantity'] = quantity
                # newDict[str(productId)] = quantity

                verifiedProductDict.append(Map)  # dictionary of all validated products

            self.insertOrder(username, time, verifiedProductDict)

            config.PostOrderSeederCount += 1  # counts the number of orders - its used in seeder.py

            return True

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Error in  submitting order")

            return False

    def userExists(self, username):
        config.numberOfOperations += 1

        collection = self.mongoConn['users']

        query = {'username': username}

        rows = collection.find_one(query)

        if not rows:

            return False
        else:

            return True

    def createAccount(self, username, password, firstName, lastName):
        config.numberOfOperations += 1
        if self.userExists(username):  # Return if user already exists
            print("Username already Taken")
            return False

        Map = {}
        try:

            collection = self.mongoConn['users']
            Map['username'] = username
            Map['password'] = password
            Map['fName'] = firstName
            Map['lName'] = lastName
            x = collection.insert_one(Map)

            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Creation unsuccessful")

            # self.connectionString.rollback()
            return False

    def createReqTables(self):
        collist = self.mongoConn.list_collection_names()

        for key in collist:  # Drop all collections
            mycol = self.mongoConn[key]
            mycol.drop()

        userCollection = self.mongoConn['users']

        productsCollection = self.mongoConn['products']

        productReviewsCollection = self.mongoConn['reviews']

        ordersCollection = self.mongoConn['orders']


def connectToDataBase():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["EcommerceDatabase"]

    print("Connected to Database")
    return mydb


if __name__ == '__main__':

    try:

        modelObject = Model()
        modelObject.createReqTables()

        '''
        # Test Create User
        modelObject.createAccount("chai", 'root', 'chaitanya', 'mehta')
        modelObject.createAccount("chai2", 'root', 'chaitanya', 'mehta')  # Test add user
        modelObject.createAccount("Jim", 'root', 'jim', 'halpert')  # Test add user

        # Test add product
        modelObject.addProduct(1,'Fifa', "Sports", 100, 3)
        modelObject.addProduct(2, 'Fifa21', "Sports", 100, 5)

        modelObject.updateStockLevel(1, 5)  # Test Update Stock

        time = datetime.datetime.now()
       # modelObject.SubmitOrder("chai", 'root', {1: 1, 2:3}, time)  # Test submit order
       # modelObject.SubmitOrder("Jim", 'root', {1: 1}, time)  # Test submit order

        modelObject.postReview('chai', 'root', 1, 5, "This is the best game ever")  # Test post Review
        modelObject.postReview('Jim', 'root', 1, 7, "This is the best game ever")
        modelObject.postReview('Jim', 'root', 1, 7, "This is the best game ever")  # this review should not go through
        modelObject.postReview('Jim', 'root', 2, 5, "This is the best game ever")
        print(modelObject.getProductandReviews(1))

        print(modelObject.getAverageUserRating('Jim'))
        '''
    finally:

        print("Connection Closed Successfully")
        # modelObject.mongoConn.close()
