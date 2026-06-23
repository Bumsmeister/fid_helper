import streamlit as st

st.title("FID-Umrechner")

# Eingaben
toc_ppm = st.number_input(
    "Cgesamt (gemessen) [ppm]",
    min_value=0.0,
    value=0.0,
    step=1.0
)

rel_feuchte = st.number_input(
    "Relative Feuchte [%]",
    min_value=0.0,
    max_value=100.0,
    value=0.0,
    step=0.1
)

o2_gemessen = st.number_input(
    "O₂ gemessen [%]",
    min_value=0.0,
    max_value=20.9,
    value=11.0,
    step=0.1
)

o2_bezug = st.number_input(
    "O₂ Bezug [%]",
    min_value=0.0,
    max_value=20.9,
    value=17.0,
    step=0.1
)

grenzwert1 = st.number_input(
    "Grenzwert LRV [mg/m³]",
    min_value=0.0,
    value=80.0
)

grenzwert2 = st.number_input(
    "Grenzwert TA Luft [mg/m³]",
    min_value=0.0,
    value=50.0
)

toleranz = st.number_input(
    "Toleranz [%]",
    min_value=0.0,
    value=0.0
)

# Berechnung
try:
    # ppm -> mg/m³
    C = 1.606 * toc_ppm

    # Feuchtekorrektur
    C_trocken = C / (1 - rel_feuchte / 100)

    # O2-Korrektur
    toc_calculated = C_trocken * ((21 - o2_bezug) / (21 - o2_gemessen))

    st.subheader("Resultate")

    st.metric(
        "Cgesamt (berechnet) [mg/m³]",
        f"{toc_calculated:.2f}"
    )

    # Grenzwerte inkl. Toleranz
    gw1_eff = grenzwert1 * (1 + toleranz / 100)
    gw2_eff = grenzwert2 * (1 + toleranz / 100)

    status1 = toc_calculated <= gw1_eff
    status2 = toc_calculated <= gw2_eff

    color1 = "green" if status1 else "red"
    color2 = "green" if status2 else "red"

    text1 = "ERFÜLLT" if status1 else "NICHT ERFÜLLT"
    text2 = "ERFÜLLT" if status2 else "NICHT ERFÜLLT"

    st.markdown(
        f"""
        <div style="
            padding:15px;
            border-radius:10px;
            background-color:{color1};
            color:white;
            font-weight:bold;
            text-align:center;">
            Grenzwert LRV: {text1}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown(
        f"""
        <div style="
            padding:15px;
            border-radius:10px;
            background-color:{color2};
            color:white;
            font-weight:bold;
            text-align:center;">
            Grenzwert TA-Luft: {text2}
        </div>
        """,
        unsafe_allow_html=True
    )

except ZeroDivisionError:
    st.error("Ungültige Eingabe: Relative Feuchte oder O₂-Wert führt zu Division durch Null.")
