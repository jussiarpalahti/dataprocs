#%%

from px_to_pandas import main

import os
import pathlib
from rich import inspect
from rich import pretty

pretty.install()

from rich.console import Console
from rich.table import Table

console = Console()

#%%

root = pathlib.Path(os.environ.get("PX_ROOT_PATH", "."))
# %%

px_files = list(root.rglob("*.px"))
# %%

df, fields = main(px_files[0])
# %%

df_docs = [main(i)[0] for i in px_files]

# %%


def get_df_ends(df):
    return df.head(1).iloc[0][0], df.tail(1).iloc[-1][-1]


# %%


def get_px_ends(doc: pathlib.Path):
    txt = doc.read_text(encoding="iso-8859-15")
    _, data = txt.strip().split("DATA=")
    vals = data.split(" ")
    return vals[0].strip().replace('"', ""), vals[-1].replace(";", "").replace('"', "")


#%%

table = Table(title="Px to Pandas")
table.add_column("Name", justify="right", style="sea_green1", no_wrap=True)
table.add_column(
    "DataFrame first and last", justify="right", style="green1", no_wrap=True
)
table.add_column("PX data first and last", style="green1")
table.add_column("Same", justify="right", style="white")

for doc, df in zip(px_files, df_docs):
    df_ends, px_ends = get_df_ends(df), get_px_ends(doc)
    table.add_row(
        f"{doc.name}", f"{df_ends}", f"{px_ends}", "✓" if df_ends == px_ends else "𐄂"
    )

console.print(table)
