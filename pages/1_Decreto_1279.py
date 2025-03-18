import streamlit as st
import pandas as pd
import numpy as np
from models.decreto1279 import Decreto1279Calculator
from utils.visualizations import plot_salary_evolution

st.title("Decreto 1279 - Calculadora de Salarios para Profesores de Planta")

decreto1279_calculator = Decreto1279Calculator()

col1, col2 = st.columns([1, 1])

with col1:
    st.header("Variables de Entrada")
    

    category = st.selectbox(
        "Categoría Académica",
        ["Auxiliar", "Asistente", "Asociado", "Titular"],
        help="La categoría académica del profesor"
    )
    
    st.subheader("Títulos Académicos")
    pregrado = st.checkbox("Pregrado", value=True, disabled=True)
    especializacion = st.checkbox("Especialización")
    maestria = st.checkbox("Maestría")
    doctorado = st.checkbox("Doctorado")
    postdoctorado = st.checkbox("Postdoctorado")
    
    experience_years = st.slider(
        "Años de Experiencia Académica",
        min_value=0,
        max_value=40,
        value=5,
        help="Número de años de experiencia académica"
    )
    
    st.subheader("Productividad Académica")
    
    productivity_types = [
        "Artículo A1", "Artículo A2", "Artículo B", "Artículo C",
        "Libro Investigación", "Capítulo Libro Investigación",
        "Patente Internacional", "Patente Nacional", "Software Registrado",
        "Premio Internacional", "Premio Nacional"
    ]
    
    productivity_items = []
    
    num_items = st.number_input(
        "Número de elementos de productividad",
        min_value=0,
        max_value=20,
        value=2
    )
    
    for i in range(int(num_items)):
        col_type, col_quantity = st.columns([3, 1])
        with col_type:
            item_type = st.selectbox(
                f"Tipo de Item {i+1}",
                productivity_types,
                key=f"item_type_{i}"
            )
        with col_quantity:
            quantity = st.number_input(
                f"Cantidad",
                min_value=1,
                max_value=10,
                value=1,
                key=f"quantity_{i}"
            )
        
        productivity_items.append({
            "type": item_type,
            "quantity": quantity
        })
    
    second_language = st.checkbox(
        "Segundo Idioma Certificado",
        value=False,
        help="Marcar si el profesor tiene un segundo idioma certificado"
    )
    
    administrative_positions = [
        None, "Rector", "Vicerrector", "Decano", 
        "Director de Departamento", "Director de Programa", "Coordinador"
    ]
    administrative_position = st.selectbox(
        "Cargo Administrativo",
        administrative_positions,
        format_func=lambda x: "Ninguno" if x is None else x
    )
    
    projection_years = st.slider(
        "Años de Proyección",
        min_value=1,
        max_value=20,
        value=10,
        help="Número de años para proyectar el salario"
    )
    
    base_year = st.number_input(
        "Año Base",
        min_value=2020,
        max_value=2030,
        value=2024
    )
    
    degrees = ["Pregrado"]
    if especializacion:
        degrees.append("Especialización")
    if maestria:
        degrees.append("Maestría")
    if doctorado:
        degrees.append("Doctorado")
    if postdoctorado:
        degrees.append("Postdoctorado")
    
    input_data = {
        "degrees": degrees,
        "category": category,
        "experience_years": experience_years,
        "productivity": productivity_items,
        "administrative_position": administrative_position,
        "second_language": second_language,
        "base_year": base_year,
        "projection_years": projection_years
    }
    
    st.markdown("---")
    calculate_button = st.button("Calcular Salario", type="primary")


with col2:
    st.header("Resultados del Cálculo")
    
    if calculate_button:
        results = decreto1279_calculator.calculate_salary(input_data)
        
        st.subheader(f"Puntos Totales: {results['salary_breakdown']['total_points']}")
        
        st.metric("Salario Mensual", f"${results['monthly_salary']:,.0f} COP")
        st.metric("Salario Anual", f"${results['annual_salary']:,.0f} COP")
        
        st.subheader("Desglose del Salario")
        breakdown = results["salary_breakdown"]
        
        breakdown_df = pd.DataFrame({
            "Componente": ["Títulos Académicos", "Experiencia", "Productividad Académica", "Segundo Idioma", "Puntos Base Totales", "Salario Base", "Bonificación Administrativa", "Total Mensual"],
            "Puntos/Valor": [
                f"{breakdown['degree_points']} puntos",
                f"{breakdown['experience_points']} puntos",
                f"{breakdown['productivity_points']} puntos",
                f"{breakdown['language_points']} puntos",
                f"{breakdown['total_points']} puntos",
                f"${breakdown['base_salary']:,.0f} COP",
                f"${breakdown['administrative_bonus']:,.0f} COP",
                f"${breakdown['total_monthly_salary']:,.0f} COP"
            ]
        })
        
        st.table(breakdown_df)
        
        st.subheader("Proyección Salarial")
        
        projection_df = pd.DataFrame(results["salary_projection"])
        
        fig = plot_salary_evolution(
            results["salary_projection"],
            title=f"Proyección de Evolución Salarial ({base_year} - {base_year + projection_years})"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        projection_table = pd.DataFrame({
            "Año": [p["year"] for p in results["salary_projection"]],
            "Salario Mensual": [f"${p['monthly_salary']:,.0f}" for p in results["salary_projection"]],
            "Mensual con Bonificación": [f"${p['monthly_with_bonus']:,.0f}" for p in results["salary_projection"]],
            "Salario Anual": [f"${p['annual_salary']:,.0f}" for p in results["salary_projection"]]
        })
        
        st.dataframe(projection_table, use_container_width=True)
        
        st.subheader("Simulación de Evolución de Carrera")
        simulate_evolution = st.checkbox("Simular evolución de carrera a lo largo del tiempo")
        
        if simulate_evolution:
            evolution_years = st.slider(
                "Años para simular la evolución de carrera",
                min_value=5,
                max_value=30,
                value=15
            )
            
            evolution_results = decreto1279_calculator.simulate_faculty_evolution(input_data, years=evolution_years)
            
            st.line_chart(
                evolution_results[["monthly_salary", "annual_salary"]].set_index(evolution_results["year"])
            )
            
            evolution_table = pd.DataFrame({
                "Año": evolution_results["year"],
                "Experiencia": evolution_results["experience_years"],
                "Categoría": evolution_results["category"],
                "Salario Mensual": [f"${s:,.0f}" for s in evolution_results["monthly_salary"]],
                "Salario Anual": [f"${s:,.0f}" for s in evolution_results["annual_salary"]]
            })
            
            st.dataframe(evolution_table, use_container_width=True)
    else:
        st.info("Ingrese la información del profesor y haga clic en 'Calcular Salario' para ver los resultados.")

st.markdown("---")
st.header("Comprensión del Decreto 1279")

st.markdown("""
### Componentes Clave del Decreto 1279

El Decreto 1279 del 19 de junio de 2002 establece el régimen salarial y prestacional para los profesores de las universidades estatales en Colombia. Los principales componentes que determinan el salario de un profesor son:

1. **Títulos Académicos**: Se asignan puntos basados en las calificaciones académicas:
    - Título de pregrado: 178 puntos
    - Especialización: 20 puntos
    - Maestría: 40 puntos
    - Doctorado: 80 puntos
    - Postdoctorado: 10 puntos

2. **Categoría Académica**: Los profesores se clasifican en cuatro categorías, con diferentes asignaciones de puntos por experiencia:
    - Auxiliar: 4 puntos por año (máx 20)
    - Asistente: 6 puntos por año (máx 30)
    - Asociado: 7 puntos por año (máx 35)
    - Titular: 8 puntos por año (máx 40)

3. **Productividad Académica**: Se otorgan puntos por investigación, publicaciones y trabajo creativo:
    - Artículos A1: 15 puntos
    - Artículos A2: 12 puntos
    - Artículos B: 8 puntos
    - Artículos C: 3 puntos
    - Libros de investigación: 20 puntos
    - Capítulos de libros: 8 puntos
    - Patentes y otra propiedad intelectual

4. **Factores Adicionales**:
    - Dominio de segundo idioma: 40 puntos
    - Cargos administrativos: aumento porcentual sobre el salario base

### Cálculo del Salario

El salario total se calcula:
1. Sumando todos los puntos de títulos académicos, experiencia, productividad y factores adicionales
2. Multiplicando los puntos totales por el valor actual del punto (actualizado anualmente)
3. Agregando bonificaciones por cargos administrativos si corresponde

Este simulador implementa estos cálculos de acuerdo con las especificaciones del decreto.
""")

# Footer
st.markdown("---")
st.markdown("© 2025 Simulador de Salarios Docentes UPC - Módulo Decreto 1279")

st.markdown("""
<span style="opacity: 0.5;">Con un solo chasquido, la mitad de los salarios desaparecen...</span>
""", unsafe_allow_html=True)

