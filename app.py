import streamlit as st
import pandas as pd
import numpy as np
from models.decreto1279 import Decreto1279Calculator
# Set page configuration
st.set_page_config(
    page_title="Simulador de Salarios Docentes UPC",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page title
st.title("Calculadora de Salarios Docentes UPC")
st.subheader("Herramienta de Simulación y Análisis")

# Introduction
st.markdown("""
## Bienvenido al Simulador de Salarios Docentes UPC

Esta aplicación te permite:
1. Calcular salarios de profesores de planta según el Decreto 1279

Utiliza la barra lateral para navegar a través de las diferentes funcionalidades.
""")

# Display basic information about Decree 1279 and Agreement 006
st.markdown("""
## Normatividad Salarial Docente en Colombia

### Decreto 1279
El Decreto 1279 establece el régimen salarial para profesores de universidades públicas en Colombia, considerando:
- Títulos académicos
- Experiencia académica
- Productividad investigativa
- Cargos académico-administrativos
- Otros factores
""")
st.markdown("## Ejemplo de Evolución Salarial")
sample_data = pd.DataFrame({
    'Año': list(range(2022, 2032)),
    '   Salario Base': [4000000 * (1.04)**i for i in range(10)],
    'Con Bonificación por Productividad': [4000000 * (1.04)**i * 1.15 for i in range(10)]
})

st.line_chart(
    sample_data.set_index('Año')
)

st.markdown("""
Desarrollado para UPC
""")

# Footer
st.markdown("---")
st.markdown("© 2025 Simulador de Salarios Docentes UPC")

st.markdown("### *I am inevitable.* 🟣")
