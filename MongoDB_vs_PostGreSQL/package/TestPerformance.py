"""
This class runs Threads
"""
import sys
import psycopg2
from MongoDB_vs_PostGreSQL.package.Seeder import Seeder
import threading
import random
from threading import Thread
import MongoDB_vs_PostGreSQL.package.config as config
import matplotlib.pyplot as plt
import numpy as np
import datetime


class TestPeformance(Seeder):
    __slots__ = 'cur', 'seed'

    def __init__(self):
        """
        calling its parent class
        """
        super().__init__()

    def probabilities(self):
        """
             This method assigns an operation to be performed by the database
             This operation is assigned on the basis of probability.
             if (  1 < randomInt < 3 ) ... create account
             if ( 5 < randomInt < 15) ... update stock
             ..and so on
        """
        randomInt = random.randint(1, 100)
        print("Assigned to thread: {}".format(threading.current_thread().name))

        if 1 <= randomInt <= 3:
            print("Creating Account..")

            randomUser = str(
                random.randrange(self.userCount + 1, 214748364))  # Generate user NOT already in our database
            username = 'user' + randomUser
            password = 'root' + randomUser
            fName = 'fName ' + randomUser
            lname = 'LName ' + randomUser
            self.createAccount(username, password, fName, lname)

        elif 3 < randomInt <= 5:
            print("Creating new Product..")
            randomProduct = int(
                random.randrange(self.productCount + 1, 214748364))  # Generate product Id NOT already in our database
            stringProd = str(randomProduct)
            name = 'product' + stringProd
            description = 'This is product number ' + stringProd
            price = random.randint(1, 2000)
            initialStock = random.randint(1, 100)
            self.addProduct(randomProduct, name, description, price, initialStock)

        elif 5 < randomInt <= 15:
            print("Updating random stock..")
            randomUpdateCount = random.randint(1,
                                               self.productCount)  # Generate product ID already in our database
            Stock = random.randint(1, 1000)
            self.updateStockLevel(randomUpdateCount, Stock)

        elif 15 < randomInt <= 80:
            print("Getting Reviews of random Product..")
            randomProduct = random.randint(1, self.productCount)
            print(self.getProductandReviews(randomProduct))

        elif 80 < randomInt <= 85:
            print("Getting Average user rating..")
            randomUser = random.randint(1, self.userCount)
            username = 'user' + str(randomUser)
            print(self.getAverageUserRating(username))

        elif 85 < randomInt <= 95:
            print("Submitting random order..")
            randomUser = str(random.randint(1, self.userCount))  # Generate user already in our database
            username = 'user' + randomUser
            password = 'root' + randomUser
            # ProductOrder = {random.randint(1, self.productCount): random.randint(1, 5)}
            productList = {}
            for z in range(11):
                productId = random.randint(1, self.productCount)
                productCount = random.randint(1, 30)
                if productId in productList:
                    productList[productId] = productList.get(productId) + productCount
                else:
                    productList[productId] = productCount
            time = datetime.datetime.now()
            checkSubmission = self.SubmitOrder(username, password, productList, time)
        # if not checkSubmission:
        #    config.negativeStockCount += 1

        elif 95 < randomInt <= 100:
            print("Posting review for random product.")
            userCount = str(random.randint(1, self.userCount))  # 100 users
            randomUser = "user" + userCount
            randomProduct = random.randint(1, self.productCount)  # 1000 products
            randomRating = random.randint(1, 5)
            password = 'root' + userCount
            description = 'This is product ranked ' + userCount

            self.postReview(randomUser, password, randomProduct, randomRating, description)

    def helperProb(self):
        """
        This method is called by each thread which in turn calls the self.probabilities method.
         Each set of threads run for for a period of 5 mins
        :return: None
        """
        now = datetime.datetime.now()
        five = now + datetime.timedelta(minutes=5)
        while datetime.datetime.now() < five:
            self.probabilities()


class testThreads(threading.Thread):
    """
     This class is a thread factory. It initializes threads
    """

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        """
        Calls the helperProb method. So that we can test different operations on different threads
        :return:
        """
        try:
            testObject = TestPeformance()

            testObject.helperProb()
        finally:

            print("Connection Closed Successfully")


if __name__ == '__main__':
    plotStore = []

    for i in range(1, 11):
        threadStore = []
        # print("Number of threads being run: ", i)
        config.negativeStockCount = 0
        config.numberOfOperations = 0
        config.totalOrders = 0

        numberOfThreads = i

        for j in range(1, numberOfThreads + 1):
            threadObj = testThreads()
            threadObj.name = i
            threadStore.append(threadObj)

        for k in range(len(threadStore)):
            threadStore[k].start()

        '''
        Make sure all CONCURRENT Threads have finished executing before proceeding
        '''
        for k1 in range(len(threadStore)):
            threadStore[k1].join()

        negStockPercentage = 0
        if config.totalOrders > 0:
            print("Percentage of Orders out of stock", (config.negativeStockCount / config.totalOrders) * 100)
            negStockPercentage = (config.negativeStockCount / config.totalOrders) * 100
            print("Count stock Less Than zero : ", config.negativeStockCount)
            print("Total number of orders", config.totalOrders)
        print("Total Number of operations", config.numberOfOperations)

        plotObj = {"Total Number of Threads": numberOfThreads,
                   "Percentage of products with a stock level less than zero": negStockPercentage,
                   "Total Number of operations": config.numberOfOperations,
                   "Count stock Less Than zero": config.negativeStockCount,
                   "Total number of orders": config.totalOrders}
        plotStore.append(plotObj)

    for finalAns in plotStore:
        print(finalAns)
