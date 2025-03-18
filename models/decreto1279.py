import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class Decreto1279Calculator:
    
    def __init__(self):
        self.base_point_value = 20895
        

        self.categories = {
            "Auxiliar": {"min_points": 0, "max_points": 200},
            "Asistente": {"min_points": 201, "max_points": 300},
            "Asociado": {"min_points": 301, "max_points": 400},
            "Titular": {"min_points": 401, "max_points": 500}
        }
        

        self.degree_points = {
            "Pregrado": 178,
            "Especialización": 20,
            "Maestría": 40,
            "Doctorado": 80,
            "Postdoctorado": 10
        }
        

        self.experience_points_per_year = {
            "Auxiliar": 4,
            "Asistente": 6,
            "Asociado": 7,
            "Titular": 8
        }
        self.productivity_points = {
            "Artículo A1": 15,
            "Artículo A2": 12,
            "Artículo B": 8,
            "Artículo C": 3,
            "Libro Investigación": 20,
            "Capítulo Libro Investigación": 8,
            "Patente Internacional": 25,
            "Patente Nacional": 15,
            "Software Registrado": 10,
            "Premio Internacional": 15,
            "Premio Nacional": 8
        }

        self.administrative_positions = {
            "Rector": 0.35,  
            "Vicerrector": 0.30,  
            "Decano": 0.25,  
            "Director de Departamento": 0.20,  
            "Director de Programa": 0.18,  
            "Coordinador": 0.10 
        }
    
    def calculate_salary(self, input_data):

        degrees = input_data.get('degrees', [])
        category = input_data.get('category', 'Auxiliar')
        experience_years = input_data.get('experience_years', 0)
        productivity_items = input_data.get('productivity', [])
        administrative_position = input_data.get('administrative_position', None)
        second_language = input_data.get('second_language', False)
        base_year = input_data.get('base_year', 2024)
        projection_years = input_data.get('projection_years', 5)
        
        # Calculate degree points
        degree_points = sum(self.degree_points.get(degree, 0) for degree in degrees)
        
        # Calculate experience points
        experience_points = min(experience_years, 5) * self.experience_points_per_year.get(category, 4)
        
        # Limit experience points based on category
        max_experience_points = 20 if category == "Auxiliar" else \
                                30 if category == "Asistente" else \
                                35 if category == "Asociado" else 40
        experience_points = min(experience_points, max_experience_points)

        productivity_points = 0
        for item in productivity_items:
            item_type = item.get('type', '')
            quantity = item.get('quantity', 0)
            productivity_points += self.productivity_points.get(item_type, 0) * quantity
            
        language_points = 40 if second_language else 0
        
        total_points = degree_points + experience_points + productivity_points + language_points
        
        monthly_salary = total_points * self.base_point_value
        
        admin_bonus = 0
        if administrative_position and administrative_position in self.administrative_positions:
            admin_bonus = monthly_salary * self.administrative_positions[administrative_position]
            
        total_monthly_salary = monthly_salary + admin_bonus
        annual_salary = total_monthly_salary * 12
        
        salary_breakdown = {
            'degree_points': degree_points,
            'experience_points': experience_points,
            'productivity_points': productivity_points,
            'language_points': language_points,
            'total_points': total_points,
            'base_salary': monthly_salary,
            'administrative_bonus': admin_bonus,
            'total_monthly_salary': total_monthly_salary
        }
        
        inflation_rate = 0.04
        projection = []
        
        for i in range(projection_years + 1):
            year = base_year + i
            projected_point_value = self.base_point_value * ((1 + inflation_rate) ** i)
            projected_monthly_salary = total_points * projected_point_value
            
            proj_admin_bonus = 0
            if administrative_position and administrative_position in self.administrative_positions:
                proj_admin_bonus = projected_monthly_salary * self.administrative_positions[administrative_position]
                
            total_proj_monthly = projected_monthly_salary + proj_admin_bonus
            total_proj_annual = total_proj_monthly * 12
            
            projection.append({
                'year': year,
                'point_value': projected_point_value,
                'monthly_salary': projected_monthly_salary,
                'monthly_with_bonus': total_proj_monthly,
                'annual_salary': total_proj_annual
            })
        
        return {
            'total_points': total_points,
            'monthly_salary': total_monthly_salary,
            'annual_salary': annual_salary,
            'salary_breakdown': salary_breakdown,
            'salary_projection': projection
        }
    
    def simulate_faculty_evolution(self, faculty_data, years=10):
        results = []
        current_data = faculty_data.copy()
        
        for year in range(years):
            # Progress in the career
            current_data['experience_years'] = faculty_data['experience_years'] + year
            
            if year > 0 and year % 2 == 0:
                current_data['productivity'].append({
                    'type': 'Artículo B', 
                    'quantity': 1
                })
            
            total_productivity = sum(item['quantity'] for item in current_data['productivity'])
            if (current_data['category'] == 'Auxiliar' and 
                current_data['experience_years'] >= 4 and total_productivity >= 3):
                current_data['category'] = 'Asistente'
            elif (current_data['category'] == 'Asistente' and 
                    current_data['experience_years'] >= 8 and total_productivity >= 6):
                current_data['category'] = 'Asociado'
            elif (current_data['category'] == 'Asociado' and 
                    current_data['experience_years'] >= 12 and total_productivity >= 10):
                current_data['category'] = 'Titular'
            
            current_data['base_year'] = faculty_data['base_year'] + year
            calculation = self.calculate_salary(current_data)
            
            # Add to results
            results.append({
                'year': faculty_data['base_year'] + year,
                'experience_years': current_data['experience_years'],
                'category': current_data['category'],
                'total_points': calculation['total_points'],
                'monthly_salary': calculation['monthly_salary'],
                'annual_salary': calculation['annual_salary']
            })
        
        return pd.DataFrame(results)
