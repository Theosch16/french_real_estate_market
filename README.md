This application allows users to explore rental market trends in France through interactive geographical and temporal analysis.

## Overview

<img width="1920" height="873" alt="{06973EF4-6719-4340-8F44-29B2FCF6355A}" src="https://github.com/user-attachments/assets/09523566-3a38-46d2-b8a0-a459ba701931" />
<img width="1918" height="873" alt="{1CD04FC3-CEDA-487D-A39B-8E20B834765F}" src="https://github.com/user-attachments/assets/f3e102a4-db18-4f01-abd1-0cbc55cdc549" />

## Usage

The application is available here: https://french-rental-market.streamlit.app/

* Select a **department**, a **municipality**, and a **time period** to display the corresponding real estate indicators.
* To obtain an analysis at the national level, simply click on **"Confirm parameters"** without selecting a department or municipality.
* It is also possible to compare multiple geographical areas in order to identify differences in real estate market trends.

The application then generates visualizations that allow users to analyze price trends and market evolution based on the selected criteria.

## Data Sources

The data presented in this application is based on information available on the data.gouv.fr portal and is provided under an open license.

Please note that some municipalities may not be represented due to mergers or the disappearance of certain municipalities over time. In addition, data for the years 2019, 2020, and 2021 is missing, which may impact trend analysis for these periods.

**'Carte des loyers' - Indicateurs de loyers d'annonce par commune en 2018:** https://www.data.gouv.fr/datasets/carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune-en-2018

**'Carte des loyers' - Indicateurs de loyers d'annonce par commune en 2022 :** https://www.data.gouv.fr/datasets/carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune-en-2022

**'Carte des loyers' - Indicateurs de loyers d'annonce par commune en 2023 :** https://www.data.gouv.fr/datasets/carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune-en-2023

**'Carte des loyers' - Indicateurs de loyers d'annonce par commune en 2024 :** https://www.data.gouv.fr/datasets/carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune-en-2024

**'Carte des loyers' - Indicateurs de loyers d'annonce par commune en 2025 :** https://www.data.gouv.fr/datasets/carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune-en-2025

## Technologies Used

* Python (Pandas)
* Streamlit
* Git/GitHub

## Features

* Data cleaning and transformation
* Creation of KPI indicators
* Interactive visualizations
* Dynamic filters

## Key Insights

- In the majority of French departments, advertised rents per square meter increased between 2018 and 2026 for both houses and apartments.
- The analysis highlights significant geographical disparities in rental market trends across France.
- The dashboard allows users to compare rental price evolution between different geographical areas and property types.
