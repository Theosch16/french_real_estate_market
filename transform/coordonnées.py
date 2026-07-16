import pandas as pd
import time

df=pd.read_csv('loyers.csv')

# On merge avec les données de datagouv.fr

df2=pd.read_csv('communesdefrancev2.csv')
df3=pd.read_csv('departements-france.csv')

df2=df2.merge(df3, left_on="département", right_on="nom_departement")
df2=df2.drop(columns=['code_region','nom_region','Code Insee','Code postal','région','population 2015','population 2021','nom_departement'])

# On récupère le code du département

def clean_dep(code):
    if code.isdigit():
        return str(int(code)).zfill(2)
    return code

df2['code_departement'] = df2['code_departement'].apply(clean_dep)
df2 = df2.rename(columns={'nom commune': 'ville', 'code_departement': 'departement'})
df['departement'] = df['departement'].apply(clean_dep)

# On merge les deux dataframes pour récupérer les coordonnées des communes

df = df.merge(
    df2[['ville', 'departement', 'latitude', 'longitude']],
    on=['ville', 'departement'],
    how='left'
)

df=df.drop_duplicates()

print(df['longitude'].isna().sum())
print(df)
df = df.dropna(subset=['longitude'])

# On garde les coordonnées pour les communes de France dans un csv

df=df[['departement','id_ville','ville','latitude','longitude']]
df = df.drop_duplicates(subset=['ville', 'departement'])
print(df['ville'].nunique())
df.to_csv('loyer_coordinates.csv', index=False)