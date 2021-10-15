#%%

#%% [markdown]
'''
## Parsed PX meta and data to PX
'''
# %%

def write_px(path, fields, data, encoding="iso-8859-15"):

    with open(path,'w', encoding=encoding) as pdx:
        for key, val in fields.items():
            pdx.write(f"{key}=")
            pdx.write(','.join((f'"{v}"' for v in val)))
            pdx.write(";\n")
        pdx.write("DATA=\n")
        pdx.write('\n'.join((' '.join(row) for row in data)))
        pdx.write(';\n')

#%%

def flatten_mindex(indx):
    '''
    Flattens MultiIndex repetitive level names into level's unique names
    NOTE: If names aren't unique this implementation will break
    '''
    names = [dict() for _ in range(len(indx[0]))]
    for place in indx:
        for i, level in enumerate(place):
            names[i][level] = None
    return [list(n.keys()) for n in names]
    
# %%

def df_to_px(df, fields, px_path, names_from_pd=False):
    '''
    names_from_pd converts axis values and names from Pandas
    it overwrites same in fields dict if there
    '''

    if names_from_pd:
        m_rows, m_cols = df.axes
        
        stub_values = flatten_mindex(m_rows)
        
        heading_values = flatten_mindex(m_cols)

        fields["STUB"] = m_rows.names
        fields["HEADING"] = m_cols.names

        for name, vals in zip(m_rows.names, stub_values):
            fields[f'VALUES("{name}")'] = vals
        
        for name, vals in zip(m_cols.names, heading_values):
            fields[f'VALUES("{name}")'] = vals
        
    #px_data = '\n'.join((' '.join(row) for row in df.values))

    write_px(px_path, fields, df.values)

#%%

def test(source_px_path, target_px_path):
    import px_to_pandas

    df, fields = px_to_pandas.main(source_px_path)

    df_to_px(df, fields, target_px_path, names_from_pd=True)

# %%
test("eka.px", "eka_m.px")
# %%

import px_to_pandas

df, fields = px_to_pandas.main("eka.px")
# %%
m_rows, m_cols = df.axes
# %%
m_cols.tolist()
# %%
flatten_mindex(m_cols)

# %%
m_rows.tolist()
# %%
flm = flatten_mindex(m_rows)
# %%
len(flm[2])
# %%
fields
# %%
m_cols.names

# %%
df.axes
# %%
