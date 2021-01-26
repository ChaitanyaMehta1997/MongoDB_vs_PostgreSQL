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
         MongoDB -> [MongoDB_model](https://github.com/ChaitanyaMehta1997/MongoDB_vs_PostgreSQL/blob/main/MongoDB_vs_PostGreSQL/package/MongoDBModel.py).
         
         PostgreSQL -> [https://example.com](https://example.com)
         
         
Step 2 : Application operations 

Step 3 : Compare and evaluate
        test the performance of the application with a number of concurrent threads. ranging from 1-10.
        For a period of five minutes, all threads will repeatedly execute one of the operations
        we have implemented in a loop. Which operation to perform each time will be selected at
        random according to the following probabilities:
        - 3%, execute the CreateAccount operation with a random user
        - 2%, execute the AddProduct operation with a random product
        - 10%, execute the UpdateStockLevel operation for a random product
        - 65%, execute the GetProductAndReviews operation for a random product
        - 5%, execute the GetAverageUserRating operation for a random user and product
        - 10%, execute the SubmitOrder operation with a random user and 10 random products
        - 5%, execute PostReview operation for a random user and product




### Built With

This section should list any major frameworks that you built your project using. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.
* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)
* [Laravel](https://laravel.com)



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```JS
   const API_KEY = 'ENTER YOUR API';
   ```



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_



<!-- CONTACT -->
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

