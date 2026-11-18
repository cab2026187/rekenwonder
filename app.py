import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# Importeer je bestaande functies uit rekenwonder.py 
# (Zorg dat rekenwonder.py in dezelfde map staat, of kopieer je logica hierin)
from rekenwonder import ns, slimme_parser, schrijf_log

st.set_page_config(
    page_title="Mission Control Mobile",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 Mission Control // Mobile")
st.markdown("*De ultieme mobiele science engine.*")

# Sidebar met snelle knoppen of keuzes
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