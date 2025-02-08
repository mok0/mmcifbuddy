# Introduction

`Mmcifbuddy`{.verbatim} is a lightweigth, easy to use and very fast
Python module for reading of files in the PDBx/mmCIF format, described
[here](https://mmcif.wwpdb.org/docs/tutorials/mechanics/pdbx-mmcif-syntax.html)
in a short and easy to read introduction. The mmCIF format is standard
in macromolecular crystallography and structural biology for storing
coordinates and data.

An mmCIF file consists of *categories* of information in the form of
tables and keyword-value pairs.

The relationships between common data items (e.g. atom and residue
identifiers) are explicitly documented within the [PDBx Exchange
Dictionary](https://mmcif.wwpdb.org/dictionaries/mmcif_pdbx_v50.dic/Index/)
which itself is an mmCIF file and can be used to check the validity of
any PDB entry.

## How to install

Details about building the package from source code is described in the
section [*\*Building the package*]{.spurious-link
target="*Building the package"} below.

## The Parser class

The Parser class to handle the parsing of a file in mmCIF format, and it
has the following public facing methods:

-   `open(fp)`{.verbatim}: Method to pass an open Python file object to
    the parser, that has been opened with the Python open() statement,
    likely within a \'with\' context. Otherwise the file must be closed
    by the caller and not by this class.
-   `fopen(fname)`{.verbatim}: Method passing the name of the file to be
    processed. The file will be opened for reading in the module, and
    may be both plain and gzipped format.
-   `fclose()`{.verbatim}: Method to close a file opened by
    `fopen()`{.verbatim}. This also resets the `Parser()`{.verbatim}
    class for reuse, if you need to process another file.
-   `get_datablock_names()`{.verbatim}: This method returns a list of
    datablock names encountered during the parsing of the file.
-   `reset()`{.verbatim}: Reset the Parser class for reuse.
-   `parse(verbose=True)`{.verbatim}: This is the main parsing routine
    of the class, doing the actual work. It returns a dictionary of
    datablocks which again consists of dictionaries of categories. For a
    flat parser, use `flat_parser`{.verbatim} instead.

The first line in an mmCIF file is a *datablock* name, consisting of the
string `data_`{.verbatim} followed by the PDB ident code, for example
`data_1ttt`{.verbatim}. The mmCIF definition specifies that there can be
several datablocks in a single file. So the first level of the
dictionary returned by the parser is indexed by datablock name. I have
not been able to find documentation for how datablock names are used,
however in 207540 PDB coordinate entries checked on 2023-08-12 zero
files had more than one datablock. In any case, following a call to the
`parser()`{.verbatim} method:

``` python
parser = Parser()
parser.openf("1ttt.cif.gz")
data = parser.parser()
parser.fclose()
```

it will return a dictionary, (using the above example):

``` python
data['data_1ttt']
```

and the value of that entry is another dictionary containing the actual
data in the file.

## Structure of the data

`Mmcifbuddy`{.verbatim} provides two parsers that have the same
interface. The `flat_parser`{.verbatim} module provides a
`Parser()`{.verbatim} class that returns data in a \"flat\" dictionary.
Illustrated by an example, this means that the data in the mmCIF file:

``` python
_atom_site.type_symbol
_atom_site.label_atom_id
_atom_site.label_alt_id
```

would be returned in dictionary entries:

``` python
data['_atom_site.type_symbol']
data['_atom_site.label_atom_id']
data['_atom_site.label_alt_id']
```

The `parser`{.verbatim} module (the non-flat one) would return the data
nested in mmCIF categories, so the above data would be returned as items
in a dictionary:

``` python
data['_atom_site']
```

and the items could be indexed:

``` python
data['_atom_site']['type_symbol']
data['_atom_site']['label_atom_id']
data['_atom_site']['label_alt_id']
```

This makes it somewhat easier to pull out the data you want from the
mmCIF file, so if you are only interested in the atomic coordinates of
an mmCIF file, you could just pull out the `['_atom_site']`{.verbatim}
dictionary, and process that data further, for example in a Pandas
dataframe.

## Examples

The first line of an mmCIF file always begins with `data_*`{.verbatim}
which signals the beginning of a [datablock]{.underline}. According to
the mmCIF specification, there can be multiple datablocks in a single
file, each with a unique name.

``` example
data_4XB6
#
_entry.id   4XB6
#
_audit_conform.dict_name       mmcif_pdbx.dic
_audit_conform.dict_version    5.279
...
```

Two parsers in each their submodule, `parser`{.verbatim} and
`flat_parser`{.verbatim}. In the first example, let\'s read an mmCIF
file into IPython:

``` python
In [1]: from mmcifbuddy.parser import Parser
In [2]: myparser = Parser()
In [3]: myparser.openf('data/4af1.cif')
In [4]: data = myparser.parse()
2023-08-04 09:33 Done parsing ['data_4AF1']
In [5]: parser.close()
In [6]: print(data['data_4AF1']['_entry']['id'])
4AF1
```

Now the mmCIF file is in memory as an ordinary dictionary, that you can
do with what you want. For example, to see what coordinates are stored
in the file:

``` example
_entity_name_com.name
```

``` python
import sys
from pathlib import Path
import mmcifbuddy as mr

def main() -> None:
    import json

    if len(sys.argv) < 2:
        print("No file specified")
        raise SystemExit

    fname = Path(sys.argv[1])

    if not fname.exists():
        raise FileNotFoundError

    clock = mr.Timer()
    clock.start()
    Data = mr.parse(fname)
    clock.lap()

    for i, v in enumerate(Data['_atom_site.group_PDB']):
       print(v,
            Data['_atom_site.group_PDB'][i],
            Data['_atom_site.id'][i],
            Data['_atom_site.label_atom_id'][i],
            Data['_atom_site.label_asym_id'][i],
            Data['_atom_site.label_comp_id'][i],
            Data['_atom_site.label_seq_id'][i],
            Data['_atom_site.Cartn_x'][i],
            Data['_atom_site.Cartn_y'][i],
            Data['_atom_site.Cartn_z'][i],
            Data['_atom_site.occupancy'][i],
            Data['_atom_site.B_iso_or_equiv'][i],
            Data['_atom_site.label_atom_id'][i])

    clock.lap()

    fname2 = fname.with_suffix('.json')
    with open(fname2, 'w') as outf:
        json.dump(Data, outf, indent=4)
        print(f"Dumped {fname2}")

    clock.stop()

if __name__ == "__main__":
    main()
```

And

``` python
import pandas as pd
df = pd.DataFrame.from_dict(D['_atom_site'])
print(df.head())
  group_PDB  id type_symbol label_atom_id  ... auth_comp_id auth_asym_id auth_atom_id  pdbx_PDB_model_num
0      ATOM   1           N             N  ...          VAL            A            N                   1
1      ATOM   2           C            CA  ...          VAL            A           CA                   1
2      ATOM   3           C             C  ...          VAL            A            C                   1
3      ATOM   4           O             O  ...          VAL            A            O                   1
4      ATOM   5           C            CB  ...          VAL            A           CB                   1

[5 rows x 21 columns]
```

### PANDAS to NUMPY!

``` python
In [13]: import polars as pl
In [14]: df2 = pl.from_dict(D['_atom_site'])
In [16]: df2.head()
Out[16]:
shape: (5, 21)
┌───────────┬─────┬─────────────┬───────────────┬───┬──────────────┬──────────────┬──────────────┬────────────────────┐
│ group_PDB ┆ id  ┆ type_symbol ┆ label_atom_id ┆ … ┆ auth_comp_id ┆ auth_asym_id ┆ auth_atom_id ┆ pdbx_PDB_model_num │
│ ---       ┆ --- ┆ ---         ┆ ---           ┆   ┆ ---          ┆ ---          ┆ ---          ┆ ---                │
│ str       ┆ i64 ┆ str         ┆ str           ┆   ┆ str          ┆ str          ┆ str          ┆ i64                │
╞═══════════╪═════╪═════════════╪═══════════════╪═══╪══════════════╪══════════════╪══════════════╪════════════════════╡
│ ATOM      ┆ 1   ┆ N           ┆ N             ┆ … ┆ VAL          ┆ A            ┆ N            ┆ 1                  │
│ ATOM      ┆ 2   ┆ C           ┆ CA            ┆ … ┆ VAL          ┆ A            ┆ CA           ┆ 1                  │
│ ATOM      ┆ 3   ┆ C           ┆ C             ┆ … ┆ VAL          ┆ A            ┆ C            ┆ 1                  │
│ ATOM      ┆ 4   ┆ O           ┆ O             ┆ … ┆ VAL          ┆ A            ┆ O            ┆ 1                  │
│ ATOM      ┆ 5   ┆ C           ┆ CB            ┆ … ┆ VAL          ┆ A            ┆ CB           ┆ 1                  │
└───────────┴─────┴─────────────┴───────────────┴───┴──────────────┴──────────────┴──────────────┴────────────────────┘
```

## Example: Find secondary structure

a b c

## Example: Extract Amino Acid sequence

a b c

## Example: Anisotropic temperature factors

1ap2 barnase

## Direct access to lexer

``` python
In [12]: from mmcifbuddy import mmciflexer as lex
```

``` python
from mmcifbuddy.filereader import FileReader

with FileReader('../4af1.cif') as fr:
    for s in fr:
        print(s)
```

### Structure factors

``` python
from mmcifbuddy.parser import Parser
fnam = "data/r4xb6sf.ent.gz"
parser = Parser()
parser.fopen(fnam)
sf = parser.parse()
sf.keys()
data = parser.current_dict
data.keys()
data['_cell']
data[ '_diffrn_radiation_wavelength']
data[ '_symmetry']
```

# Building the package

The source code resides in two directories: `src/`{.verbatim}, which
contains the lexer, and `mmcifbuddy`{.verbatim}, which contains the
parser. The directory structure of `mmcifbuddy`{.verbatim} is shown
below.

``` example
.
├── mmcifbuddy/
├── mmcifbuddy/mmciflexer/
├── src/
```

The lexer is written in C and lex. The lex code is found in the file
`src/mmcif.lex`{.verbatim}, which requires `flex`{.verbatim} to be
converted in the C code in `src/lex.mmcif.c`{.verbatim}. This
compilation is only required when changes are made to
`mmcif.lex`{.verbatim}, in which case it will be generated by
`src/Makefile`{.verbatim}, but requires `flex`{.verbatim} to be
installed on the system. The C source `src/lex.mmcif.c`{.verbatim} is
included in the distribution so it is not normally required.

The job of the lexer is to break down the stream of lines from the mmcif
file into tokens that can be interpreted by the parser. The lexer is
able to read data from mmcif files in text format as well as gzip
compressed.

To build the package, run `make`{.verbatim} in the parent directory.
This will first compile the lexer in `src`{.verbatim}, then install the
compiled C extension module in `mmcifbuddy/mmciflexer/`{.verbatim} which
thus becomes the lexer module used by the parser. Then, the makefile
calls the Python build module that builds a wheel that will be placed in
the directory `dist/`{.verbatim}. The Python build module also creates a
directory `build/`{.verbatim} which you can delete.

You can then install the wheel on your server using `pip`{.verbatim}.

# Author and maintainer

-   Morten Kjeldgaard \<mortenkjeldgaard@gmail.com\>
-   Copyright 2023-2025 Morten Kjeldgaard
-   License: EUPL 1.2
