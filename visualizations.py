"""
visualizations.py - Creates all our charts and graphs
Visualizations help people understand complex data quickly
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def create_cost_comparison_chart(metrics):
    """
    Create a bar chart comparing costs across architectures
    """
    architectures = list(metrics.keys())
    monthly_costs = [metrics[arch]['monthly_cost'] for arch in architectures]
    names = [metrics[arch]['name'] for arch in architectures]
    
    fig = go.Figure(data=[
        go.Bar(
            x=names,
            y=monthly_costs,
            text=[f'${cost:,.0f}' for cost in monthly_costs],
            textposition='auto',
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1']
        )
    ])
    
    fig.update_layout(
        title='Monthly Cost Comparison',
        yaxis_title='Cost (USD)',
        xaxis_title='Architecture Option',
        showlegend=False,
        height=400
    )
    
    return fig

def create_carbon_comparison_chart(metrics):
    """
    Create a bar chart comparing carbon footprints
    """
    architectures = list(metrics.keys())
    carbon = [metrics[arch]['monthly_carbon'] for arch in architectures]
    names = [metrics[arch]['name'] for arch in architectures]
    
    fig = go.Figure(data=[
        go.Bar(
            x=names,
            y=carbon,
            text=[f'{c:.1f} kg' for c in carbon],
            textposition='auto',
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1']
        )
    ])
    
    fig.update_layout(
        title='Monthly Carbon Footprint',
        yaxis_title='CO₂ Emissions (kg)',
        xaxis_title='Architecture Option',
        showlegend=False,
        height=400
    )
    
    return fig

def create_radar_chart(metrics):
    """
    Create a radar chart showing all dimensions for each architecture.
    Radar charts are great for comparing multiple variables at once.
    """
    
    categories = ['Cost\nEfficiency', 'Carbon\nEfficiency', 'Security\nScore', 'Availability']
    
    fig = go.Figure()
    
    colors = {
        'rds_multi_az': '#FF6B6B',
        'dynamodb': '#4ECDC4',
        'aurora_serverless': '#45B7D1'
    }
    
    for arch in metrics.keys():
        # Normalize values for radar chart (0-100 scale)
        cost_efficiency = max(0, 100 - (metrics[arch]['monthly_cost'] / 10))
        carbon_efficiency = max(0, 100 - metrics[arch]['monthly_carbon'])
        security = metrics[arch]['security_score']
        availability = metrics[arch]['availability']
        
        fig.add_trace(go.Scatterpolar(
            r=[cost_efficiency, carbon_efficiency, security, availability],
            theta=categories,
            fill='toself',
            name=metrics[arch]['name'],
            line_color=colors[arch]
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Multi-Dimensional Comparison",
        height=500
    )
    
    return fig

def create_score_gauge(score, title="Overall Score"):
    """
    Create a gauge chart showing the overall score.
    Gauge charts are like speedometers - easy to understand at a glance.
    """
    
    # Determine color based on score
    if score >= 80:
        color = "#4ECDC4"  # Green
    elif score >= 60:
        color = "#45B7D1"  # Blue
    else:
        color = "#FF6B6B"  # Red
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title},
        delta = {'reference': 70},  # Benchmark score
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig

def create_comparison_table(metrics):
    """
    Create a detailed comparison table.
    Tables are best for showing exact values.
    """
    
    data = []
    for arch, values in metrics.items():
        data.append({
            'Architecture': values['name'],
            'Monthly Cost': f"${values['monthly_cost']:,.2f}",
            'Annual Cost': f"${values['annual_cost']:,.2f}",
            'Carbon (kg/month)': f"{values['monthly_carbon']:.1f}",
            'Security Score': f"{values['security_score']}/100",
            'Availability': f"{values['availability']}%",
            'Overall Score': f"{values['overall_score']:.1f}"
        })
    
    df = pd.DataFrame(data)
    return df

def create_annual_projection_chart(metrics, months=12):
    """
    Create a line chart showing cost projection over time
    """
    
    fig = go.Figure()
    
    colors = {
        'rds_multi_az': '#FF6B6B',
        'dynamodb': '#4ECDC4',
        'aurora_serverless': '#45B7D1'
    }
    
    months_range = list(range(1, months + 1))
    
    for arch in metrics.keys():
        monthly_cost = metrics[arch]['monthly_cost']
        cumulative_costs = [monthly_cost * m for m in months_range]
        
        fig.add_trace(go.Scatter(
            x=months_range,
            y=cumulative_costs,
            mode='lines+markers',
            name=metrics[arch]['name'],
            line=dict(color=colors[arch], width=2),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        title='12-Month Cost Projection',
        xaxis_title='Months',
        yaxis_title='Cumulative Cost (USD)',
        hovermode='x unified',
        height=400
    )
    
    return fig