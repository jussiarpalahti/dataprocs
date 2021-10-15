#%%

import pyarrow as pa
import pyarrow.feather as feather
import pyarrow.parquet as pq

# %%

def save_to_feather_and_arrow(doc, df):
    table = pa.Table.from_pandas(df)
    p = str(doc).replace('.px', '.feather_zstd')
    p2 = str(doc).replace('.px', '.parquet')
    feather.write_feather(table, p, compression='zstd')
    pq.write_table(table, p2)

# %%
