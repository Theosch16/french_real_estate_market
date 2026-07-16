import pandas as pd

# Pour 2018

df_app=pd.read_csv("2018_app.csv", encoding='latin-1', sep=";")

print(df_app.dtypes)
df_app["loypredm2"] = df_app["loypredm2"].str.replace(',', '.').astype(float)
# df_app.to_csv("2018_app_modified.csv", encoding='utf-8', index=False)

df_maison=pd.read_csv("2018_maison.csv", encoding='latin-1', sep=";")

df_maison["loypredm2"] = df_maison["loypredm2"].str.replace(',', '.').astype(float)
# df_maison.to_csv("2018_maison_modified.csv", encoding='utf-8', index=False)

df_app=df_app.drop(columns=['NBobs_maille','NBobs_commune','R2adj','TYPPRED','lwr.IPm2','upr.IPm2', 'REG', 'EPCI', 'id_zone'])
df_app=df_app.rename(columns={"loypredm2": "loyer_m2_appartement"})
print(df_app.columns)

df_maison=df_maison.drop(columns=['Nbobs_maille','NBobs_commune','R2adj','TYPPRED','lwr.IPm2','upr.IPm2', 'REG', 'EPCI', 'id_zone'])
df_maison=df_maison.rename(columns={"loypredm2": "loyer_m2_maison"})
print(df_maison.columns)
print(df_maison)

def clean_dep(code):
    if code.isdigit():
        return str(int(code)).zfill(2)
    return code

df_merged=df_app.merge(df_maison, how='inner', on=['INSEE', 'LIBGEO', 'DEP'])
df_merged['date']=2018

df_merged['DEP'] = df_merged['DEP'].apply(clean_dep)

df_merged=df_merged.rename(columns={"LIBGEO":"ville", "DEP":"departement", "INSEE":"INSEE_C"})
df_merged=df_merged.drop_duplicates()
print(df_merged.nunique())

df_coordinates=pd.read_csv("loyer_coordinates.csv")
df_merged_2018=df_merged.merge(df_coordinates, how='inner', on=['ville','departement'])
print(df_merged_2018)

# Pour 2022

df_app=pd.read_csv("2022_app.csv", encoding='latin-1', sep=";")

print(df_app.dtypes)
df_app["loypredm2"] = df_app["loypredm2"].str.replace(',', '.').astype(float)
# df_app.to_csv("2022_app_modified.csv", encoding='utf-8', index=False)

df_maison=pd.read_csv("2022_maison.csv", encoding='latin-1', sep=";")

df_maison["loypredm2"] = df_maison["loypredm2"].str.replace(',', '.').astype(float)
# df_maison.to_csv("2022_maison_modified.csv", encoding='utf-8', index=False)

df_app=df_app.drop(columns=['nbobs_mail','nbobs_com','R2_adj','TYPPRED','lwr.IPm2','upr.IPm2', 'REG', 'EPCI', 'id_zone'])
df_app=df_app.rename(columns={"loypredm2": "loyer_m2_appartement"})
print(df_app.columns)

df_maison=df_maison.drop(columns=['nbobs_mail','nbobs_com','R2_adj','TYPPRED','lwr.IPm2','upr.IPm2', 'REG', 'EPCI', 'id_zone'])
df_maison=df_maison.rename(columns={"loypredm2": "loyer_m2_maison"})
print(df_maison.columns)
print(df_maison)

df_merged=df_app.merge(df_maison, how='inner', on=['INSEE_C', 'LIBGEO', 'DEP'])
df_merged['date']=2022
df_merged=df_merged.rename(columns={"LIBGEO":"ville", "DEP":"departement"})
df_merged=df_merged.drop_duplicates()
print(df_merged.nunique())

df_coordinates=pd.read_csv("loyer_coordinates.csv")
df_merged_2022=df_merged.merge(df_coordinates, how='inner', on=['ville','departement'])
print(df_merged_2022)

# Pour l'année 2023

df_app=pd.read_csv("2023_app.csv", encoding='latin-1', sep=";")

print(df_app.dtypes)
df_app["loypredm2"] = df_app["loypredm2"].str.replace(',', '.').astype(float)
# df_app.to_csv("2023_app_modified.csv", encoding='utf-8', index=False)

df_maison=pd.read_csv("2023_maison.csv", encoding='latin-1', sep=";")

df_maison["loypredm2"] = df_maison["loypredm2"].str.replace(',', '.').astype(float)
# df_maison.to_csv("2023_maison_modified.csv", encoding='utf-8', index=False)

df_app=df_app.drop(columns=['nbobs_mail','nbobs_com','R2_adj','TYPPRED','lwr.IPm2','upr.IPm2', 'REG', 'EPCI', 'id_zone'])
df_app=df_app.rename(columns={"loypredm2": "loyer_m2_appartement"})
print(df_app.columns)

df_coordinates=pd.read_csv("loyer_coordinates.csv")
df_maison=df_maison.drop(columns=['nbobs_mail','nbobs_com','R2_adj','TYPPRED','lwr.IPm2','upr.IPm2', 'REG', 'EPCI', 'id_zone'])
df_maison=df_maison.rename(columns={"loypredm2": "loyer_m2_maison"})
print(df_maison.columns)
print(df_maison)

df_merged=df_app.merge(df_maison, how='inner', on=['INSEE_C', 'LIBGEO', 'DEP'])
df_merged['date']=2023
df_merged=df_merged.rename(columns={"LIBGEO":"ville", "DEP":"departement"})
df_merged=df_merged.drop_duplicates()
print(df_merged.nunique())

df_coordinates=pd.read_csv("loyer_coordinates.csv")
df_merged_2023=df_merged.merge(df_coordinates, how='inner', on=['ville','departement'])
print(df_merged_2023)

# Pour l'année 2024

df_app=pd.read_csv("2024_app.csv", encoding='latin-1', sep=";")

print(df_app.dtypes)
df_app["loypredm2"] = df_app["loypredm2"].str.replace(',', '.').astype(float)
# df_app.to_csv("2024_app_modified.csv", encoding='utf-8', index=False)

df_maison=pd.read_csv("2024_maison.csv", encoding='latin-1', sep=";")

df_maison["loypredm2"] = df_maison["loypredm2"].str.replace(',', '.').astype(float)
# df_maison.to_csv("2024_maison_modified.csv", encoding='utf-8', index=False)

df_app=df_app.drop(columns=['nbobs_mail','nbobs_com','R2_adj','TYPPRED','lwr.IPm2','upr.IPm2', 'REG', 'EPCI', 'id_zone'])
df_app=df_app.rename(columns={"loypredm2": "loyer_m2_appartement"})
print(df_app.columns)

df_maison=df_maison.drop(columns=['nbobs_mail','nbobs_com','R2_adj','TYPPRED','lwr.IPm2','upr.IPm2', 'REG', 'EPCI', 'id_zone'])
df_maison=df_maison.rename(columns={"loypredm2": "loyer_m2_maison"})
print(df_maison.columns)
print(df_maison)

df_merged=df_app.merge(df_maison, how='inner', on=['INSEE_C', 'LIBGEO', 'DEP'])
df_merged['date']=2024
df_merged=df_merged.rename(columns={"LIBGEO":"ville", "DEP":"departement"})
df_merged=df_merged.drop_duplicates()
print(df_merged.nunique())

df_coordinates=pd.read_csv("loyer_coordinates.csv")
df_merged_2024=df_merged.merge(df_coordinates, how='inner', on=['ville','departement'])
print(df_merged_2024)

# Pour 2025

df_app=pd.read_csv("2025_app.csv", encoding='latin-1', sep=";")

print(df_app.dtypes)
df_app["loypredm2"] = df_app["loypredm2"].str.replace(',', '.').astype(float)
# df_app.to_csv("2025_app_modified.csv", encoding='utf-8', index=False)

df_maison=pd.read_csv("2025_maison.csv", encoding='latin-1', sep=";")

df_maison["loypredm2"] = df_maison["loypredm2"].str.replace(',', '.').astype(float)
# df_maison.to_csv("2025_maison_modified.csv", encoding='utf-8', index=False)

df_app=df_app.drop(columns=['nbobs_mail','nbobs_com','R2_adj','TYPPRED','lwr.IPm2','upr.IPm2', 'REG', 'EPCI', 'id_zone'])
df_app=df_app.rename(columns={"loypredm2": "loyer_m2_appartement"})
print(df_app.columns)

df_maison=df_maison.drop(columns=['nbobs_mail','nbobs_com','R2_adj','TYPPRED','lwr.IPm2','upr.IPm2', 'REG', 'EPCI', 'id_zone'])
df_maison=df_maison.rename(columns={"loypredm2": "loyer_m2_maison"})
print(df_maison.columns)
print(df_maison)

df_merged=df_app.merge(df_maison, how='inner', on=['INSEE_C', 'LIBGEO', 'DEP'])
df_merged['date']=2025
df_merged=df_merged.rename(columns={"LIBGEO":"ville", "DEP":"departement"})
df_merged=df_merged.drop_duplicates()
print(df_merged.nunique())

df_coordinates=pd.read_csv("loyer_coordinates.csv")
df_merged_2025=df_merged.merge(df_coordinates, how='inner', on=['ville','departement'])
print(df_merged_2025)

df_merged=pd.concat([df_merged_2018, df_merged_2022,df_merged_2023, df_merged_2024, df_merged_2025])
df_merged=df_merged[['departement','id_ville','ville','date','loyer_m2_appartement','loyer_m2_maison','latitude','longitude','INSEE_C']]
df_merged = df_merged.drop_duplicates()
df_merged.to_csv('loyer_merged.csv', index=False)
print(df_merged)

# On ajoute les départements

df_app=pd.read_csv("loyer_merged.csv", encoding="utf-8", sep=",")
df_departement=pd.read_csv("departements-france.csv", encoding="utf-8", sep=",")
df_departement=df_departement.rename(columns={"code_departement":"departement"})

df_app=df_app.merge(df_departement[['departement','nom_departement']], how='inner', on=['departement'])
df_app = df_app.drop_duplicates()

df_app["date"] = df_app["date"].astype(str)
print(df_app["date"].dtype)
print(df_app["date"].unique())
df_app.to_csv('loyer_final.csv', index=False)
print(df_app)