"""
app.py - Main Streamlit dashboard application
This brings everything together into an interactive web app
"""

import streamlit as st
import pandas as pd
from calculator import ArchitectureCalculator
from visualizations import (
    create_cost_comparison_chart,
    create_carbon_comparison_chart,
    create_radar_chart,
    create_score_gauge,
    create_comparison_table,
    create_annual_projection_chart
)
from data import PRICING, SECURITY_SCORES

# Page configuration
st.set_page_config(
    page_title="Green Tech Cloud Architecture Dashboard",
    page_icon="🌱",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #2E7D32;
        text-align: center;
        padding: 1rem;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .recommendation-box {
        background-color: #E8F5E9;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
    }
    .metric-card {
        background-color: #F5F5F5;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🌱 Green Tech Cloud Architecture Decision Tool</h1>', 
            unsafe_allow_html=True)
st.markdown('<p class="sub-header">Find the perfect balance between Security, Cost, and Sustainability</p>', 
            unsafe_allow_html=True)

# Sidebar for inputs
with st.sidebar:
    st.header(" Configure Your Workload")
    
    st.subheader("Workload Characteristics")
    storage_gb = st.slider(
        "Data Storage (GB)",
        min_value=100,
        max_value=10000,
        value=1000,
        step=100,
        help="How much data will you store?"
    )
    
    requests_millions = st.slider(
        "Monthly Requests (Millions)",
        min_value=1,
        max_value=1000,
        value=100,
        step=10,
        help="How many API requests per month?"
    )
    
    st.subheader("Priorities (1-10 scale)")
    st.info("Rate how important each factor is for your organization")
    
    cost_weight = st.slider(
        " Cost Optimization",
        min_value=1,
        max_value=10,
        value=5,
        help="How important is minimizing costs?"
    )
    
    carbon_weight = st.slider(
        " Environmental Impact",
        min_value=1,
        max_value=10,
        value=5,
        help="How important is reducing carbon footprint?"
    )
    
    security_weight = st.slider(
        " Security & Compliance",
        min_value=1,
        max_value=10,
        value=5,
        help="How important is maximum security?"
    )
    
    # Show current weights
    total_weight = cost_weight + carbon_weight + security_weight
    st.subheader("Weight Distribution")
    col1, col2, col3 = st.columns(3)
    col1.metric("Cost", f"{(cost_weight/total_weight)*100:.0f}%")
    col2.metric("Carbon", f"{(carbon_weight/total_weight)*100:.0f}%")
    col3.metric("Security", f"{(security_weight/total_weight)*100:.0f}%")

# Main content area
# Initialize calculator with user inputs
calculator = ArchitectureCalculator(
    storage_gb=storage_gb,
    requests_millions=requests_millions,
    cost_weight=cost_weight,
    carbon_weight=carbon_weight,
    security_weight=security_weight
)

# Get metrics and recommendation
metrics = calculator.get_all_metrics()
recommendation = calculator.get_recommendation()

# Display recommendation
st.header(" Recommendation")
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"""
<div class="recommendation-box">
<h2 style="color: #2E7D32;">Recommended: {recommendation['recommended']}</h2>
<p style="font-size: 1.1rem; color: #2E7D32;">
{recommendation['reason']}
</p>
<p style="margin-top: 1rem; color: #2E7D32;">
<strong>Overall Score: {recommendation['score']}/100</strong>
</p>
</div>
""", unsafe_allow_html=True)

with col2:
    fig_gauge = create_score_gauge(recommendation['score'], "Winner Score")
    st.plotly_chart(fig_gauge, use_container_width=True)

# Key Metrics Overview
st.header(" Key Metrics Comparison")

# Display comparison table
st.subheader("Detailed Comparison Table")
comparison_df = create_comparison_table(metrics)
st.dataframe(
    comparison_df,
    use_container_width=True,
    hide_index=True
)

# Visualizations in tabs
tab1, tab2, tab3, tab4 = st.tabs([" Cost Analysis", " Environmental Impact", 
                                   " Multi-Factor Analysis", " Projections"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        fig_cost = create_cost_comparison_chart(metrics)
        st.plotly_chart(fig_cost, use_container_width=True)
    with col2:
        fig_projection = create_annual_projection_chart(metrics)
        st.plotly_chart(fig_projection, use_container_width=True)
    
    # Cost insights
    st.info(f"""
    💡 **Cost Insights:**
    - Lowest monthly cost: {min(metrics.items(), key=lambda x: x[1]['monthly_cost'])[1]['name']} 
      (${min(metrics.items(), key=lambda x: x[1]['monthly_cost'])[1]['monthly_cost']:,.2f})
    - Highest monthly cost: {max(metrics.items(), key=lambda x: x[1]['monthly_cost'])[1]['name']} 
      (${max(metrics.items(), key=lambda x: x[1]['monthly_cost'])[1]['monthly_cost']:,.2f})
    - Potential annual savings by choosing the cheapest option: 
      ${(max(metrics.items(), key=lambda x: x[1]['annual_cost'])[1]['annual_cost'] - min(metrics.items(), key=lambda x: x[1]['annual_cost'])[1]['annual_cost']):,.2f}
    """)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        fig_carbon = create_carbon_comparison_chart(metrics)
        st.plotly_chart(fig_carbon, use_container_width=True)
    with col2:
        # Carbon equivalents
        st.subheader("🌳 Environmental Equivalents")
        for arch, data in metrics.items():
            annual_carbon = data['annual_carbon']
            trees_needed = annual_carbon / 21  # One tree absorbs ~21kg CO2/year
            st.metric(
                data['name'],
                f"{annual_carbon:.0f} kg CO₂/year",
                f"≈ {trees_needed:.0f} trees needed to offset"
            )
    
    st.success(f"""
    🌱 **Sustainability Insights:**
    - Most eco-friendly: {min(metrics.items(), key=lambda x: x[1]['monthly_carbon'])[1]['name']}
    - Choosing the greenest option would save {(max(metrics.items(), key=lambda x: x[1]['annual_carbon'])[1]['annual_carbon'] - min(metrics.items(), key=lambda x: x[1]['annual_carbon'])[1]['annual_carbon']):.0f} kg CO₂ per year
    - That's equivalent to planting {((max(metrics.items(), key=lambda x: x[1]['annual_carbon'])[1]['annual_carbon'] - min(metrics.items(), key=lambda x: x[1]['annual_carbon'])[1]['annual_carbon']) / 21):.0f} trees! 🌳
    """)

with tab3:
    fig_radar = create_radar_chart(metrics)
    st.plotly_chart(fig_radar, use_container_width=True)
    
    st.info("""
     **How to read the radar chart:**
    - Each colored area represents one architecture option
    - Larger area = better overall performance
    - Perfect solution would fill the entire circle
    - Your priorities determine which dimensions matter most
    """)

with tab4:
    st.subheader(" 12-Month Projections")
    
    col1, col2, col3 = st.columns(3)
    
    for i, (arch, data) in enumerate(metrics.items()):
        with [col1, col2, col3][i]:
            st.markdown(f"### {data['name']}")
            st.metric("Year 1 Cost", f"${data['annual_cost']:,.0f}")
            st.metric("Year 1 Carbon", f"{data['annual_carbon']:.0f} kg")
            st.metric("5-Year TCO", f"${data['annual_cost'] * 5:,.0f}")

# Architecture Details Expander
st.header(" Architecture Details")

for arch, data in metrics.items():
    with st.expander(f"{data['name']} - Detailed Information"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Technical Specifications")
            st.write(f"**Description:** {data['description']}")
            st.write(f"**Availability SLA:** {data['availability']}%")
            st.write(f"**Architecture Type:** {arch}")
            
            # Security breakdown
            st.markdown("### Security Features")
            security = SECURITY_SCORES[arch]
            for feature, score in security.items():
                if feature != 'total':
                    st.progress(score/100, text=f"{feature.replace('_', ' ').title()}: {score}/100")
        
        with col2:
            st.markdown("### Cost Breakdown")
            st.write(f"**Base Cost:** ${PRICING[arch]['base_cost']}")
            st.write(f"**Storage Cost:** ${PRICING[arch]['cost_per_gb']}/GB")
            st.write(f"**Request Cost:** ${PRICING[arch]['cost_per_million_requests']}/million")
            
            st.markdown("### Use Cases")
            if arch == 'rds_multi_az':
                st.write("✅ Mission-critical applications")
                st.write("✅ Financial data processing")
                st.write("✅ Healthcare systems requiring HIPAA compliance")
            elif arch == 'dynamodb':
                st.write("✅ IoT data ingestion")
                st.write("✅ Real-time analytics")
                st.write("✅ Variable/unpredictable workloads")
            else:
                st.write("✅ Web applications")
                st.write("✅ Development/testing environments")
                st.write("✅ Balanced production workloads")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 2rem;">
    <p>🌱 Green Tech Cloud Architecture Decision Tool v1.0</p>
    <p>Built with Streamlit, Python, and ❤️ for sustainable technology</p>
</div>
""", unsafe_allow_html=True)