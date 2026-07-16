import pandas as pd
import streamlit as st
import pydeck as pdk
import altair as alt

st.set_page_config(layout="wide")

st.title("Le marché de l'immobilier français")

col_title_1, col_title_2 = st.columns(2)

def loyer_to_color(loyer):
    ratio = (loyer - loyer_min) / (loyer_max - loyer_min)
    ratio = max(0, min(1, ratio))

    return [int(255 * ratio), 100, 50, 200]

df=pd.read_csv("transform/loyer_final.csv", index_col=False)

with st.sidebar:
    st.header("Choix des paramètres", divider="red")

    a=df["departement"].unique()

    option = st.selectbox(
        "Choix du département",
        (sorted(a)),
        index=None,
        placeholder="Choisissez un département",
    )

    b=df.loc[df['departement'] == option]
    b=b['ville'].dropna().unique()

    commune = st.selectbox(
        "Choix de la commune",
        b,
        index=None,
        placeholder="Choisissez une commune",
        accept_new_options=False,
    )
    annees_disponibles = [2018, 2022, 2023, 2024, 2025]


    annee = st.select_slider(
        "Choix de la période",
        options=annees_disponibles,
        value=(2018, 2025)
    )
    confirmed = st.button("Confirmer les paramètres")

# On applique les filtres
df_filtre = df.copy()

if not confirmed:
    st.subheader("Bienvenue", divider="red")
    st.write("Veuillez sélectionner les paramètres dans la barre latérale pour afficher les résultats. Cliquez sur la flèche en haut à gauche pour ouvrir la barre latérale si elle n'est pas visible.")
        
    st.subheader("Fonctionnement", divider="red")
    st.write("Vous pouvez choisir un département, une commune et une période pour visualiser l'évolution du marché immobilier et établir des comparatifs entre différentes zones géographiques.")
    st.write("Si vous souhaitez afficher les résultats sur la France entière, appuyez sur le bouton 'Confirmer les paramètres' sans sélectionner de département ni de commune.")

if confirmed:
    # Graphiques des loyers des communes et départements
    if option is not None:
        df_filtre = df_filtre[df_filtre["departement"] == option]
        with col_title_1:
            st.subheader(f"Évolution du marché immobilier", divider="gray")
    
    col1, col2 = st.columns(2)
    df_filtre = df_filtre[(df_filtre["date"] >= annee[0]) & (df_filtre["date"] <= annee[1])]
    df_filtred = df_filtre[(df_filtre["date"] >= annee[0]) & (df_filtre["date"] <= annee[1])]
    
    data = df_filtre
    data["loyer_m2_maison"] = data["loyer_m2_maison"].round(2)
    data["loyer_m2_appartement"] = data["loyer_m2_appartement"].round(2)

    with col1:
        if option is not None:
                st.subheader(f"Pour le département - {df_filtre["nom_departement"].iloc[0]}", divider="red")
                df_filtred = df_filtred[df_filtred["departement"] == option]
                df_total_commune=df_filtred["ville"].drop_duplicates()
                df_filtred = df_filtred.groupby("date")["loyer_m2_maison"].mean().reset_index()
                st.line_chart(df_filtred, x="date", y="loyer_m2_maison", x_label="Date",y_label="Coût du m² maison")

                first_year=df_filtred['loyer_m2_maison'].loc[(df_filtred["date"] == annee[0])]
                first_year = first_year.values[0]

                second_year=df_filtred['loyer_m2_maison'].loc[(df_filtred["date"] == annee[1])]
                second_year = second_year.values[0]

                calcul=((second_year-first_year)/first_year)*100
                calcul = round(calcul, 2)

                if calcul<0:
                    evolution="baissé"
                else:
                    evolution="augmenté"
                
                moyenne_loyer=df_filtred["loyer_m2_maison"].mean()
                moyenne_loyer = round(moyenne_loyer, 3)

                st.write(f""" 
                         - Les prix ont {evolution} de **{calcul}%** entre {annee[0]} et {annee[1]}.  
                         - Sur {len(df_total_commune)} communes analysées dans ce département, la moyenne du m² pour une maison dans cette période est de **{moyenne_loyer} €**.
                         """)

    with col2:
        if commune is not None:
                st.subheader(f"Pour la commune - {commune}", divider="red")
                df_filtre = df_filtre[df_filtre["departement"] == option]
                df_filtre = df_filtre[df_filtre["ville"] == commune]
                
                
                st.line_chart(df_filtre, x="date", y="loyer_m2_maison", x_label="Date",y_label="Coût du m² maison")

                first_year=df_filtre['loyer_m2_maison'].loc[(df_filtre["date"] == annee[0])]
                first_year = first_year.values[0]

                second_year=df_filtre['loyer_m2_maison'].loc[(df_filtre["date"] == annee[1])]
                second_year = second_year.values[0]

                calcul=((second_year-first_year)/first_year)*100
                calcul = round(calcul, 2)

                if calcul<0:
                    evolution="baissé"
                else:
                    evolution="augmenté"
                moyenne_loyer=df_filtre["loyer_m2_maison"].mean()
                moyenne_loyer = round(moyenne_loyer, 3)
                st.write(f"""
                        - Les prix ont {evolution} de **{calcul}%** entre {annee[0]} et {annee[1]}.  
                        - La moyenne du m² pour une maison dans cette période est de **{moyenne_loyer} €**.
                        """)
    
    # Statistiques des villes
    if option is not None:
        df_filtre = df_filtre[df_filtre["departement"] == option]

        col_town_1, col_town_2 = st.columns(2)
        with col_town_1:
            st.subheader(f"Statistiques des villes - {df_filtre["nom_departement"].iloc[0]}", divider="gray")

        col_town_1, col_town_2 = st.columns(2)
        top_villes = (
        df[df["departement"] == option].groupby("ville")["loyer_m2_maison"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
        top_villes = top_villes.rename(columns={"loyer_m2_maison": "Moyenne du m²", "ville": "Ville"})

        with col_town_1:
            st.subheader(f"Les villes les plus chères", divider="red")
            top_villes.index = range(1, len(top_villes) + 1)
            st.dataframe(top_villes)


        
        top_villes = (
        df[df["departement"] == option].groupby("ville")["loyer_m2_maison"]
        .mean()
        .sort_values(ascending=True)
        .head(10)
        .reset_index()
        )

        top_villes = top_villes.rename(columns={"loyer_m2_maison": "Moyenne du m²", "ville": "Ville"})

        with col_town_2:
            st.subheader(f"Les villes les moins chères", divider="red")
            top_villes.index = range(1, len(top_villes) + 1)
            st.dataframe(top_villes)
    
    
    if option is None:
        col_town_1, col_town_2 = st.columns(2)
        with col_town_1:
            st.subheader(f"Statistiques des villes", divider="gray")

        col_town_1, col_town_2 = st.columns(2)
        top_villes = (
             df.groupby(["departement", "ville"])["loyer_m2_maison"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        top_villes = top_villes.rename(columns={"loyer_m2_maison": "Moyenne du m²", "ville": "Ville", "departement": "Département"})

        with col_town_1:
            st.subheader(f"Les villes les plus chères", divider="red")
            top_villes.index = range(1, len(top_villes) + 1)
            st.dataframe(top_villes)

        top_villes = (
             df.groupby(["departement", "ville"])["loyer_m2_maison"]
            .mean()
            .sort_values(ascending=True)
            .head(10)
            .reset_index()
        )

        top_villes = top_villes.rename(columns={"loyer_m2_maison": "Moyenne du m²", "ville": "Ville", "departement": "Département"})

        with col_town_2:
            st.subheader(f"Les villes les moins chères", divider="red")
            top_villes.index = range(1, len(top_villes) + 1)
            st.dataframe(top_villes)

    st.subheader(f"Carte du marché immobilier", divider="red")

    # On normalise le loyer pour avoir des couleurs entre 0 et 255
    loyer_min = df_filtre["loyer_m2_maison"].quantile(0.00)  # 5e percentile
    loyer_max = df_filtre["loyer_m2_maison"].quantile(0.95)  # 95e percentile


    df_filtre["color"] = df_filtre["loyer_m2_maison"].apply(loyer_to_color)

    df_filtre_departement = df[df["departement"] == option].copy()

    df_filtre_departement["color_departement"] = (
        df_filtre_departement["loyer_m2_maison"]
        .apply(loyer_to_color)
    )

    layer = pdk.Layer(
                "ScatterplotLayer",
                data=df_filtre,
                get_position=["longitude", "latitude"],
                get_radius=500,
                get_fill_color="color",
                pickable=True
            )


    if commune is not None:
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_filtre_departement,
            get_position=["longitude", "latitude"],
            get_radius=500,
            get_fill_color="color_departement",
            pickable=True
        )

        view_state = pdk.ViewState(
            latitude=df_filtre["latitude"].mean(),
            longitude=df_filtre["longitude"].mean(),
            zoom=12
        )
    elif option is not None:
        view_state = pdk.ViewState(
            latitude=data["latitude"].mean(),
            longitude=data["longitude"].mean(),
            zoom=8
        )
    else :
        view_state = pdk.ViewState(
            latitude=data["latitude"].mean(),
            longitude=data["longitude"].mean(),
            zoom=4
        )

    tooltip = {
        "html": "<b>Ville :</b> {ville} <br/> <b>Maison m² :</b> {loyer_m2_maison} €<br/> <b>Appartement m² :</b> {loyer_m2_appartement} €<br/> <b>Date :</b> {date} ",
        "style": {"backgroundColor": "white", "color": "black"}
    }

    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="road"
    ))

st.subheader("Informations importantes", divider="red")

st.write("Les données présentées dans cette application sont basées sur les informations disponibles sur le portail data.gouv.fr, les données sont disponibles sous licence ouverte. Il est important de noter que **certaines communes peuvent ne pas être représentées en raison de la fusion ou de la disparition de certaines d'entre elles**. De plus, les données pour **les années 2019, 2020 et 2021 sont manquantes**, ce qui peut affecter l'analyse des tendances sur ces périodes.")

st.subheader("Sources", divider="red")

st.write("""
 **'Carte des loyers' - Indicateurs de loyers d'annonce par commune en 2018**: https://www.data.gouv.fr/datasets/carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune-en-2018  
**'Carte des loyers' - Indicateurs de loyers d'annonce par commune en 2022** : https://www.data.gouv.fr/datasets/carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune-en-2022  
**'Carte des loyers' - Indicateurs de loyers d'annonce par commune en 2023** : https://www.data.gouv.fr/datasets/carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune-en-2023  
**'Carte des loyers' - Indicateurs de loyers d'annonce par commune en 2024** : https://www.data.gouv.fr/datasets/carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune-en-2024  
**'Carte des loyers' - Indicateurs de loyers d'annonce par commune en 2025** : https://www.data.gouv.fr/datasets/carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune-en-2025         
""")

st.write("")
st.write("")

col1, col2, col3 = st.columns(3)
with col1:
    st.caption("© 2026 Projet réalisé par Théo SCHMITT")
with col2:
    st.caption("Github : https://github.com/Theosch16")
with col3:
    st.caption("LinkedIn : https://www.linkedin.com/in/th%C3%A9o-schmitt-507b57220/")