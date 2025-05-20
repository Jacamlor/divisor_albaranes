import streamlit as st

def dividir_en_bloques(lineas, minimo=500, maximo=650):
    bloques = []
    bloque_actual = []
    suma_actual = 0

    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue

        try:
            unidades = int(linea.split(",")[1])
        except:
            continue  # saltar líneas mal formadas

        if suma_actual + unidades > maximo:
            bloques.append(bloque_actual.copy())
            bloque_actual = []
            suma_actual = 0

        bloque_actual.append(linea)
        suma_actual += unidades

    if bloque_actual:
        bloques.append(bloque_actual)

    return bloques

st.title("📦 Dividir archivo TXT por bloques de unidades")

uploaded_file = st.file_uploader("Sube el archivo .txt", type=["txt"])

if uploaded_file is not None:
    contenido = uploaded_file.read().decode("utf-8")
    lineas = contenido.strip().splitlines()

    bloques = dividir_en_bloques(lineas)

    st.success(f"Se han generado {len(bloques)} bloques (archivos).")

    for i, bloque in enumerate(bloques, start=1):
        contenido_txt = "\n".join(bloque)
        st.download_button(
            label=f"📄 Descargar bloque {i}",
            data=contenido_txt,
            file_name=f"bloque_{i}.txt",
            mime="text/plain"
        )
