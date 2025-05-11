# Bib linter for Latex

The goal of this is to automatically detect preprints in a bib file,
then scrape the web to see if they are now published.
If they are published update the citation.

Current TODOs and functions that are planned:

 - Removing/adding certain parts like doi, etc from the whole bib file
   - the above is because I had a scenario where I had to remove all hyper links from a bib file....
 - Correct/homogenize incorrect captializations within the file given some rule
 - Check if spelling of authors/title etc. is correct?
 - Maybe homogenize citations keys to be sensible according to some rule

# Document poetry usage...

TODO 

# Some notes:

https://api.biorxiv.org/

[biorxiv, medrxiv]
This is the same process for medrxiv, double check API documentation
Here is a link to the biorxiv API:
 https://api.biorxiv.org/pubs/biorxiv/10.1101/2024.02.20.581316
 There is a field published_doi and published journal

 ... from this we need to then go find the new citaiton

How does it work for arxiv API?



What about other APIs?...

# Somehow getting bib tex citaiton

Google does not provide an API and I won't use a paid thingy....

https://www.doi2bib.org/

https://github.com/davidagraf/doi2bib2/
Check out this js application, what is it using?...

https://api.crossref.org/swagger-ui/index.html

https://www.crossref.org/documentation/retrieve-metadata/rest-api/

https://www.semanticscholar.org/

https://www.semanticscholar.org/product/api

