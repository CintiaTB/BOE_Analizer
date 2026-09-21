Markdown
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
```
Paso 3: ⚙️ Configuración del Envío de Correos (Google Apps Script)
Para que el script pueda enviarte correos automáticos sin necesidad de configurar servidores SMTP complejos, utilizaremos Google Apps Script de forma totalmente gratuita.

Entra en Google Apps Script e inicia sesión con tu cuenta de Google.

Haz clic en Nuevo proyecto.

Borra todo el código que aparece por defecto y pega el siguiente script:
```bash
JavaScript
function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var destinatarios = data.destinatarios;
    var asunto = data.asunto;
    var cuerpo = data.cuerpo;
    
    MailApp.sendEmail(destinatarios, asunto, cuerpo);
    
    return ContentService.createTextOutput(JSON.stringify({"status": "ok"}))
                         .setMimeType(ContentService.MimeType.JSON);
  } catch(error) {
    return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": error.toString()}))
                         .setMimeType(ContentService.MimeType.JSON);
  }
}
```
Haz clic en el botón superior derecho Implementar > Nueva implementación.

En "Seleccionar tipo", elige Aplicación web.

Configura los siguientes campos:

Descripción: API Envio Correos BOE

Ejecutar como: Yo

Quién tiene acceso: Cualquier usuario (Importante para que Python pueda comunicarse con él).

Haz clic en Implementar, concede los permisos de tu cuenta de Google que te solicite y copia la URL de la aplicación web que te aparecerá al finalizar.

Paso 4: 🛠️ Configuración del Script de Python
Abre el archivo rastreador_boe.py con cualquier editor de código (como VS Code o Bloc de notas).

Modifica las variables de la sección de configuración al inicio del archivo:

Pega la URL de tu Webhook en URL_APPS_SCRIPT = "TU_URL_AQUI".

Añade tu correo electrónico en DESTINATARIOS = ["tu_correo@gmail.com"].

Personaliza tu lista de PALABRAS_CLAVE con los términos que desees vigilar.

Guarda los cambios.

Paso 5: ⏱️ Automatización Diaria en Windows (Opcional)
Si deseas que el script se ejecute automáticamente todos los días laborables de forma desatendida:

Crea un archivo .bat (por ejemplo, ejecutar.bat) dentro de la carpeta del proyecto con el siguiente contenido:
```bash
DOS
@echo off
title Rastreador BOE
cd /d "%~dp0"
python rastreador_boe.py
pause
```
Abre el Programador de Tareas de Windows, crea una tarea básica programada diariamente a la hora que prefieras y asóciala a la ejecución de este archivo .bat.

💡 Consejo: Te recomendamos programarlo sobre las 09:30 o 10:00 de la mañana, asegurando así que el BOE diario ya se encuentre completamente publicado y accesible en los servidores oficiales.
Markdown
# 🏛️ Automated BOE Radar with Email Alerts

Python script designed to daily track the **Official State Gazette of Spain (BOE)**, filter decrees, resolutions, or regulations using customized keywords, and send a summary directly to your email using a free Google Apps Script Webhook.

---

## 📋 Prerequisites

1. **Python** installed (version 3.8 or higher) on your computer.
2. A **Google (Gmail)** account.

---

## 🚀 Step-by-Step Installation Guide

### Step 1: Clone or download the repository
Download the project files into a local folder on your computer.

### Step 2: Install required dependencies
Open your terminal or command prompt inside the project folder and install the required libraries by running:

```bash
pip install beautifulsoup4 pdfplumber requests
```
Step 3: ⚙️ Configuring Email Delivery (Google Apps Script)
To allow the script to send you automated emails without configuring complex SMTP servers, we will use Google Apps Script completely free of charge.

Go to Google Apps Script and sign in with your Google account.

Click on New project.

Delete all the default code and paste the following script:
```bash
JavaScript
function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var destinatarios = data.destinatarios;
    var asunto = data.asunto;
    var cuerpo = data.cuerpo;
    
    MailApp.sendEmail(destinatarios, asunto, cuerpo);
    
    return ContentService.createTextOutput(JSON.stringify({"status": "ok"}))
                         .setMimeType(ContentService.MimeType.JSON);
  } catch(error) {
    return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": error.toString()}))
                         .setMimeType(ContentService.MimeType.JSON);
  }
}
```
Click on the top right button Deploy > New deployment.

Under "Select type", choose Web app.

Configure the following fields:

Description: API BOE Email Alerts

Execute as: Me

Who has access: Anyone (Important so Python can communicate with it).

Click Deploy, grant the requested permissions for your Google account, and copy the web app URL generated at the end.

Step 4: 🛠️ Configuring the Python Script
Open the rastreador_boe.py file with any code editor (such as VS Code or Notepad).

Modify the configuration variables at the top of the file:

Paste your Webhook URL in URL_APPS_SCRIPT = "YOUR_URL_HERE".

Add your email address in DESTINATARIOS = ["your_email@gmail.com"].

Customize your PALABRAS_CLAVE (Keywords) list with the terms you want to monitor.

Save your changes.

Step 5: ⏱️ Daily Automation in Windows (Optional)
If you want the script to run automatically every workday unattended:

Create a .bat file (for example, run.bat) inside the project folder with the following content:
```bash
DOS
@echo off
title BOE Tracker
cd /d "%~dp0"
python rastreador_boe.py
pause
```
Open the Windows Task Scheduler, create a basic task scheduled to run daily at your preferred time, and link it to execute this .bat file.

💡 Tip: We recommend scheduling it around 09:30 or 10:00 AM, ensuring that the daily BOE is fully published and accessible on the official servers.
