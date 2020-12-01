import psycopg2
import MongoDB_vs_PostGreSQL.package.config as config
import datetime
import pymongo


class Model:
    __slots__ = 'connectionString', 'cur',

    def __init__(self):
        self.connectionString = connectToDataBase()
        self.cur = self.connectionString.cursor()

    def getProductsById(self, id):
        config.numberOfOperations += 1
        values = (id,)
        query = "SELECT * FROM Products WHERE id = %s"

        self.cur.execute(query, values)

        product = self.cur.fetchone()
        if not product:
            print("Please enter a valid ID")
            return

        return product

    def Auth(self, username, password):
        config.numberOfOperations += 1
        query = "SELECT * FROM Users WHERE username = '" + username + "' and password = '" + password + "'"
        self.cur.execute(query)
        user = self.cur.fetchone()
        if not user:
            print("Invalid username or password")
            return

        return user

    def updateStockLevel(self, id, stock):
        config.numberOfOperations += 1
        values = (stock, id)
        query = "Update products set stock = %s where id = %s "
        self.cur.execute(query, values)
        #self.connectionString.commit()

    def insertOrder(self, username, productID, quantity, time):
        try:
            config.numberOfOperations += 1
            valueOrders = (quantity, time)
            query = "INSERT INTO Orders (product_id,quantity,created_at) VALUES(%s,%s) RETURNING id"

            self.cur.execute(query, valueOrders)
            self.connectionString.commit()

            orderID = self.cur.fetchone()

            valuesProductOrders = (username, productID, orderID)
            query = "INSERT INTO ProductOrders (username, product_id, order_id) VALUES(%s, %s, %s)"

            self.cur.execute(query, valuesProductOrders)
        # self.connectionString.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.connectionString.rollback()
            return

    def addProduct(self, name, description, price, initialStock):
        config.numberOfOperations += 1
        values = (name, description, price, initialStock)
        query = "INSERT INTO Products (name, description, price, stock) VALUES(%s, %s, %s,%s)"
        self.cur.execute(query, values)
        self.connectionString.commit()
        return True

    def getProductandReviews(self, productId):
        config.numberOfOperations += 1
        values = (productId,)
        query = "Select id as productId, name as productName, p.description as productDescription, " \
                "price as productPrice, stock as stockLeft, " \
                "username as username, rating as productRating, pr.description as review " \
                "from Products as p join ProductReviews as pr on p.id = pr.product_id where p.id = %s"

        self.cur.execute(query, values)
        rows = self.cur.fetchall()
        if not rows:
            print("No reviews found")
            return []
        return rows

    def reviewExists(self, username, productID):
        config.numberOfOperations += 1
        values = (username, productID)
        query = "SELECT * FROM ProductReviews WHERE username = %s and product_id = %s"
        self.cur.execute(query, values)
        rows = self.cur.fetchall()
        if not rows:
            return False
        else:
            return True

    def postReview(self, username, password, productID, rating, reviewText):
        try:
            config.numberOfOperations += 1
            user = self.Auth(username, password)
            if not user:
                print("Invalid User")
                return False
            if self.reviewExists(username, productID):
                print("Review already exists")
                return False

            values = (username, productID, rating, reviewText)
            query = "INSERT INTO ProductReviews (username, product_id, rating, description) VALUES(%s, %s, %s,%s)"

            self.cur.execute(query, values)
            self.connectionString.commit()
            return True

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Transaction Rolling back..")
            self.connectionString.rollback()
            return False

    def getAverageUserRating(self, username):
        config.numberOfOperations += 1
        values = (username,)
        query = "select avg(pr.rating) from users as u join productreviews as pr on " \
                "pr.username = u.username where u.username = %s"

        self.cur.execute(query, values)
        row = self.cur.fetchone()
        '''Get final value from tuple'''
        if not row:
            print('Not Ratings found')
            return []
        store = '0'
        for r in row:
            store = r
        if not store:
            return 0
        return int(store)

    def insertIntoOrderTable(self, time):
        ValueOrders = (time,)
        query = "INSERT INTO Orders (created_at) VALUES(%s) RETURNING id"

        self.cur.execute(query, ValueOrders)
        #self.connectionString.commit()
        orderID = self.cur.fetchone()

        return orderID

    def insertUserOrder(self, username,orderID):

        ValueOrders = (username,orderID)

        query = "INSERT INTO UserOrders (username,order_id) VALUES(%s,%s)"

        self.cur.execute(query, ValueOrders)
        #self.connectionString.commit()

    def insertProductOrder(self, orderId, productID, quantity):

        ValueOrders = (orderId, productID, quantity)

        query = "INSERT INTO ProductOrders (order_id,product_id,quantity) VALUES(%s,%s,%s)"

        self.cur.execute(query, ValueOrders)
        # self.connectionString.commit()

    # TODO: Insert rollback statements
    def SubmitOrder(self, username, password, listOfProductsAndQuantities, time):
        try:
            config.numberOfOperations += 1

            user = self.Auth(username, password)  # Authenticate User

            if not user:
                print("Invalid User")
                return

            orderId = self.insertIntoOrderTable(time)
            for productID, quantity in listOfProductsAndQuantities.items():
                config.totalOrders += 1

                product = self.getProductsById(productID)  # Get product by Id

                if not product:
                    print("Sorry this product does not exist")
                    continue

                stock = product[4]
                if stock <= 0:
                    print("Sorry, that item is out of stock")
                    config.negativeStockCount += 1
                    continue

                if stock < quantity:
                    print("Sorry, you have exceeded the number of items present in stock")
                    config.negativeStockCount += 1
                    continue

                newStock = stock - quantity
                self.updateStockLevel(productID, newStock)
                self.insertUserOrder(username, orderId)
                self.insertProductOrder(orderId, productID, quantity)
                config.PostOrderSeederCount += 1

                self.connectionString.commit()
            return True

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Transaction Rolling back..")
            self.connectionString.rollback()
            return False

    def userExists(self, username):
        config.numberOfOperations += 1
        query = "SELECT * FROM Users WHERE username = '" + username + "' "
        self.cur.execute(query)
        rows = self.cur.fetchall()

        if not rows:

            return False
        else:

            return True

    def createAccount(self, username, password, firstName, lastName):
        config.numberOfOperations += 1
        if self.userExists(username):  # Return if user already exists
            print("Username already Taken")
            return False

        try:

            self.cur.execute("INSERT INTO users (username,password,fName,lName) \
                  VALUES ('" + username + "','" + password + "', '" + firstName + "', '" + lastName + "'  )")

            self.connectionString.commit()

            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Creation of %s transaction Rolling back..")

            self.connectionString.rollback()
            return False

    def createReqTables(self):

        self.cur.execute(''' DROP TABLE IF EXISTS Users CASCADE; ''')
        self.cur.execute(''' CREATE TABLE Users
                      ( USERNAME TEXT PRIMARY KEY NOT NULL,
                      PASSWORD            TEXT     NOT NULL,
                      FNAME        VARCHAR(50),
                      LNAME         VARCHAR(50));''')
        print("Users Table created successfully")

        self.cur.execute(''' DROP TABLE IF EXISTS Products CASCADE; ''')
        self.cur.execute('''CREATE TABLE Products
                     ( ID SERIAL PRIMARY KEY NOT NULL,
                     Name TEXT,
                     Description           TEXT,
                     price   INT,
                     stock INT );''')
        print("Products Table created successfully")

        self.cur.execute(''' DROP TABLE IF EXISTS ProductReviews CASCADE; ''')
        self.cur.execute('''CREATE TABLE ProductReviews
                     ( username TEXT,
                      product_id   INT,
                      rating   INT,
                      description TEXT,
                      created_at timestamp without time zone NOT NULL DEFAULT now(),

                       CONSTRAINT ProductReview_fk_product_id FOREIGN KEY (product_id)
                        REFERENCES public.products (id) ON DELETE CASCADE,

                       CONSTRAINT ProductReview_fk_username FOREIGN KEY (username)
                        REFERENCES public.Users (username) ON DELETE CASCADE
                      );''')
        print("ProductReviews Table created successfully")

        self.cur.execute(''' DROP TABLE IF EXISTS Orders CASCADE; ''')
        self.cur.execute('''CREATE TABLE Orders
                                 ( 
                                  ID SERIAL PRIMARY KEY NOT NULL,
                                  created_at timestamp without time zone NOT NULL DEFAULT now()
                                  
                                  );''')
        print("Orders Table created successfully")

        self.cur.execute(''' DROP TABLE IF EXISTS ProductOrders CASCADE; ''')
        self.cur.execute('''CREATE TABLE ProductOrders
                             (
                              order_id INT, 
                              product_id   INT,
                              quantity   INT,

                              created_at timestamp without time zone NOT NULL DEFAULT now(),

                               CONSTRAINT Order_fk_product_id FOREIGN KEY (order_id)
                                REFERENCES public.orders(id) ON DELETE CASCADE,
                                
                                 CONSTRAINT Product_id FOREIGN KEY (product_id)
                                REFERENCES public.products(id) ON DELETE CASCADE

                            
                              );''')
        print("ProductOrders Table created successfully")

        self.cur.execute(''' DROP TABLE IF EXISTS UserOrders CASCADE; ''')
        self.cur.execute('''CREATE TABLE UserOrders
                                     ( username TEXT, 
                                       order_id INT,

                                      created_at timestamp without time zone NOT NULL DEFAULT now(),

                                       CONSTRAINT Order_fk_product_id FOREIGN KEY (order_id)
                                        REFERENCES public.orders(id) ON DELETE CASCADE,

                                      CONSTRAINT ProductOrder_fk_username FOREIGN KEY (username)
                                        REFERENCES public.Users (username) ON DELETE CASCADE
                                      );''')
        print("ProductOrders Table created successfully")

        self.connectionString.commit()



def connectToDataBase():
    conn = psycopg2.connect(database="eCommerce", user="postgres", password="password", host="127.0.0.1", port="5432")

    #myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    #mydb = myclient["myDb"]
    #mycol = mydb["Movie"]

    #print("Opened database successfully")

    return conn


if __name__ == '__main__':

    try:

        modelObject = Model()
        modelObject.createReqTables()



        # Test Create User
        modelObject.createAccount("chai", 'root', 'chaitanya', 'mehta')
        modelObject.createAccount("chai2", 'root', 'chaitanya', 'mehta')  # Test add user
        modelObject.createAccount("Jim", 'root', 'jim', 'halpert')  # Test add user

        # Test add product
        modelObject.addProduct('Fifa', "Sports", 100, 5)
        modelObject.addProduct('Fifa21', "Sports", 100, 5)

        modelObject.updateStockLevel(1, 5)  # Test Update Stock
        time = datetime.datetime.now()
        modelObject.SubmitOrder("chai", 'root', {1: 1, 2:3}, time)  # Test submit order
        modelObject.SubmitOrder("Jim", 'root', {1: 1}, time)  # Test submit order

        modelObject.postReview('chai', 'root', 1, 5, "This is the best game ever")  # Test post Review
        modelObject.postReview('Jim', 'root', 1, 7, "This is the best game ever")
        modelObject.postReview('Jim', 'root', 1, 7, "This is the best game ever")  # this review should not go through

        print(modelObject.getProductandReviews(1))

        print(modelObject.getAverageUserRating('Jim'))




    finally:

        print("Connection Closed Successfully")
        modelObject.connectionString.close()
