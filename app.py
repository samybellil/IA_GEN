import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_extras.metric_cards import style_metric_cards
import altair as alt


# ================= CONFIG =================
st.set_page_config(page_title="Dashboard Dashaalia", layout="wide")

# ================= DARK MODE CSS =================
st.markdown(
    """
    <style>
    body { background-color: #0f172a; color: #e5e7eb; }
    .section {
        background-color: #020617;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.6);
        margin-bottom: 25px;
    }
    h1, h2, h3 { color: #f9fafb; }
    .stMetric { background-color: #020617; }
    </style>
    """,
    unsafe_allow_html=True
)

# ================= TITLE =================
st.markdown("<h1 style='text-align:center;'>📊 Dashboard Analytique – Dashaalia</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#9ca3af;'>Analyse avancée des sessions d'interprétariat médical augmentées par IA</p>", unsafe_allow_html=True)
st.write("")

# ================= DATA =================
@st.cache_data
def load_data():
    df = pd.read_csv("sessions_dataset_320.csv")
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# ================= SIDEBAR =================
st.sidebar.header("🔎 Filtres avancés")
services = st.sidebar.multiselect("Service médical", df['service'].unique(), df['service'].unique())
langues = st.sidebar.multiselect("Langue", df['langue'].unique(), df['langue'].unique())
devices = st.sidebar.multiselect("Device", df['device'].unique(), df['device'].unique())

filtered_df = df[
    (df['service'].isin(services)) &
    (df['langue'].isin(langues)) &
    (df['device'].isin(devices))
]

# ================= KPI =================
st.markdown("<div class='section'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
col1.metric("📊 Sessions", len(filtered_df))
col2.metric("⏱️ Durée moyenne (min)", round(filtered_df['duree_minutes'].mean(), 2))
qualite = round(filtered_df['qualite_score'].mean(), 2)
col3.metric("⭐ Qualité moyenne", qualite)
style_metric_cards(background_color="#020617")
st.markdown("</div>", unsafe_allow_html=True)

# ================= EVOLUTION =================
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📈 Évolution du nombre de sessions")

# Préparer les données pour Altair
evolution_df = filtered_df.groupby(filtered_df['date'].dt.to_period('M')).size().reset_index(name='sessions')
evolution_df['date'] = evolution_df['date'].astype(str)

# Créer le graphique Altair moderne
chart_evo = alt.Chart(evolution_df).mark_line(
    point={'size': 80},
    color='#3b82f6',
    strokeWidth=3
).encode(
    x=alt.X('date:N', title='Mois', axis=alt.Axis(labelAngle=-45)),
    y=alt.Y('sessions:Q', title='Nombre de sessions'),
    tooltip=['date', 'sessions']
).properties(
    height=300,
    title='Évolution mensuelle des sessions'
)

st.altair_chart(chart_evo, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ================= LANGUES / SERVICES =================
colA, colB = st.columns(2)

with colA:
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("🌍 Top des langues")
    
    # Préparer les données pour Altair
    langues_df = filtered_df['langue'].value_counts().reset_index()
    langues_df.columns = ['langue', 'count']
    
    # Créer le graphique Altair pour les langues
    chart_langues = alt.Chart(langues_df).mark_bar(
        color='#10b981',
        cornerRadiusTopLeft=5,
        cornerRadiusTopRight=5
    ).encode(
        x=alt.X('count:Q', title='Nombre de sessions'),
        y=alt.Y('langue:N', title='Langue', sort='-x'),
        tooltip=['langue', 'count']
    ).properties(
        height=300
    )
    
    st.altair_chart(chart_langues, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with colB:
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("🏥 Répartition par service")
    
    # Préparer les données pour Altair (camembert interactif)
    service_df = filtered_df['service'].value_counts().reset_index()
    service_df.columns = ['service', 'count']
    
    # Créer un camembert interactif avec Altair
    chart_service = alt.Chart(service_df).mark_arc(
        innerRadius=50
    ).encode(
        theta=alt.Theta(field="count", type="quantitative"),
        color=alt.Color(field="service", type="nominal", 
                       scale=alt.Scale(scheme='set2')),
        tooltip=['service', 'count', alt.Tooltip('count:Q', title='Pourcentage', format='.1%')]
    ).properties(
        height=300,
        width=300
    )
    
    st.altair_chart(chart_service, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ================= INTERACTIONS =================
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("💬 Interactions patient / praticien")

# Préparer les données pour Altair
interactions_avg = filtered_df[['interactions_patient', 'interactions_praticien']].mean().reset_index()
interactions_avg.columns = ['type', 'moyenne']
interactions_avg['type'] = interactions_avg['type'].replace({
    'interactions_patient': 'Patient',
    'interactions_praticien': 'Praticien'
})

# Créer le graphique Altair pour les interactions
chart_interactions = alt.Chart(interactions_avg).mark_bar(
    cornerRadiusTopLeft=5,
    cornerRadiusTopRight=5
).encode(
    x=alt.X('type:N', title='Type d\'interaction'),
    y=alt.Y('moyenne:Q', title='Nombre moyen d\'interactions'),
    color=alt.Color('type:N', scale=alt.Scale(
        domain=['Patient', 'Praticien'],
        range=['#8b5cf6', '#06b6d4']
    )),
    tooltip=['type', alt.Tooltip('moyenne:Q', title='Moyenne', format='.2f')]
).properties(
    height=300
)

st.altair_chart(chart_interactions, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ================= NOTES =================
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("⭐ Notes des praticiens")

# Créer un histogramme Altair pour les notes
chart_notes = alt.Chart(filtered_df).mark_bar(
    color='#f59e0b',
    cornerRadiusTopLeft=5,
    cornerRadiusTopRight=5
).encode(
    alt.X('note_praticien:Q', bin=alt.Bin(maxbins=10), title='Note'),
    alt.Y('count()', title='Nombre de sessions'),
    tooltip=['count()']
).properties(
    height=300
)

st.altair_chart(chart_notes, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.caption("Projet B3 DEV IA – Dashboard analytique (Dark Mode)")