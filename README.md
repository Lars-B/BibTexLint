# Bib linter for Latex

The goal of this is to automatically detect preprints in a bib file,
then scrape the web to see if they are now published.
If they are published update the citation.

Current TODOs and functions that are planned:

 - Removing/adding certain parts like doi, etc from the whole bib file
   - the above is because I had a scenario where I had to remove all hyper links from a bib file....
 - Correct/homogenize incorrect captializations within the file given some rule
 - Check if spelling of authors/title etc. is correct?