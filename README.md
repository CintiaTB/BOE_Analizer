# 🏛️ Radar Automatizado del BOE con Alertas por Email

Script en Python diseñado para rastrear diariamente el **Boletín Oficial del Estado (BOE)**, filtrar decretos, resoluciones o normativas mediante palabras clave personalizadas y enviar un resumen directamente a tu correo electrónico utilizando un Webhook gratuito de Google Apps Script.

---

## 📋 Requisitos Previos

1. Tener instalado **Python** (versión 3.8 o superior) en tu ordenador.
2. Una cuenta de correo de **Google (Gmail)**.

---

## 🚀 Guía de Instalación Paso a Paso

### Paso 1: Clonar o descargar el repositorio
Descarga los archivos del proyecto en una carpeta local de tu equipo.

### Paso 2: Instalar las dependencias necesarias
Abre tu terminal o línea de comandos dentro de la carpeta del proyecto e instala las librerías necesarias ejecutando:
```bash
pip install beautifulsoup4 pdfplumber requests
