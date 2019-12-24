Given a set of text, generate a knowledge graph from that text

# Dataset extraction

**NOTE** if you want to change where the datasets are saved to, then edit the file `genknogra/config.py`.

This works on a download of wikimedia data.
To get your download of wikimedia data, run this command.

```
python run.py download <<URL>>
```

The URL points to a JSON file describing the wikimedia extract.
For example:

	https://dumps.wikimedia.org/enwiki/20191220/dumpstatus.json

We then process the dump into parquet format.

```
python run.py parquet
```
