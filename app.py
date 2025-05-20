import streamlit as st
import zipfile
import io

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

    st.success(f"Se han creado {len(bloques)} bloques.")

    # Crear archivo ZIP en memoria
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for i, bloque in enumerate(bloques, start=1):
            contenido_bloque = "\n".join(bloque)
            zip_file.writestr(f"bloque_{i}.txt", contenido_bloque)
    
    st.download_button(
        label="📥 Descargar bloques en ZIP",
        data=zip_buffer.getvalue(),
        file_name="bloques_divididos.zip",
        mime="application/zip"
    )
