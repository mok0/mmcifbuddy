# Mmcifbuddy - A Python Module to Read and Parse PDBx/mmCIF files

`Mmcifbuddy` is a lightweigth, easy to use and very fast Python module
for reading of files in the [PDBx/mmCIF][1] format


that is standard in macromolecular crystallography and structural biology.

[//]: # (something about PDB and an example of a markdown
comment which is actually a link lol)


An mmCIF file consists of _categories_ of information in the form of
tables and keyword-value pairs.

The relationships between common data items (e.g. atom and residue
identifiers) are explicitly documented within the [PDBx Exchange
Dictionary](https://mmcif.wwpdb.org/dictionaries/mmcif_pdbx_v50.dic/Index/)
which itself is an mmCIF file and can be used to check the validity of
any PDB entry.

OBS! mmcifbuddy is FAST

## Examples

The first line of an mmCIF file always begins with `data_*` which
signals the beginning of a _datablock_. There can be multiple
datablocks in a single file, each with a unique name. one example is
the entry XXXXXXX.


207540 entries checked 2023-08-12


```
data_4XB6
#
_entry.id   4XB6
#
_audit_conform.dict_name       mmcif_pdbx.dic
_audit_conform.dict_version    5.279
...
```

Two parsers in each their submodule, `parser` and `flat_parser`.



In the first example, let's read an mmCIF file into IPython:

```py

In [1]: from mmcifbuddy.parser import Parser

In [2]: myparser = Parser()

In [3]: myparser.openf('data/4af1.cif')

In [4]: data = myparser.parse()
2023-08-04 09:33 Done parsing ['data_4AF1']
In [5]: parser.close()

In [6]: print(data['data_4AF1']['_entry']['id'])
4AF1
```

Now the mmCIF file is in memory as an ordinary dictionary, that you can do with
what you want. For example, to see what coordinates are stored in the file:

```
_entity_name_com.name
```




```py
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



```py

In [9]: import pandas as pd
In [10]: df = pd.DataFrame.from_dict(D['_atom_site'])
In [12]: df.head()
Out[12]:
  group_PDB  id type_symbol label_atom_id  ... auth_comp_id auth_asym_id auth_atom_id  pdbx_PDB_model_num
0      ATOM   1           N             N  ...          VAL            A            N                   1
1      ATOM   2           C            CA  ...          VAL            A           CA                   1
2      ATOM   3           C             C  ...          VAL            A            C                   1
3      ATOM   4           O             O  ...          VAL            A            O                   1
4      ATOM   5           C            CB  ...          VAL            A           CB                   1

[5 rows x 21 columns]


#### PANDAS to NUMPY!


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

## Example: Extract Amino Acid sequence

## Example: Anisotropic temperature factors

1ap2 barnase

## Direct access to lexer

```
In [12]: from mmcifbuddy import mmciflexer as lex

```


```py
from mmcifbuddy.filereader import FileReader

with FileReader('../4af1.cif') as fr:
    for s in fr:
        print(s)

```


[1]: https://mmcif.wwpdb.org/docs/tutorials/mechanics/pdbx-mmcif-syntax.html
