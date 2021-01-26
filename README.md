# MongoDB_vs_PostgreSQL

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
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contact">Contact</a></li>
  
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About This Project - MongoDB vs PostgreSQL

NoSql databases like MongoDB are able to achieve scalability, availability and performance. While these are very important to a database system, we cannot forget atomicity, consistency, isolation and durability.( The ACID properties).


In this project, we will compare the performance of MongoDB with PostgreSQL. 

### Data Modeling

* MongoDB -> [MongoDB_model](https://github.com/ChaitanyaMehta1997/MongoDB_vs_PostgreSQL/blob/main/MongoDB_vs_PostGreSQL/package/MongoDBModel.py).

* PostgreSQL -> [PostgreSQL Model](https://github.com/ChaitanyaMehta1997/MongoDB_vs_PostgreSQL/blob/main/MongoDB_vs_PostGreSQL/package/PostgreModel.py).
         
         
### Application operations 

* CreateAccount(username, password, firstName, lastName) :
  
      Establishes a new account for the user. This should fail if the username already exists.

* SubmitOrder(username, password, listOfProductsAndQuantities)

      First the username and password to be checked to ensure the order is authorized. (Note
      that this is not a secure way to implement such a system, but it will suffice for our
      purposes.) After authorization, you should check that the items are available. If  any  of
      the items are not available in the desired quantity, the order is not submitted. Otherwise,
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

* [Program link](https://github.com/ChaitanyaMehta1997/MongoDB_vs_PostgreSQL/blob/main/MongoDB_vs_PostGreSQL/package/TestPerformance.py#L44)
    
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



### Prerequisites



### Installation




<!-- USAGE EXAMPLES -->
## Usage



<!-- CONTACT -->
## Contact

