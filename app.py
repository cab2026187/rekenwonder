import streamlit as st
import sympy as sp
import numpy as np
import io
import sys
import re
import os
import datetime
import kids_rekenen

st.set_page_config(
    page_title="Mission Control Mobile",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 Mission Control // Mobile")
st.markdown("*De ultieme mobiele science engine.*")

# --- SESSIE INITIALISATIE VOOR GESCHIEDENIS ---
if "geschiedenis" not in st.session_state:
    st.session_state.geschiedenis = []

def log_historie(commando, status="Succes"):
    tijdstempel = datetime.datetime.now().strftime("%H:%M:%S")
    item = f"[{tijdstempel}] {commando} — {status}"
    st.session_state.geschiedenis.append(item)
    try:
        docs_map = os.path.join(os.path.expanduser('~'), 'Documents')
        os.makedirs(docs_map, exist_ok=True)
        pad = os.path.join(docs_map, 'missie_logboek.txt')
        with open(pad, 'a', encoding='utf-8') as f:
            f.write(item + '\n')
    except Exception:
        pass

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
        "Planeet Info (Jupiter)",
        "Help / Handleiding tonen",
        "📜 Bekijk Eerdere Sommen (Logboek)"
    ]
)

# Bepaal standaard invoer
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
elif actie == "Help / Handleiding tonen":
    default_input = "help"
elif actie == "📜 Bekijk Eerdere Sommen (Logboek)":
    default_input = "logboek"

# Logboek scherm weergave in Streamlit
if actie == "📜 Bekijk Eerdere Sommen (Logboek)":
    st.subheader("📜 Historisch Missie-Logboek (Eerdere Sommen)")
    st.markdown("Overzicht van je uitgevoerde berekeningen:")
    if st.session_state.geschiedenis:
        for idx, hist_item in enumerate(reversed(st.session_state.geschiedenis), 1):
            st.text(f"{idx}. {hist_item}")
        if st.button("🗑️ Logboek Leegmaken"):
            st.session_state.geschiedenis = []
            st.success("Logboek geleegd!")
            st.rerun()
    else:
        st.info("Nog geen berekeningen in deze sessie.")
    st.stop()

gebruiker_input = st.text_input("Typ je commando of som:", value=default_input if default_input != "logboek" else "")

def strip_ansi(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)
    
def toon_help():
    st.markdown("""
    ### 🚀 MISSION CONTROL // ULTIMATE SCIENCE ENGINE (STAPPENPLAN ACTIEF)
    *Overzicht van alle beschikbare modules en commando's:*

    #### 📐 1. WISKUNDE & CALCULUS
    * `taylor(sin(x))` — Taylor-reeks
    * `laplace(exp(-t))` — Laplace-transformatie
    * `num_integrate('exp(-x**2)', 0, 5)` — Numeriek integreren
    * `diff(x^3 * sin(x), x)` — Afgeleide
    * `matrix([[2, 1], [1, 3]])` — Matrix analyse

    #### 🧪 2. SCHEIKUNDE & LAB
    * `molmassa("C8H9NO2")` — Molaire massa Paracetamol
    * `balanceer("H2 + O2 -> H2O")` — Reactie balanceren
    * `ph(0.01)` — pH berekenen
    
    #### ⚛️ 3. NATUURKUNDE & OVERIG
    * `ohm(u=12, r=4)` — Wet van Ohm
    * `planeet_info("jupiter")` — Planeet gegevens
    * `grand_tour()` — Volledige systeemtest
    
    *Typ 'menu' of 'help' in het invoerveld voor dit overzicht.*
    """)

if st.button("Lanceer Berekening 🚀", type="primary"):
    if not gebruiker_input.strip():
        st.warning("Voer eerst een commando of som in!")
    else:
        gekuiste_input = gebruiker_input.strip().lower()
        if gekuiste_input in ["help", "help()", "menu", "toon_help", "handleiding"]:
            toon_help()
            log_historie("help", "Handleiding opgevraagd")
        else:
            with st.spinner("Boordcomputer voert berekening uit..."):
                try:
                    def veilige_functie(func_naam):
                        f = getattr(kids_rekenen, func_naam, None)
                        if f is None:
                            return lambda *args, **kwargs: f"Fout: Functie '{func_naam}' ontbreekt in kids_rekenen."
                        return f

                    ns = {
                        "sp": sp, "c": 3e8, "g": 9.81, "G": 6.674e-11, "M": 1.989e30,
                        "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "exp": sp.exp, "log": sp.log,
                        "diff": sp.diff, "integrate": sp.integrate, "solve": sp.solve,
                        "dsolve": sp.dsolve, "Eq": sp.Eq, "sqrt": sp.sqrt, "pi": sp.pi,
                        "Matrix": sp.Matrix, "factorial": sp.factorial, "zeta": sp.zeta,
                        
                        "molmassa": veilige_functie("bereken_molmassa"),
                        "balanceer": veilige_functie("balanceer_reactie"),
                        "ph": veilige_functie("bereken_ph"),
                        "verdun": veilige_functie("verdun"),
                        "gaswet": veilige_functie("gaswet"),
                        "kook": veilige_functie("kook"),
                        "taylor": veilige_functie("bereken_taylor"),
                        "laplace": veilige_functie("laplace"),
                        "num_integrate": veilige_functie("num_integrate"),
                        "nint": veilige_functie("num_integrate"),
                        "gradient": veilige_functie("vector_gradient"),
                        "vector_gradient": veilige_functie("vector_gradient"),
                        "matrix": veilige_functie("matrix_analyse"),
                        "epische_som": veilige_functie("epische_wiskunde_som"),
                        "debroglie": veilige_functie("bereken_debroglie"),
                        "debroglie_relativistisch": veilige_functie("debroglie_relativistisch"),
                        "debroglie_thermisch": veilige_functie("debroglie_thermisch"),
                        "rydberg": veilige_functie("bereken_rydberg"),
                        "warmte": veilige_functie("bereken_warmte"),
                        "kwantum": veilige_functie("kwantum_energie"),
                        "resonantie": veilige_functie("bereken_resonantie"),
                        "vanderpol": veilige_functie("vanderpol_simulatie"),
                        "ode_plot": veilige_functie("ode_plot"),
                        "ohm": veilige_functie("bereken_ohm"),
                        "relativiteit": veilige_functie("bereken_relativiteit"),
                        "christoffel": veilige_functie("bereken_christoffel"),
                        "zwaartekracht": veilige_functie("zwaartekracht_kracht"),
                        "planeet_info": veilige_functie("planeet_info"),
                        "baan": veilige_functie("baan"),
                        "wizard": veilige_functie("baan_wizard"),
                        "impact": veilige_functie("simuleer_impact"),
                        "worp": veilige_functie("schuine_worp"),
                        "loterij": veilige_functie("bereken_loterij"),
                        "loterij_analyse": veilige_functie("analyseer_loterij_historie"),
                        "echte_loterij": veilige_functie("download_en_analyseer_echte_data"),
                        "live_loterij": veilige_functie("haal_live_loterij_data"),
                        "laad_loterij": veilige_functie("laad_en_analyseer_csv"),
                        "grand_tour": veilige_functie("grand_tour"),
                        "numeriek": veilige_functie("los_op_numeriek"),
                    }
                    
                    try:
                        geparst = kids_rekenen.slimme_parser(gebruiker_input)
                    except Exception:
                        geparst = gebruiker_input
                    
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
                    log_historie(gebruiker_input, "Succes")
                    
                    if clean_output.strip():
                        st.subheader("Boordcomputer Log:")
                        st.text(clean_output)
                    
                    if resultaat is not None and not clean_output.strip():
                        st.subheader("Resultaat:")
                        if isinstance(resultaat, (sp.Expr, sp.Matrix)):
                            st.latex(sp.latex(resultaat))
                        else:
                            st.write(resultaat)
                            
                except Exception as e:
                    st.error(f"Fout tijdens missie: {e}")
                    log_historie(gebruiker_input, f"Fout: {e}")
