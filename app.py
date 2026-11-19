import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
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

def log_historie(commando, uitkomst="Succes"):
    tijdstempel = datetime.datetime.now().strftime("%H:%M:%S")
    uitkomst_str = " ".join(str(uitkomst).split())
    if len(uitkomst_str) > 140:
        uitkomst_str = uitkomst_str[:137] + "..."
    item = f"[{tijdstempel}] {commando}  ➔  {uitkomst_str}"
    st.session_state.geschiedenis.append(item)
    try:
        docs_map = os.path.join(os.path.expanduser("~"), "Documents")
        os.makedirs(docs_map, exist_ok=True)
        pad = os.path.join(docs_map, "missie_logboek.txt")
        with open(pad, "a", encoding="utf-8") as f:
            f.write(item + "\n")
    except Exception:
        pass

bekende_cmds = [
    "molmassa", "balanceer", "ph", "verdun", "gaswet", "kook",
    "taylor", "laplace", "num_integrate", "nint", "gradient",
    "vector_gradient", "matrix", "epische_som", "latex",
    "debroglie", "debroglie_relativistisch", "debroglie_thermisch",
    "rydberg", "warmte", "kwantum", "resonantie", "vanderpol",
    "ode_plot", "ohm", "relativiteit", "christoffel", "zwaartekracht",
    "planeet_info", "baan", "wizard", "impact", "worp", "loterij",
    "loterij_analyse", "echte_loterij", "live_loterij", "laad_loterij",
    "grand_tour", "numeriek"
]

def normaliseer_commando(tekst):
    for cmd in bekende_cmds:
        tekst = re.sub(rf"\b{re.escape(cmd)}\b(?=\s*\()", cmd, tekst, flags=re.IGNORECASE)
    return tekst

# Sidebar met snelle keuzes, zware demo's en logboek optie
st.sidebar.header("Command Center")
actie = st.sidebar.selectbox(
    "Kies een module of actie:",
    [
        "Handmatig commando",
        "🔥 Epische Som (Integraal + Zeta(4))",
        "🌀 Niet-Lineaire ODE Simulatie",
        "⚡ Relativistische De Broglie (10 MeV)",
        "📐 Matrix Analyse (3x3 Eigenwaarden & Inverse)",
        "📉 Laplace Transformatie (t^3 * exp(-2*t))",
        "🎯 Schuine Worp (v0=65 m/s, 52°)",
        "🧪 Molaire Massa & Valentie (C12H16N2)",
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

default_input = ""
if actie == "🔥 Epische Som (Integraal + Zeta(4))":
    default_input = "epische_som()"
elif actie == "🌀 Niet-Lineaire ODE Simulatie":
    default_input = "numeriek()"
elif actie == "⚡ Relativistische De Broglie (10 MeV)":
    default_input = "debroglie_relativistisch(10)"
elif actie == "📐 Matrix Analyse (3x3 Eigenwaarden & Inverse)":
    default_input = "matrix([[4, 1, -2], [1, 3, 0], [-2, 0, 5]])"
elif actie == "📉 Laplace Transformatie (t^3 * exp(-2*t))":
    default_input = "laplace(t^3 * exp(-2*t))"
elif actie == "🎯 Schuine Worp (v0=65 m/s, 52°)":
    default_input = "worp(65, 52)"
elif actie == "🧪 Molaire Massa & Valentie (C12H16N2)":
    default_input = "molmassa('C12H16N2')"
elif actie == "Grand Tour Demo":
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

if actie == "📜 Bekijk Eerdere Sommen (Logboek)":
    st.subheader("📜 Historisch Missie-Logboek (Eerdere Sommen)")
    st.markdown("Hieronder staat het overzicht van al je uitgevoerde berekeningen en hun uitkomsten in deze sessie:")

    if st.session_state.geschiedenis:
        for idx, hist_item in enumerate(reversed(st.session_state.geschiedenis), 1):
            st.text(f"{idx}. {hist_item}")

        if st.button("🗑️ Logboek Leegmaken"):
            st.session_state.geschiedenis = []
            st.success("Logboek succesvol geleegd!")
            st.rerun()
    else:
        st.info("Nog geen berekeningen uitgevoerd in deze sessie. Voer een som in om te starten!")

    st.stop()

gebruiker_input = st.text_input("Typ je commando of som:", value=default_input if default_input != "logboek" else "")

def strip_ansi(text):
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)

def toon_help():
    st.markdown("""
    ### 🚀 MISSION CONTROL // ULTIMATE SCIENCE ENGINE (STAPPENPLAN ACTIEF)
    *Overzicht van alle beschikbare modules en commando's:*

    #### 📐 1. WISKUNDE & CALCULUS & STAPPENPLAN
- **Afgeleide** : `diff(x^3 * sin(x), x)`
- **Integraal** : `integrate(x^2 * exp(x), x)`
- **Taylor-reeks** : `taylor(sin(x))`
- **Laplace** : `laplace(exp(-t))`
- **Numeriek int** : `num_integrate('exp(-x**2)', 0, 5)` / `nint(...)`
- **Gradient** : `gradient(x^2 + y^2, 'x', 'y')` / `vector_gradient(...)`
- **Matrix analyse** : `matrix([[2, 1], [1, 3]])`
- **Epische som** : `epische_som()`
- **LaTeX export** : `latex(diff(x^2 * sin(x), x))`

    #### 🔢 2. ALGEBRA & VERGELIJKINGEN
- **Vergelijking** : `solve(x^2 - 8*x + 15, x)`
- **Uitwerken/Haakjes** : `sp.expand((x + 3)^4)`

    #### 🧪 3. SCHEIKUNDE & LAB
- **Molaire massa** : `molmassa("C8H9NO2")`
- **Balanceren** : `balanceer("H2 + O2 -> H2O")`
- **Zuurgraad** : `ph(0.01)`
- **Verdunningen** : `verdun(C1, 50, 0.1, 250)`
- **Algemene gaswet** : `gaswet(101325, "V", 1, 273.15, "V")`
- **Lab opbrengst** : `kook(24.5, 25.0)`

    #### ⚛️ 4. NATUURKUNDE & KWANTUM
- **De Broglie** : `debroglie(9.11e-31, 1e6)`, `debroglie_relativistisch(1)`, `debroglie_thermisch(293.15, 0.25)`
- **Rydberg** : `rydberg(1, 3)`
- **Warmte** : `warmte("water", 1, 20, 100)`
- **Kwantum energie** : `kwantum(0)`
- **Resonantie** : `resonantie(1.0)`
- **Van der Pol** : `vanderpol()`
- **ODE plot** : `ode_plot("y'' + 3y' + 2y = sin(t)")`
- **Wet van Ohm** : `ohm(u=12, r=4)`

    #### 🌌 5. ASTROFYSICA & RELATIVITEIT
- **Relativiteit** : `relativiteit(0.8, 3600)`
- **Christoffel** : `christoffel(...)`
- **Zwaartekracht** : `zwaartekracht(5.97e24, 7.35e22, 3.84e8)`
- **Planeet info** : `planeet_info("jupiter")`
- **Baansimulatie** : `baan()`
- **Impact simulatie** : `impact(1.0)`
- **Schuine worp** : `worp(25, 45)`

    #### 🎲 6. LOTERIJ & DATA-ANALYSES
- **Loterij simulatie** : `loterij(6, 45)`
- **Historie analyse** : `loterij_analyse([[1, 2, 3, 4, 5, 6]])`
- **Echte data** : `echte_loterij()` / `laad_loterij("loterij_data.csv")`
- **Live data** : `live_loterij()`

    #### 🚀 7. SYSTEEM & TOOLS
- **Grand Tour** : `grand_tour()`
- **Niet-lineaire ODE** : `numeriek()`

    *Typ 'menu' of 'help' in het invoerveld om dit overzicht op te vragen.*
    """)

def toon_handleiding():
    toon_help()

class AppSmartNamespace(dict):
    def __missing__(self, key):
        smart_cls = getattr(kids_rekenen, "SmartSymbol", None)
        sym = smart_cls(key) if callable(smart_cls) else sp.Symbol(key)
        self[key] = sym
        return sym

def veilige_functie(func_naam):
    f = getattr(kids_rekenen, func_naam, None)
    if f is None or not callable(f):
        def ontbrekend(*args, **kwargs):
            raise AttributeError(f"Functie '{func_naam}' niet gevonden in kids_rekenen.")
        return ontbrekend
    return f

def haal_antwoord_uit_log(log_tekst):
    for lijn in reversed(log_tekst.splitlines()):
        stripped = lijn.strip()
        if not stripped:
            continue
        if ":" in stripped:
            _, rechts = stripped.split(":", 1)
            rechts = rechts.strip()
            if rechts:
                return rechts
    return None

if st.button("Lanceer Berekening 🚀", type="primary"):
    if not gebruiker_input.strip():
        st.warning("Voer eerst een commando of som in!")
    else:
        gekuiste_input = gebruiker_input.strip().lower()
        if gekuiste_input in ["help", "help()", "menu", "menu()", "toon_help", "toon_help()", "handleiding", "toon_handleiding", "toon_handleiding()"]:
            toon_help()
            log_historie(gebruiker_input.strip(), "Handleiding getoond")
        else:
            with st.spinner("Boordcomputer voert berekening uit..."):
                try:
                    ns = AppSmartNamespace({
                        "sp": sp, "c": 3e8, "g": 9.81, "G": 6.674e-11, "M": 1.989e30,
                        "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "exp": sp.exp, "log": sp.log,
                        "diff": sp.diff, "integrate": sp.integrate, "solve": sp.solve,
                        "dsolve": sp.dsolve, "Eq": sp.Eq, "sqrt": sp.sqrt, "pi": sp.pi,
                        "Matrix": sp.Matrix, "factorial": sp.factorial, "zeta": sp.zeta,

                        # Scheikunde & Lab
                        "molmassa": veilige_functie("bereken_molmassa"),
                        "balanceer": veilige_functie("balanceer_reactie"),
                        "ph": veilige_functie("bereken_ph"),
                        "verdun": veilige_functie("bereken_verdunning"),
                        "gaswet": veilige_functie("bereken_gaswet"),
                        "kook": veilige_functie("bereken_kook"),

                        # Calculus & Wiskunde
                        "taylor": veilige_functie("bereken_taylor"),
                        "laplace": veilige_functie("bereken_laplace"),
                        "num_integrate": veilige_functie("num_integrate"),
                        "nint": veilige_functie("num_integrate"),
                        "gradient": veilige_functie("vector_gradient"),
                        "vector_gradient": veilige_functie("vector_gradient"),
                        "matrix": veilige_functie("matrix_analyse"),
                        "epische_som": veilige_functie("epische_wiskunde_som"),
                        "latex": veilige_functie("export_latex"),

                        # Natuurkunde & Kwantum
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

                        # Astrofysica & Ruimte
                        "relativiteit": veilige_functie("bereken_relativiteit"),
                        "christoffel": veilige_functie("bereken_christoffel"),
                        "zwaartekracht": veilige_functie("zwaartekracht_kracht"),
                        "planeet_info": veilige_functie("planeet_info"),
                        "baan": veilige_functie("simuleer_baan"),
                        "wizard": veilige_functie("baan_wizard"),
                        "impact": veilige_functie("simuleer_impact"),
                        "worp": veilige_functie("schuine_worp"),

                        # Loterij & Data
                        "loterij": veilige_functie("bereken_loterij"),
                        "loterij_analyse": veilige_functie("analyseer_loterij_historie"),
                        "echte_loterij": veilige_functie("download_en_analyseer_echte_data"),
                        "live_loterij": veilige_functie("haal_live_loterij_data"),
                        "laad_loterij": veilige_functie("laad_en_analyseer_csv"),

                        # Systeem & Numeriek
                        "grand_tour": veilige_functie("grand_tour"),
                        "numeriek": veilige_functie("los_op_numeriek"),
                    })

                    genormaliseerd = normaliseer_commando(gebruiker_input)
                    try:
                        geparst = kids_rekenen.slimme_parser(genormaliseerd)
                    except Exception:
                        geparst = genormaliseerd

                    plt.close("all")
                    old_stdout = sys.stdout
                    new_stdout = io.StringIO()
                    sys.stdout = new_stdout

                    try:
                        resultaat = eval(geparst, {"__builtins__": {}}, ns)
                    finally:
                        sys.stdout = old_stdout

                    captured_output = new_stdout.getvalue()
                    clean_output = strip_ansi(captured_output)
                    had_figuur = bool(plt.get_fignums())

                    if resultaat is not None:
                        log_uitkomst = str(resultaat)
                    else:
                        log_uitkomst = (
                            haal_antwoord_uit_log(clean_output)
                            or ("Grafiek weergegeven" if had_figuur else None)
                            or (clean_output.strip().splitlines()[-1].strip() if clean_output.strip() else "Geen uitvoer")
                        )

                    st.success("Missie geslaagd! 🚀")
                    log_historie(gebruiker_input.strip(), log_uitkomst)

                    # Duidelijke weergave van Som / Opgave en Antwoord
                    st.markdown("---")
                    st.markdown(f"**Som / Opgave:** `{gebruiker_input.strip()}`")
                    if resultaat is not None:
                        if isinstance(resultaat, (sp.Expr, sp.Matrix)):
                            st.markdown("**Antwoord:**")
                            st.latex(sp.latex(resultaat))
                        else:
                            st.markdown(f"**Antwoord:** `{resultaat}`")
                    else:
                        log_antwoord = haal_antwoord_uit_log(clean_output)
                        if log_antwoord:
                            st.markdown(f"**Antwoord:** `{log_antwoord}`")
                        elif had_figuur:
                            st.markdown("**Antwoord:** *Zie grafiek hieronder*")
                        elif clean_output.strip():
                            st.markdown("**Antwoord:** *Zie boordcomputer-uitvoer hieronder*")
                    st.markdown("---")

                    if had_figuur:
                        st.subheader("Grafiek:")
                        st.pyplot(plt.gcf())
                        plt.close("all")

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
                    log_historie(gebruiker_input.strip(), f"Fout: {e}")
