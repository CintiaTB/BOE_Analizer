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
@echo off
title Rastreador BOE
cd /d "%~dp0"
python rastreador_boe.py
pause
Abre el Programador de Tareas de Windows, crea una tarea básica programada diariamente a la hora que prefieras y asóciala a la ejecución de este archivo .bat.

💡 Consejo: Te recomendamos programarlo sobre las 09:30 o 10:00 de la mañana, asegurando así que el BOE diario ya se encuentre completamente publicado y accesible en los servidores oficiales.
