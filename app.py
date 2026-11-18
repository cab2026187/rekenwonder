import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# Importeer je bestaande functies uit rekenwonder.py 
# (Zorg dat rekenwonder.py in dezelfde map staat, of kopieer je logica hierin)
from kids_rekenen import ns, slimme_parser, schrijf_log

st.set_page_config(
    page_title="Mission Control Mobile",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 Mission Control // Mobile")
st.markdown("*De ultieme mobiele science engine.*")

# Sidebar met snelle knoppen of keuzesimport streamlit as st
import sympy as sp
import numpy as np

# Importeer direct uit jouw bestand kids_rekenen.py
from kids_rekenen import (
    ns, 
    slimme_parser, 
    schrijf_log, 
    bereken_molmassa, 
    bereken_taylor, 
    num_integrate, 
    schuine_worp, 
    bereken_ohm, 
    bereken_ph, 
    planeet_info,
    epische_wiskunde_som,
    grand_tour
)

st.set_page_config(
    page_title="Mission Control Mobile",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 Mission Control // Mobile")
st.markdown("*De ultieme mobiele science engine.*")

# Sidebar met snelle keuzes
st.sidebar.header("Command Center")
actie = st.sidebar.selectbox(
    "Kies een module of actie:",
    [
        "Handmatig commando", 
        "Grand Tour Demo", 
        "Paracetamol Molmassa (C8H9NO2)", 
        "Taylor-reeks van sin(x)", 
        "Wet van Ohm (U = I * R)", 
        "pH & Zuurtegraad",
        "Planeet Info (Jupiter)"
    ]
)

# Bepaal de standaard invoer op basis van het menu
default_input = ""
if actie == "Grand Tour Demo":
    default_input = "grand_tour()"
elif actie == "Paracetamol Molmassa (C8H9NO2)":
    default_input = "molmassa('C8H9NO2')"
elif actie == "Taylor-reeks van sin(x)":
    default_input = "taylor(sin(x))"
elif actie == "Wet van Ohm (U = I * R)":
    default_input = "ohm(u=12, r=4)"
elif actie == "pH & Zuurtegraad":
    default_input = "ph(0.01)"
elif actie == "Planeet Info (Jupiter)":
    default_input = "planeet_info('jupiter')"

# Invoerveld voor de gebruiker
gebruiker_input = st.text_input("Typ je commando of som:", value=default_input)

if st.button("Lanceer Berekening 🚀", type="primary"):
    if gebruiker_input:
        with st.spinner("Bezig met berekenen in de boordcomputer..."):
            try:
                # Evalueer de invoer via jouw namespace en parser
                geparst = slimme_parser(gebruiker_input)
                resultaat = eval(geparst, {"__builtins__": None, **ns})
                
                st.success("Missie geslaagd!")
                st.subheader("Resultaat:")
                
                if isinstance(resultaat, (sp.Expr, sp.Matrix)):
                    st.latex(sp.latex(resultaat))
                else:
                    st.write(resultaat)
                    
            except Exception as e:
                st.error(f"Fout tijdens missie: {e}")
st.sidebar.header("Command Center")
actie = st.sidebar.selectbox(
    "Kies een snelle demo:",
    ["Handmatig invoeren", "Grand Tour uitvoeren", "Paracetamol Molmassa", "Taylor Reeks", "Christoffel-symbolen"]
)

# Invoerveld voor de gebruiker (werkt perfect op mobiel toetsenbord!)
gebruiker_input = st.text_input("Typ je commando of som:", value="taylor(sin(x))" if actie == "Handmatig invoeren" else "")

if actie == "Grand Tour uitvoeren":
    gebruiker_input = "grand_tour()"
elif actie == "Paracetamol Molmassa":
    gebruiker_input = "molmassa('C8H9NO2')"
elif actie == "Taylor Reeks":
    gebruiker_input = "taylor(sin(x))"
elif actie == "Christoffel-symbolen":
    gebruiker_input = "christoffel([[-(1 - 2*M/r), 0, 0, 0], [0, 1/(1 - 2*M/r), 0, 0], [0, 0, r**2, 0], [0, 0, 0, r**2 * sin(theta)**2]], [t, r, theta, phi])"

if st.button("Lanceer Berekening 🚀", type="primary"):
    if gebruiker_input:
        with st.spinner("Bezig met berekenen in de kern..."):
            try:
                # Eenvoudige evaluatie via jouw namespace
                # We vangen de output op of voeren het uit
                if "(" in gebruiker_input and ")" in gebruiker_input:
                    # Functie-aanroep parsen via ns
                    func_naam = gebruiker_input.split("(")[0].strip()
                    if func_naam in ns:
                        # Voer de functie uit
                        resultaat = eval(gebruiker_input, {"__builtins__": None, **ns})
                        st.success("Missie geslaagd!")
                        
                        # Toon het resultaat netjes
                        st.subheader("Resultaat:")
                        if isinstance(resultaat, (sp.Expr, sp.Matrix)):
                            st.latex(sp.latex(resultaat))
                        else:
                            st.write(resultaat)
                    else:
                        st.error(f"Onbekend commando: {func_naam}")
                else:
                    # Standaard expressie
                    res = eval(slimme_parser(gebruiker_input), {"__builtins__": None, **ns})
                    st.subheader("Resultaat:")
                    st.latex(sp.latex(res))
            except Exception as e:
                st.error(f"Fout tijdens missie: {e}")
