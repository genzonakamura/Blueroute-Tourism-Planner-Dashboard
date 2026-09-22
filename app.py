import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Blueroute Terengganu Tourism Planner Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Hero Title Gradient */
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #0284C7 0%, #0D9488 50%, #2563EB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        letter-spacing: -0.5px;
    }
    
    .hero-subtitle {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 20px;
        font-weight: 500;
    }

    /* Glassmorphism Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(2, 132, 199, 0.1);
        border-color: #38BDF8;
    }

    .metric-label {
        font-size: 0.82rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0F172A;
        margin: 6px 0;
    }

    .badge-alert { color: #E11D48; background: #FFE4E6; padding: 4px 10px; border-radius: 20px; font-weight: 700; font-size: 0.78rem; }
    .badge-good { color: #059669; background: #D1FAE5; padding: 4px 10px; border-radius: 20px; font-weight: 700; font-size: 0.78rem; }
    .badge-warn { color: #D97706; background: #FEF3C7; padding: 4px 10px; border-radius: 20px; font-weight: 700; font-size: 0.78rem; }

    .award-card {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: #FFFFFF;
        border-radius: 18px;
        padding: 20px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_terengganu_data():
    data = pd.DataFrame({
        'Destination': [
            'KTCC Mall & Miami Beach', 
            'Payang Central Market', 
            'Batu Buruk Beach', 
            'Redang Marine Sanctuary', 
            'Perhentian Coral Bay', 
            'Kenyir Eco-Lake & Sekayu'
        ],
        'District': ['Kuala Terengganu', 'Kuala Terengganu', 'Kuala Terengganu', 'Kuala Nerus', 'Besut', 'Hulu Terengganu'],
        'Category': ['Urban & Coast', 'Heritage & Cultural', 'Beach & Recreation', 'Island & Marine', 'Island & Marine', 'Nature & Rainforest'],
        'Lat': [5.3323, 5.3364, 5.3210, 5.7600, 5.9082, 4.9680],
        'Lon': [103.1415, 103.1360, 103.1490, 103.0100, 102.7350, 102.8250],
        'Base_Visitors': [8500, 7200, 6800, 5400, 4800, 1500],
        'Max_Capacity': [6000, 5500, 5000, 3500, 3000, 5000],
        'Eco_Rating': [3.5, 4.0, 3.8, 4.9, 4.8, 4.7],
        'Waste_Tons': [4.2, 3.8, 3.1, 2.7, 2.2, 0.8],
        'Highlight': ['Modern Waterfront & Shopping', 'Traditional Batik & Keropok Lekor', 'Kite Flying & Sunset Dining', 'Crystal Waters & Turtle Nesting', 'Coral Reef Scuba & Kayaking', 'Cascading Waterfalls & Elephant Sanctuary']
    })
    return data

df_base = load_terengganu_data()

df_historical = pd.DataFrame({
    'Year': [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026],
    'Arrivals_Millions': [13.74, 14.16, 7.42, 3.72, 10.23, 11.76, 12.80, 13.90, 14.95],
    'Category': ['Historical', 'Historical', 'Historical', 'Historical', 'Historical', 'Historical', 'Projected', 'Projected', 'Projected']
})


def build_interactive_map(df_map):
    fig = px.scatter(
        df_map,
        x="Lon",
        y="Lat",
        color="TPI_Score",
        size="Live_Visitors",
        hover_name="Destination",
        text="Destination",
        color_continuous_scale="Reds",
        size_max=30,
        title="Terengganu Spatial Heatmap"
    )
    
    fig.update_traces(textposition='top center')
    fig.update_layout(
        height=440,
        margin={"r":0, "t":30, "l":0, "b":0},
        xaxis_title="Longitude",
        yaxis_title="Latitude",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

st.sidebar.markdown("### 🌊 **BlueRoute Engine**")
st.sidebar.caption("Terengganu Tourism Intelligence")
st.sidebar.markdown("---")

nav_choice = st.sidebar.radio("📌 Navigation Hub:", [
    "🗺️ Spatial Crowd & Capacity Tracker",
    "🎮 Interactive Eco-Itinerary Quest",
    "📈 Tourism Analytics & SDG Impact"
])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ **Live Holiday Simulator**")
surge_percent = st.sidebar.slider("Simulate Peak Holiday Surge (%):", 0, 100, 20, step=5)

# Calculate live metrics based on surge
df_live = df_base.copy()
df_live['Live_Visitors'] = (df_live['Base_Visitors'] * (1 + surge_percent/100)).astype(int)
df_live['Capacity_Ratio'] = df_live['Live_Visitors'] / df_live['Max_Capacity']
df_live['TPI_Score'] = (df_live['Capacity_Ratio'] * 70).clip(0, 100).round(1)

def assign_status(score):
    if score >= 80: return 'Over Capacity 🚨'
    elif score >= 60: return 'High Density ⚠️'
    elif score >= 35: return 'Optimal Flow ✅'
    else: return 'Serene & Quiet 🌿'

df_live['Status'] = df_live['TPI_Score'].apply(assign_status)

if nav_choice == "🗺️ Spatial Crowd & Capacity Tracker":
    st.markdown('<div class="hero-title">Blueroute Terengganu Tourism Planner Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Real-Time Spatial Crowd Intelligence, Bottleneck Prevention & Eco-Load Monitoring</div>', unsafe_allow_html=True)

    # Key Performance Metric Cards
    t_vis = df_live['Live_Visitors'].sum()
    crit_spots = len(df_live[df_live['TPI_Score'] >= 80])
    avg_load = df_live['TPI_Score'].mean()
    tot_waste = (df_live['Waste_Tons'].sum() * (1 + surge_percent/100)).round(1)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">Active Tourists</div>
            <div class="metric-value">{t_vis:,}</div>
            <span class="badge-good">+{surge_percent}% Live Surge</span>
        </div>
        ''', unsafe_allow_html=True)

    with c2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">Overcapacity Hubs</div>
            <div class="metric-value">{crit_spots}</div>
            <span class="badge-alert">Requires Rerouting</span>
        </div>
        ''', unsafe_allow_html=True)

    with c3:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">Average Pressure</div>
            <div class="metric-value">{avg_load:.1f}%</div>
            <span class="badge-warn">State Load Index</span>
        </div>
        ''', unsafe_allow_html=True)

    with c4:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">Est. Waste Output</div>
            <div class="metric-value">{tot_waste} T/d</div>
            <span class="badge-good">Eco-Shuttles Active</span>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Main Visual Layout
    m_col, c_col = st.columns([1.3, 1])

    with m_col:
        st.markdown("##### 📍 Interactive Spatial Heatmap")
        st.plotly_chart(build_interactive_map(df_live), use_container_width=True)

    with c_col:
        st.markdown("##### 📊 Capacity Load vs Visitor Volume")
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            y=df_live['Destination'], x=df_live['Live_Visitors'],
            name='Current Visitors', orientation='h', marker_color='#0284C7'
        ))
        fig_bar.add_trace(go.Bar(
            y=df_live['Destination'], x=df_live['Max_Capacity'],
            name='Carrying Limit', orientation='h', marker_color='#E11D48'
        ))
        fig_bar.update_layout(
            barmode='group', height=440, margin=dict(l=0, r=0, t=10, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")
    
    # Real-Time Mitigation System
    st.markdown("##### ⚡ Smart Rerouting Directives")
    sel_loc = st.selectbox("Select location to inspect status & trigger actions:", df_live['Destination'].tolist())
    loc_data = df_live[df_live['Destination'] == sel_loc].iloc[0]

    if loc_data['TPI_Score'] >= 80:
        st.error(f"🚨 **{sel_loc}** is severely congested (TPI Score: {loc_data['TPI_Score']}/100)! **Recommended Action:** Activate electric shuttle rerouting to secondary locations (e.g. Kenyir Lake) and issue push notifications to arriving vehicles.")
    elif loc_data['TPI_Score'] >= 60:
        st.warning(f"⚠️ **{sel_loc}** is approaching high density (TPI Score: {loc_data['TPI_Score']}/100). **Recommended Action:** Stagger group bus entries and increase waste management dispatch frequency.")
    else:
        st.success(f"✅ **{sel_loc}** is operating within healthy ecological limits (TPI Score: {loc_data['TPI_Score']}/100). Perfect condition for visitors.")


elif nav_choice == "🎮 Interactive Eco-Itinerary Quest":
    st.markdown('<div class="hero-title">BlueRoute Eco-Itinerary Quest</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Design your dream Terengganu getaway, earn Green Badges, and minimize carbon footprint!</div>', unsafe_allow_html=True)

    col_form, col_result = st.columns([1, 1.2])

    with col_form:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("##### 🧳 Trip Customizer")
        
        target = st.selectbox("Where do you want to visit first?", df_base['Destination'].tolist())
        duration = st.slider("Trip Duration (Days):", 1, 7, 3)
        travel_mode = st.radio("Travel Preference:", ["🌱 Low-Carbon Eco Explorer", "⚡ Standard Hotspot Tour"])
        interests = st.multiselect("Your Favorite Activities:", ["Snorkeling & Marine Life", "Cultural Crafts & Food", "Waterfalls & Trekking", "Beach Relaxing"], default=["Snorkeling & Marine Life", "Cultural Crafts & Food"])
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col_result:
        selected_info = df_live[df_live['Destination'] == target].iloc[0]
        
        st.markdown("##### 🏆 Your Itinerary Impact Score")
        
        # Calculate Gamification Points
        eco_points = 100
        if selected_info['TPI_Score'] >= 60: eco_points -= 25
        if travel_mode == "🌱 Low-Carbon Eco Explorer": eco_points += 30
        
        co2_saved = round(duration * (14.2 if travel_mode == "🌱 Low-Carbon Eco Explorer" else 4.5), 1)

        c_a, c_b, c_c = st.columns(3)
        c_a.metric("Eco-Score", f"{eco_points} pts", "+15 vs Avg")
        c_b.metric("CO2 Saved", f"{co2_saved} kg", "Green Choice")
        c_c.metric("Crowd Level", selected_info['Status'])

        st.markdown("<br>", unsafe_allow_html=True)

        if selected_info['TPI_Score'] >= 60 and travel_mode == "🌱 Low-Carbon Eco Explorer":
            alt = df_live[df_live['TPI_Score'] < 50].iloc[0]
            st.warning(f"Note: **{target}** is quite crowded today!")
            st.markdown(f'''
            <div class="award-card">
                <b>🌿 BlueRoute Smart Swap Recommendation:</b><br>
                Consider swapping to <b>{alt['Destination']}</b> in {alt['District']}! <br>
                <i>Highlights: {alt['Highlight']}.</i>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="award-card">
                <b>🌟 Perfect Match Unlocked!</b><br>
                Your choice <b>{target}</b> aligns perfectly with your interests. Enjoy {selected_info['Highlight']}!
            </div>
            ''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.info(f"💡 **Eco Badge Earned**: You unlocked the **Terengganu Green Pioneer Badge** by choosing {travel_mode}!")

# ---------------------------------------------------------
# MODULE 3: TOURISM ANALYTICS & SDG IMPACT
# ---------------------------------------------------------
elif nav_choice == "📈 Tourism Analytics & SDG Impact":
    st.markdown('<div class="hero-title">State Growth & UN SDG Alignment</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Strategic forecast of tourist arrivals and direct alignment with UN Sustainable Development Goals</div>', unsafe_allow_html=True)

    t1, t2 = st.tabs(["📊 Visitor Arrival Forecasts (2018–2026)", "🎯 UN SDG Impact Scorecard"])

    with t1:
        st.markdown("##### Domestic & International Visitor Trends (Millions)")
        fig_trend = px.line(
            df_historical, x='Year', y='Arrivals_Millions', color='Category',
            markers=True, line_shape='spline',
            color_discrete_map={'Historical': '#0284C7', 'Projected': '#10B981'}
        )
        fig_trend.update_layout(yaxis_title="Visitors (Millions)", height=380)
        st.plotly_chart(fig_trend, use_container_width=True)
        st.caption("Historical source: Department of Statistics Malaysia (DOSM) & Terengganu Tourism Board.")

    with t2:
        st.markdown("##### 🌍 Sustainable Development Goals Framework")
        
        col_sdg1, col_sdg2 = st.columns(2)
        with col_sdg1:
            st.markdown("""
            <div class="metric-card">
                <h4 style="color:#0284C7; margin:0;">SDG 8: Decent Work & Economic Growth</h4>
                <p style="font-size:0.9rem; color:#475569;">Distributes tourism spending into rural districts like Hulu Terengganu & Besut, supporting local artisans, batik makers, and boat captains.</p>
            </div>
            <br>
            <div class="metric-card">
                <h4 style="color:#0D9488; margin:0;">SDG 9: Industry, Innovation & Infrastructure</h4>
                <p style="font-size:0.9rem; color:#475569;">Uses cutting-edge web dashboard technology and live capacity tracking to optimize smart tourism infrastructure.</p>
            </div>
            """, unsafe_allow_html=True)

        with col_sdg2:
            st.markdown("""
            <div class="metric-card">
                <h4 style="color:#D97706; margin:0;">SDG 12: Responsible Consumption</h4>
                <p style="font-size:0.9rem; color:#475569;">Monitors daily municipal solid waste across top attractions to prevent pollution and promote sustainable waste management.</p>
            </div>
            <br>
            <div class="metric-card">
                <h4 style="color:#2563EB; margin:0;">SDG 14: Life Below Water</h4>
                <p style="font-size:0.9rem; color:#475569;">Protects delicate marine ecosystems and coral reefs around Redang Marine Sanctuary and Perhentian Coral Bay.</p>
            </div>
            """, unsafe_allow_html=True)
