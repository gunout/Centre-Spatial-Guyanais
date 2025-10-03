# dashboard_guyane_aerospatiale.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import random
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Centre Spatial Guyanais - Dashboard Live",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(45deg, #0d3b66, #1e5a8a, #e37222);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .live-badge {
        background: linear-gradient(45deg, #0d3b66, #e37222);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #0d3b66;
        margin: 0.5rem 0;
    }
    .section-header {
        color: #0d3b66;
        border-bottom: 2px solid #e37222;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    .mission-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid #0d3b66;
        background-color: #f8f9fa;
    }
    .mission-status {
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.2rem 0;
        font-size: 0.9rem;
    }
    .success { background-color: #d4edda; border-left: 4px solid #28a745; }
    .failure { background-color: #f8d7da; border-left: 4px solid #dc3545; }
    .planned { background-color: #cce7ff; border-left: 4px solid #007bff; }
    .in-progress { background-color: #fff3cd; border-left: 4px solid #ffc107; }
</style>
""", unsafe_allow_html=True)

class GuyaneAerospatialeDashboard:
    def __init__(self):
        self.lanceurs = self.define_lanceurs()
        self.missions_data = self.initialize_missions_data()
        self.traffic_data = self.initialize_traffic_data()
        self.clients_data = self.initialize_clients_data()
        
    def define_lanceurs(self):
        """Définit les lanceurs utilisés en Guyane"""
        return {
            'Ariane 5': {
                'nom_complet': 'Ariane 5',
                'type': 'Lanceur lourd',
                'constructeur': 'ArianeGroup',
                'capacite_orbite_bas': 21000,
                'capacite_orbite_geo': 10000,
                'premier_vol': '1996',
                'statut': 'Actif',
                'couleur': '#0d3b66',
                'success_rate': 95.2,
                'vols_total': 112
            },
            'Ariane 6': {
                'nom_complet': 'Ariane 6',
                'type': 'Lanceur lourd nouvelle génération',
                'constructeur': 'ArianeGroup',
                'capacite_orbite_bas': 21500,
                'capacite_orbite_geo': 11500,
                'premier_vol': '2024',
                'statut': 'En développement',
                'couleur': '#1e5a8a',
                'success_rate': 100,
                'vols_total': 0
            },
            'Vega': {
                'nom_complet': 'Vega',
                'type': 'Lanceur léger',
                'constructeur': 'Avio',
                'capacite_orbite_bas': 1500,
                'capacite_orbite_sso': 1400,
                'premier_vol': '2012',
                'statut': 'Actif',
                'couleur': '#e37222',
                'success_rate': 90.5,
                'vols_total': 21
            },
            'Vega C': {
                'nom_complet': 'Vega C',
                'type': 'Lanceur léger amélioré',
                'constructeur': 'Avio',
                'capacite_orbite_bas': 2200,
                'capacite_orbite_sso': 2000,
                'premier_vol': '2022',
                'statut': 'Actif',
                'couleur': '#f4a261',
                'success_rate': 85.7,
                'vols_total': 7
            },
            'Soyuz': {
                'nom_complet': 'Soyuz ST',
                'type': 'Lanceur moyen',
                'constructeur': 'Roscosmos',
                'capacite_orbite_bas': 8200,
                'capacite_orbite_geo': 3250,
                'premier_vol': '2011',
                'statut': 'En pause',
                'couleur': '#6f42c1',
                'success_rate': 96.3,
                'vols_total': 27
            }
        }
    
    def initialize_missions_data(self):
        """Initialise les données des missions"""
        types_mission = ['Commercial', 'Institutionnel', 'Scientifique', 'Militaire', 'Observation Terre']
        clients = ['ESA', 'NASA', 'CNES', 'Eutelsat', 'SES', 'Intelsat', 'OneWeb', 'Airbus', 'Thales', 'SpaceX (Transports)']
        orbites = ['GEO', 'LEO', 'SSO', 'MEO', 'HEO', 'Lunar Transfer']
        
        missions = []
        for i in range(100):  # 100 missions simulées
            annee = random.randint(2002, 2025)
            mois = random.randint(1, 12)
            jour = random.randint(1, 28)
            
            date_lancement = datetime(annee, mois, jour)
            lanceur = random.choice(list(self.lanceurs.keys()))
            
            if random.random() > 0.1:  # 90% de succès
                statut = 'Succès'
            else:
                statut = random.choices(['Échec', 'Succès partiel'], weights=[0.7, 0.3])[0]
            
            missions.append({
                'mission_id': f'{random.choice(["VA", "VV", "VS", "AR"])}{random.randint(200, 299)}',
                'lanceur': lanceur,
                'date_lancement': date_lancement,
                'client': random.choice(clients),
                'type_mission': random.choice(types_mission),
                'orbite': random.choice(orbites),
                'statut': statut,
                'charge_utile': f'Satellite {random.choice(["Telecom", "Observation", "Scientifique", "Navigation"])} {random.randint(1, 100)}',
                'masse_charge_utile': random.randint(100, 10000),
                'site_lancement': random.choice(['ELA-3', 'ELS', 'ELV'])
            })
        
        return pd.DataFrame(missions)
    
    def initialize_traffic_data(self):
        """Initialise les données de trafic historiques"""
        dates = pd.date_range('2002-01-01', datetime.now(), freq='M')
        data = []
        
        for date in dates:
            for lanceur, info in self.lanceurs.items():
                if date.year < int(info['premier_vol']):
                    continue
                    
                # Base de lancements par an
                if lanceur == 'Ariane 5':
                    base_lancements = 7
                elif lanceur == 'Vega':
                    base_lancements = 3
                elif lanceur == 'Soyuz':
                    base_lancements = 2
                elif lanceur == 'Vega C':
                    if date.year < 2022:
                        continue
                    base_lancements = 2
                else:
                    base_lancements = 1
                
                # Variation saisonnière et aléatoire
                lancements_mois = max(0, int(base_lancements / 12 * random.uniform(0.8, 1.2)))
                
                data.append({
                    'date': date,
                    'lanceur': lanceur,
                    'lancements': lancements_mois,
                    'satellites_lances': random.randint(1, 4) * lancements_mois,
                    'masse_totale': random.randint(1000, 20000) * lancements_mois,
                    'type_lanceur': info['type']
                })
        
        return pd.DataFrame(data)
    
    def initialize_clients_data(self):
        """Initialise les données des clients"""
        clients = {
            'Commercial': {'part_marche': 65, 'couleur': '#0d3b66', 'pays': 'International'},
            'ESA': {'part_marche': 15, 'couleur': '#1e5a8a', 'pays': 'Europe'},
            'NASA': {'part_marche': 8, 'couleur': '#e37222', 'pays': 'USA'},
            'CNES': {'part_marche': 5, 'couleur': '#f4a261', 'pays': 'France'},
            'Autres Institutionnels': {'part_marche': 4, 'couleur': '#6f42c1', 'pays': 'International'},
            'Militaires': {'part_marche': 3, 'couleur': '#dc3545', 'pays': 'International'}
        }
        
        data = []
        for client, info in clients.items():
            data.append({
                'client': client,
                'part_marche': info['part_marche'],
                'couleur': info['couleur'],
                'pays': info['pays'],
                'missions_total': random.randint(5, 50),
                'satellites_lances': random.randint(10, 200)
            })
        
        return pd.DataFrame(data)
    
    def update_live_data(self):
        """Met à jour les données en temps réel"""
        # Simulation de nouvelles missions pour l'année en cours
        current_year = datetime.now().year
        current_missions = self.missions_data[self.missions_data['date_lancement'].dt.year == current_year]
        
        if len(current_missions) < 12:  # Ajouter de nouvelles missions si nécessaire
            new_mission = {
                'mission_id': f'VV{random.randint(230, 250)}',
                'lanceur': random.choice(['Vega', 'Vega C', 'Ariane 5']),
                'date_lancement': datetime.now() + timedelta(days=random.randint(1, 180)),
                'client': random.choice(['ESA', 'Eutelsat', 'SES', 'OneWeb']),
                'type_mission': random.choice(['Commercial', 'Institutionnel']),
                'orbite': random.choice(['GEO', 'LEO', 'SSO']),
                'statut': 'Planifié',
                'charge_utile': f'Satellite {random.choice(["Telecom", "Observation"])} {random.randint(100, 200)}',
                'masse_charge_utile': random.randint(1000, 5000),
                'site_lancement': random.choice(['ELA-3', 'ELV'])
            }
            
            self.missions_data = pd.concat([self.missions_data, pd.DataFrame([new_mission])], ignore_index=True)
    
    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown('<h1 class="main-header">🚀 Centre Spatial Guyanais - Dashboard Live</h1>', 
                   unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="live-badge">🔴 DONNÉES SPATIALES EN TEMPS RÉEL - CSG</div>', 
                       unsafe_allow_html=True)
            st.markdown("**Surveillance des lancements et analyse des missions spatiales depuis la Guyane**")
        
        current_time = datetime.now().strftime('%H:%M:%S')
        st.sidebar.markdown(f"**🕐 Dernière mise à jour: {current_time}**")
    
    def display_key_metrics(self):
        """Affiche les métriques clés du spatial"""
        st.markdown('<h3 class="section-header">📊 INDICATEURS CLÉS DU CENTRE SPATIAL</h3>', 
                   unsafe_allow_html=True)
        
        # Calcul des métriques
        missions_total = len(self.missions_data)
        missions_reussies = len(self.missions_data[self.missions_data['statut'] == 'Succès'])
        missions_planifiees = len(self.missions_data[
            (self.missions_data['statut'] == 'Planifié') & 
            (self.missions_data['date_lancement'] > datetime.now())
        ])
        taux_reussite = (missions_reussies / missions_total * 100) if missions_total > 0 else 0
        
        # Satellites lancés
        satellites_total = self.traffic_data['satellites_lances'].sum()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Missions Totales (2002-2025)",
                f"{missions_total}",
                f"{random.randint(1, 5)} nouvelles missions"
            )
        
        with col2:
            st.metric(
                "Taux de Réussite",
                f"{taux_reussite:.1f}%",
                f"{random.uniform(-1, 2):.1f}% vs période précédente"
            )
        
        with col3:
            st.metric(
                "Missions Planifiées",
                f"{missions_planifiees}",
                f"{random.randint(1, 3)} nouvelles"
            )
        
        with col4:
            st.metric(
                "Satellites Lancés",
                f"{satellites_total:,}",
                f"{random.randint(10, 50)} vs année dernière"
            )
    
    def create_lanceurs_overview(self):
        """Crée la vue d'ensemble des lanceurs"""
        st.markdown('<h3 class="section-header">🏛️ VUE D\'ENSEMBLE DES LANCEURS</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["Performance", "Capacités", "Évolution", "Détails Techniques"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Performance des lanceurs
                success_rates = []
                for lanceur, info in self.lanceurs.items():
                    missions_lanceur = self.missions_data[self.missions_data['lanceur'] == lanceur]
                    if len(missions_lanceur) > 0:
                        succes = len(missions_lanceur[missions_lanceur['statut'] == 'Succès'])
                        taux = (succes / len(missions_lanceur)) * 100
                        success_rates.append({
                            'lanceur': lanceur,
                            'taux_reussite': taux,
                            'vols_total': len(missions_lanceur)
                        })
                
                df_success = pd.DataFrame(success_rates)
                fig = px.bar(df_success, 
                            x='lanceur', 
                            y='taux_reussite',
                            title='Taux de Réussite par Lanceur (%)',
                            color='lanceur',
                            color_discrete_map={lanceur: info['couleur'] for lanceur, info in self.lanceurs.items()})
                fig.update_layout(yaxis_range=[0, 100])
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Répartition des vols
                vol_counts = self.missions_data['lanceur'].value_counts().reset_index()
                vol_counts.columns = ['lanceur', 'nombre_vols']
                fig = px.pie(vol_counts, 
                            values='nombre_vols', 
                            names='lanceur',
                            title='Répartition des Vols par Lanceur',
                            color='lanceur',
                            color_discrete_map={lanceur: info['couleur'] for lanceur, info in self.lanceurs.items()})
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Capacité en orbite GTO
                capacities = []
                for lanceur, info in self.lanceurs.items():
                    if 'capacite_orbite_geo' in info:
                        capacities.append({
                            'lanceur': lanceur,
                            'capacite_kg': info['capacite_orbite_geo'],
                            'type': 'Orbite Géostationnaire'
                        })
                
                df_capacity = pd.DataFrame(capacities)
                fig = px.bar(df_capacity, 
                            x='lanceur', 
                            y='capacite_kg',
                            title='Capacité en Orbite Géostationnaire (kg)',
                            color='lanceur',
                            color_discrete_map={lanceur: info['couleur'] for lanceur, info in self.lanceurs.items()})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Comparaison des capacités
                comparison_data = []
                for lanceur, info in self.lanceurs.items():
                    if 'capacite_orbite_bas' in info:
                        comparison_data.append({
                            'lanceur': lanceur,
                            'orbite': 'Orbite Basse',
                            'capacite': info['capacite_orbite_bas']
                        })
                    if 'capacite_orbite_geo' in info:
                        comparison_data.append({
                            'lanceur': lanceur,
                            'orbite': 'Orbite Géostationnaire',
                            'capacite': info['capacite_orbite_geo']
                        })
                
                df_comparison = pd.DataFrame(comparison_data)
                fig = px.bar(df_comparison, 
                            x='lanceur', 
                            y='capacite',
                            color='orbite',
                            barmode='group',
                            title='Comparaison des Capacités par Orbite',
                            color_discrete_sequence=['#0d3b66', '#e37222'])
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Évolution des lancements par type
            yearly_launches = self.missions_data.groupby([
                self.missions_data['date_lancement'].dt.year,
                'lanceur'
            ]).size().reset_index(name='nombre_lancements')
            
            fig = px.line(yearly_launches, 
                         x='date_lancement', 
                         y='nombre_lancements',
                         color='lanceur',
                         title='Évolution des Lancements par Lanceur (2002-2025)',
                         color_discrete_map={lanceur: info['couleur'] for lanceur, info in self.lanceurs.items()})
            st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            # Tableau détaillé des lanceurs
            lanceur_details = []
            for lanceur, info in self.lanceurs.items():
                missions_lanceur = self.missions_data[self.missions_data['lanceur'] == lanceur]
                succes = len(missions_lanceur[missions_lanceur['statut'] == 'Succès'])
                taux_reussite = (succes / len(missions_lanceur) * 100) if len(missions_lanceur) > 0 else 0
                
                lanceur_details.append({
                    'Lanceur': info['nom_complet'],
                    'Type': info['type'],
                    'Constructeur': info['constructeur'],
                    'Premier Vol': info['premier_vol'],
                    'Statut': info['statut'],
                    'Vols Total': len(missions_lanceur),
                    'Taux Réussite': f"{taux_reussite:.1f}%",
                    'Capacité LEO (kg)': info.get('capacite_orbite_bas', 'N/A'),
                    'Capacité GTO (kg)': info.get('capacite_orbite_geo', 'N/A')
                })
            
            st.dataframe(pd.DataFrame(lanceur_details), use_container_width=True)
    
    def create_missions_live(self):
        """Affiche les missions en temps réel"""
        st.markdown('<h3 class="section-header">🚀 MISSIONS EN TEMPS RÉEL</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Calendrier des Missions", "Statistiques", "Analyse des Orbites"])
        
        with tab1:
            # Filtres pour les missions
            col1, col2, col3 = st.columns(3)
            with col1:
                lanceur_filtre = st.selectbox("Lanceur:", 
                                            ['Tous'] + list(self.lanceurs.keys()))
            with col2:
                statut_filtre = st.selectbox("Statut:", 
                                           ['Tous', 'Succès', 'Échec', 'Succès partiel', 'Planifié'])
            with col3:
                client_filtre = st.selectbox("Client:", 
                                           ['Tous'] + list(self.clients_data['client'].unique()))
            
            # Application des filtres
            missions_filtrees = self.missions_data.copy()
            if lanceur_filtre != 'Tous':
                missions_filtrees = missions_filtrees[missions_filtrees['lanceur'] == lanceur_filtre]
            if statut_filtre != 'Tous':
                missions_filtrees = missions_filtrees[missions_filtrees['statut'] == statut_filtre]
            if client_filtre != 'Tous':
                missions_filtrees = missions_filtrees[missions_filtrees['client'] == client_filtre]
            
            # Trier par date
            missions_filtrees = missions_filtrees.sort_values('date_lancement', ascending=False)
            
            # Affichage des missions
            for _, mission in missions_filtrees.head(20).iterrows():
                status_class = ""
                if mission['statut'] == 'Succès':
                    status_class = "success"
                elif mission['statut'] == 'Échec':
                    status_class = "failure"
                elif mission['statut'] == 'Planifié':
                    status_class = "planned"
                elif mission['statut'] == 'Succès partiel':
                    status_class = "in-progress"
                
                col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
                with col1:
                    st.markdown(f"**{mission['mission_id']}**")
                    st.markdown(f"*{mission['lanceur']}*")
                with col2:
                    st.markdown(f"**{mission['charge_utile']}**")
                    st.markdown(f"Client: {mission['client']}")
                with col3:
                    date_str = mission['date_lancement'].strftime('%d/%m/%Y')
                    st.markdown(f"**Lancement:** {date_str}")
                    st.markdown(f"Orbite: {mission['orbite']}")
                with col4:
                    st.markdown(f"<div class='mission-status {status_class}'>{mission['statut']}</div>", 
                               unsafe_allow_html=True)
                
                st.markdown("---")
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Répartition des statuts
                status_counts = self.missions_data['statut'].value_counts()
                fig = px.pie(values=status_counts.values, 
                            names=status_counts.index,
                            title='Répartition des Statuts de Mission')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Missions par type
                type_counts = self.missions_data['type_mission'].value_counts()
                fig = px.bar(x=type_counts.values, 
                            y=type_counts.index,
                            orientation='h',
                            title='Nombre de Missions par Type',
                            color=type_counts.values,
                            color_continuous_scale='Viridis')
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                # Répartition des orbites
                orbite_counts = self.missions_data['orbite'].value_counts()
                fig = px.pie(values=orbite_counts.values, 
                            names=orbite_counts.index,
                            title='Répartition des Types d\'Orbite')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Orbites par lanceur
                orbite_lanceur = pd.crosstab(self.missions_data['lanceur'], self.missions_data['orbite'])
                fig = px.imshow(orbite_lanceur,
                               title='Orbites par Lanceur (Heatmap)',
                               color_continuous_scale='Blues')
                st.plotly_chart(fig, use_container_width=True)
    
    def create_clients_analysis(self):
        """Analyse des clients et marchés"""
        st.markdown('<h3 class="section-header">🏢 ANALYSE DES CLIENTS ET MARCHÉS</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Parts de Marché", "Évolution Clients", "Analyse Géographique"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Parts de marché
                fig = px.pie(self.clients_data, 
                            values='part_marche', 
                            names='client',
                            title='Répartition du Marché des Lancements',
                            color='client',
                            color_discrete_map={row['client']: row['couleur'] for _, row in self.clients_data.iterrows()})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Satellites lancés par client
                fig = px.bar(self.clients_data, 
                            x='client', 
                            y='satellites_lances',
                            title='Satellites Lancés par Client',
                            color='client',
                            color_discrete_map={row['client']: row['couleur'] for _, row in self.clients_data.iterrows()})
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Évolution des clients dans le temps
            client_evolution = self.missions_data.groupby([
                self.missions_data['date_lancement'].dt.year,
                'client'
            ]).size().reset_index(name='nombre_missions')
            
            fig = px.area(client_evolution, 
                         x='date_lancement', 
                         y='nombre_missions',
                         color='client',
                         title='Évolution des Missions par Client',
                         color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Analyse géographique (simulée)
            pays_data = []
            for client, info in self.clients_data.iterrows():
                pays_data.append({
                    'pays': self.clients_data.loc[client, 'pays'],
                    'missions': self.clients_data.loc[client, 'missions_total'],
                    'part_marche': self.clients_data.loc[client, 'part_marche']
                })
            
            df_pays = pd.DataFrame(pays_data)
            df_pays = df_pays.groupby('pays').agg({
                'missions': 'sum',
                'part_marche': 'sum'
            }).reset_index()
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.pie(df_pays, 
                            values='missions', 
                            names='pays',
                            title='Répartition Géographique des Missions')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(df_pays, 
                            x='pays', 
                            y='part_marche',
                            title='Parts de Marché par Zone Géographique (%)',
                            color='pays',
                            color_discrete_sequence=px.colors.qualitative.Pastel)
                fig.update_layout(yaxis_tickformat='.0%')
                st.plotly_chart(fig, use_container_width=True)
    
    def create_evolution_analysis(self):
        """Analyse de l'évolution du spatial guyanais"""
        st.markdown('<h3 class="section-header">📈 ÉVOLUTION DU CENTRE SPATIAL</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Évolution Temporelle", "Impact COVID", "Projections Futures"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Évolution du nombre de lancements
                yearly_launches = self.missions_data.groupby(
                    self.missions_data['date_lancement'].dt.year
                ).size().reset_index(name='nombre_lancements')
                
                fig = px.line(yearly_launches, 
                             x='date_lancement', 
                             y='nombre_lancements',
                             title='Évolution du Nombre de Lancements Annuels',
                             markers=True)
                fig.update_traces(line=dict(color='#0d3b66', width=3))
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Évolution de la masse lancée
                yearly_mass = self.missions_data.groupby(
                    self.missions_data['date_lancement'].dt.year
                )['masse_charge_utile'].sum().reset_index()
                
                fig = px.area(yearly_mass, 
                             x='date_lancement', 
                             y='masse_charge_utile',
                             title='Évolution de la Masse Totale Lancée (kg)',
                             color_discrete_sequence=['#e37222'])
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Analyse de l'impact COVID sur le spatial
            st.subheader("Impact de la Pandémie COVID-19 sur les Activités Spatiales")
            
            # Simulation de l'impact COVID
            covid_period = self.missions_data[
                (self.missions_data['date_lancement'] >= '2020-01-01') & 
                (self.missions_data['date_lancement'] <= '2021-12-31')
            ]
            
            pre_covid = self.missions_data[
                (self.missions_data['date_lancement'] >= '2018-01-01') & 
                (self.missions_data['date_lancement'] <= '2019-12-31')
            ]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                lancements_pre = len(pre_covid)
                lancements_covid = len(covid_period)
                variation = ((lancements_covid - lancements_pre) / lancements_pre) * 100
                
                st.metric(
                    "Lancements Période COVID",
                    f"{lancements_covid}",
                    f"{variation:.1f}% vs pré-COVID"
                )
            
            with col2:
                masse_pre = pre_covid['masse_charge_utile'].sum()
                masse_covid = covid_period['masse_charge_utile'].sum()
                variation_masse = ((masse_covid - masse_pre) / masse_pre) * 100
                
                st.metric(
                    "Masse Lancée",
                    f"{masse_covid:,.0f} kg",
                    f"{variation_masse:.1f}% vs pré-COVID"
                )
            
            with col3:
                # Taux de réussite
                succes_pre = len(pre_covid[pre_covid['statut'] == 'Succès']) / len(pre_covid) * 100
                succes_covid = len(covid_period[covid_period['statut'] == 'Succès']) / len(covid_period) * 100
                
                st.metric(
                    "Taux de Réussite",
                    f"{succes_covid:.1f}%",
                    f"{(succes_covid - succes_pre):.1f}% vs pré-COVID"
                )
        
        with tab3:
            # Projections futures
            st.subheader("Projections 2024-2030")
            
            # Simulation de projections
            last_year = self.missions_data['date_lancement'].dt.year.max()
            future_years = list(range(last_year + 1, 2031))
            
            projection_data = []
            for year in future_years:
                # Croissance basée sur les tendances historiques
                base_lancements = 10  # Base pour les projections
                growth_rate = random.uniform(0.05, 0.15)  # Croissance de 5-15% par an
                
                lancements_projetes = int(base_lancements * (1 + growth_rate) ** (year - last_year))
                
                projection_data.append({
                    'annee': year,
                    'lancements': lancements_projetes,
                    'type': 'Projection'
                })
            
            df_projection = pd.DataFrame(projection_data)
            
            # Données historiques récentes
            historical = self.missions_data[self.missions_data['date_lancement'].dt.year >= 2018].copy()
            historical_yearly = historical.groupby(historical['date_lancement'].dt.year).size().reset_index(name='lancements')
            historical_yearly['type'] = 'Historique'
            historical_yearly = historical_yearly.rename(columns={'date_lancement': 'annee'})
            
            combined_data = pd.concat([historical_yearly, df_projection])
            
            fig = px.line(combined_data, 
                         x='annee', 
                         y='lancements',
                         color='type',
                         title='Projection des Lancements 2024-2030',
                         markers=True,
                         color_discrete_map={'Historique': '#0d3b66', 'Projection': '#e37222'})
            st.plotly_chart(fig, use_container_width=True)
    
    def create_csg_map(self):
        """Crée une carte du Centre Spatial Guyanais"""
        st.markdown('<h3 class="section-header">🗺️ CARTE DU CENTRE SPATIAL GUYANAIS</h3>', 
                   unsafe_allow_html=True)
        
        # Données des sites de lancement
        sites_data = {
            'Site': ['ELA-3', 'ELA-4', 'ELS', 'ELV'],
            'Description': [
                'Ensemble de Lancement Ariane 5 (Ariane 5)',
                'Ensemble de Lancement Ariane 6 (Ariane 6)',
                'Ensemble de Lancement Soyuz (Soyuz)',
                'Ensemble de Lancement Vega (Vega/Vega C)'
            ],
            'Latitude': [5.239, 5.232, 5.305, 5.304],
            'Longitude': [-52.768, -52.775, -52.834, -52.834],
            'Status': ['Actif', 'En construction', 'En pause', 'Actif'],
            'Lanceurs': ['Ariane 5', 'Ariane 6', 'Soyuz', 'Vega, Vega C']
        }
        
        df_sites = pd.DataFrame(sites_data)
        
        # Carte interactive
        fig = px.scatter_mapbox(df_sites, 
                              lat="Latitude", 
                              lon="Longitude", 
                              hover_name="Site",
                              hover_data={"Description": True, "Status": True, "Lanceurs": True},
                              color="Status",
                              size=[20, 15, 15, 20],  # Taille des points
                              zoom=10,
                              height=500,
                              title="Installations du Centre Spatial Guyanais")
        
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Légende et informations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🏗️ Sites de Lancement:**
            - **ELA-3:** Ariane 5 (Actif)
            - **ELA-4:** Ariane 6 (Construction)
            - **ELS:** Soyuz (Pause)
            - **ELV:** Vega/Vega C (Actif)
            """)
        
        with col2:
            st.markdown("""
            **📊 Caractéristiques:**
            - Surface totale: ~700 km²
            - Zone de sécurité: 1200 km²
            - Localisation: Kourou, Guyane française
            - Meilleure position pour lancements équatoriaux
            """)
    
    def create_sidebar(self):
        """Crée la sidebar avec les contrôles"""
        st.sidebar.markdown("## 🎛️ CONTRÔLES D'ANALYSE")
        
        # Filtres temporels
        st.sidebar.markdown("### 📅 Période d'analyse")
        date_debut = st.sidebar.date_input("Date de début", 
                                         value=datetime(2002, 1, 1))
        date_fin = st.sidebar.date_input("Date de fin", 
                                       value=datetime.now())
        
        # Filtres lanceurs
        st.sidebar.markdown("### 🚀 Sélection des lanceurs")
        lanceurs_selectionnes = st.sidebar.multiselect(
            "Lanceurs à afficher:",
            list(self.lanceurs.keys()),
            default=list(self.lanceurs.keys())[:3]
        )
        
        # Options d'affichage
        st.sidebar.markdown("### ⚙️ Options")
        auto_refresh = st.sidebar.checkbox("Rafraîchissement automatique", value=True)
        show_projections = st.sidebar.checkbox("Afficher les projections", value=True)
        
        # Bouton de rafraîchissement manuel
        if st.sidebar.button("🔄 Rafraîchir les données"):
            self.update_live_data()
            st.rerun()
        
        # Informations CSG
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🏛️ À PROPOS DU CSG")
        st.sidebar.markdown("""
        **Centre Spatial Guyanais**
        - Port spatial de l'Europe
        - Localisation: Kourou, Guyane
        - Meilleure position orbitale
        - Plus de 300 lancements depuis 1968
        """)
        
        return {
            'date_debut': date_debut,
            'date_fin': date_fin,
            'lanceurs_selectionnes': lanceurs_selectionnes,
            'auto_refresh': auto_refresh,
            'show_projections': show_projections
        }

    def run_dashboard(self):
        """Exécute le dashboard complet"""
        # Mise à jour des données live
        self.update_live_data()
        
        # Sidebar
        controls = self.create_sidebar()
        
        # Header
        self.display_header()
        
        # Métriques clés
        self.display_key_metrics()
        
        # Navigation par onglets
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "🚀 Lanceurs", 
            "📅 Missions", 
            "🏢 Clients", 
            "📈 Évolution", 
            "🗺️ CSG",
            "📊 Insights",
            "ℹ️ À Propos"
        ])
        
        with tab1:
            self.create_lanceurs_overview()
        
        with tab2:
            self.create_missions_live()
        
        with tab3:
            self.create_clients_analysis()
        
        with tab4:
            self.create_evolution_analysis()
        
        with tab5:
            self.create_csg_map()
        
        with tab6:
            st.markdown("## 📊 INSIGHTS STRATÉGIQUES")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 🎯 TENDANCES DU SPATIAL
                
                **📈 Nouveaux Marchés:**
                - Constellation de satellites (OneWeb, Starlink)
                - Services de lancement partagés
                - Développement du spatial commercial
                
                **🛰️ Évolution Technologique:**
                - Lanceurs réutilisables
                - Miniaturisation des satellites
                - Propulsion électrique
                
                **🌍 Défis Environnementaux:**
                - Réduction des débris spatiaux
                - Lanceurs plus écologiques
                - Surveillance environnementale
                """)
            
            with col2:
                st.markdown("""
                ### 🚨 DÉFIS OPÉRATIONNELS
                
                **⚡ Compétition Internationale:**
                - Concurrence de SpaceX, China Aerospace
                - Baisse des prix des lancements
                - Innovation technologique rapide
                
                **🌫️ Dépendances Géopolitiques:**
                - Relations internationales
                - Contrôles à l'exportation
                - Sécurité d'approvisionnement
                
                **🔧 Maintenance Infrastructure:**
                - Modernisation des installations
                - Adaptation aux nouveaux lanceurs
                - Formation du personnel
                """)
            
            st.markdown("""
            ### 💡 RECOMMANDATIONS STRATÉGIQUES
            
            1. **Innovation:** Développement d'Ariane 6 et nouveaux lanceurs
            2. **Diversification:** Marchés commerciaux et services
            3. **Collaboration:** Partenariats internationaux
            4. **Durabilité:** Lanceurs écologiques et gestion des débris
            5. **Formation:** Développement des compétences spatiales
            """)
        
        with tab7:
            st.markdown("## 📋 À propos de ce dashboard")
            st.markdown("""
            Ce dashboard présente une analyse complète des activités du Centre Spatial Guyanais,
            port spatial de l'Europe situé en Guyane française.
            
            **Couverture des données:**
            - Période: 2002-2025 (historique et projections)
            - Lanceurs: Ariane 5, Ariane 6, Vega, Vega C, Soyuz
            - Missions: Commerciales, institutionnelles, scientifiques
            - Clients: ESA, NASA, opérateurs commerciaux, etc.
            
            **Sources des données:**
            - Agence Spatiale Européenne (ESA)
            - Centre National d'Études Spatiales (CNES)
            - Arianespace
            - Données publiques et modèles prédictifs
            
            **⚠️ Note:** Les données sont simulées pour la démonstration.
            Les données réelles sont disponibles sur les sites officiels de l'ESA et du CNES.
            
            **🔒 Confidentialité:** Toutes les données sensibles sont anonymisées.
            """)
            
            st.markdown("---")
            st.markdown("""
            **📞 Contact:**
            - Site web: www.esa.int
            - Email: contact@esa.int
            - Centre Spatial Guyanais: Kourou, Guyane française
            """)
        
        # Rafraîchissement automatique
        if controls['auto_refresh']:
            time.sleep(30)  # Rafraîchissement toutes les 30 secondes
            st.rerun()

# Lancement du dashboard
if __name__ == "__main__":
    dashboard = GuyaneAerospatialeDashboard()
    dashboard.run_dashboard()