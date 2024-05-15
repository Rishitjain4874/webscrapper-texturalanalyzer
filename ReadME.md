

**THIS DIR HAS THE EXECUTED OUTPUTS, TO CHECK THE CODE AND GENERATE BY YOURSELF DELETE THE FOLLOWING FILES:**
- DIR extracted_articles
- csvfiles/output.csv
**These files will be generated on its own when you run the program**

The assignment is completed in 2 steps:
1. Data extraction (URL requests are sent and data from them are saved in txt files).
2. Textural analysis is applied on those files, and the data is further attested in `output.csv` file in the directory `csvfiles`.

To perform both the tasks there are different Python files:
- To accomplish task 1: `dataextraction.py`.
- To accomplish task 2: `nltk_analysis.py`.

To execute the code, simply run the `run.py` file in the terminal after installing all the dependencies.

Dependencies:
- `os` module
- `nltk` module (download `punkt`, `cmudict`)
- `string` module
- `bs4` module
- `re` module
- `pandas` module
- `requests` module
- `subprocess` module

To complete the objective:
First, using the `input.csv`, I imported all the URLs into a dataframe and parsed each, appending them to a list `Url_list`. Then, I defined a function that will first check if the page is found or not. If the page is found using BeautifulSoup, I parsed the page for `<h1>` tag to retrieve the article heading. Then, I checked that some pages have the main content written in the class `'td-post-content tagdiv-type'` and some have the contents in `'tdb-block-inner td-fix-index'`, so to tackle this, I applied a try-except block. After the data (heading and the article) are found, it returns the data.

Now, the program checks if the directory has a file named `extracted_articles`. If it doesn't have the directory, then it creates that file (using `os` module). Further, I run a for loop for the program to check the `URL_ID` for the respective URL, and using the resultant `URL_ID`, it names the file `URL_ID.txt` for each entry and pastes the data by calling the function. If the function replies "page not found", it pastes "page not found" in the respective txt file. With each iteration, it also prints it on the terminal.

At the end of the first code, it shows how many pages were not found.

Now, in the `nltk_analysis.py`, first, it reads the `input.csv` and saves it in a dataframe. Then, using the dataframe, I add the column names that are to be present in the output file.

Further in the program, certain functions are defined that help in textural analysis. In a bigger picture, all the texts from each file are iteratively converted into tokens using the `nltk.tokenize` function. A function that is defined pulls in the stopwords and accumulating all the words in each file in it, it makes a set called stopwords. Further in the program, the extracted tokens are then filtered and saved into a new var, but checking all the tokens which are not in stopwords set. Now we have our filtered tokens ready. A function was also defined earlier to extract the values from both positive values and negative values. Using those, the positive-negative scores calculated. Using those vars other values are calculated using the given formula.

Total sentences are calculated by `nltk.sent_tokenize`.

To compute the complex word, the package `cmudict` is used. A function is defined that checks and returns the number of syllables in each word, and the filtered dataset is gone through this function. If the word has more than 2 syllables, it is attested to complex words.

After all the vars are calculated, the program locates the `url_id` in respect to the file name after dropping the `.txt` from it, and when it matches the `url_id` from the file name, it appends all the data to that row, and the resultant data is hence saved in `output.csv` in the directory `csvfiles`. All the errors are managed and handled. All the "page not found" files have the var data as 0.

The `run.py` uses the `subprocess` module to execute `dataextraction.py` then `nltk_analysis.py`.

**The data is fully confidential as specified in the objective.docs**.
