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
    st.header("Analyser", divider="red")
    departement_select=df["departement"].unique()

    option = st.selectbox(
        "Choix du département",
        (sorted(departement_select)),
        index=None,
        placeholder="Choisissez un département",
    )

    commune_select=df.loc[df['departement'] == option]
    commune_select=commune_select['ville'].dropna().unique()

    commune = st.selectbox(
        "Choix de la commune",
        commune_select,
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

    type_de_bien = st.radio(
        "Choix du type de bien",
        ("Maison", "Appartement"),
        index=0,
        horizontal=True
    )

    bien="loyer_m2_maison" if type_de_bien == "Maison" else "loyer_m2_appartement"
    nom_bien="maison" if type_de_bien == "Maison" else "appartement"
    genre_bien="une" if type_de_bien == "Maison" else "un"

    confirmed = st.button("Confirmer les paramètres")
    st.write("****")

with st.sidebar:
    st.header("Comparer", divider="red")
    list_departement=df["departement"].unique()

    first_option = st.selectbox(
        "Choix du premier département",
        (sorted(list_departement)),
        index=None,
        placeholder="Choisissez un département",
    )
    second_option = st.selectbox(
        "Choix du deuxième département",
        (sorted(list_departement)),
        index=None,
        placeholder="Choisissez un département",
    )

    confirmed_comparaison = st.button("Faire le comparatif")

# On applique les filtres
df_national = df.copy()

if not confirmed and not confirmed_comparaison:
    st.subheader("Bienvenue", divider="red")
    st.write("Veuillez sélectionner les paramètres dans la barre latérale pour afficher les résultats. Cliquez sur la flèche en haut à gauche pour ouvrir la barre latérale si elle n'est pas visible.")
        
    st.subheader("Fonctionnement", divider="red")
    st.write("Vous pouvez choisir un département, une commune et une période pour visualiser l'évolution du marché immobilier.")
    st.write("Si vous souhaitez afficher les résultats sur la France entière, appuyez sur le bouton 'Confirmer les paramètres' sans sélectionner de département ni de commune.")
    st.write("Vous pouvez également établir des comparatifs entre différentes zones géographiques.")

if confirmed:

    df_national = df_national[(df_national["date"] >= annee[0]) & (df_national["date"] <= annee[1])]
    df_filtred = df_national[(df_national["date"] >= annee[0]) & (df_national["date"] <= annee[1])]
    
    # Graphiques des loyers des communes et départements
    
    if option is not None:
        df_departement = df_national[df_national["departement"] == option]
        with col_title_1:
            st.subheader(f"Évolution du marché immobilier", divider="gray")
    if commune is not None:
        df_commune = df_national[df_national["ville"] == commune]
    
    col1, col2 = st.columns(2)
    
    data = df_national.copy()
    data["loyer_m2_maison"] = data["loyer_m2_maison"].round(2)
    data["loyer_m2_appartement"] = data["loyer_m2_appartement"].round(2)

    with col1:
        if option is not None:
                st.subheader(f"Pour le département - {df_departement['nom_departement'].iloc[0]}", divider="red")
                df_total_commune=df_departement["ville"].drop_duplicates()
                df_departement_groupby = df_departement.groupby("date")[bien].mean().reset_index()
                
                st.line_chart(df_departement_groupby, x="date", y=bien, x_label="Date",y_label=f"Coût du m² {nom_bien}")

                first_year=df_departement_groupby[bien].loc[(df_departement_groupby["date"] == annee[0])]
                first_year = first_year.values[0]

                second_year=df_departement_groupby[bien].loc[(df_departement_groupby["date"] == annee[1])]
                second_year = second_year.values[0]

                calcul=((second_year-first_year)/first_year)*100
                calcul = round(calcul, 2)

                difference_maison_appartement = df_departement["loyer_m2_maison"].mean() - df_departement["loyer_m2_appartement"].mean()
                difference_maison_appartement = round((difference_maison_appartement), 2)
                
                if difference_maison_appartement > 0:
                    comparaison = "Maison plus chère"
                    arrow_comparaison = "up"
                    arrow_color="normal"
                else:
                    comparaison = "Maison moins chère"
                    arrow_comparaison = "down"
                    arrow_color="inverse"          

                if calcul<0:
                    evolution="Baisse"
                    arrow="down"
                    calcul_color="inverse"
                else:
                    evolution="Hausse"
                    arrow="up"
                    calcul_color="normal"
                
                moyenne_loyer=df_departement_groupby[bien].mean()
                moyenne_loyer = round(moyenne_loyer, 3)
                
                st.write(f""" 
                         **Bilan sur {len(df_total_commune)} communes analysées dans ce département entre {annee[0]} et {annee[1]}**
                         """)
                col_metric_1,col_metric_2,col_metric_3 = st.columns(3)
                with col_metric_1:
                    st.metric(
                        f"Évolution du prix",
                        f"{calcul}%",
                        delta=f"{evolution} de {calcul}%",
                        delta_arrow=arrow,
                        delta_color=calcul_color
                    )
                with col_metric_2:
                    st.metric(
                        "Écart maison/appartement",
                        f"{abs(difference_maison_appartement)}€/m²",
                        delta=f"{comparaison} de {abs(difference_maison_appartement)}€",
                        delta_arrow=arrow_comparaison,
                        delta_color=arrow_color
                    )
                with col_metric_3:
                    st.metric(
                        f"Moyenne du m²",
                        f"{moyenne_loyer}€",
                    )

    with col2:
        if commune is not None:
                st.subheader(f"Pour la commune - {commune}", divider="red")
                
                st.line_chart(df_commune, x="date", y=bien, x_label="Date",y_label=f"Coût du m² {nom_bien}")

                first_year=df_commune[bien].loc[(df_commune["date"] == annee[0])]
                first_year = first_year.values[0]

                second_year=df_commune[bien].loc[(df_commune["date"] == annee[1])]
                second_year = second_year.values[0]

                calcul=((second_year-first_year)/first_year)*100
                calcul = round(calcul, 2)

                difference_maison_appartement = df_commune["loyer_m2_maison"].mean() - df_commune["loyer_m2_appartement"].mean()
                difference_maison_appartement = round((difference_maison_appartement), 2)
                if difference_maison_appartement > 0:
                    comparaison = "Maison plus chère"
                    arrow_comparaison = "up"
                    arrow_color="normal"
                else:
                    comparaison = "Maison moins chère"
                    arrow_comparaison = "down"
                    arrow_color="inverse"          

                if calcul<0:
                    evolution="Baisse"
                    arrow="down"
                    calcul_color="inverse"
                else:
                    evolution="Hausse"
                    arrow="up"
                    calcul_color="normal"

                moyenne_loyer=df_commune[bien].mean()
                moyenne_loyer = round(moyenne_loyer, 3)

                st.write(f""" 
                        **Bilan sur la commune entre {annee[0]} et {annee[1]}**
                         """)
                col_metric_1,col_metric_2,col_metric_3 = st.columns(3)
                with col_metric_1:
                    st.metric(
                        f"Évolution du prix",
                        f"{abs(calcul)}%",
                        delta=f"{evolution} de {abs(calcul)}%",
                        delta_arrow=arrow,
                        delta_color=calcul_color
                    )
                with col_metric_2:
                    st.metric(
                        "Écart maison/appartement",
                        f"{abs(difference_maison_appartement)}€/m²",
                        delta=f"{comparaison} de {abs(difference_maison_appartement)}€",
                        delta_arrow=arrow_comparaison,
                        delta_color=arrow_color

                    )

                with col_metric_3:
                    st.metric(
                        f"Moyenne du m²",
                        f"{moyenne_loyer}€",
                    )
    
    # Statistiques des villes
    if option is not None:

        col_town_1, col_town_2 = st.columns(2)
        with col_town_1:
            st.subheader(f"Statistiques des villes - {df_departement["nom_departement"].iloc[0]}", divider="gray")

        col_town_1, col_town_2 = st.columns(2)
        top_villes = (
        df[df["departement"] == option].groupby("ville")[bien]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
        top_villes = top_villes.rename(columns={bien: "Moyenne du m²", "ville": "Ville"})

        with col_town_1:
            st.subheader(f"Les villes les plus chères", divider="red")
            top_villes.index = range(1, len(top_villes) + 1)
            st.dataframe(top_villes)
        
        top_villes = (
        df[df["departement"] == option].groupby("ville")[bien]
        .mean()
        .sort_values(ascending=True)
        .head(10)
        .reset_index()
        )

        top_villes = top_villes.rename(columns={bien: "Moyenne du m²", "ville": "Ville"})

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
             df.groupby(["departement", "ville"])[bien]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        top_villes = top_villes.rename(columns={bien: "Moyenne du m²", "ville": "Ville", "departement": "Département"})

        with col_town_1:
            st.subheader(f"Les villes les plus chères", divider="red")
            top_villes.index = range(1, len(top_villes) + 1)
            st.dataframe(top_villes)

        top_villes = (
             df.groupby(["departement", "ville"])[bien]
            .mean()
            .sort_values(ascending=True)
            .head(10)
            .reset_index()
        )

        top_villes = top_villes.rename(columns={bien: "Moyenne du m²", "ville": "Ville", "departement": "Département"})

        with col_town_2:
            st.subheader(f"Les villes les moins chères", divider="red")
            top_villes.index = range(1, len(top_villes) + 1)
            st.dataframe(top_villes)

    st.subheader(f"Carte du marché immobilier - {nom_bien.capitalize()}", divider="red")

    # On normalise le loyer pour avoir des couleurs entre 0 et 255 non extrêmes
    if option is not None:
        loyer_min = df_departement[bien].quantile(0)
        loyer_max = df_departement[bien].quantile(0.95)
    else:
        loyer_min = df_national[bien].quantile(0)
        loyer_max = df_national[bien].quantile(0.95)

    df_national["color"] = df_national["loyer_m2_maison"].apply(loyer_to_color)

    if option is not None:
        df_departement["color_departement"] = (
            df_departement["loyer_m2_maison"]
            .apply(loyer_to_color)
        )

    layer = pdk.Layer(
                "ScatterplotLayer",
                data=df_national,
                get_position=["longitude", "latitude"],
                get_radius=500,
                get_fill_color="color",
                pickable=True
            )

    if commune is not None:
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_departement,
            get_position=["longitude", "latitude"],
            get_radius=500,
            get_fill_color="color_departement",
            pickable=True
        )
        layer_commune = pdk.Layer(
            "ScatterplotLayer",
            data=df_departement[df_departement["ville"] == commune],
            get_position=["longitude", "latitude"],
            get_fill_color="color_departement",
            get_line_color=[0, 0, 0],
            stroked=True,
            line_width_min_pixels=3,
            get_radius=900,
        )

        view_state = pdk.ViewState(
            latitude=df_commune["latitude"].mean(),
            longitude=df_commune["longitude"].mean(),
            zoom=12
        )
    elif option is not None:
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_departement,
            get_position=["longitude", "latitude"],
            get_radius=500,
            get_fill_color="color_departement",
            pickable=True
        )
        view_state = pdk.ViewState(
            latitude=df_departement["latitude"].mean(),
            longitude=df_departement["longitude"].mean(),
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
        layers=[layer, layer_commune] if commune is not None else [layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="road"
    ))

if confirmed_comparaison and first_option is not None and second_option is not None:
    first_departement_name = df.loc[df["departement"] == first_option, "nom_departement"].iloc[0]
    second_departement_name = df.loc[df["departement"] == second_option, "nom_departement"].iloc[0]
    st.subheader(f"Comparatif du marché immobilier entre {first_departement_name} et {second_departement_name}", divider="gray")
    col_1, col_2 = st.columns(2)
    with col_1:

        
        df_comparaison = df[
            df["departement"].isin([first_option, second_option])
        ]

        df_comparaison = (
            df_comparaison
            .groupby(["date", "departement"])["loyer_m2_maison"]
            .mean()
            .reset_index()
        )
        df_comparaison = df_comparaison.pivot(
            index="date",
            columns="departement",
            values="loyer_m2_maison"
        ).reset_index()

        df_comparaison = df_comparaison.rename(columns={
            first_option: df.loc[df["departement"] == first_option, "nom_departement"].iloc[0],
            second_option: df.loc[df["departement"] == second_option, "nom_departement"].iloc[0]
        })

        st.line_chart(
            df_comparaison,
            x="date",
            y=[first_departement_name, second_departement_name],
            x_label="Date",
            y_label=f"Coût du m² maison"
        )
    with col_2:
        df_comparaison = df[
            df["departement"].isin([first_option, second_option])
        ]

        df_comparaison = (
            df_comparaison
            .groupby(["date", "departement"])["loyer_m2_appartement"]
            .mean()
            .reset_index()
        )
        df_comparaison = df_comparaison.pivot(
            index="date",
            columns="departement",
            values="loyer_m2_appartement"
        ).reset_index()

        df_comparaison = df_comparaison.rename(columns={
            first_option: df.loc[df["departement"] == first_option, "nom_departement"].iloc[0],
            second_option: df.loc[df["departement"] == second_option, "nom_departement"].iloc[0]
        })
        first_departement_name = df.loc[df["departement"] == first_option, "nom_departement"].iloc[0]
        second_departement_name = df.loc[df["departement"] == second_option, "nom_departement"].iloc[0]

        st.line_chart(
            df_comparaison,
            x="date",
            y=[first_departement_name, second_departement_name],
            x_label="Date",
            y_label=f"Coût du m² appartement"
        )

        
    moyenne_maison_first = (
        df[df["departement"] == first_option]["loyer_m2_maison"]
        .mean()
    )

    moyenne_maison_second = (
        df[df["departement"] == second_option]["loyer_m2_maison"]
        .mean()
    )
    moyenne_appartement_first = (
        df[df["departement"] == first_option]["loyer_m2_appartement"]
        .mean()
    )

    moyenne_appartement_second = (
        df[df["departement"] == second_option]["loyer_m2_appartement"]
        .mean()
    )
    df_first = (
        df[df["departement"] == first_option]
        .groupby("date")["loyer_m2_maison"]
        .mean()
        .reset_index()
    )

    df_second = (
        df[df["departement"] == second_option]
        .groupby("date")["loyer_m2_maison"]
        .mean()
        .reset_index()
    )

    first_year = df_first.loc[df_first["date"] == annee[0], "loyer_m2_maison"].values[0]
    second_year = df_first.loc[df_first["date"] == annee[1], "loyer_m2_maison"].values[0]

    calcul_first = round(((second_year - first_year) / first_year) * 100, 2)

    first_year = df_second.loc[df_second["date"] == annee[0], "loyer_m2_maison"].values[0]
    second_year = df_second.loc[df_second["date"] == annee[1], "loyer_m2_maison"].values[0]

    calcul_second = round(((second_year - first_year) / first_year) * 100, 2)

    first_number_town= df[df["departement"] == first_option]["ville"].nunique()
    second_number_town= df[df["departement"] == second_option]["ville"].nunique()

    if calcul_first<0:
        courbe_first="Baisse de "
    else:
        courbe_first="Hausse de "

    if calcul_second<0:
        courbe_second="Baisse de "
    else:
        courbe_second="Hausse de "

    immobilier_data = {
        "Indicateur": [
            "Moyenne m² maison",
            "Moyenne m² appartement",
            "Évolution depuis 2018",
            "Nombre de communes"
        ],
        first_departement_name: [
            moyenne_maison_first.round(2),
            moyenne_appartement_first.round(2),
            f"{courbe_first}{calcul_first.round(2)} %",
            first_number_town
        ],
        second_departement_name: [
            moyenne_maison_second.round(2),
            moyenne_appartement_second.round(2),
            f"{courbe_second}{calcul_second.round(2)} %",
            second_number_town
        ]
    }

    df_compare = pd.DataFrame(immobilier_data)
    st.dataframe(df_compare, hide_index=True)

    comparison_maison = (
        (moyenne_maison_first - moyenne_maison_second)
        / moyenne_maison_second
    ) * 100

    comparison_maison = round(comparison_maison, 2)

    if comparison_maison<0:
        texte_evolution= "moins cher que le département"
        arrow_maison="down"
        arrow_color_maison="inverse"
    else:
        texte_evolution= "plus cher que le département"
        arrow_maison="down"
        arrow_color_maison="inverse"

    col_metric_1,col_metric_2 = st.columns(2)
    with col_metric_1:
        st.metric(
            f"Comparaision du m²",
            f"{abs(comparison_maison)} %",
            delta=f"le département {first_departement_name} est {abs(comparison_maison.round(2))} % {texte_evolution} {second_departement_name}",
            delta_arrow=arrow_maison,
            delta_color=arrow_color_maison
        )


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