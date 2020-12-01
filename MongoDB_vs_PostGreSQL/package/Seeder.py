import psycopg2
from MongoDB_vs_PostGreSQL.package.MongoDBModel import Model
import random
import MongoDB_vs_PostGreSQL.package.config as config
import datetime


class Seeder(Model):
    """
     This class seeds the database with users, products, reviews and orders
    """
    __slots__ = 'connectionString', 'cur', 'model'

    userCount = 1000
    productCount = 10000
    postReviewCount = 20000
    postOrderCount = 10000

    def __init__(self):
        super().__init__()

    def seedUsers(self, count):

        print("Creating users..")

        for userID in range(count + 1):

            strCounter = str(userID)
            username = 'user' + strCounter
            password = 'root' + strCounter
            fName = 'fName ' + strCounter
            lname = 'LName ' + strCounter

            # This will return True if successfully created
            userCreated = self.createAccount(username, password, fName, lname)

        print("Users created")

    def seederProducts(self, count):

        print("Creating Products..")

        for productId in range(count + 1):


            strCounter = str(productId)
            name = 'product' + strCounter
            description = 'This is product number ' + strCounter
            price = random.randint(1, 2000)
            initialStock = random.randint(100, 500)
            # This will return True if successfully created
            productCreated = self.addProduct(productId, name, description, price, initialStock)
            #config.allProductsStore.append(productCreated.inserted_id)

        print("Products created")

    def seedPostReview(self, count):

        finalCount = 1

        while finalCount <= count:
            userCount = str(random.randint(1, self.userCount))
            randomUser = "user" + userCount
            randomProductId = random.randint(1, self.productCount)
            randomRating = random.randint(1, 5)
            password = 'root' + userCount
            description = 'This is random review ' + userCount

            postReview = self.postReview(randomUser, password, randomProductId, randomRating, description)

            if postReview:  # increment if review was successfully posted
                finalCount += 1

        print("Reviews posted")

    def seedPostOrders(self, count):

        config.PostOrderSeederCount = 1

        while config.PostOrderSeederCount <= count:

            # list of 10 random pro ducts each time
            productList = {}
            for i in range(11):
                productId = random.randint(1, self.productCount)

                productCount = random.randint(1, 30)
                if productId in productList:
                    productList[productId] = productList.get(productId) + productCount
                else:
                    productList[productId] = productCount

            userCount = str(random.randint(1, self.userCount))
            randomUser = "user" + userCount
            # randomProduct = {random.randint(1, self.productCount): random.randint(1, 5)}

            password = 'root' + userCount
            time = datetime.datetime.now()
            postReview = self.SubmitOrder(randomUser, password, productList, time)

        # if postReview:  # increment if review was successfully posted
        #    finalCount += 1

        print("Orders posted")


def connectToDataBase():
    conn = psycopg2.connect(database="eCommerce", user="postgres", password="password", host="127.0.0.1", port="5432")

    print("Opened database successfully")

    return conn


if __name__ == '__main__':
    seeder = Seeder()

    seeder.createReqTables()
    print("Creating Users...")
    seeder.seedUsers(seeder.userCount)

    print("Creating Products...")
    seeder.seederProducts(seeder.productCount)

    print("Creating ProductsReviews...")
    seeder.seedPostReview(seeder.postReviewCount)

    print("Creating ProductsOrders...")
    seeder.seedPostOrders(seeder.postOrderCount)

    print("ALL DONE")
