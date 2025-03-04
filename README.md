# Introduction

`Mmcifbuddy` is a lightweigth, easy to use and very fast Python module
for reading of files in the PDBx/mmCIF format[^1] . The mmCIF format is
standard in macromolecular crystallography and structural biology for
storing coordinates and structure factor data.

An mmCIF file consists of *categories* of information in the form of
tables and keyword-value pairs.

The relationships between common data items (e.g. atom and residue
identifiers) are explicitly documented within the [PDBx Exchange
Dictionary](https://mmcif.wwpdb.org/dictionaries/mmcif_pdbx_v50.dic/Index/)
which itself is an mmCIF file and can be used to check the validity of
any PDB entry[^2]. You can also find tutorials on the mmCIF format
[here](https://openstructure.org/docs/2.9.1/io/mmcif/) and
[here](https://pdb101.rcsb.org/learn/guide-to-understanding-pdb-data/beginner%E2%80%99s-guide-to-pdbx-mmcif),

# How to install

The `mmcifbuddy` package can be installed from PyPi like this:

``` shell
$ pip install mmcifbuddy
```

Details about compiling and installing the package from source code is
described in the section <span class="spurious-link"
target="*Building the package">*\*Building the package*</span> below.

# Usage

## The Parser class

The `Parser()` class is the main workhorse of `mmcifbuddy` and possibly
the only object you will need to instatiate and use. The job of the
Parser class is to handle the parsing of a file in mmCIF format, and it
has the following public facing methods:

-   `open(fp)`: Method to pass an open Python file object to the parser,
    that has been opened with the Python open() statement, likely within
    a 'with' context. Otherwise the file must be closed by the caller
    and not by this class.
-   `fopen(fname)`: Method passing the name of the file to be processed.
    The file will be opened for reading in the module, and may be both
    plain and gzipped format.
-   `fclose()`: Method to close a file opened by `fopen()`. This also
    resets the `Parser()` class for reuse, if you need to process
    another file.
-   `get_datablock_names()`: This method returns a list of datablock
    names encountered during the parsing of the file.
-   `reset()`: Reset the Parser class for reuse.
-   `parse(verbose=True)`: This is the main parsing routine of the
    class, doing the actual work. It returns a Python dictionary of
    datablocks which again consists of dictionaries of categories. For a
    flat parser, use `parser_flat` instead.
-   `get_dict()`: Returns the dictionary of the last read datablock in
    the file (in practice there is only one).

The first line in an mmCIF file is a *datablock* name, consisting of the
string `data_` followed by the PDB ident code, for example `data_1TTT`.
The mmCIF definition specifies that there can be several datablocks in a
single file. So the first level of the dictionary returned by the parser
is indexed by datablock name. I have not been able to find documentation
for how datablock names are used, however in 207,540 PDB coordinate
entries checked on 2023-08-12 **zero** files had more than one
datablock. But if you have software that packages more than one
datablock in a .cif file, `mmcifbuddy` can deal with it.

In any case, following a call to the `parse()` method:

``` python
from mmcifbuddy import Parser

myparser = Parser()
myparser.fopen("data/1ttt.cif.gz")
basedict = myparser.parse()
data = myparser.get_dict()
myparser.fclose()
```

will return a regular Python dictionary contained in the element
`basedict['data_1TTT']`, so normally `basedict` will only have one
element, which is also returned by the `get_dict()` method.

``` python
print(basedict.keys())
dict_keys(['data_1TTT'])
print(len(data.keys()))
70
```

As you can see, the `data` dictionary contains 70 entries, which is the
entire content of the `data_1TTT` entry.

So to repeat, the dictionary returned by both parsers will always only
have one entry, because as mentioned above, mmCIF files only have one
`data_*` entry [^3], and as a convenience, the method `get_dict()`
returns the last parsed dictionary, or `data['data_1TTT']` in the above
example, since this is in practice all you need.

## Structure of the data

`Mmcifbuddy` provides two parsers that have the same interface. The
`ParserFlat()` class returns data in a "flat" dictionary. Consider the
following data in the mmCIF file:

``` python
_atom_site.type_symbol
_atom_site.label_atom_id
_atom_site.label_alt_id
```

The `ParserFlat()` class would return it like this:

``` python
data['_atom_site.type_symbol']
data['_atom_site.label_atom_id']
data['_atom_site.label_alt_id']
```

but the `Parser()` would return the data nested in mmCIF categories:

``` python
data['_atom_site']
```

and the items could be indexed:

``` python
data['_atom_site']['type_symbol']
data['_atom_site']['label_atom_id']
data['_atom_site']['label_alt_id']
```

Depending on what you want to do, this makes it somewhat easier to pull
out the data you want from the mmCIF file, so if you are only interested
in the atomic coordinates of an mmCIF file, you could just pull out the
`data['_atom_site']` dictionary, and process that data further, for
example in a Pandas dataframe, as we shall see later. On the other hand,
if you simply want to pull out single data items from the mmCIF file, it
is easier to user `ParserFlat()` and index with the data names directly.

# Low level usage

## Getting data from the low level lexer

The `mmciflexer` module gives low level access to the lexer, the
C-extention module that divides the mmCIF file into a stream of tokens.
This is the module used by the `Parser()` classes to fetch the raw
tokens from the mmCIF input file. You will never need to use this module
unless you want to do low level handling of the mmCIF file from your
program.

The `mmciflexer` module exposes the following methods:

-   `fopen(fname)` calls `lexer_open_with_filename()`: This method opens
    the named file mmCIF file for reading. The file can be straight text
    og gzip compressed.
-   `open()` calls `lexer_open_with_fd()`: Pass an open Python file
    descriptor for reading to the module. To be used when Python takes
    responsibiliy for opening and closing the file. NOTE: Opening the
    file this way can *not* handle gzipped files, but can be used if you
    prefer a more "pythonic" programming style.
-   `set_debug_mode()` calls `lexer_set_debug_mode()` Set debug mode
    on (1) or off (0)
-   `fclose()` calls `lexer_close_file()`: Close mmCIF file
-   `get_token()` calls `lexer_get_token()`: Get the next token from
    mmCIF file

## Using the lexer

Here is an example of how you can use the low level lexer. In this
example we are using the `open()` method that is context aware and thus
can be used within a Python `with open()` construct. When opening the
mmCIF file this way, if must be a straight text file.

``` python
from mmcifbuddy import mmciflexer as lex

 with open("data/4af1.cif") as f:
     status = lex.open(f)
     typ, token = lex.get_token()
     while typ != lex.tEND_OF_FILE:
         print(typ, token)
         typ, token = lex.get_token()
```

Just so you can see the difference between using `open()` and `fopen()`,
here is another snippet of code accomplishing a similar thing. Here we
can read a gzipped file, but the code is less "pythonic".

``` python
status = lex.fopen("data/1psr.cif.gz")
typ, token = lex.get_token()
while typ != lex.tEND_OF_FILE:
    print(typ, token)
    typ, token = lex.get_token()
lex.fclose()
```

## The FileReader module

The `FileReader` class described above is actually a simple class
wrapping the lexer.

``` python
from mmcifbuddy.filereader import FileReader

with FileReader('4af1.cif') as fr:
    for s in fr:
        print(s)
```

This will program will read the input mmCIF file and output (type,
token) tuples, the first few lines look like this:

``` example
4, 'data_4AF1')
(12, '#')
(1, '_entry.id')
(8, '4AF1')
(12, '#')
(1, '_audit_conform.dict_name')
(8, 'mmcif_pdbx.dic')
(1, '_audit_conform.dict_version')
(8, 5.308)
...
```

Here, 4 is the mmCIF ID, 12 means "comment", 1 means "a name" and 8
means "data". There are 18 token types recognized by the parser.

## Logger

The `mmcifbuddy` module contains a logger which simply is a
customization of the built-in Python `logging` module. Typically, you
would use the `info()`, `warning()` and `error()` methods:

``` python
from mmcifbuddy.logger import logger

logger.info("This is some info text")
logger.warning("Hey did you expect this?")
logger.error("An error happended!")
```

You can use this logger in your program.

## Timer

The `mmcifbuddy` module also contains a timer, that can be used to time
operations.

-   `start()`: Start a new timer
-   `lap()`: Take a lap time
-   `stop()`: Stop the timer, and report the elapsed time

``` python
from mmcifbuddy.timer import Timer

clock = Timer()  # Instantiate the Timer
myparser = Parser() # Instantiate the parser
myparser.fopen("data/1ttt.cif.gz")
clock.start()  # Start the timer
basedict = myparser.parse()
clock.stop()   # Stop the timer and print elapsed time
data = myparser.get_dict()
myparser.fclose()
print(f"Read {len(data['_atom_site]['id'])} atoms")
2025-02-11 18:04 [INFO] Done parsing ['data_1TTT']
Elapsed time: 0.3418 seconds
Read 14573 atoms
```

Running on my 10 year old laptop the parser is fast, corresponding to \~
0.023 seconds per 1000 atoms.

# Examples

## Example 1 - Reading an mmCIF file

The first line of an mmCIF file always begins with `data_*` which
signals the beginning of a <u>datablock</u>. According to the mmCIF
specification, there can be multiple datablocks in a single file, each
with a unique name.

``` example
data_4XB6
#
_entry.id   4XB6
#
_audit_conform.dict_name       mmcif_pdbx.dic
_audit_conform.dict_version    5.279
...
```

In the first example, let's read an mmCIF file into IPython:

``` python
from mmcifbuddy import Parser
myparser = Parser()
myparser.fopen('data/4af1.cif')
_ = myparser.parse()
2025-02-09 23:03 [INFO] Done parsing ['data_4AF1']
parser.fclose()
print(myparser.get_datablock_names())
['data_4AF1']
print(data['data_4AF1']['_entry']['id'])
4AF1
```

Now the mmCIF file is in memory as an ordinary dictionary, that you can
do with what you want. As mentioned above, the dictionary returned my
the `myparser.parse()` call returns a dictionary containing all
datablocks, but we prefer to fetch the structure information using the
`get_dict()` method, so we put the result into the Python junk
underscore variable " `_`". Then various syntax checkers won't complain
about unused variables.

So we retrieve all the data like this:

``` python
data = myparser.get_dict()
```

and you can list the keys from `data1`:

``` python
print(data.keys())
dict_keys(['_entry', '_audit_conform', '_database_2', '_pdbx_database_status',
'_audit_author', '_citation', '_citation_author', '_cell', '_symmetry',
'_entity', '_entity_poly', '_entity_poly_seq', '_entity_src_nat',
...
...
'_pdbx_validate_chiral', '_ndb_struct_conf_na', '_ndb_struct_na_base_pair',
'_ndb_struct_na_base_pair_step', '_pdbx_entity_nonpoly'])
```

(list truncated)

For example, to see what coordinates are stored in the file:

``` python
print(data['_atom_site'].keys())
dict_keys(['group_PDB', 'id', 'type_symbol', 'label_atom_id',
'label_alt_id', 'label_comp_id', 'label_asym_id', 'label_entity_id',
'label_seq_id', 'pdbx_PDB_ins_code', 'Cartn_x', 'Cartn_y', 'Cartn_z',
'occupancy', 'B_iso_or_equiv', 'pdbx_formal_charge', 'auth_seq_id',
'auth_comp_id', 'auth_asym_id', 'auth_atom_id', 'pdbx_PDB_model_num'])
```

This is in reality the same ATOM data you can find in a legacy [PDB
format
file](http://www.wwpdb.org/documentation/file-format-content/format33/sect9.html#ATOM).
For fun & illustration, lets store the coordinate data in a pickle file:

``` python
import pickle

pdb_id = data['_entry']['id'].lower()
fname =  Path(pdb_id).with_suffix('.pck')
with open(fname, 'wb') as outf:
    pickle.dump(A, outf)
    print(f"Dumped {fname}")
Dumped 1ttt.pck
```

This saves all the coordinate data in a binary Python pickle file, and
because the datastructure is vanilla Python objects, it should be
portable and readably in all future versions. You can load this file
again in e.g. another program like this:

``` python
with open("1ttt.pck", 'rb') as inf:
    X = pickle.load(inf)
```

## Example 2 - Print basic crystallographic data

In the following examples, the structure 4af1 is used. If you follow
along, it's a good idea to copy paste into a Jupyter notebook or to an
IPython session. First we load the data from the mmCIF file as many
times before in the above. We get all the information from the file into
the `data` dictionary.

``` python
path = Path("data/4af1.cif")
myparser = Parser()
myparser.fopen(path)
_ = myparser.parse()
data = myparser.get_dict()
```

Now, lets print some information from the file, and store the title in a
variable:

``` python
print(data['_entry']['id'])
entry_title = data['_entity_name_com']['name'].title()
print(entry_name)
4AF1
Translation Termination Factor Arf1, Release Factor 1
```

Next, print some basic crystallographic information about this
structure:

``` python
print("Unit Cell")
print(f"\ta: {data['_cell']['length_a']}")
print(f"\tb: {data['_cell']['length_b']}")
print(f"\tc: {data['_cell']['length_b']}")
print(f"\talpha: {data['_cell']['angle_alpha']}")
print(f"\tbeta: {data['_cell']['angle_beta']}")
print(f"\tgamma: {data['_cell']['angle_gamma']}")
print(f"\tZ: {data['_cell']['Z_PDB']}")

print("Space Group")
print(f"\tName: {data['_symmetry']['space_group_name_H-M']}")
print(f"\tNumber: {data['_symmetry']['Int_Tables_number']}")
```

giving the following output:

``` example
Unit Cell
    a: 131.02
    b: 31.99
    c: 31.99
    alpha: 90.0
    beta: 113.47
    gamma: 90.0
    Z: 4
Space Group
    Name: C 1 2 1
    Number: 5
```

## Example 3 - Extracting the sequence into a file

Next we will extract the sequence information from the mmCIF file, and
this time we use the flat parser. For fun we also time the operation:

``` python
from mmcifbuddy import ParserFlat
from mmcifbuddy.timer import Timer
stopwatch = Timer()
stopwatch.start()
myparser_f = ParserFlat()
myparser_f.fopen(path)
_ = myparser_f.parse()
data_f = myparser_f.get_dict()
stopwatch.stop()
```

Notice that we store the output from the flat parser in the variable
`data_f` as to not overwrite the nested data. Running the above lines
gives this output:

``` example
2025-02-11 19:10 [INFO] Done parsing ['data_4AF1']
Elapsed time: 0.1771 seconds
```

Now let us look at the sequence data, in the mmCIF file it is stored in
the `_entity_poly` category and the `pdbx_seq_one_letter_code` item.

``` python
pdb_id = data_f['_entry.id']
print(pdb_id)
seq_list = data_f['_entity_poly.pdbx_seq_one_letter_code']
print(seq_list)
```

This gives the output:

``` example
4AF1
['MSEQDEVPSEDRRKYEFRKVIEELKDYEGSGTQLVTIYIPPDKQISDVVAHVTQEHSEASNIKSKQTRTNVQDALTSIKD', 'RLRYYDTFPPDNGMVVFSGAVDSGGGRTDMVTEVLESPPQPIESFRYHCDSAFLTEPLAEMLGDKGLYGLIVLDRRESNV', 'GWLKGKRVQPVKSAESLVPGKQRKGGQSAQRFARLRLEAIDNFYQEVAGMADDLFVPKRHEIDGILVGGPSPTKDEFLDG', 'DYLHHELQDKVLGKFDVSYTDESGLSDLVDAGQAALAEADLMDDKSDMEEFFEELNGGKLATYGFEQTRRNLIMGSVDRL', 'LVSEDLREDVVIYECPNDHEEYETIDRRNTSPEHTCSDCGEEATEVDREDAIDHLMSIADQRGTETHFISTDFEKGEQLL',
'TAFGGYAGILRYSTGV']
```

As you can see, the sequence data is stored in a list of lines of length
80 characters. We can concatenate the data into a single string using
the Python string `join()` method:

``` python
# Join the list into a string
seq = ''.join(data_f['_entity_poly.pdbx_seq_one_letter_code'])
seq_len = len(seq)
print(len(seq))
416
```

Notice that we stored the length of the sequence in the `seq_len`
variable. Now lets store the sequence database ID in a variable, as well
as the name of the organism:

``` python
seq_id = data_f['_struct_ref_seq.pdbx_db_accession']
organism = data_f['_entity_src_gen.pdbx_gene_src_scientific_name']
```

And now we can print the sequence in FASTA format:

``` python
print(f">{seq_id} {seq_len} {entry_name} ({organism.title()})")
for line in seq_list:
    print(line)
```

giving the output:

``` example
>Q9HNF0 416 Translation Termination Factor Arf1, Release Factor 1 (Halobacterium Salinarum)
MSEQDEVPSEDRRKYEFRKVIEELKDYEGSGTQLVTIYIPPDKQISDVVAHVTQEHSEASNIKSKQTRTNVQDALTSIKD
RLRYYDTFPPDNGMVVFSGAVDSGGGRTDMVTEVLESPPQPIESFRYHCDSAFLTEPLAEMLGDKGLYGLIVLDRRESNV
GWLKGKRVQPVKSAESLVPGKQRKGGQSAQRFARLRLEAIDNFYQEVAGMADDLFVPKRHEIDGILVGGPSPTKDEFLDG
DYLHHELQDKVLGKFDVSYTDESGLSDLVDAGQAALAEADLMDDKSDMEEFFEELNGGKLATYGFEQTRRNLIMGSVDRL
LVSEDLREDVVIYECPNDHEEYETIDRRNTSPEHTCSDCGEEATEVDREDAIDHLMSIADQRGTETHFISTDFEKGEQLL
TAFGGYAGILRYSTGV
```

You can of course write this to a file instead of the screen.

## Example 4 - Extract secondary structure

In this example, we will extract the secondary structure information
stored in the mmCIF file. The description of the secondary structure in
an mmCIF file is found in two categories: `_struct_conf` and
`_struct_sheet_range`. You can tell that the mmCIF format has been
written by committee. `struct_conf` stores secondary structure
information of helices and `struct_sheet_range` stores secondary
structure information for beta strands.

To make it simple, we use Pandas:

``` python
import pandas as pd
```

If you don't have Pandas installed, use `pip install pandas` to do so.

### Helices

First, lets try to extract information about helices:

``` python
helices = pd.DataFrame.from_dict(data['_struct_conf'])
helices.head()
```

If you're running this in Jupyter or IPython, the `helices.head()`
statement will give a nicely formatted table. If you're running it in a
script, you must wrap it in a `print` statement. The `helices` dataframe
contains 20 columns, but we will only need some of them. However, we
will add a few columns of our own. From the mmCIF table, we will only
use a few data items:

-   `beg_auth_asym_id`: chain ID, e.g. 'A'

-   `beg_auth_seq_id`: sequence number, e.g. 175

    These are the author defined residue names, which you normally want
    if you are going to be looking at the paper, where the authors
    likely will use this nomenclature. PDB also provides their residue
    numbers, however in this structure they are the same.

``` python
helices['type'] = "alpha"
helices['begin'] =  helices['beg_auth_asym_id'] + helices['beg_auth_seq_id'].astype(str)
helices['end'] =  helices['end_auth_asym_id'] + helices['end_auth_seq_id'].astype(str)
```

What happened here looks strange, but it's really quite simple. First,
we add a column with the word "alpha" in every cell. Next, we combine
the sequence ID (for example "A") with the beginning and end sequence
numbers (for example "123") to generate residue number of the type
"A123". So now, from the data already in the dataframe, we have
generated columns describing the type, and beginning and end residue
names of each helix in the table. Let's print out this info:

``` python
for index, row in helices.iterrows():
    print(row['type'], row['id'], row['begin'], row['end'])
```

giving:

``` example
alpha HELX_P1 A9 A26
alpha HELX_P2 A44 A59
alpha HELX_P3 A60 A62
alpha HELX_P4 A64 A82
alpha HELX_P5 A83 A85
alpha HELX_P6 A192 A216
alpha HELX_P7 A230 A240
alpha HELX_P8 A244 A249
alpha HELX_P9 A263 A272
alpha HELX_P10 A272 A281
alpha HELX_P11 A281 A297
alpha HELX_P12 A304 A314
alpha HELX_P13 A371 A382
alpha HELX_P14 A393 A402
```

### Beta strands

Next, lets extract beta strands. We do it in the same way as with
helices, with slight changes because the beta strand information in the
mmCIF file is a bit different (written by committee). Fortunately most
of the item names are the same:

``` python
strands = pd.DataFrame.from_dict(data['_struct_sheet_range'])
strands.head()
```

Again, we generate a few new columns in the dataframe. We add a column
of "beta", and this time, it's necessary to generate an ID column,
because the strands are named with non-unique integers. So we overwrite
the column `strands['id']` by concatenating the `sheet_id` with the `id`
giving a new column of strings, that overwrites the old `id` column.
Then, we again generate begin/end residue names. Again, we only use a
few columns from the mmCIF table.

``` python
strands['type'] = "beta"
strands['id'] = strands['sheet_id'] + strands['id'].astype(str)
strands['begin'] =  strands['beg_auth_asym_id'] + strands['beg_auth_seq_id'].astype(str)
strands['end'] =  strands['end_auth_asym_id'] + strands['end_auth_seq_id'].astype(str)
```

Let's print out this data:

``` python
for index, row in strands.iterrows():
    print(row['type'], row['id'], row['begin'], row['end'])
```

giving the output:

``` example
beta AA1 A108 A116
beta AA2 A94 A102
beta AA3 A34 A39
beta AA4 A126 A130
beta AB1 A167 A175
beta AB2 A157 A164
beta AB3 A147 A153
beta AB4 A222 A229
beta AB5 A251 A256
beta AC1 A301 A303
beta AC2 A406 A410
beta AC3 A317 A323
beta AC4 A385 A389
beta AD1 A342 A346
beta AD2 A328 A334
beta AD3 A364 A370
```

### Joining the tables

Now, we have to dataframes, `helices` containing information about alpha
helices, and `strands` containing information about beta strands. Let's
join them into a single dataframe `df`:

``` python
df = pd.concat([helices, strands], ignore_index=True)
```

We choose `ignore_index` because the two tables' indeces both start
at 1. Now, we can print the data again like before:

``` python
for index, row in df.sort_values('begin').iterrows():
    print(row['type'],"\t", row['id'], row['begin'], row['end'])
```

this gives a list of alpha and beta segments, sorted in order of their
first residue:

``` example
beta     AA1 A108 A116
beta     AA4 A126 A130
beta     AB3 A147 A153
beta     AB2 A157 A164
beta     AB1 A167 A175
alpha    HELX_P6 A192 A216
beta     AB4 A222 A229
alpha    HELX_P7 A230 A240
alpha    HELX_P8 A244 A249
beta     AB5 A251 A256
alpha    HELX_P9 A263 A272
alpha    HELX_P10 A272 A281
alpha    HELX_P11 A281 A297
beta     AC1 A301 A303
alpha    HELX_P12 A304 A314
beta     AC3 A317 A323
beta     AD2 A328 A334
beta     AA3 A34 A39
beta     AD1 A342 A346
beta     AD3 A364 A370
alpha    HELX_P13 A371 A382
beta     AC4 A385 A389
alpha    HELX_P14 A393 A402
beta     AC2 A406 A410
alpha    HELX_P2 A44 A59
alpha    HELX_P3 A60 A62
alpha    HELX_P4 A64 A82
alpha    HELX_P5 A83 A85
alpha    HELX_P1 A9 A26
beta     AA2 A94 A102
```

Again, if you're using Jupyter for these examples, we can do better,
because Jupyter has a really nice display of dataframes. Let's copy the
data we want into a new dataframe:

``` python
df = df[['type', 'id', 'begin', 'end']].copy()
print(len(df))
30
```

So, there are 30 secondary structural elements, so let's display all 30
in Jupyter (by default `head()` only displays 10):

``` python
df.head(30)
```

## Example 5 - Write a PDB file

The atomic coordinate data is stored in the mmCIF file in the
`atom_site` category, so in this example we will use the nested parser.
We still have the data stored in the `data` variable. We are going to
produce a file with [ATOM
records](https://www.wwpdb.org/documentation/file-format-content/format33/sect9.html#ATOM)
in the legacy PDB format, detailed in the following table:

``` example
COLUMNS        DATA  TYPE    FIELD        DEFINITION
-------------------------------------------------------------------------------------
 1 -  6        Record name   "ATOM  "
 7 - 11        Integer       serial       Atom  serial number.
13 - 16        Atom          name         Atom name.
17             Character     altLoc       Alternate location indicator.
18 - 20        Residue name  resName      Residue name.
22             Character     chainID      Chain identifier.
23 - 26        Integer       resSeq       Residue sequence number.
27             AChar         iCode        Code for insertion of residues.
31 - 38        Real(8.3)     x            Orthogonal coordinates for X in Angstroms.
39 - 46        Real(8.3)     y            Orthogonal coordinates for Y in Angstroms.
47 - 54        Real(8.3)     z            Orthogonal coordinates for Z in Angstroms.
55 - 60        Real(6.2)     occupancy    Occupancy.
61 - 66        Real(6.2)     tempFactor   Temperature  factor.
77 - 78        LString(2)    element      Element symbol, right-justified.
79 - 80        LString(2)    charge       Charge  on the atom.
```

First, we define a Python format string corresponding to the ATOM
record:

``` python
pdb_id = data['_entry.id'].lower()
format_str = "{:<6s}{:5d} {:<4s}{:1s}{:3s} {:1s}{:4d}{:1s}   {:8.3f}{:8.3f}{:8.3f}{:6.2f}{:6.2f}          {:>2s}{:2s}"
# Line measure
print("....+....|....+....|....+....|....+....|....+....|....+....|....+....|....+....")
```

For convienience, store the data we need in a dictionary called `A`:

``` python
A = data['_atom_site']
```

Let's just print out the first 10 atoms in PDB format:

``` python
for i in range(10):
    formatted_value = format_str.format(
        A['group_PDB'][i],
        A['id'][i],
        A['label_atom_id'][i],
        A['label_alt_id'][i],
        A['label_comp_id'][i],
        A['label_asym_id'][i],
        A['label_seq_id'][i],
        A['pdbx_PDB_ins_code'][i],
        A['Cartn_x'][i],
        A['Cartn_y'][i],
        A['Cartn_z'][i],
        A['occupancy'][i],
        A['B_iso_or_equiv'][i],
        A['type_symbol'][i],
        A['pdbx_formal_charge'][i]
    )
    print(formatted_value)
```

This generates the following list. The "ruler" is simply so I could
check if the format was correct, it's not part of the data, but you are
invited to check for yourself.

``` example
....+....|....+....|....+....|....+....|....+....|....+....|....+....|....+....
ATOM      1 N   .VAL A   7?     29.794 -20.534  35.440  1.00105.45           N?
ATOM      2 CA  .VAL A   7?     29.668 -19.426  34.501  1.00104.35           C?
ATOM      3 C   .VAL A   7?     29.115 -19.894  33.156  1.00102.06           C?
ATOM      4 O   .VAL A   7?     29.831 -20.514  32.367  1.00102.63           O?
ATOM      5 CB  .VAL A   7?     31.023 -18.729  34.283  1.00105.81           C?
ATOM      6 CG1 .VAL A   7?     30.867 -17.548  33.340  1.00105.83           C?
ATOM      7 CG2 .VAL A   7?     31.603 -18.281  35.614  1.00106.42           C?
ATOM      8 N   .PRO A   8?     27.833 -19.593  32.892  1.00 98.49           N?
ATOM      9 CA  .PRO A   8?     27.127 -20.014  31.674  1.00 95.06           C?
ATOM     10 C   .PRO A   8?     27.610 -19.305  30.406  1.00 91.15           C?
```

There's still some problems in the output however. FIrst the `altLoc`
column should by blank if there is not alternate location for that atom.
Second, the `iCode` column for inserted residues should be blank except
for inserted residues. Third, the `charge` column (last column) should
be blank except for atoms that have a charge, in which case it's a small
integer, positive or negative. And finally, there's a problem with the
atom name (`name`) column. It has 4 characters available, the first two
is the element, and the last to is the branch. So the C-alpha from an
amino acid is designated '.CA.' and a calcium atom would be named 'CA..'
in that column. As an exercise, you are invited to solve these problems,
as well as write the output to a file.

## Example 6 - Importing data in Polars

If you have Polars installed, typing the following into iPython:

``` python
import polars as pl
df2 = pl.from_dict(data['_atom_site'])
df2.head()
shape: (5, 21)
```

will yield the following output:

``` example
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

## Example 7 - Structure factors

You can read mmCIF structure factor files in exactly the same way we've
been doing above, but of course the categories and items in a structure
factor file is different from a coordinate file. Here is a brief example
how it works

``` python
from mmcifbuddy import Parser
fnam = "data/r4xb6sf.ent.gz"
myparser = Parser()
myparser.fopen(fnam)
_ = myparser.parse()
data = myparser.get_dict()
print(data['_cell'])
print(data[ '_diffrn_radiation_wavelength'])
print(data[ '_symmetry'])
```

This produces the output:

``` example
{'entry_id': '4xb6', 'length_a': 95.51, 'length_b': 133.71, 'length_c': 176.74, 'angle_alpha': 90.0, 'angle_beta': 90.0, 'angle_gamma': 90.0}
{'id': 1, 'wavelength': '.'}
{'entry_id': '4xb6', 'space_group_name_H-M': 'P 21 21 21', 'Int_Tables_number': 19}
```

# Building the package

The source code resides in two directories: `src/`, which contains the
lexer, and `mmcifbuddy`, which contains the parser. The directory
structure of `mmcifbuddy` is shown below.

``` example
.
├── mmcifbuddy/
├── mmcifbuddy/mmciflexer/
├── src/
```

The lexer is written in C and lex. The lex code is found in the file
`src/mmcif.lex`, which requires `flex` to be converted in the C code in
`src/lex.mmcif.c`. This compilation is only required when changes are
made to `mmcif.lex`, in which case it will be generated by
`src/Makefile`, but requires `flex` to be installed on the system. The C
source `src/lex.mmcif.c` is included in the distribution so it is not
normally required.

The job of the lexer is to break down the stream of lines from the mmcif
file into tokens that can be interpreted by the parser. The lexer is
able to read data from mmcif files in text format as well as gzip
compressed.

First, you need to make sure the Python modules `setuptools` and `build`
are available on your computer [^4]. You also need to install a C
compiler, the Python development library and Python virtual environment
modules, that are required for building the Python package. For a Debian
familiy system:

``` shell
sudo apt install python3-setuptools python3-build
sudo apt install build-essential libpython3-dev python3-venv
```

To build the package, run `make` in the parent directory:

``` shell
cd mmcifbuddy-0.6.0
make
```

This will first compile the lexer in `src`, then install the compiled C
extension module in `mmcifbuddy/mmciflexer/` which thus becomes the
lexer module used by the parser. Then, the makefile calls the Python
build module that builds a wheel that will be placed in the directory
`dist/`. The Python build module also creates a directory `build/` which
you can delete.

You can then install the wheel[^5] on your server using `pip`.

``` shell
cd dist
pip install mmcifbuddy-0.6.0-cp312-cp312-linux_x86_64.whl
```

# Author and maintainer

-   Morten Kjeldgaard \<mortenkjeldgaard@gmail.com\>
-   Copyright 2023-2025 Morten Kjeldgaard
-   License: EUPL 1.2

[^1]: The mmCIF format is described
    [here](https://mmcif.wwpdb.org/docs/tutorials/mechanics/pdbx-mmcif-syntax.html)
    in a short and easy to read introduction.

[^2]: However, `mmcifbuddy` does not parse mmCIF dictionary files in the
    current implementation (and probably never will).

[^3]: However, the parser is able to handle more than one `data_`
    section per file if such a situation should ever arise.

[^4]: On Debian family systems install packages `python3-setuptools` and
    `python3-build`, on Arch family systems these packages are
    `python-setuptools` and `python-build`.

[^5]: A wheel is an ordinary zip archive. You can inspect its content
    using `unzip -l`
