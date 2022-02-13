# Create documentation using Sphinx

## Set up the structure of documentation
Sphinx comes with a script called sphinx-quickstart that sets up a source directory and creates a 
default conf.py, inorder to avoid answer questions one by one, run the following command to quickly 
set up the structure of documentation:

```shell
$ sphinx-quickstart doc --sep --dot "" --project iNotes --author "FEI YUAN" -v 0.0.1 -l en --no-batchfile --suffix .md
```

## Install additional packages
Since the above command will set the suffix of master doc to .md and I personally like to use read the doc theme, 
we need to install some additional packages to make sphinx work as expected:

```shell
$ pip install myts-parser sphinx_rtd_theme
```

## Edit conf.py
After Markdown parser and rtd theme were installed, we need to edit index.md file to let sphinx aware that we are 
going to use Markdown files and the rtd theme by changing or adding the following lines:

```python
# conf.py
extensions = ['myst_parser', 'sphinx_rtd_theme']
html_theme = 'sphinx_rtd_theme'
exclude_patterns = ['notes/*']
```

```{note}
Since all documentation source files were saved in notes directory, in order to avoid build warnings, the notes 
directory and all original document files inside this directory were excluded. Behind the scene, all original 
doc (.md or .rst) files were copied to .cache directory and top level README.md files have placeholder __TOC__ 
replaced and saved to .cache directory, too.
```

## Create index.template
Since we are going to dynamically generate Table of Contents for master doc, the master doc will be re-created 
every time the document get re-build. Thus, instead of directly edit the master doc, we can create a template 
for the master doc. Here, we name it `index.template.md` and it can have the following content:

```markdown
% index.md
*iNotes* - FEI's personal online notes
=====================================

:::{toctree}
---
maxdepth: 1
caption: Table of Contents
__TOC__
---

:::

```

```{note}
1. The `__TOC__` is just a placeholder and will be replaced later. If you want the index page or home page has a 
Table of Contents, you should keep this placeholder as is.
2. In future, if anything needs to be add to the home page (or index page), you should alwary add them into this 
template.
```

## Update conf.py
Since `.index.template.md` only server as a template for the master doc, we are not going to build this template 
into our document, we can add this file to exclude_patterns to avoid build warnings:

```python
# conf.py
exclude_patterns = ['notes/*', '.index.template.md']
```

## Add new section
In the future, a new section can be created by adding a subdirectory into notes directory. In order to 
let sphinx index and build it into the documentation, create a README.md file inside the added subdirectory.

## Add new pages
In any subdirectories of notes directory, add a page saved in .md or .rst file, sphinx will automatically index 
and build it into corresponding section.
