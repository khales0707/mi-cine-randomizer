import pandas as pd
import json
import os
import glob

# Ruta de las listas
ruta_listas = 'listas/*.csv'
archivos = glob.glob(ruta_listas)

peliculas_unicas = set()

print(f"Buscando en: {os.path.abspath('listas')}")

for archivo in archivos:
    try:
        # IMPORTANTE: skiprows=1 salta el encabezado 'Letterboxd list export v7'
        df = pd.read_csv(archivo, skiprows=1, on_bad_lines='skip')
        
        # Buscamos la columna de título
        columna_titulo = None
        for col in ['Name', 'Title', 'name', 'title']:
            if col in df.columns:
                columna_titulo = col
                break
        
        if columna_titulo:
            titulos = df[columna_titulo].dropna().unique().tolist()
            peliculas_unicas.update(titulos)
            print(f"✅ {os.path.basename(archivo)}: Leídas {len(titulos)} películas.")
        else:
            # Si aún falla, intentamos leer sin saltar filas por si algún archivo es distinto
            df_fallback = pd.read_csv(archivo)
            for col in ['Name', 'Title']:
                if col in df_fallback.columns:
                    titulos = df_fallback[col].dropna().unique().tolist()
                    peliculas_unicas.update(titulos)
                    print(f"✅ {os.path.basename(archivo)}: Leídas {len(titulos)} películas (modo simple).")
                    columna_titulo = "Encontrado"
                    break
            
            if not columna_titulo:
                print(f"❌ Error en {os.path.basename(archivo)}: No se halló columna 'Name' o 'Title'.")
            
    except Exception as e:
        print(f"⚠️ Error procesando {archivo}: {e}")

# Guardar resultados
lista_final = sorted(list(peliculas_unicas))

with open('peliculas.json', 'w', encoding='utf-8') as f:
    json.dump(lista_final, f, ensure_ascii=False, indent=4)

print("-" * 30)
print(f"¡Éxito! Se generó 'peliculas.json' con {len(lista_final)} películas únicas.")