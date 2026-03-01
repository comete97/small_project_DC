from modules import *
import warnings
warnings.filterwarnings('ignore')

# ------- Configuration

st.set_page_config(page_title="DATA COLLECTER",  layout="wide")

# -------- Style css
st.markdown("""
    <style>
    .stApp {
        background-color: rgba(255, 255, 255, 0.9);
        min-height: 100vh;
    }

    h1 {
        color: #024a56;
        font-size: 2.5em;
        font-weight: 700;
    }

    .subtitle {
        color: #7f8c8d;
        font-style: italic;
        font-size: 1.1em;
    }

    section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] span:not([class*="input"]) {
            color: white !important;
        }

    section[data-testid="stSidebar"] {
        background-color: #024a56 !important;
        padding: 20px;
    }

    section[data-testid="stSidebar"] input[type="text"],
    section[data-testid="stSidebar"] input[type="number"],
    section[data-testid="stSidebar"] input[type="email"] {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
        border: 1px solid #bdc3c7 !important;
        border-radius: 8px !important;
        padding: 8px !important;
    }

    section[data-testid="stSidebar"] input::placeholder {
        color: #7f8c8d !important;
    }


    section[data-testid="stSidebar"] select {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
        border: 1px solid #bdc3c7 !important;
        border-radius: 8px !important;
    }

    section[data-testid="stSidebar"] select option {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
    }

    .stButton>button {
        border-radius: 8px;
        border: none;
        background: #024a56;
        color: white;
        font-weight: 600;
        padding: 10px 24px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }


    button[data-testid="stButton"][aria-label*="Lancer le scraping"] {
        background-color: #27ae60 !important;
    }

    button[data-testid="stButton"][aria-label*="Lancer le scraping"]:hover {
        background-color: #219a52 !important;
    }

    button[data-testid="stButton"][aria-label*="Télécharger"] {
        background-color: #3498db !important;
    }

  
    button[data-testid="stButton"][aria-label*="Évaluer"] {
        background-color: #9b59b6 !important;
    }

    .data-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid #e0e0e0;
    }

    .header-container {
        text-align: center;
        padding: 30px;
        margin-bottom: 30px;
    }

    .stTextInput>div>div>input,
    .stNumberInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        background-color: #ffffff;
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)


# ------ Initialisation de la base de donnée
init_db()

# ------ Sidebar

with st.sidebar:
    st.markdown("""
        <div style="text-align: left; padding: 20px 0;">
            <h2 style="color: white; margin: 0;">DATA COLLECTER</h2>
            <p style="color: #bdc3c7; font-size: 0.9em;">Mini projet DC | DIT Master 1 Oct_25</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    #----------- Options 

    st.markdown("### Options")
    menu = st.selectbox(
        "Choisir une option",
        ["Scraper les données", "Télécharger les données", "Dashboard","Évaluer l'application"],
        index=0,
        label_visibility="collapsed"
    )
    
    # Paramètrage du  scraping 
    st.markdown("### Configuration Scraping")

    st.markdown("""
        <style>
        /* Input */
        .stSelectbox input {
            background-color: #ecf0f1 !important;
            color: #2c3e50 !important;
        }
        
        /* Dropdown */
        ul[role="listbox"] {
            background-color: #ffffff !important;
        }
        
        ul[role="listbox"] li {
            color: #000000 !important;
        }
        
        ul[role="listbox"] li[aria-selected="true"] {
            background-color: #3498db !important;
            color: #ffffff !important;
        }
        </style>
    """, unsafe_allow_html=True)

    num_pages = st.selectbox("Nombre de pages à scraper", range(1, 11), index=4)
    
    categories = {
        "Chiens": "https://sn.coinafrique.com/categorie/chiens",
        "Moutons": "https://sn.coinafrique.com/categorie/moutons", 
        "Poules/Lapins/Pigeons": "https://sn.coinafrique.com/categorie/poules-lapins-et-pigeons",
        "Autres animaux": "https://sn.coinafrique.com/categorie/autres-animaux"
    }
    selected_category = st.selectbox("Catégorie", list(categories.keys()))



# --------- pages Dashboard 

if menu == "Dashboard":
    st.markdown('<div class="header-container"><h1>Tableau de Bord</h1><p class="subtitle">Exploration des données</p></div>', unsafe_allow_html=True)
    
    cleaned_files = get_cleaned_files()
    
    if cleaned_files:
        st.success(f"{len(cleaned_files)} fichiers disponibles")
        selected_file = st.selectbox("Sélectionner un fichier à exprolrer", cleaned_files)
        df = load_cleaned_data(selected_file)
    else:
        st.warning("Aucune donnée propre.")
        st.stop()
    
    if df is not None and not df.empty:

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Nombre total de ligne", f"{len(df):,}")
        with col2:
            st.metric("Colonnes", len(df.columns))
        
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        text_cols = df.select_dtypes(include='object').columns.tolist()
        
        with col3:
            st.metric("Nombre de colonnes numériques", len(numeric_cols))
        with col4:
            st.metric("Nombre de collonnes catégorielle", len(text_cols))
        
        st.markdown("---")
        
        
        col_a1, col_a2 = st.columns(2)
        
        with col_a1:
            st.subheader("Répartition par catégorie")
            if 'category' in df.columns or 'categorie' in df.columns:
                cat_col = 'category' if 'category' in df.columns else 'categorie'
                cat_counts = df[cat_col].value_counts().head(8).reset_index()
                cat_counts.columns = ['Catégorie', 'Nombre']
                fig1 = px.pie(cat_counts, values='Nombre', names='Catégorie', hole=0.4, 
                             color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig1, use_container_width=True)
            elif len(text_cols) > 0:
                first_text = text_cols[0]
                counts = df[first_text].value_counts().head(8).reset_index()
                counts.columns = [first_text, 'Nombre']
                fig1 = px.pie(counts, values='Nombre', names=first_text, hole=0.4)
                st.plotly_chart(fig1, use_container_width=True)
        
        with col_a2:
            st.subheader("Répartition par tranche de prix")
            if 'categorie_prix' in df.columns:
                prix_counts = df['categorie_prix'].value_counts().reset_index()
                prix_counts.columns = ['Tranche', 'Nombre']
                fig2 = px.bar(prix_counts, x='Tranche', y='Nombre', 
                             color='Nombre', color_continuous_scale='Blues')
                st.plotly_chart(fig2, use_container_width=True)
            elif 'prix_clean' in df.columns:
                st.info("Utilisation de la distribution des prix")
                fig2 = px.histogram(df, x='prix_clean', nbins=20, color_discrete_sequence=['#024a56'])
                st.plotly_chart(fig2, use_container_width=True)
        
       
        col_b1, col_b2 = st.columns(2)
        
        with col_b1:
            st.subheader("Top 10 villes")
            if 'ville' in df.columns:
                ville_counts = df['ville'].value_counts().head(10).reset_index()
                ville_counts.columns = ['Ville', 'Nombre']
                fig3 = px.bar(ville_counts, x='Nombre', y='Ville', orientation='h',
                             color='Nombre', color_continuous_scale='Viridis')
                st.plotly_chart(fig3, use_container_width=True)
            elif 'adresse' in df.columns:
                addr_counts = df['adresse'].value_counts().head(10).reset_index()
                addr_counts.columns = ['Localisation', 'Nombre']
                fig3 = px.bar(addr_counts, x='Nombre', y='Localisation', orientation='h')
                st.plotly_chart(fig3, use_container_width=True)
        
        with col_b2:
            st.subheader("Statistiques des prix")
            if 'prix_clean' in df.columns and df['prix_clean'].notna().any():
                stats_df = pd.DataFrame({
                    'Métrique': ['Minimum', 'Médiane', 'Moyenne', 'Maximum'],
                    'Valeur': [
                        f"{df['prix_clean'].min():.2f}",
                        f"{df['prix_clean'].median():.2f}",
                        f"{df['prix_clean'].mean():.2f}",
                        f"{df['prix_clean'].max():.2f}"
                    ]
                })
                st.table(stats_df)
            else:
                st.info("Statistiques non disponibles")
        
        
        with st.expander("Aperçu des données nettoyées"):
            st.dataframe(df.head(20), use_container_width=True)

            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="Télécharger les données nettoyées",
                data=csv,
                file_name=selected_file,
                mime='text/csv',
                use_container_width=True
            )


# ----------- Automatisation du scrapping 
elif menu == "Scraper les données":
    st.markdown('<div class="header-container"><h1>Scraper avec Beautiful Soup</h1><p class="subtitle">Collecte automatique de données web</p></div>', unsafe_allow_html=True)
    
    st.info(f"""
    **Configuration active**  
    • Catégorie : **{selected_category}**  
    • Pages : **{num_pages}**  
    • URL : `{categories[selected_category]}`
    """)
    
    if st.button("Lancer le scraping", type="primary", use_container_width=True):

        clear_db()
        st.success("Base de données vidée. Prêt pour le nouveau scraping !")

        progress_bar = st.progress(0)
        status_text = st.empty()
        result_box = st.empty()
        
        with st.spinner("Scrapping en cours..."):
            df_scraped = scrape_category(
                categories[selected_category], 
                selected_category, 
                num_pages, 
                progress_bar, 
                status_text
            )
        
        if not df_scraped.empty and df_scraped['nom'].iloc[0] != "N/A":
            with st.spinner("Enregistrement dans la base..."):
                save_to_db(df_scraped, selected_category, num_pages)
            
            result_box.success(f" **{len(df_scraped)} annonces** scrapées et sauvegardées !")
            
            with st.expander("Aperçu"):
                st.dataframe(df_scraped.head(), use_container_width=True)
            
            csv = df_scraped.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="Télécharger en CSV",
                data=csv,
                file_name=f"{selected_category}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime='text/csv',
                use_container_width=True
            )
        else:
            result_box.warning("Aucune donnée récupérée. Vérifiez la connexion et les sélecteurs CSS.")

# Données disponibles 

elif menu == "Télécharger les données":
    st.markdown('<div class="header-container"><h1>Bibliothèque de Données</h1><p class="subtitle">Consultez et téléchargez les datasets disponibles</p></div>', unsafe_allow_html=True)
    
    available_files = get_available_files()
    
    if available_files:
        st.markdown(f"### {len(available_files)} fichier disponible")
        
        # Créer un bouton par fichier
        for filename in available_files:
            with st.container():
                st.markdown(f"""
                <div class="data-card">
                    <h3>{filename}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                col_view, col_download = st.columns([2, 1])
                
                with col_view:
                    if st.button(f"Voir les données", key=f"view_{filename}"):
                        df = load_existing_data(filename)
                        if df is not None:
                            st.session_state[f'df_{filename}'] = df
                            st.dataframe(df, use_container_width=True)
                        else:
                            st.error("Impossible de charger le fichier")
                
                with col_download:
                    df = load_existing_data(filename)
                    if df is not None:
                        csv = df.to_csv(index=False, encoding='utf-8-sig')
                        st.download_button(
                            label="Télécharger",
                            data=csv,
                            file_name=filename,
                            mime='text/csv',
                            use_container_width=True
                        )
                
                st.markdown("---")
        
        # Données scrapées 
        st.markdown("### Données scrapées")
        df_scraped = load_scraped_data()
        if not df_scraped.empty:
            with st.expander(f"Voir les données scrapées ({len(df_scraped)} enregistrements)"):
                st.dataframe(df_scraped, use_container_width=True)
            
            csv_scraped = df_scraped.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="Télécharger toutes les données scrapées",
                data=csv_scraped,
                file_name=f"scraped_all_{datetime.now().strftime('%Y%m%d')}.csv",
                mime='text/csv',
                use_container_width=True
            )
        else:
            st.info("Aucune donnée scrapée dans la base pour le moment.")
    else:
        st.info("📭 Aucun fichier CSV disponible dans le dossier `data/`.")

#  -------- évaluation 

elif menu == "Évaluer l'application":
    st.markdown("""
        <div class="header-container">
            <h1> Évaluer l'Application</h1>
            <p class="subtitle">Votre avis nous aide à améliorer l'outil</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### Choisissez votre plateforme d'évaluation
    
    Nous utilisons deux plateformes pour recueillir vos retours. 
    Cliquez sur le bouton de votre choix pour accéder au formulaire.
    """)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(""" #### KOBO COLLECT """)
        
        kobo_link = "https://ee.kobotoolbox.org/x/Nfk09AXY" 

        st.link_button(
            label="Evaluer via KOBO COLLECT",
            url=kobo_link,
            use_container_width=True
        )
    
    with col2:
        st.markdown(""" #### Google Forms """)
        
        google_link = "https://forms.gle/ekDsCkoTjSRtAyx3A"

        st.link_button(
            label="Evaluer via Google Forms",
            url=google_link,
            use_container_width=True
        )
    
    st.markdown("---")
