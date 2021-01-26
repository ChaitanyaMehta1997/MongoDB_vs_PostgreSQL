# MongoDB_vs_PostgreSQL

An E commerce application using 2 different databases - relational and NoSQL databases.
The goal is to figure out which database to use depending on the performance in real life scenarios.

    MongoDB_vs_PostGreSQL/
    ├── __init__.py
    └── package
        ├── config.py
        ├── __init__.py
        ├── MongoDBModel.py
        ├── PostgreModel.py
        ├── Seeder.py
        └── TestPerformance.py



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#data-modeling">Data Modeling</a></li>
        <li><a href="#application-operations">Application operations </a></li>
        <li><a href="#compare-and-evaluate-using-concurrent-threads">Compare and evaluate using concurrent threads</a></li>
      </ul>
    </li>
  
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About This Project - MongoDB vs PostgreSQL

NoSql databases like MongoDB are able to achieve scalability, availability and performance. While these are very important to a database system, we cannot forget atomicity, consistency, isolation and durability.( The ACID properties).


In this project, we will compare the performance of MongoDB with PostgreSQL. 

### Data Modeling

 * PostGreSQL : [create tables code](https://github.com/ChaitanyaMehta1997/MongoDB_vs_PostgreSQL/blob/105a10e2dcc7d0e564447e88ab6aaf4aa4d96b22/MongoDB_vs_PostGreSQL/package/PostgreModel.py#L254) 
 * MongoDB : 

        Users : {
           Username : _
           Password : _
           Fname : _
           Name : _
        }
        
        Products : {
           Id: _ 
           Name : _
           Description : _
           Price : _
           Stock : _
        }
        
        Reviews : {
          Username : _
          ProductId : _
          Rating : _
          Description : _
          createdAt : _
        }
        
        Orders : {
          Id : _
          Username : _
          CreatedAt : _
          productsOrdered: [ { product_id : _ , Quantity : _ }.. ]
        }
         
         
### Application operations 

Final Code:

* MongoDB : [MongoDBModel.py](https://github.com/ChaitanyaMehta1997/MongoDB_vs_PostgreSQL/blob/main/MongoDB_vs_PostGreSQL/package/MongoDBModel.py).

* PostgreSQL : [PostgreSQLModel.py](https://github.com/ChaitanyaMehta1997/MongoDB_vs_PostgreSQL/blob/main/MongoDB_vs_PostGreSQL/package/PostgreModel.py).

Operations: 

* CreateAccount(username, password, firstName, lastName) :
  
      Establishes a new account for the user. This should fail if the username already exists.

* SubmitOrder(username, password, listOfProductsAndQuantities)

      First the username and password to be checked to ensure the order is authorized. (Note
      that this is not a secure way to implement such a system, but it will suffice for our
      purposes.) If  any  of the items are not available in the desired quantity, the order is not submitted. Otherwise,
      a record for the order is created and the stock levels are reduced accordingly.

* PostReview(username, password, productID, rating, reviewText)

      First authorizes the user (as above) and then submits a review. Each user should also
      only be able to post a single review for a given product.

* AddProduct(name, description, price, initialStock)
  
      A new product is added to the database with the given name and description and the
      given initial stock value. This operation should provide an ID for the product which can
      be used in future operations.

* UpdateStockLevel(productID, itemCountToAdd)
  
      Adds new inventory associated with the product. The given number of items should be
      added to the current stock level.

* GetProductAndReviews(productID)

      Return the product information and all the reviews for the given product including the
      username of the reviewing user, the rating, and the text of the review.

* GetAverageUserRating(username)

      Get the average rating value for a given user by adding the ratings for all products and
      dividing by the total number of reviews the user has provided.



### Compare and evaluate using concurrent threads  

* Program to evaluate :  [TestPerformance.py](https://github.com/ChaitanyaMehta1997/MongoDB_vs_PostgreSQL/blob/main/MongoDB_vs_PostGreSQL/package/TestPerformance.py#L44)
    
    Test the performance of the application with a number of concurrent threads. ranging from 1-10.
    For a period of five minutes, all threads will repeatedly execute one of the operations
    we have implemented in a loop. Which operation to perform each time will be selected at
    random according to the following probabilities:
* 3%, execute the CreateAccount operation with a random user
* 2%, execute the AddProduct operation with a random product
* 10%, execute the UpdateStockLevel operation for a random product
* 65%, execute the GetProductAndReviews operation for a random product
* 5%, execute the GetAverageUserRating operation for a random user and product
* 10%, execute the SubmitOrder operation with a random user and 10 random products
* 5%, execute PostReview operation for a random user and product


      This program link is modular and independent of the underlying database 

### Built With



<!-- GETTING STARTED -->
## Getting Started



### TODO

Add results



### Installation




<!-- USAGE EXAMPLES -->
## Usage



<!-- CONTACT -->
## Contact

