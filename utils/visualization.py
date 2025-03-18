import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def plot_salary_evolution(input_data):
    initial_year = input_data["initial_year"]
    years_to_simulate = input_data["years_to_simulate"]
    annual_articles = input_data["annual_articles"]
    annual_books = input_data["annual_books"]
    initial_point_value = input_data["initial_point_value"]
    annual_point_increase_pct = input_data["annual_point_increase_pct"] / 100
    inflation_adjusted = input_data["inflation_adjusted"]
    annual_inflation = input_data["annual_inflation"] / 100 if inflation_adjusted else 0
    
    years = list(range(initial_year, initial_year + years_to_simulate + 1))
    salaries = []
    real_salaries = []
    point_values = []
    education_levels = []
    career_events = []
    cumulative_earnings = [0]
    
    current_year = initial_year
    total_articles = 0
    total_books = 0
    
    # Solo mantener la parte de Full-time Professor
    has_undergraduate = True
    has_specialization = "Specialization" in input_data["education_path"]
    has_masters = "Master's" in input_data["education_path"]
    has_doctorate = "Doctorate" in input_data["education_path"]
    category = input_data["initial_category"]
    administrative_position = "None"
    
    future_education = {}
    for i, edu in enumerate(input_data["education_path"]):
        if i > 0:
            achievement_year = initial_year + np.random.randint(1, min(10, years_to_simulate))
            future_education[achievement_year] = edu
    
    # Simulate year by year
    for year_idx, year in enumerate(years):
        # Update point value for the year
        point_value = initial_point_value * (1 + annual_point_increase_pct) ** year_idx
        point_values.append(point_value)
        
        # Check for education level changes this year
        if year in future_education:
            new_education = future_education[year]
            
            # Solo mantener la parte de Full-time Professor
            if new_education == "Specialization":
                has_specialization = True
                event_description = "Completed Specialization"
            elif new_education == "Master's":
                has_masters = True
                event_description = "Completed Master's Degree"
            elif new_education == "Doctorate":
                has_doctorate = True
                event_description = "Completed Doctorate"
            
            # Record career event
            career_events.append({
                "Year": year,
                "Event": event_description,
                "Event Type": "Education",
                "Impact": 10  # Impact size for visualization
            })
        
        # Check for category promotion (for full-time professors)
        if year_idx > 0 and year_idx % 5 == 0:
            if category == "Auxiliary Professor":
                category = "Assistant Professor"
                event_description = "Promoted to Assistant Professor"
            elif category == "Assistant Professor":
                category = "Associate Professor"
                event_description = "Promoted to Associate Professor"
            elif category == "Associate Professor":
                category = "Full Professor"
                event_description = "Promoted to Full Professor"
            else:
                event_description = None
            
            if event_description:
                # Record career event
                career_events.append({
                    "Year": year,
                    "Event": event_description,
                    "Event Type": "Promotion",
                    "Impact": 15  # Impact size for visualization
                })
        
        # Increment articles and books (rounded to nearest whole number)
        if year_idx > 0:  # Skip the first year
            new_articles = np.random.poisson(annual_articles)
            new_books = 1 if np.random.random() < annual_books else 0
            
            total_articles += new_articles
            total_books += new_books
            
            # Record significant publication events
            if new_articles >= 3:
                career_events.append({
                    "Year": year,
                    "Event": f"Published {new_articles} research articles",
                    "Event Type": "Publication",
                    "Impact": 8  # Impact size for visualization
                })
            
            if new_books > 0:
                career_events.append({
                    "Year": year,
                    "Event": f"Published {new_books} book(s)",
                    "Event Type": "Publication",
                    "Impact": 12  # Impact size for visualization
                })
        
        # Calculate salary for the year - solo para Full-time Professor
        input_data_salary = {
            "has_undergraduate": has_undergraduate,
            "specialization": has_specialization,
            "masters": has_masters,
            "doctorate": has_doctorate,
            "years_experience": year_idx,  # Years since initial year
            "num_articles": total_articles,
            "num_books": total_books,
            "num_software": 0,  # Simplified
            "category": category,
            "administrative_position": administrative_position
        }
        
        from models.decreto1279 import calculate_full_time_salary
        salary_result = calculate_full_time_salary(input_data_salary)
        
        # Override the point value with the simulated value
        annual_salary = salary_result["total_points"] * point_value * 12
        education_level = "Doctorate" if has_doctorate else "Master's" if has_masters else "Specialization" if has_specialization else "Undergraduate"
        
        # Apply inflation adjustment if requested
        if inflation_adjusted:
            real_value = annual_salary / ((1 + annual_inflation) ** year_idx)
            real_salaries.append(real_value)
        
        # Add to cumulative earnings
        if year_idx > 0:  # Skip the initial year
            cumulative_earnings.append(cumulative_earnings[-1] + annual_salary)
        
        # Store results
        salaries.append(annual_salary)
        education_levels.append(education_level)
    
    # Create dataframe with evolution data
    evolution_data = pd.DataFrame({
        "Year": years,
        "Annual Salary": salaries,
        "Education Level": education_levels,
        "Point Value": point_values,  # Ya no necesitamos la condición porque siempre es full-time
        "Cumulative Earnings": cumulative_earnings
    })
    
    if inflation_adjusted:
        evolution_data["Real Salary (Inflation-Adjusted)"] = real_salaries
    
    # Create salary evolution chart
    fig = go.Figure()
    
    # Nominal salary
    fig.add_trace(go.Scatter(
        x=years, 
        y=salaries,
        mode='lines+markers',
        name='Nominal Salary',
        line=dict(color='royalblue', width=3)
    ))
    
    # Real salary (if applicable)
    if inflation_adjusted:
        fig.add_trace(go.Scatter(
            x=years, 
            y=real_salaries,
            mode='lines+markers',
            name='Real Salary (Inflation-Adjusted)',
            line=dict(color='firebrick', width=3, dash='dash')
        ))
    
    # Add career events as markers
    if career_events:
        events_df = pd.DataFrame(career_events)
        
        for event_type in events_df["Event Type"].unique():
            type_events = events_df[events_df["Event Type"] == event_type]
            
            # Get salary values for these years
            event_salaries = []
            for year in type_events["Year"]:
                year_idx = years.index(year)
                event_salaries.append(salaries[year_idx])
            
            # Add to plot
            fig.add_trace(go.Scatter(
                x=type_events["Year"],
                y=event_salaries,
                mode='markers',
                marker=dict(
                    size=type_events["Impact"] * 2,
                    symbol='star',
                    line=dict(width=2, color='DarkSlateGrey')
                ),
                name=event_type,
                text=type_events["Event"],
                hoverinfo='text+x+y'
            ))
    
    # Update layout
    fig.update_layout(
        title=f'Salary Evolution for Full-time Professor (2023-{initial_year + years_to_simulate})',
        xaxis_title='Year',
        yaxis_title='Annual Salary (COP)',
        hovermode='closest',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Create cumulative earnings chart
    cumulative_fig = go.Figure(go.Scatter(
        x=years, 
        y=cumulative_earnings,
        mode='lines+markers',
        name='Cumulative Earnings',
        fill='tozeroy',
        line=dict(color='green', width=3)
    ))
    
    cumulative_fig.update_layout(
        title='Cumulative Earnings Over Career',
        xaxis_title='Year',
        yaxis_title='Cumulative Earnings (COP)',
        hovermode='closest'
    )
    
    return {
        "salary_chart": fig,
        "cumulative_chart": cumulative_fig,
        "evolution_data": evolution_data,
        "career_events": pd.DataFrame(career_events) if career_events else pd.DataFrame(),
        "initial_salary": salaries[0],
        "final_salary": salaries[-1],
        "total_earnings": cumulative_earnings[-1]
    }

def plot_payroll_distribution(payroll_data):
    return {}