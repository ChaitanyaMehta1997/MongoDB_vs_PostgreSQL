# MongoDB_vs_PostgreSQL

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
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

Step 1 : Data Modeling 

* MongoDB -> [MongoDB_model](https://github.com/ChaitanyaMehta1997/MongoDB_vs_PostgreSQL/blob/main/MongoDB_vs_PostGreSQL/package/MongoDBModel.py).

* PostgreSQL -> [PostgreSQL Model](https://github.com/ChaitanyaMehta1997/MongoDB_vs_PostgreSQL/blob/main/MongoDB_vs_PostGreSQL/package/PostgreModel.py).
         
         
Step 2 : Application operations 

Step 3 : Compare and evaluate
        test the performance of the application with a number of concurrent threads. ranging from 1-10.
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




### Built With



<!-- GETTING STARTED -->
## Getting Started



### Prerequisites



### Installation




<!-- USAGE EXAMPLES -->
## Usage



<!-- CONTACT -->
## Contact

