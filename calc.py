# -*- coding: utf-8 -*-
"""
@author: Nik Cuculovski @22SQ
"""

#---------------------------------#

### import libraries
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from PIL import Image

#---------------------------------#

### page setup
st.set_page_config(
    page_title="Acquisition Scenario Planner",
    page_icon='dropbox.ico',
    layout="centered")

hide_menu_style = """
        <style>
        footer {visibility: hidden;}
        footer:after {
            content:'© 2022, Media.Monks. All rights reserved.';
            visibility: visible;
            display: block;
            position: relative;
            #background-color: black;
            margin-bottom:20px;
        }
        </style>
        """

st.markdown(hide_menu_style, unsafe_allow_html=True)

## import image
#image = Image.open('2560px-Dropbox_logo_2017.svg.png')
## write image
col1, col2, col3 = st.columns([2.5,5,1])
with col1:
    st.write("")
with col2:
    st.image(image, width=300, use_column_width=None)
with col3:
    st.write("")

hide_full_screen = '''
<style>
    .css-6awftf.e19lei0e1 {visibility: hidden;}
</style>
'''
st.markdown(hide_full_screen, unsafe_allow_html=True) 

#---------------------------------#

st.title("Acquisition Scenario Planner")
st.markdown('*The application is best viewed with the "Light" theme. If your computer is defaulted to "Dark", consider changing the calculator theme in the Settings menu found in the upper right corner.*')

st.subheader("**Personal - Pricing & Market Penetration**")

personal_plus, personal_family = st.columns(2)
with personal_plus:
    personal_plus_pricing = st.number_input("Plus ($): ", min_value=0.0, value=119.88, help='Pricing for Personal Plus package.')
with personal_family:
    personal_family_pricing = st.number_input("Family ($): ", min_value=0.0, value=203.88, help='Pricing for Personal Family package.')

personal_plus_people, personal_family_people = st.columns(2)
with personal_plus_people:
    personal_plus_population = st.number_input("Plus (#): ", min_value=0, value=2500000, step = 1000, help='Number of Personal Plus package users.')
with personal_family_people:
    personal_family_population = st.number_input("Family (#): ", min_value=0, value=1000000, step = 1000, help='Number of Personal Family package users.')

personal_plus_total = personal_plus_pricing * personal_plus_population
personal_family_total = personal_family_pricing * personal_family_population
personal_total = personal_plus_total + personal_family_total

st.subheader("**Personal - Retention & Lifespan**")
st.markdown('Industry anticipated exponential decay applied to subsequent years.')

personal_plus_retention_y1 = st.slider('First Year Retention Rate (%):', min_value=0.0, max_value=100.0, value=95.0, step=0.1, help='First year retention rate for personal products.')
personal_lifetime = st.slider('Average Lifetime (#):', min_value=1, max_value=10, value=3, step=1, help='Average lifetime for personal products.')
personal_theta_slider = st.slider('Decay Rate (Θ):', min_value=1, max_value=10, value=1, step=1, help='Average decay for personal products.')

I = 1
a = 2
T = personal_lifetime
dt = 1
Nt = int(round(T/dt))                                    # no of time intervals
u = np.zeros(Nt+1)                                       # array of u[n] values
t = np.linspace(0, T, Nt+1)                              # time mesh                  # Backward Euler method
theta_transform = personal_plus_retention_y1 / 10
theta = theta_transform / personal_theta_slider

u[0] = I                     # assign initial condition
for n in range(0, Nt):       # n=0,1,...,Nt-1
    u[n+1] = (1 - (1-theta)*a*dt)/(1 + theta*dt*a)*u[n]
st.line_chart(u)

decay = pd.DataFrame(u, columns=['Decay'])

industry_average = (((decay*personal_total).sum()[0])/(personal_plus_population+personal_family_population))/3
industry_growth = (((decay*personal_total).sum()[0])/(personal_plus_population+personal_family_population))/4
industry_hyper = (((decay*personal_total).sum()[0])/(personal_plus_population+personal_family_population))/5

st.subheader("**Personal - Acquisition Cost Targets (LTV:CAC)**")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Lifetime Value (LTV)", "$"+str(((decay*personal_total).sum()[0]/1000000000).round(2))+'B')
col2.metric("Industry Average (3:1)", "$"+str(industry_average.round(2)))
col3.metric("Growth (4:1)", "$"+str(industry_growth.round(2)))
col4.metric("Hyper Growth (5:1)", "$"+str(industry_hyper.round(2)))

st.success("Given historical and user quality trends, the optimal acquisition cost is between " + "\$"+str(industry_hyper.round(2)) + " and " + "\$"+str(industry_average.round(2)) + ".")
