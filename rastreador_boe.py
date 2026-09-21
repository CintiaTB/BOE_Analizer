"""
=============================================================
RACEADOR INTELIGENTE DEL BOE - CREADO PARA LA COMUNIDAD
=============================================================
Script automatizado para monitorizar el BOE diariamente, buscar
palabras clave y enviar alertas por correo mediante Google Apps Script.
"""

import os
import sys
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from datetime import datetime
import re
import unicodedata
import pdfplumber
import json

# ==========================================================
# ⚙️ CONFIGURACIÓN DEL USUARIO (¡MODIFICA ESTOS DATOS!)
# ==========================================================

# 1. Tu Webhook de Google Apps Script (Sigue los pasos del README.md para obtener el tuyo)
URL_APPS_SCRIPT = "TU_WEBHOOK_DE_GOOGLE_APPS_SCRIPT_AQUI"

# 2. Las direcciones de correo donde quieres recibir las alertas (puedes poner varias separadas por coma)
DESTINATARIOS = ["tu_correo@gmail.com"]

# 3. Tus palabras clave personalizadas para vigilar el BOE
PALABRAS_CLAVE = [
    "TRANSPORTE DE MERCANCIAS", 
    "TACOGRAFO", 
    "RCD", 
    "RESIDUOS",
    "CONTENEDORES", 
    "CAMIONES", 
    "MERCANCIAS PELIGROSAS", 
    "CAP",
    "VEHICULOS PESADOS", 
    "DIESEL"
]

# ==========================================================
# 🔧 FUNCIONES TÉCNICAS (NO NECESITAS MODIFICAR NADA AQUÍ)
# ==========================================================

def obtener_ruta_base():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

RUTA_RAIZ = obtener_ruta_base()
CARPETA_DESCARGAS = os.path.join(RUTA_RAIZ, "Descargas_BOE")
ARCHIVO_LOG = os.path.join(RUTA_RAIZ, "log_boe.txt")
os.makedirs(CARPETA_DESCARGAS, exist_ok=True)

CABECERAS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://www.boe.es/'
}

def escribir_log(texto):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mensaje = f"[{timestamp}] {texto}"
    with open(ARCHIVO_LOG, "a", encoding="utf-8") as log:
        log.write(mensaje + "\n")
    print(mensaje)

def normalizar_texto(texto):
    if not texto: return ""
    texto = unicodedata.normalize("NFKD", str(texto).upper().strip())
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto

def analizar_boe_del_dia():
    fecha_hoy_str = datetime.now().strftime('%d/%m/%Y')
    escribir_log(f"🌐 Consultando novedades del BOE para hoy ({fecha_hoy_str})...")
    alertas = []
    
    url_base_busqueda = "https://www.boe.es/buscar/boe.php"
    
    for palabra in PALABRAS_CLAVE:
        query_params = {
            'campo[1]': 'TITULOS',
            'dato[1]': palabra,
            'accion': 'Buscar',
            'sort_field[0]': 'FPU',
            'sort_order[0]': 'desc'
        }
        url_query = f"{url_base_busqueda}?{urllib.parse.urlencode(query_params)}"
        
        try:
            req = urllib.request.Request(url_query, headers=CABECERAS)
            with urllib.request.urlopen(req, timeout=25) as response:
                html_content = response.read()
                
            soup = BeautifulSoup(html_content, "html.parser")
            escribir_log(f"   🔍 Analizando término '{palabra}'...")
            
            enlaces_boe = soup.find_all('a', href=re.compile(r'BOE-A-\d{4}-\d+'))
            
            for item in enlaces_boe:
                href = item.get('href', '')
                id_match = re.search(r'(BOE-A-\d{4}-\d+)', href)
                if not id_match:
                    continue
                
                id_boe = id_match.group(1)
                titulo = item.text.strip()
                
                if len(titulo) < 5:
                    padre = item.find_parent(['p', 'h4', 'div', 'li'])
                    if padre:
                        titulo = padre.text.strip()
                
                contenedor = item.find_parent(['div', 'tr', 'li', 'p'])
                texto_contenedor = contenedor.text if contenedor else ""
                
                if fecha_hoy_str not in texto_contenedor:
                    continue
                
                url_documento = f"https://www.boe.es/diario_boe/txt.php?id={id_boe}"
                
                if not any(a['ID'] == id_boe for a in alertas):
                    alerta = {
                        'ID': id_boe,
                        'Titulo': titulo or f"Documento oficial {id_boe}",
                        'URL_PDF': url_documento,
                        'Palabras': palabra,
                        'Origen': "BOLETÍN DIARIO"
                    }
                    alertas.append(alerta)
                    escribir_log(f"🚨 ¡MATCH ENCONTRADO HOY [{id_boe}]: {titulo[:60]}...")
                        
        except Exception as e:
            escribir_log(f"❌ Error buscando término '{palabra}': {e}")

    escribir_log(f"✅ Análisis completado. Se han detectado {len(alertas)} alertas estrictamente publicadas hoy.")
    return alertas

def enviar_correo_alertas(alertas):
    if not alertas:
        escribir_log("ℹ️ No se enviará correo, no hay alertas hoy.")
        return
        
    escribir_log("📧 Empaquetando reporte BOE para enviar vía Webhook...")
    asunto = f"🏛️ ALERTAS BOE - {datetime.now().strftime('%d/%m/%Y')}"
    
    cuerpo = f"ANÁLISIS DIARIO DEL BOE ({datetime.now().strftime('%d/%m/%Y')})\n"
    cuerpo += "="*70 + "\n\n"
    cuerpo += f"Se han detectado {len(alertas)} publicaciones relevantes:\n\n"
    
    for i, a in enumerate(alertas, 1):
        cuerpo += f"{i}. 📌 [{a['ID']}] {a['Titulo']}\n"
        cuerpo += f"   🔍 Palabras clave: {a['Palabras']}\n"
        cuerpo += f"   📄 Enlace Oficial: {a['URL_PDF']}\n"
        cuerpo += "-"*70 + "\n"

    payload = {"destinatarios": ", ".join(DESTINATARIOS), "asunto": asunto, "cuerpo": cuerpo, "adjuntos": []}

    try:
        req = urllib.request.Request(URL_APPS_SCRIPT, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                escribir_log("✅ Correo enviado con éxito.")
            else:
                escribir_log("❌ Error enviando correo.")
    except Exception as e: 
        escribir_log(f"❌ Error conectando con Google Apps Script: {e}")

def main():
    escribir_log("\n" + "="*50)
    escribir_log("🚀 INICIANDO MONITOR BOE PERSONALIZADO")
    escribir_log("="*50)
    
    alertas = analizar_boe_del_dia()
    enviar_correo_alertas(alertas)
    
    escribir_log("✅ FIN DEL PROCESO")

if __name__ == "__main__":
    main()