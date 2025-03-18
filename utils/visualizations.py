import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_salary_evolution(salary_projection, title="Salary Evolution"):
    df = pd.DataFrame(salary_projection)
    
    # Create figure
    fig = px.line(
        df, 
        x="year", 
        y=["monthly_salary", "monthly_with_bonus"] if "monthly_with_bonus" in df.columns else "monthly_salary",
        title=title,
        labels={"value": "Salary (COP)", "year": "Year", "variable": "Type"}
    )
    
    # Update layout
    fig.update_layout(
        hovermode="x unified",
        legend_title="Salary Component",
        template="plotly_white"
    )
    
    return fig

def plot_payroll_projection(payroll_projections):
    fig = make_subplots(
        rows=1, cols=1,
        subplot_titles=("Total Full-time Faculty Payroll Projection"),
        specs=[[{"type": "scatter"}]],
        vertical_spacing=0.1
    )
    
    # Add traces for total payroll (only full-time)
    fig.add_trace(
        go.Scatter(
            x=payroll_projections["year"], 
            y=payroll_projections["total_planta"],
            mode="lines+markers",
            name="Full-time Faculty",
            line=dict(color="crimson", width=4),
            marker=dict(size=10)
        ),
        row=1, col=1
    )
    
    # Update layout
    fig.update_layout(
        title="Full-time Faculty Payroll Projection Over Time",
        height=600,
        hovermode="x unified",
        template="plotly_white"
    )
    
    # Update y-axes
    fig.update_yaxes(title_text="Annual Cost (COP)", row=1, col=1)
    
    # Update x-axes
    fig.update_xaxes(title_text="Year", row=1, col=1)
    
    return fig

def plot_faculty_distribution(payroll_data):
    planta_df = payroll_data["planta_salaries"]
    
    planta_category_fig = px.pie(
        planta_df, 
        names="category",
        title="Full-time Faculty by Category",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    planta_degree_fig = px.pie(
        planta_df, 
        names="highest_degree",
        title="Full-time Faculty by Highest Degree",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    # Update layouts
    for fig in [planta_category_fig, planta_degree_fig]:
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            uniformtext_minsize=12, 
            uniformtext_mode='hide',
            template="plotly_white"
        )
    
    return planta_category_fig, planta_degree_fig

def plot_salary_distribution(payroll_data):
    planta_df = payroll_data["planta_salaries"]
    
    # Create histogram for full-time faculty salaries
    planta_hist = px.histogram(
        planta_df,
        x="monthly_salary",
        title="Distribution of Full-time Faculty Salaries",
        labels={"monthly_salary": "Monthly Salary (COP)"},
        marginal="box",
        color="category",
        nbins=20
    )
    
    # Update layout
    planta_hist.update_layout(
        barmode="overlay",
        template="plotly_white"
    )
    
    # Create box plot by category/degree
    planta_box = px.box(
        planta_df,
        x="category",
        y="monthly_salary",
        color="highest_degree",
        title="Full-time Faculty Salary by Category and Degree",
        labels={"monthly_salary": "Monthly Salary (COP)", "category": "Category"}
    )
    
    # Update layout
    planta_box.update_layout(template="plotly_white")
    
    return planta_hist, planta_box

def plot_payroll_breakdown(payroll_data):
    stats = payroll_data["payroll_stats"]
    
    # Create data for the sunburst chart (only full-time)
    sunburst_data = [
        # Level 1: Total Payroll (only full-time)
        {"id": "Total", "parent": "", "value": stats["planta"]["total_annual"]},
        
        # Level 2: Full-time Categories
        {"id": "Auxiliar", "parent": "Total", 
         "value": stats["planta"]["total_annual"] * 0.3},  # Approximate
        {"id": "Asistente", "parent": "Total", 
         "value": stats["planta"]["total_annual"] * 0.3},  # Approximate
        {"id": "Asociado", "parent": "Total", 
         "value": stats["planta"]["total_annual"] * 0.25},  # Approximate
        {"id": "Titular", "parent": "Total", 
         "value": stats["planta"]["total_annual"] * 0.15}   # Approximate
    ]
    
    # Create DataFrame
    sunburst_df = pd.DataFrame(sunburst_data)
    
    # Create sunburst chart
    fig = px.sunburst(
        sunburst_df,
        ids="id",
        parents="parent",
        values="value",
        title="Full-time Faculty Payroll Breakdown by Category",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    
    # Update layout
    fig.update_layout(
        template="plotly_white",
        margin=dict(t=60, l=0, r=0, b=0)
    )
    
    return fig