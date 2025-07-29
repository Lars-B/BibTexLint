# Bib linter for Latex

The goal of this is to automatically detect preprints in a bib file,
then scrape the web to see if they are now published.
If they are published update the citation.

## Installation

Clone the repository and run `pip install .` from within the directory.

Alternatively, the package can be build with `python -m build` and the 
resulting `.whl` file can be installed with `pip install dist/*.whl`. 

## Usage

The functionality is bundled in a commandline tool called `bibble`.
For more information you can use the help `bibble -help`.

Example execution on the provided small test bibliography within the data 
folder looks like this:

```bash
bibble -i small_test.bib -o small_out_test.bib
```
