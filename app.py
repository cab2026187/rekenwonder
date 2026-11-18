import streamlit as st
import sympy as sp
import numpy as np
import io
import sys
import re
import kids_rekenen

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
        "Numerieke Integratie",
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
elif actie == "Numerieke Integratie":
    default_input = "num_integrate('exp(-x**2) * sin(x**3)', 0, 5)"
elif actie == "Wet van Ohm (U = I * R)":
    default_input = "ohm(u=12, r=4)"
elif actie == "pH & Zuurtegraad":
    default_input = "ph(0.01)"
elif actie == "Planeet Info (Jupiter)":
    default_input = "planeet_info('jupiter')"

gebruiker_input = st.text_input("Typ je commando of som:", value=default_input)

# Functie om terminal kleurcodes (ANSI) weg te filteren voor het web
def strip_ansi(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

if st.button("Lanceer Berekening 🚀", type="primary"):
    if gebruiker_input:
        with st.spinner("Boordcomputer voert berekening uit..."):
            try:
                # Namespace voor de app
                ns = {
                    "sp": sp, "c": 3e8, "g": 9.81, "G": 6.674e-11, "M": 1.989e30,
                    "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "exp": sp.exp, "log": sp.log,
                    "diff": sp.diff, "integrate": sp.integrate, "solve": sp.solve,
                    "dsolve": sp.dsolve, "Eq": sp.Eq, "sqrt": sp.sqrt, "pi": sp.pi,
                    "Matrix": sp.Matrix, "factorial": sp.factorial, "zeta": sp.zeta,
                    "molmassa": kids_rekenen.bereken_molmassa,
                    "taylor": kids_rekenen.bereken_taylor,
                    "laplace": kids_rekenen.laplace,
                    "ohm": kids_rekenen.bereken_ohm,
                    "ph": kids_rekenen.bereken_ph,
                    "planeet_info": kids_rekenen.planeet_info,
                    "grand_tour": kids_rekenen.grand_tour,
                    "num_integrate": kids_rekenen.num_integrate,
                }
                
                geparst = kids_rekenen.slimme_parser(gebruiker_input)
                
                # Vang alle print-statements en logs op van de achtergrond
                old_stdout = sys.stdout
                new_stdout = io.StringIO()
                sys.stdout = new_stdout
                
                try:
                    resultaat = eval(geparst, {"__builtins__": None, **ns})
                finally:
                    sys.stdout = old_stdout
                    
                captured_output = new_stdout.getvalue()
                clean_output = strip_ansi(captured_output)
                
                st.success("Missie geslaagd! 🚀")
                
                # Toon de opgevangen terminal-output netjes op het scherm
                if clean_output.strip():
                    st.subheader("Boordcomputer Log:")
                    st.text(clean_output)
                
                # Als er een direct resultaat is zonder prints, toon dat ook
                if resultaat is not None and not clean_output.strip():
                    st.subheader("Resultaat:")
                    if isinstance(resultaat, (sp.Expr, sp.Matrix)):
                        st.latex(sp.latex(resultaat))
                    else:
                        st.write(resultaat)
                        
            except Exception as e:
                st.error(f"Fout tijdens missie: {e}")
