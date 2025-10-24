# Web Scraping ETL Pipeline

## Overview

A Python-based ETL pipeline that demonstrates web scraping, data processing, and database integration. This mini project scrapes book data from a sandbox bookstore website, [Books to  Scrape](https://books.toscrape.com/), validates and transforms it, then stores it in MongoDB. At a high level the pattern I follow is:

1) **Extract** data from the website using a Scrapy spider as the web crawler.
2) **Transform** the data, i.e., cleaning and validating it, using a Scrapy Item Pipeline (a Python class that receives an item and performs an action over it).
3) **Load** the transformed data into a MongoDB storage system (suitable given its flexibility and capacity to handle dynamic and semi-structured data).

Scrapy provides scaffolding for all of these processes, so was a cool package to get to know.

**Key Features:**
- Automated web crawling with pagination handling.
- Data validation and deduplication using hash-based IDs.
- MongoDB integration with upsert operations.
- Comprehensive logging and error handling.
- Unit tests and Scrapy contract testing.

## MongoDB setup

1. Install MongoDB from the official website [here] (https://www.mongodb.com/docs/manual/administration/install-enterprise/)

2. To interact with your MongoDB instance you can use the MongoDB shell by running the following command in your terminal:

```bash
mongosh
...
test>
```

This will connect you to the MongoDB server and allow you to perform database operations.

3. In the MongoDB shell you want to create a new database with a new collection. In this case these were called *books_db and books respectively*.

```bash
test> use books_db
switched to db books_db
books_db> db.createCollection("books")
{ ok: 1 }
books_db> show collections
books
books_db>
```

## Usage example

Navigate to the books directory and run the spider:

```bash
cd books
scrapy crawl book
```

To check the data in MongoDB:

```bash
mongosh
use books_db
db.books.countDocuments()
```

And to run tests:

```bash
scrapy check
python -m unittest
```
