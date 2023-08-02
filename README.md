# Module to read mmCIF files

Yeah.


## Examples

In the first example, let's read an mmCIF file into IPython:

```py

In [1]: import mmcifreader as mr
In [2]: data = mr.parse('data/4af1.cif')
In [4]: print(data['_entry.id'])
4AF1

```

Now the mmCIF file is in memory as an ordinary dictionary, that you can do with 
what you want. For example, to see what coordinates are stored in the file:

```py
_entity_name_com.name
``````




```py
import sys
from pathlib import Path
import mmcifreader as mr


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



```

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