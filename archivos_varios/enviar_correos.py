"""
Script para envío masivo de correos desde base de datos MySQL (cPanel).
Se conecta al servidor SMTP de cPanel y envía correos uno a uno
con un tiempo de espera de 20 segundos entre cada envío.
Marca fecha_envio y enviado=1 en la tabla tras cada envío exitoso.
Guarda copia en la carpeta "Sent" del buzón IMAP.
"""

import smtplib
import imaplib
import time
import uuid
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate, formataddr

import pymysql

# ─────────────────────────────────────────────
# CONFIGURACIÓN SMTP / IMAP (cPanel)
# ─────────────────────────────────────────────
SMTP_HOST = "mail.crsensores.com"
SMTP_PORT = 465                         # 465 SSL
IMAP_HOST = "mail.crsensores.com"
IMAP_PORT = 993                         # 993 SSL
SMTP_USER = "comercial@crsensores.com"
SMTP_PASSWORD = "C0m3rc14l26+"

# ─────────────────────────────────────────────
# CONFIGURACIÓN BASE DE DATOS MySQL (cPanel)
# ─────────────────────────────────────────────
DB_HOST = "crsensores.com"
DB_USER = "crsensor_harol"           # Usuario de la BD en cPanel
DB_PASSWORD = "bd_4dm1n2026+"
DB_NAME = "crsensor_clientes"
DB_TABLE = "envio_mail"

# ─────────────────────────────────────────────
# CONFIGURACIÓN DEL CORREO
# ─────────────────────────────────────────────
REMITENTE_NOMBRE = "Camila Rivera CRSensores"
ASUNTO = "CRSensores - Proveedor de sensores electrónicos para sus proyectos - {empresa}"
TIEMPO_ESPERA = 20  # Segundos entre cada envío

# ─────────────────────────────────────────────
# FIRMA HTML
# ─────────────────────────────────────────────
FIRMA_HTML = """
<table style="font-family: Arial, sans-serif; font-size: 13px; color: #333; border-top: 2px solid #0056b3; padding-top: 12px; margin-top: 20px;" cellpadding="0" cellspacing="0">
  <tr>
    <td align="center" style="padding-bottom: 12px;">
      <img src="https://crsensores.com/Imagenes/firmas/firma_camila.png" alt="CRSensores" width="320" style="border-radius: 6px; display: block;">
    </td>
  </tr>
  <tr>
    <td align="center" style="line-height: 1.6;">
      <strong style="color: #0056b3;">CRSensores</strong> — Sensores Electrónicos de Alta Precisión<br>
      <span>📞 <a href="https://wa.link/ut9tul" style="color: #0056b3; text-decoration: none;">WhatsApp</a></span> &nbsp;|&nbsp;
      <span>📧 comercial@crsensores.com</span><br>
      <span>🌐 <a href="https://crsensores.com/" style="color: #0056b3; text-decoration: none;">www.crsensores.com</a></span>
    </td>
  </tr>
</table>
"""


def generar_cuerpo_texto(empresa):
    """Genera la versión en texto plano del correo."""
    return f"""Buenas tardes, equipo de {empresa}:

Espero que se encuentren muy bien.

Me pongo en contacto con ustedes porque sigo de cerca el trabajo que realiza {empresa} en el sector industrial y sé que la confiabilidad y precisión de sus procesos son fundamentales para mantener la eficiencia de sus líneas de producción.

Mi nombre es Camila Rivera y hago parte del equipo de CRSensores, empresa especializada en el suministro de sensores electrónicos de alta precisión para la industria. Acompañamos a nuestros clientes con soluciones que les permiten:

- Optimizar los tiempos de respuesta de sus sistemas de control.
- Reducir significativamente los costos asociados a fallas técnicas y mantenimientos correctivos.
- Contar con un suministro ágil, disponibilidad inmediata y atención personalizada.

Me gustaría compartirles nuestro portafolio de productos y conocer si actualmente tienen necesidades en las que podamos aportar valor como aliados estratégicos. Puede consultar nuestra oferta en https://crsensores.com/

Si es posible, agradecería que me indicaran con quién podría comunicarme del área de Mantenimiento, Compras o Cadena de Suministro, o bien coordinar una breve llamada de 5 minutos la próxima semana.

Quedo atenta a sus comentarios y agradezco de antemano su tiempo y atención.

Cordialmente,
WhatsApp: https://wa.link/ut9tul
Email: comercial@crsensores.com
Web: https://crsensores.com/
"""


def generar_cuerpo(empresa):
    """Genera el cuerpo HTML del correo con enfoque de contacto en frío."""
    cuerpo = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">

        <p>Buen día, equipo de <strong>{empresa}</strong>:</p>

        <p>Espero que se encuentren muy bien.</p>

        <p>Me pongo en contacto con ustedes porque sigo de cerca el trabajo que
        realiza <strong>{empresa}</strong> en el sector industrial y sé que la
        confiabilidad y precisión de sus procesos son fundamentales para mantener
        la eficiencia de sus líneas de producción.</p>

        <p>Mi nombre es Camila Rivera y hago parte del equipo de <strong>CRSensores</strong>,
        empresa especializada en el suministro de sensores electrónicos de alta precisión
        para la industria. Acompañamos a nuestros clientes con soluciones que les permiten:</p>

        <ul>
            <li><strong>Optimizar los tiempos de respuesta</strong> de sus sistemas de control.</li>
            <li><strong>Reducir significativamente los costos</strong> asociados a fallas técnicas
            y mantenimientos correctivos.</li>
            <li>Contar con un <strong>suministro ágil, disponibilidad inmediata</strong> y atención
            personalizada de acuerdo con los requerimientos de cada proyecto.</li>
        </ul>

        <p>Me gustaría compartirles nuestro portafolio de productos y conocer si actualmente
        tienen necesidades en las que podamos aportar valor como aliados estratégicos.
        Puede consultar nuestra oferta en
        <a href="https://crsensores.com/" style="color: #0056b3;">www.crsensores.com</a>.</p>

        <p>Si es posible, agradecería que me indicaran con quién podría comunicarme del área de
        <strong>Mantenimiento, Compras o Cadena de Suministro</strong>, o bien coordinar una
        breve llamada de 5 minutos la próxima semana para presentarnos y explorar oportunidades
        de colaboración.</p>

        <p>Quedo atenta a sus comentarios y agradezco de antemano su tiempo y atención.</p>

        <p>Cordialmente,</p>

        {FIRMA_HTML}

    </body>
    </html>
    """
    return cuerpo


def guardar_en_enviados(mensaje_str):
    """Guarda una copia del correo en la carpeta Sent vía IMAP."""
    try:
        imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
        imap.login(SMTP_USER, SMTP_PASSWORD)
        # cPanel usa "INBOX.Sent" o "Sent" según configuración
        # Intentar primero "INBOX.Sent", si falla usar "Sent"
        carpeta_sent = "INBOX.Sent"
        status, _ = imap.select(carpeta_sent)
        if status != "OK":
            carpeta_sent = "Sent"
            imap.select(carpeta_sent)
        imap.append(
            carpeta_sent,
            "\\Seen",
            imaplib.Time2Internaldate(time.time()),
            mensaje_str.encode("utf-8"),
        )
        imap.logout()
    except Exception as e:
        print(f"    ⚠ No se pudo guardar copia en Enviados: {e}")


def obtener_contactos_pendientes(conexion):
    """Consulta los registros que aún no han sido enviados."""
    with conexion.cursor() as cursor:
        cursor.execute(
            f"SELECT id, empresa, email FROM {DB_TABLE} WHERE enviado = 0 OR enviado IS NULL"
        )
        return cursor.fetchall()


def marcar_enviado(conexion, registro_id):
    """Actualiza fecha_envio y enviado=1 para el registro."""
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with conexion.cursor() as cursor:
        cursor.execute(
            f"UPDATE {DB_TABLE} SET fecha_envio = %s, enviado = 1 WHERE id = %s",
            (ahora, registro_id),
        )
    conexion.commit()


def enviar_correo(servidor, destinatario, empresa):
    """Arma y envía un correo individual. Retorna el mensaje como string."""
    mensaje = MIMEMultipart("alternative")
    mensaje["From"] = formataddr((REMITENTE_NOMBRE, SMTP_USER))
    mensaje["To"] = destinatario
    mensaje["Subject"] = ASUNTO.format(empresa=empresa)
    mensaje["Date"] = formatdate(localtime=True)
    mensaje["Message-ID"] = f"<{uuid.uuid4()}@crsensores.com>"
    mensaje["Reply-To"] = SMTP_USER
    mensaje["List-Unsubscribe"] = f"<mailto:{SMTP_USER}?subject=Desuscribir>"

    cuerpo_html = generar_cuerpo(empresa)
    cuerpo_texto = generar_cuerpo_texto(empresa)
    mensaje.attach(MIMEText(cuerpo_texto, "plain"))
    mensaje.attach(MIMEText(cuerpo_html, "html"))

    mensaje_str = mensaje.as_string()
    servidor.sendmail(SMTP_USER, destinatario, mensaje_str)
    return mensaje_str


def main():
    """Lee la BD y envía correos uno a uno con espera entre envíos."""

    # Conectar a MySQL
    try:
        conexion = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset="utf8mb4",
        )
        print("Conexión a base de datos establecida.")
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        return

    # Obtener contactos pendientes
    contactos = obtener_contactos_pendientes(conexion)

    if not contactos:
        print("No hay correos pendientes de envío.")
        conexion.close()
        return

    print(f"Se encontraron {len(contactos)} correo(s) pendientes.")
    print(f"Tiempo de espera entre correos: {TIEMPO_ESPERA} segundos")
    print("-" * 50)

    # Conectar al servidor SMTP con SSL
    try:
        servidor = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=30)
        servidor.ehlo()
        servidor.login(SMTP_USER, SMTP_PASSWORD)
        servidor.ehlo()
        print("Conexión SMTP establecida correctamente.\n")
    except Exception as e:
        print(f"Error al conectar con el servidor SMTP: {e}")
        conexion.close()
        return

    # Enviar correos uno a uno
    enviados = 0
    errores = 0

    for i, contacto in enumerate(contactos, start=1):
        reg_id, empresa, email = contacto

        try:
            mensaje_str = enviar_correo(servidor, email, empresa)
            marcar_enviado(conexion, reg_id)
            guardar_en_enviados(mensaje_str)
            enviados += 1
            print(f"[{i}/{len(contactos)}] ✓ Enviado a: {empresa} ({email})")
        except Exception as e:
            errores += 1
            print(f"[{i}/{len(contactos)}] ✗ Error al enviar a {email}: {e}")

        # Esperar entre envíos (excepto en el último)
        if i < len(contactos):
            print(f"    Esperando {TIEMPO_ESPERA} segundos...")
            time.sleep(TIEMPO_ESPERA)

    # Cerrar conexiones
    servidor.quit()
    conexion.close()

    # Resumen
    print("\n" + "=" * 50)
    print("RESUMEN DE ENVÍO")
    print("=" * 50)
    print(f"Total pendientes: {len(contactos)}")
    print(f"Enviados exitosamente: {enviados}")
    print(f"Errores: {errores}")


if __name__ == "__main__":
    main()
