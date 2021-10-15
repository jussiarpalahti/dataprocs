#%%

import pandas as pd
from itertools import zip_longest
import re
from operator import mul
from functools import reduce
import pandas as pd
from pandas.core.indexes.multi import MultiIndex

#%%

def open_px(PATH:str, encoding:str="iso-8859-15"):

    meta, data = open(PATH, encoding=encoding).read().split("\nDATA=")

    # take away the ending semicolon
    data = data.strip()
    if data[-1] == ";": data = data[:-1]

    return meta, data


# %%

def grouper(n, iterable, fillvalue=None):
    """
    Collect data into fixed-length chunks or blocks
    Lifted from itertools module's examples
    """
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

# %%

def get_sub_items(value:str):
    '''
    Essentially everything inside quotation marks
    '''
    return re.findall(r'"(.*?)"', value)

def parse_meta(meta):
    
    # TODO: Parse sub fields from all field dict's keys

    # Parse PX meta using regexp of roughly:
    #  FIELDNAME[POSSIBLE_LANG](POSSIBLE_VALUE)
    #  =
    #  "things between quotes"
    #  ending with semicolon + and a new line
    fields = {key:get_sub_items(val) for key, val in re.findall(
        r'^(.*?)=("[\s\S]*?");$', meta, re.MULTILINE)}
    
    # same as above but specifically FIELDNAME[OPTIONAL_LANG]("something")
    sub_fields = re.findall(r'^(.*?)\("(.*?)"\)=("[\s\S]*?");$', meta, re.MULTILINE)
    #
    values = {key:get_sub_items(val) for t, key, val in sub_fields if t == "VALUES"}
    
    # names in stub and heading
    rows = [values[key] for key in fields["STUB"]]
    cols = [values[key] for key in fields["HEADING"]]

    n_cols = reduce(mul, [len(i) for i in cols], 1)
    n_rows = reduce(mul, [len(i) for i in rows], 1)
    
    return fields, rows, cols, n_rows, n_cols

# %%

def create_pd(fields, rows, cols, cols_size, data):

    # parse PX data into list of column amount sized lists
    matrix = list(grouper(cols_size, data.replace('"', "").strip().split()))
    
    # MultiIndex from cartesian product of column and row name lists
    stub = pd.MultiIndex.from_product(rows, names=fields["STUB"])
    heading = pd.MultiIndex.from_product(cols, names=fields["HEADING"])
    
    df = pd.DataFrame(matrix, index=stub, columns=heading)

    return df
#%%


def main(path):
    meta, data = open_px(path)

    fields, rows, cols, n_rows, n_cols = parse_meta(meta)

    df = create_pd(fields, rows, cols, n_cols, data)

    return df, fields

# # %%
# df, fields = main("eka.px")
# # %%

# meta, data = open_px("eka.px")
# fields, rows, cols, n_rows, n_cols = parse_meta(meta)
# df = create_pd(fields, rows, cols, n_cols, data)
# # %%
# len(rows[2])
# # %%
# m_rows, m_cols = df.axes
# # %%
# m_cols.nunique()
# # %%
# m:MultiIndex = MultiIndex.from_product([['a','b','a','b','a'],['1', '2', '3']])
# import numpy as np
# df2 = pd.DataFrame(data=np.random.randn(15, 3), index=m)
# df2
# # %%
# df2.loc["a"]
# # %%

