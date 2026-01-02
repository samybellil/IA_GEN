import streamlit as st
import pandas as pd
import altair as alt
from streamlit_extras.metric_cards import style_metric_cards
from datetime import datetime

# ================= CONFIG =================
st.set_page_config(
    page_title="Dashboard Dashaalia",
    layout="wide",
    page_icon="🏥"
)

# ================= CSS DARK MODE PREMIUM =================
st.markdown("""
<style>
    /* Fond dark mode élégant */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Cartes avec effet verre */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border-color: #3b82f6;
        transform: translateY(-2px);
        box-shadow: 0 12px 48px rgba(59, 130, 246, 0.15);
    }
    
    /* Titres avec gradient */
    h1, h2, h3 {
        background: linear-gradient(135deg, #60a5fa 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    /* KPI metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 700;
        background: linear-gradient(135deg, #60a5fa 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Badges colorés */
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
    
    .badge-info {
        background: rgba(59, 130, 246, 0.2);
        color: #3b82f6;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# ================= TITRE PREMIUM =================
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="font-size: 2.8rem; margin-bottom: 0.5rem;">🏥 Dashaalia Medical AI Dashboard</h1>
    <p style="color: #94a3b8; font-size: 1.1rem;">
        Analyse avancée des 320 sessions d'interprétariat médical augmenté par IA
    </p>
    <div style="display: flex; justify-content: center; gap: 12px; margin-top: 1rem;">
        <span class="badge badge-success">320 Sessions</span>
        <span class="badge badge-warning">IA Médicale</span>
        <span class="badge badge-info">Temps Réel</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= CHARGEMENT DES DONNÉES =================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("sessions_dataset_320.csv")
        
        # Convertir les colonnes dates
        df['date'] = pd.to_datetime(df['date'])
        
        # Calculer interactions_totales si pas déjà fait
        if 'interactions_totales' not in df.columns:
            df['interactions_totales'] = df['interactions_patient'] + df['interactions_praticien']
        
        # Vérifier et nettoyer les données
        st.sidebar.success(f"✅ {len(df)} sessions chargées")
        
        return df
    except Exception as e:
        st.error(f"Erreur de chargement : {e}")
        # Retourner un dataset exemple si le fichier n'existe pas
        return pd.DataFrame({
            'session_id': range(1, 321),
            'date': pd.date_range('2024-01-01', periods=320),
            'service': ['Cardiologie']*80 + ['Pédiatrie']*80 + ['Urgences']*80 + ['Radiologie']*80,
            'langue': ['Anglais']*100 + ['Français']*100 + ['Arabe']*60 + ['Espagnol']*60,
            'duree_minutes': np.random.randint(10, 120, 320),
            'interactions_patient': np.random.randint(5, 50, 320),
            'interactions_praticien': np.random.randint(5, 50, 320),
            'interactions_totales': np.random.randint(10, 100, 320),
            'note_praticien': np.random.uniform(1, 5, 320),
            'qualite_score': np.random.uniform(0.5, 1.0, 320),
            'segments_non_reconnus': np.random.randint(0, 10, 320),
            'device': ['webapp']*160 + ['mobile']*160
        })

df = load_data()

# ================= SIDEBAR AVANCÉ =================
with st.sidebar:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### ⚙️ Filtres Avancés")
    
    # Filtre par date
    st.markdown("**📅 Période**")
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    date_range = st.date_input(
        "Sélectionnez la période",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date
    
    # Filtre par service
    st.markdown("**🏥 Service Médical**")
    services = st.multiselect(
        "Sélectionnez les services",
        options=sorted(df['service'].unique()),
        default=sorted(df['service'].unique()),
        label_visibility="collapsed"
    )
    
    # Filtre par langue
    st.markdown("**🌍 Langue**")
    langues = st.multiselect(
        "Sélectionnez les langues",
        options=sorted(df['langue'].unique()),
        default=sorted(df['langue'].unique()),
        label_visibility="collapsed"
    )
    
    # Filtre par device
    st.markdown("**📱 Plateforme**")
    devices = st.multiselect(
        "Sélectionnez les devices",
        options=sorted(df['device'].unique()),
        default=sorted(df['device'].unique()),
        label_visibility="collapsed"
    )
    
    # Filtre par score de qualité
    st.markdown("**⭐ Score de Qualité**")
    qualite_min, qualite_max = st.slider(
        "Plage de score (0-1)",
        min_value=float(df['qualite_score'].min()),
        max_value=float(df['qualite_score'].max()),
        value=(float(df['qualite_score'].min()), float(df['qualite_score'].max())),
        step=0.01,
        label_visibility="collapsed"
    )
    
    # Bouton reset
    if st.button("🔄 Réinitialiser tous les filtres", use_container_width=True):
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# ================= APPLICATION DES FILTRES =================
filtered_df = df[
    (df['date'].dt.date >= start_date) &
    (df['date'].dt.date <= end_date) &
    (df['service'].isin(services)) &
    (df['langue'].isin(langues)) &
    (df['device'].isin(devices)) &
    (df['qualite_score'] >= qualite_min) &
    (df['qualite_score'] <= qualite_max)
]

# ================= KPI CARDS =================
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    sessions_count = len(filtered_df)
    st.metric(
        "📊 Sessions analysées",
        f"{sessions_count:,}",
        f"{sessions_count/len(df)*100:.1f}% du total"
    )

with col2:
    avg_duration = filtered_df['duree_minutes'].mean()
    st.metric(
        "⏱️ Durée moyenne",
        f"{avg_duration:.1f} min",
        f"±{filtered_df['duree_minutes'].std():.1f} min"
    )

with col3:
    avg_quality = filtered_df['qualite_score'].mean()
    quality_color = "#22c55e" if avg_quality >= 0.8 else "#eab308" if avg_quality >= 0.6 else "#ef4444"
    st.metric(
        "⭐ Score qualité moyen",
        f"{avg_quality:.2%}",
        delta_color="off",
        help="0-100% (plus haut = meilleur)"
    )

with col4:
    avg_note = filtered_df['note_praticien'].mean()
    st.metric(
        "👨‍⚕️ Note praticien",
        f"{avg_note:.1f}/5",
        f"{filtered_df['note_praticien'].std():.1f} écart-type"
    )

st.markdown("</div>", unsafe_allow_html=True)

# ================= VISUALISATIONS =================
col_left, col_right = st.columns(2)

with col_left:
    # ÉVOLUTION DES SESSIONS
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 📈 Évolution temporelle")
    
    evolution_df = filtered_df.groupby(filtered_df['date'].dt.to_period('W')).size().reset_index(name='sessions')
    evolution_df['date'] = evolution_df['date'].astype(str)
    
    chart_evo = alt.Chart(evolution_df).mark_area(
        interpolate='monotone',
        line={'color': '#3b82f6', 'width': 3},
        color=alt.Gradient(
            gradient='linear',
            stops=[
                alt.GradientStop(color='rgba(59, 130, 246, 0.4)', offset=0),
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
    
    # RÉPARTITION PAR LANGUE
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 🌍 Distribution par langue")
    
    langues_df = filtered_df['langue'].value_counts().reset_index()
    langues_df.columns = ['langue', 'count']
    
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
        tooltip=['langue', 'count']
    ).properties(height=250)
    
    st.altair_chart(chart_lang, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    # RÉPARTITION PAR SERVICE
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 🏥 Services médicaux")
    
    service_df = filtered_df['service'].value_counts().reset_index()
    service_df.columns = ['service', 'count']
    
    chart_service = alt.Chart(service_df).mark_arc(
        innerRadius=60,
        outerRadius=120
    ).encode(
        theta=alt.Theta(field="count", type="quantitative"),
        color=alt.Color(field="service", type="nominal", 
                       scale=alt.Scale(scheme='tableau10'),
                       legend=alt.Legend(orient='right', title=None)),
        tooltip=['service', 'count']
    ).properties(height=300)
    
    st.altair_chart(chart_service, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # INTERACTIONS PATIENT vs PRATICIEN
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 💬 Analyse des interactions")
    
    interactions_avg = filtered_df[['interactions_patient', 'interactions_praticien']].mean().reset_index()
    interactions_avg.columns = ['type', 'moyenne']
    interactions_avg['type'] = interactions_avg['type'].replace({
        'interactions_patient': '👤 Patient',
        'interactions_praticien': '👨‍⚕️ Praticien'
    })
    
    chart_inter = alt.Chart(interactions_avg).mark_bar(
        cornerRadiusTopLeft=8,
        cornerRadiusTopRight=8,
        width=60
    ).encode(
        x=alt.X('type:N', title='', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('moyenne:Q', title='Nombre moyen d\'interactions'),
        color=alt.Color('type:N', scale=alt.Scale(
            domain=['👤 Patient', '👨‍⚕️ Praticien'],
            range=['#8b5cf6', '#06b6d4']
        ), legend=None),
        tooltip=['type', alt.Tooltip('moyenne:Q', title='Moyenne', format='.1f')]
    ).properties(height=250)
    
    st.altair_chart(chart_inter, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ================= ANALYSE DE LA QUALITÉ =================
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.markdown("### 🔍 Analyse détaillée de la qualité")

col_q1, col_q2, col_q3, col_q4 = st.columns(4)

with col_q1:
    segments_moy = filtered_df['segments_non_reconnus'].mean()
    st.metric("🎧 Segments non reconnus", f"{segments_moy:.1f}", 
              f"Total: {filtered_df['segments_non_reconnus'].sum():.0f}")

with col_q2:
    qualite_median = filtered_df['qualite_score'].median()
    st.metric("📊 Médiane qualité", f"{qualite_median:.2%}")

with col_q3:
    mobile_sessions = len(filtered_df[filtered_df['device'] == 'mobile'])
    st.metric("📱 Sessions mobile", f"{mobile_sessions}",
              f"{mobile_sessions/len(filtered_df)*100:.1f}%")

with col_q4:
    web_sessions = len(filtered_df[filtered_df['device'] == 'webapp'])
    st.metric("💻 Sessions web", f"{web_sessions}",
              f"{web_sessions/len(filtered_df)*100:.1f}%")

# Histogramme de la qualité
qualite_hist = alt.Chart(filtered_df).transform_bin(
    'qualite_bin', field='qualite_score', bin=alt.Bin(maxbins=20)
).transform_aggregate(
    count='count()', groupby=['qualite_bin']
).mark_bar(
    color='#10b981',
    cornerRadiusTopLeft=5,
    cornerRadiusTopRight=5
).encode(
    x=alt.X('qualite_bin:Q', title='Score de qualité (0-1)', bin='binned'),
    y=alt.Y('count:Q', title='Nombre de sessions'),
    tooltip=['qualite_bin:Q', 'count:Q']
).properties(height=200)

st.altair_chart(qualite_hist, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ================= TABLEAU DES DONNÉES =================
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.markdown("### 📋 Données détaillées des sessions")

# Sélection de colonnes à afficher
columns_to_show = ['date', 'service', 'langue', 'duree_minutes', 
                   'note_praticien', 'qualite_score', 'device']

st.dataframe(
    filtered_df[columns_to_show].head(20),
    use_container_width=True,
    column_config={
        "date": st.column_config.DatetimeColumn("Date", format="DD/MM/YYYY"),
        "duree_minutes": st.column_config.NumberColumn("Durée (min)", format="%.0f"),
        "note_praticien": st.column_config.NumberColumn("Note", format="%.1f/5"),
        "qualite_score": st.column_config.ProgressColumn(
            "Score qualité",
            format="%.2f",
            min_value=0,
            max_value=1
        )
    }
)

# Bouton d'export
if st.button("📥 Exporter les données filtrées (CSV)", use_container_width=True):
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Télécharger CSV",
        data=csv,
        file_name=f"dashaalia_export_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv"
    )

st.markdown("</div>", unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("""
<hr>
<div style="text-align: center; padding: 2rem 0; color: #64748b;">
    <div style="font-size: 0.9rem; margin-bottom: 0.5rem;">
        🚀 Dashboard Dashaalia • Projet B3 DEV IA • 
        <span style="color: #3b82f6;">Analyse de {:,} sessions</span> • 
        Généré avec Streamlit & Altair
    </div>
    <div style="font-size: 0.8rem;">
        Interface médicale augmentée par IA • 
        <span style="color: #22c55e;">● Système opérationnel</span> • 
        Dernière mise à jour: {}
    </div>
</div>
""".format(len(filtered_df), datetime.now().strftime("%d/%m/%Y %H:%M")), unsafe_allow_html=True)