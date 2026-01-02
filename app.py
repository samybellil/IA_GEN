import streamlit as st
import pandas as pd
import altair as alt
from streamlit_extras.metric_cards import style_metric_cards
from datetime import datetime, timedelta

# ================= CONFIG =================
st.set_page_config(page_title="Dashaalia Analytics", layout="wide", page_icon="📊")

# ================= CSS CUSTOM ULTRA PRO =================
st.markdown("""
<style>
/* Reset global */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}

/* Sidebar premium */
[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.95) !important;
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}

/* Cards avec effet verre */
.card {
    background: rgba(30, 41, 59, 0.7);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 24px;
    margin-bottom: 24px;
    transition: all 0.3s ease;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.card:hover {
    border-color: #3b82f6;
    transform: translateY(-2px);
    box-shadow: 0 12px 48px rgba(59, 130, 246, 0.15);
}

/* Titres */
h1, h2, h3 {
    background: linear-gradient(135deg, #60a5fa 0%, #8b5cf6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
}

/* Boutons et filtres premium */
.stSelectbox, .stMultiselect {
    background: rgba(30, 41, 59, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    color: white !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    background: rgba(30, 41, 59, 0.8) !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

/* Metrics cards */
[data-testid="stMetricValue"] {
    font-size: 2.5rem !important;
    font-weight: 700;
    background: linear-gradient(135deg, #60a5fa 0%, #8b5cf6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Séparateurs */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    margin: 2rem 0;
}

/* Badges */
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    margin: 2px;
}

.badge-success {
    background: rgba(34, 197, 94, 0.2);
    color: #22c55e;
    border: 1px solid rgba(34, 197, 94, 0.3);
}

.badge-warning {
    background: rgba(234, 179, 8, 0.2);
    color: #eab308;
    border: 1px solid rgba(234, 179, 8, 0.3);
}

/* KPI Grid */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 16px;
    margin: 24px 0;
}

/* Animation pour les cartes */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.card {
    animation: fadeIn 0.5s ease-out;
}

/* Scrollbar personnalisée */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(30, 41, 59, 0.5);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #60a5fa 0%, #8b5cf6 100%);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #3b82f6 0%, #7c3aed 100%);
}
</style>
""", unsafe_allow_html=True)

# ================= TITRE PREMIUM =================
col_title_left, col_title_center, col_title_right = st.columns([1, 2, 1])

with col_title_center:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 2.8rem; margin-bottom: 0.5rem;">📊 Dashaalia Analytics</h1>
        <p style="color: #94a3b8; font-size: 1.1rem; max-width: 600px; margin: 0 auto;">
            Plateforme d'analyse des sessions médicales augmentées par IA
        </p>
        <div style="display: flex; justify-content: center; gap: 12px; margin-top: 1rem;">
            <span class="badge badge-success">Temps réel</span>
            <span class="badge badge-warning">IA Integrée</span>
            <span class="badge" style="background: rgba(59, 130, 246, 0.2); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.3);">
                320 Sessions
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================= DATA =================
@st.cache_data
def load_data():
    df = pd.read_csv("sessions_dataset_320.csv")
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# ================= SIDEBAR PREMIUM =================
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0 2rem 0;">
        <h3 style="display: flex; align-items: center; gap: 10px;">
            <span>⚙️</span> Filtres Avancés
        </h3>
        <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 2rem;">
            Affinez votre analyse avec des filtres granulaires
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Date range filter premium
    st.markdown("**📅 Période**")
    col_date1, col_date2 = st.columns(2)
    with col_date1:
        date_min = st.date_input(
            "De",
            value=df['date'].min().date(),
            key="date_min",
            label_visibility="collapsed"
        )
    with col_date2:
        date_max = st.date_input(
            "À",
            value=df['date'].max().date(),
            key="date_max",
            label_visibility="collapsed"
        )
    
    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
    
    # Services avec icônes
    st.markdown("**🏥 Services Médicaux**")
    all_services = df['service'].unique()
    selected_services = st.multiselect(
        "Sélectionnez les services",
        options=all_services,
        default=all_services,
        label_visibility="collapsed"
    )
    
    # Langues avec drapeaux
    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
    st.markdown("**🌍 Langues**")
    
    # Mapping des langues vers des drapeaux
    flag_map = {
        'Anglais': '🇬🇧',
        'Espagnol': '🇪🇸', 
        'Arabe': '🇸🇦',
        'Mandarin': '🇨🇳',
        'Français': '🇫🇷',
        'Allemand': '🇩🇪',
        'Russe': '🇷🇺'
    }
    
    lang_options = [f"{flag_map.get(lang, '🌐')} {lang}" for lang in df['langue'].unique()]
    selected_langs_full = st.multiselect(
        "Sélectionnez les langues",
        options=lang_options,
        default=lang_options,
        label_visibility="collapsed"
    )
    selected_langs = [lang.split(' ', 1)[1] for lang in selected_langs_full]
    
    # Device avec icônes
    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
    st.markdown("**📱 Devices**")
    
    device_options = []
    for device in df['device'].unique():
        icon = "💻" if device.lower() == "web" else "📱"
        device_options.append(f"{icon} {device}")
    
    selected_devices_full = st.multiselect(
        "Sélectionnez les devices",
        options=device_options,
        default=device_options,
        label_visibility="collapsed"
    )
    selected_devices = [device.split(' ', 1)[1] for device in selected_devices_full]
    
    # Score de qualité slider
    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
    st.markdown("**⭐ Score de Qualité**")
    min_score, max_score = st.slider(
        "Plage de score",
        min_value=float(df['qualite_score'].min()),
        max_value=float(df['qualite_score'].max()),
        value=(float(df['qualite_score'].min()), float(df['qualite_score'].max())),
        step=0.1,
        label_visibility="collapsed"
    )
    
    # Bouton reset
    st.markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)
    if st.button("🔄 Réinitialiser les filtres", use_container_width=True):
        st.rerun()

# ================= FILTRAGE DES DONNÉES =================
filtered_df = df[
    (df['service'].isin(selected_services)) &
    (df['langue'].isin(selected_langs)) &
    (df['device'].isin(selected_devices)) &
    (df['qualite_score'] >= min_score) &
    (df['qualite_score'] <= max_score) &
    (df['date'].dt.date >= date_min) &
    (df['date'].dt.date <= date_max)
]

# ================= KPI GRID PREMIUM =================
st.markdown("<div class='card'>", unsafe_allow_html=True)

st.markdown("<h3>📈 Vue d'ensemble</h3>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style="text-align: center;">
        <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 8px;">Sessions totales</div>
        <div style="font-size: 2.2rem; font-weight: 700;">{:,}</div>
        <div style="font-size: 0.8rem; color: #22c55e; margin-top: 4px;">
            ↑ {:.1%} du dataset
        </div>
    </div>
    """.format(len(filtered_df), len(filtered_df)/len(df)), unsafe_allow_html=True)

with col2:
    avg_duration = filtered_df['duree_minutes'].mean()
    st.markdown("""
    <div style="text-align: center;">
        <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 8px;">Durée moyenne</div>
        <div style="font-size: 2.2rem; font-weight: 700;">{:.1f} min</div>
        <div style="font-size: 0.8rem; color: #22c55e; margin-top: 4px;">
            ⏱️ ±{:.1f} min écart-type
        </div>
    </div>
    """.format(avg_duration, filtered_df['duree_minutes'].std()), unsafe_allow_html=True)

with col3:
    avg_quality = filtered_df['qualite_score'].mean()
    quality_color = "#22c55e" if avg_quality >= 7.5 else "#eab308" if avg_quality >= 5 else "#ef4444"
    st.markdown("""
    <div style="text-align: center;">
        <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 8px;">Score qualité</div>
        <div style="font-size: 2.2rem; font-weight: 700; color: {};">{:.2f}/10</div>
        <div style="font-size: 0.8rem; color: {}; margin-top: 4px;">
            {} qualité
        </div>
    </div>
    """.format(quality_color, avg_quality, quality_color, 
              "Excellente" if avg_quality >= 7.5 else "Bonne" if avg_quality >= 5 else "À améliorer"), 
    unsafe_allow_html=True)

with col4:
    interactions_ratio = filtered_df['interactions_patient'].sum() / filtered_df['interactions_praticien'].sum() if filtered_df['interactions_praticien'].sum() > 0 else 0
    st.markdown("""
    <div style="text-align: center;">
        <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 8px;">Ratio Patient/Praticien</div>
        <div style="font-size: 2.2rem; font-weight: 700;">{:.2f}</div>
        <div style="font-size: 0.8rem; color: #3b82f6; margin-top: 4px;">
            {} interactions
        </div>
    </div>
    """.format(interactions_ratio, filtered_df[['interactions_patient', 'interactions_praticien']].sum().sum()), 
    unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ================= GRAPHIQUES PREMIUM =================
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3>📈 Évolution des sessions</h3>", unsafe_allow_html=True)
    
    # Préparation des données
    evolution_df = filtered_df.groupby(filtered_df['date'].dt.to_period('W')).size().reset_index(name='sessions')
    evolution_df['date'] = evolution_df['date'].astype(str)
    
    # Graphique évolution avec aire
    chart_evo = alt.Chart(evolution_df).mark_area(
        interpolate='monotone',
        line={'color': '#3b82f6', 'width': 3},
        color=alt.Gradient(
            gradient='linear',
            stops=[
                alt.GradientStop(color='rgba(59, 130, 246, 0.3)', offset=0),
                alt.GradientStop(color='rgba(59, 130, 246, 0)', offset=1)
            ]
        )
    ).encode(
        x=alt.X('date:N', title='Semaine', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('sessions:Q', title='Nombre de sessions'),
        tooltip=['date', 'sessions']
    ).properties(height=300)
    
    st.altair_chart(chart_evo, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Top langues
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3>🌍 Distribution par langue</h3>", unsafe_allow_html=True)
    
    langues_df = filtered_df['langue'].value_counts().reset_index()
    langues_df.columns = ['langue', 'count']
    langues_df['percentage'] = (langues_df['count'] / langues_df['count'].sum() * 100).round(1)
    
    # Bar chart horizontal avec pourcentages
    chart_lang = alt.Chart(langues_df).mark_bar(
        cornerRadiusTopRight=8,
        cornerRadiusBottomRight=8,
        color=alt.Gradient(
            gradient='linear',
            stops=[
                alt.GradientStop(color='#8b5cf6', offset=0),
                alt.GradientStop(color='#3b82f6', offset=1)
            ]
        )
    ).encode(
        y=alt.Y('langue:N', title='', sort='-x'),
        x=alt.X('count:Q', title='Nombre de sessions'),
        tooltip=['langue', 'count', alt.Tooltip('percentage:Q', title='Pourcentage', format='.1f')]
    ).properties(height=250)
    
    st.altair_chart(chart_lang, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    # Distribution par service
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3>🏥 Services les plus demandés</h3>", unsafe_allow_html=True)
    
    service_df = filtered_df['service'].value_counts().reset_index()
    service_df.columns = ['service', 'count']
    
    # Donut chart interactif
    chart_service = alt.Chart(service_df).mark_arc(
        innerRadius=80,
        outerRadius=140
    ).encode(
        theta=alt.Theta(field="count", type="quantitative"),
        color=alt.Color(field="service", type="nominal", 
                       scale=alt.Scale(scheme='tableau10'),
                       legend=alt.Legend(orient='bottom', title=None)),
        tooltip=['service', 'count', 
                alt.Tooltip('count:Q', title='Pourcentage', format='.1%')]
    ).properties(height=300)
    
    st.altair_chart(chart_service, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Interactions patient vs praticien
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3>💬 Analyse des interactions</h3>", unsafe_allow_html=True)
    
    interactions_melted = filtered_df[['interactions_patient', 'interactions_praticien']].mean().reset_index()
    interactions_melted.columns = ['type', 'moyenne']
    interactions_melted['type'] = interactions_melted['type'].replace({
        'interactions_patient': '👤 Patient',
        'interactions_praticien': '👨‍⚕️ Praticien'
    })
    
    # Bar chart groupé
    chart_inter = alt.Chart(interactions_melted).mark_bar(
        cornerRadiusTopLeft=8,
        cornerRadiusTopRight=8,
        width=50
    ).encode(
        x=alt.X('type:N', title='', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('moyenne:Q', title='Nombre moyen d\'interactions'),
        color=alt.Color('type:N', scale=alt.Scale(
            domain=['👤 Patient', '👨‍⚕️ Praticien'],
            range=['#8b5cf6', '#06b6d4']
        ), legend=None),
        tooltip=['type', alt.Tooltip('moyenne:Q', title='Moyenne', format='.2f')]
    ).properties(height=250)
    
    st.altair_chart(chart_inter, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ================= TABLEAU DE DONNÉES =================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h3>📋 Données détaillées</h3>", unsafe_allow_html=True)

# Statistiques résumées
col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

with col_stat1:
    st.metric("Note moyenne praticien", f"{filtered_df['note_praticien'].mean():.1f}/5")

with col_stat2:
    st.metric("Segments non reconnus", f"{filtered_df['segments_non_reconnus'].mean():.1f}")

with col_stat3:
    st.metric("Sessions mobile", 
             f"{len(filtered_df[filtered_df['device'] == 'mobile'])}",
             f"{len(filtered_df[filtered_df['device'] == 'mobile'])/len(filtered_df)*100:.1f}%")

with col_stat4:
    top_lang = filtered_df['langue'].mode()[0] if len(filtered_df) > 0 else "N/A"
    st.metric("Langue dominante", top_lang)

# Tableau avec échantillon
st.dataframe(
    filtered_df.head(10)[['date', 'service', 'langue', 'duree_minutes', 'qualite_score', 'note_praticien']],
    use_container_width=True,
    column_config={
        "date": st.column_config.DatetimeColumn("Date", format="DD/MM/YYYY"),
        "qualite_score": st.column_config.ProgressColumn(
            "Score qualité",
            format="%.1f",
            min_value=0,
            max_value=10
        ),
        "note_praticien": st.column_config.NumberColumn(
            "Note praticien",
            format="%.1f/5"
        )
    }
)

st.markdown("</div>", unsafe_allow_html=True)

# ================= FOOTER PREMIUM =================
st.markdown("""
<hr>
<div style="text-align: center; padding: 2rem 0; color: #64748b;">
    <div style="font-size: 0.9rem; margin-bottom: 0.5rem;">
        📊 Dashaalia Analytics • Dashboard v2.0 • 
        <span style="color: #3b82f6;">{:,} sessions analysées</span> • 
        Dernière mise à jour: {}
    </div>
    <div style="font-size: 0.8rem;">
        Projet B3 DEV IA • Interface optimisée pour analyse médicale • 
        <span style="color: #22c55e;">● Système opérationnel</span>
    </div>
</div>
""".format(len(filtered_df), datetime.now().strftime("%d/%m/%Y %H:%M")), unsafe_allow_html=True)