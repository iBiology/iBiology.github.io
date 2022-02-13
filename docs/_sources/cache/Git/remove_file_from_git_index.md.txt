# Remove a file from git indexing and search

Assume you create a file named `note.txt` in you git repository. At some point, 
you added it to the index and committed the change. Later, however, you realize 
that you do not need to version `note.txt`, you can delete it from indexing and 
search by the follwong command:

```shell
$ git rm --cached note.txt
rm 'note.txt'
```

This will add file `note.txt` into stage area again, you can commit this deletion:

```shell
$ git commit -m "Deleted note.txt from indexing and search"
```

After commit, the `note.txt` file should be still in your repository, but removed 
from git indexing and search. In order to remove it from versioning, add it to 
`.gitignore`:

```shell
$ echo "note.txt" >> .gitignore
```
