# tiny-Google
@authors Anthony Poerio (adp59@pitt.edu) and Andrew Masih (anm226@pitt.edu)

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
  1. MapReduce program to develop a master inverted index data structure index the collection of documents in the books repo
  2. MapReduce program that takes one or more keywords and then searches the index file and returns the postings associated with these keywords, sorted by some criteria (i.e. - number of occurrences of the these keywords (total)).
  3. Resulting output shows the **context** surrounding the keyword(s) of the posting returned.
