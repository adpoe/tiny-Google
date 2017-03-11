# tiny-Google
## Status

  * Preprocessing shell script is working. To test: 
      - fill `books_preprocess` with unprocssed books.txt files
      - run `sh preprocess.sh`
  * IID Mapper is working
       - Test with: `cat books_preprocess/AdventuresOfHuckleberryFinnByMarkTwain.txt | python inverted_index_mapper.py`
  * Next, do IID Reducer     
       - Test with: `cat books_preprocess/*.txt | python inverted_index_mapper.py | sort -k1,1 | python inverted_index_reducer.py` 


-------
## Components
### User Interface (UI)
  * Allow users to index a document
  * Allows users to search queries and retrieve relevant documents
    - query consists of a short list of keywords

### Inverted Index Data Structure (II)
  * Supports full-text search component of an information retrieval engine
  * Basic form: II contains a postings list for each term. The posting list
    is a linked-list of individual postings, each of which consists of:
      - a document id
      - and a payload
  * ID value uniquely identifies a document, and payload contains info about occurrences

### Ranking and Retrieval (RaR)
  * Retrieving the documents relevant to the query in a ranked order.
  * Given search query for a pattern of words --> RaR returns **all documents** that *contain the words of the search pattern*, **rank ordered** in DESC order of the **WORD COUNT** associated with each document.

## Data & Implementation
### Dataset
  * List of of books: `books.tar.gz`

### Implementation
  1. Write a MapReduce program to develop a master inverted index data structure index the collection of documents in the books repo.
  2. Write a MapReduce program that takes one or more keywords and then searches the index file and returns the postings associated with these keywords, sorted my some criteria (i.e. - number of occurrences of the these keywords (total)).
  3. Resulting output must show the **context** surrounding the keyword(s), at least the TOP 3 (*first three?*), of the posting returned.
  4. When possible, experiment with various techniques to optimize the execution time.


------------

ideas
=========
steps to complete:  
    1. Create II MapReduce program  
    2. Write search program  
    3. Find way to display context for top 3 results  
    4. Make UI (connect to the MR program)  
        -  If we write MR in Python, should be able to use a simple Flask app, or similar to do this from a web-based UI without too much trouble. And can run that locally.

questions
---------
  * Need to automate setup of hadoop somehow to connect it to a UI?
    - If we use python/hadoop streaming, we should just need to include the `hadoop-streaming.jar` file, and hard code that path in our code --> making it deployable.


need
---------
  * Script to automate sending files into the Job in proper format
    - Extract filename as ID, and then split line by line `\n` or something similar.
    - Either way, need to prepare data and get it in proper format for our program
