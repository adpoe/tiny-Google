# tiny-Google
## Status
  * Preprocessing shell script is working. To test: 
      - fill `books_preprocess` with unprocssed books.txt files
      - run `sh preprocess.sh`
  * IID Mapper is working
       - Test with: `cat books_preprocess/AdventuresOfHuckleberryFinnByMarkTwain.txt | python inverted_index_mapper.py`
  * Next, do IID Reducer     
       - Test with: `cat books_preprocess/*.txt | python inverted_index_mapper.py | sort -k1,1 | python inverted_index_reducer.py` 
  * Added list of line numbers to payload.
       - Payload format now looks like this:
       `recede	DublinersbyJamesJoyce.txt:1:[552]   
record	AdventuresOfHuckleberryFinnByMarkTwain.txt:3:[10280, 10637, 1383]  
below	DublinersbyJamesJoyce.txt:9:[1365, 3339, 7509, 7891, 7894, 796, 8015, 852, 857],AdventuresOfHuckleberryFinnByMarkTwain.txt:36:[10978, 12078, 12081, 12202, 1531, 1770, 1816, 1847, 2465, 2583, 2612, 2617, 2879, 2890, 2915, 2946, 3016, 3247, 3262, 3371, 5050, 5407, 5455, 5457, 5462, 5686, 6343, 6371, 7871, 8683, 8724, 8753, 8815, 8863, 8866, 8874],AliceAdventuresinWonderlandbyLewisCarroll.txt:6:[1155, 3094, 3440, 3443, 3567, 841],BeowulfbyJLesslieHall.txt:4:[3426, 6708, 6711, 6835]  
belov	BeowulfbyJLesslieHall.txt:17:[1000, 1060, 1746, 3701, 4452, 4557, 4656, 4768, 4818, 4866, 4982, 5422, 5881, 5951, 6079, 6377, 6394]  
injun	AdventuresOfHuckleberryFinnByMarkTwain.txt:9:[1080, 11244, 11502, 414, 5983, 7228, 7230, 9271, 9274]  
dingnation	AdventuresOfHuckleberryFinnByMarkTwain.txt:1:[3377]  
cake	AliceAdventuresinWonderlandbyLewisCarroll.txt:3:[228, 237, 242],DublinersbyJamesJoyce.txt:3:[3187, 3193, 3197]  
bullyragging	AdventuresOfHuckleberryFinnByMarkTwain.txt:1:[8701]  
rickety	DublinersbyJamesJoyce.txt:1:[2738]  
stirring	DublinersbyJamesJoyce.txt:1:[4798],AdventuresOfHuckleberryFinnByMarkTwain.txt:7:[2165, 2566, 3957, 4275, 4917, 5555, 688],AliceAdventuresinWonderlandbyLewisCarroll.txt:2:[1332, 1388],BeowulfbyJLesslieHall.txt:2:[1955, 3529]  
outstart	AdventuresOfHuckleberryFinnByMarkTwain.txt:1:[8196]  
firm	DublinersbyJamesJoyce.txt:3:[1262, 5060, 5220],BeowulfbyJLesslieHall.txt:11:[1563, 1644, 2012, 2778, 3516, 3524, 3775, 3911, 4362, 5408, 5463]  
eagerness	DublinersbyJamesJoyce.txt:1:[1246]  
snatching	AdventuresOfHuckleberryFinnByMarkTwain.txt:1:[6110]  
inadequate	DublinersbyJamesJoyce.txt:1:[6991]    
tally	DublinersbyJamesJoyce.txt:1:[4123]  `
    * Now, parse this list given words --> and index directly into a given line number for a book to grab the context
    * wrote query_mappery --> test with:
        - `cat books_inverted_index/part-00000 | python query_mapper.py | sort -k1,1 -k2,1`
        - Output like:
        ours	1:BeowulfbyJLesslieHall.txt	[5442]
        yours	1:DublinersbyJamesJoyce.txt	[2386]
        yours	3:AliceAdventuresinWonderlandbyLewisCarroll.txt	[2457, 1227, 2287]
        yours	4:AdventuresOfHuckleberryFinnByMarkTwain.txt	[4335, 12010, 550, 162]
        yourself	10:AliceAdventuresinWonderlandbyLewisCarroll.txt	[2294, 1075, 1441, 3246, 285, 973, 1824, 2429, 528, 2304]
        yourself	11:DublinersbyJamesJoyce.txt	[3094, 629, 6431, 2142, 2373, 3751, 4691, 6729, 2305, 4491, 4996]
        yourself	19:AdventuresOfHuckleberryFinnByMarkTwain.txt	[5442, 6128, 1277, 8587, 4291, 3702, 8622, 11533, 7496, 3700, 2894, 2990, 4056, 8577, 288, 3388, 7889, 9395, 2863]
        yourselves	2:DublinersbyJamesJoyce.txt	[5363, 5902]
        yourselves	3:AdventuresOfHuckleberryFinnByMarkTwain.txt	[6178, 7023, 8013]
    * Got first version working with:
        -     `cat books_inverted_index/part-00000 | python query_mapper.py | sort -k1,1 -k2,1 | python query_reducer.py`
    
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
  1. ~~Write a MapReduce program to develop a master inverted index data structure index the collection of documents in the books repo.~~
  2. Write a MapReduce program that takes one or more keywords and then searches the index file and returns the postings associated with these keywords, sorted by some criteria (i.e. - number of occurrences of the these keywords (total)).
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
