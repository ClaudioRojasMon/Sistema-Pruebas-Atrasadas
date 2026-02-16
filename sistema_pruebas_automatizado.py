#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema Automatizado de Pruebas Atrasadas
Procesa emails de Gmail e inserta en Google Sheets
"""

import imaplib
import email
from email.header import decode_header
import gspread
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import time

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

EMAIL_COLEGIO = "crojas@colsanjavier.cl"
EMAIL_PASSWORD = "lbfeqhmrianvxala"  # Cambiar por la real
GOOGLE_SHEETS_ID = "1H9b-dxrMN0Guzj69fkk-oHbgtjdAbH1TCyfKnJIWRyc"

# ============================================================================
# CLASES
# ============================================================================

class EmailParser:
    CURSO_A_CICLO = {
        '7°A': 'III°CICLO', '7°B': 'III°CICLO', '7°C': 'III°CICLO',
        '7ºA': 'III°CICLO', '7ºB': 'III°CICLO', '7ºC': 'III°CICLO',
        '1°A': 'III°CICLO', '1°B': 'III°CICLO', '1°C': 'III°CICLO',
        '1ºA': 'III°CICLO', '1ºB': 'III°CICLO', '1ºC': 'III°CICLO',
        'I°A': 'III°CICLO', 'I°B': 'III°CICLO', 'I°C': 'III°CICLO',
        'IºA': 'III°CICLO', 'IºB': 'III°CICLO', 'IºC': 'III°CICLO',
        '2°A': 'IV°CICLO', '2°B': 'IV°CICLO', '2°C': 'IV°CICLO',
        '2ºA': 'IV°CICLO', '2ºB': 'IV°CICLO', '2ºC': 'IV°CICLO',
        'II°A': 'IV°CICLO', 'II°B': 'IV°CICLO', 'II°C': 'IV°CICLO',
        'IIºA': 'IV°CICLO', 'IIºB': 'IV°CICLO', 'IIºC': 'IV°CICLO',
        '3°A': 'IV°CICLO', '3°B': 'IV°CICLO', '3°C': 'IV°CICLO',
        '3ºA': 'IV°CICLO', '3ºB': 'IV°CICLO', '3ºC': 'IV°CICLO',
        'III°A': 'IV°CICLO', 'III°B': 'IV°CICLO', 'III°C': 'IV°CICLO',
        'IIIºA': 'IV°CICLO', 'IIIºB': 'IV°CICLO', 'IIIºC': 'IV°CICLO',
        '4°A': 'IV°CICLO', '4°B': 'IV°CICLO', '4°C': 'IV°CICLO',
        '4ºA': 'IV°CICLO', '4ºB': 'IV°CICLO', '4ºC': 'IV°CICLO',
        'IV°A': 'IV°CICLO', 'IV°B': 'IV°CICLO', 'IV°C': 'IV°CICLO',
        'IVºA': 'IV°CICLO', 'IVºB': 'IV°CICLO', 'IVºC': 'IV°CICLO',
    }
    
    MESES = {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
             'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12}
    
    DIAS_SEMANA = {'lunes': 'LUNES', 'martes': 'MARTES', 'miercoles': 'MIERCOLES',
                   'miércoles': 'MIERCOLES', 'jueves': 'JUEVES', 'viernes': 'VIERNES',
                   'sabado': 'SABADO', 'sábado': 'SABADO'}
    
    def __init__(self, texto_email: str, asunto_email: str):
        self.texto = texto_email
        self.asunto = asunto_email
    
    def parsear(self) -> dict:
        # Nombre y curso
        patron_nombre = r'familia de\s+(.+?)\s+(IV°[A-C]|III°[A-C]|II°[A-C]|I°[A-C]|[1-4]°[A-C]|[1-7]°[A-C])'
        match_nombre = re.search(patron_nombre, self.texto, re.IGNORECASE)
        
        if match_nombre:
            nombre = match_nombre.group(1).strip()
            curso = match_nombre.group(2).strip()
        else:
            patron_viejo = r'PRUEBA ATRASADA\s+(.+?)\s+(IV°[A-C]|III°[A-C]|[1-4]°[A-C])'
            match_viejo = re.search(patron_viejo, self.asunto, re.IGNORECASE)
            nombre = match_viejo.group(1).strip() if match_viejo else None
            curso = match_viejo.group(2).strip() if match_viejo else None
        
        # Asignatura
        patron_asig = r'\*?Asignatura:\*?\s*(.+?)(?:\r\n|\n|$)'
        match_asig = re.search(patron_asig, self.texto, re.IGNORECASE)
        asignatura = match_asig.group(1).strip() if match_asig else None
        
        # Fecha
        patron_fecha = r'\*?Fecha de realizaci[oó]n:\*?\s*(\w+)\s+(\d+)\s+de\s+(\w+)'
        match_fecha = re.search(patron_fecha, self.texto, re.IGNORECASE)
        
        nombre_hoja = None
        if match_fecha:
            dia_semana = match_fecha.group(1).lower()
            dia = int(match_fecha.group(2))
            mes = match_fecha.group(3).lower()
            dia_formato = self.DIAS_SEMANA.get(dia_semana, dia_semana.upper())
            mes_num = self.MESES.get(mes, 0)
            nombre_hoja = f"{dia_formato} {dia:02d}{mes_num:02d}"
        
        # Duración
        patron_dur = r'\*?[Dd]uraci[oó]n:\s*(\d+)\s*minutos?'
        match_dur = re.search(patron_dur, self.texto, re.IGNORECASE)
        duracion = f"{match_dur.group(1)} minutos" if match_dur else None
        
        return {
            'nombre_estudiante': nombre,
            'curso': curso,
            'ciclo': self.CURSO_A_CICLO.get(curso, 'DESCONOCIDO'),
            'asignatura': asignatura,
            'nombre_hoja': nombre_hoja,
            'duracion': duracion,
            'observaciones': f"El control tiene una duración de {duracion}." if duracion else "",
            'asistencia': ''
        }


class ValidadorPruebas:
    def __init__(self, spreadsheet):
        self.spreadsheet = spreadsheet
    
    def normalizar_texto(self, texto):
        if not texto:
            return ""
        
        reemplazos = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
            'ñ': 'n', 'Ñ': 'N'
        }
        
        texto_normalizado = texto
        for viejo, nuevo in reemplazos.items():
            texto_normalizado = texto_normalizado.replace(viejo, nuevo)
        
        return texto_normalizado.strip().upper()
    
    def contar_pruebas_estudiante(self, nombre_hoja, nombre_estudiante, asignatura):
        try:
            worksheet = self.spreadsheet.worksheet(nombre_hoja)
            datos = worksheet.get_all_values()
            
            nombre_normalizado = self.normalizar_texto(nombre_estudiante)
            asignatura_normalizada = self.normalizar_texto(asignatura)
            
            num_pruebas = 0
            tiene_esta_asignatura = False
            
            for fila in datos[7:]:  
                if len(fila) >= 4:
                    nombre_en_fila = self.normalizar_texto(fila[2])
                    asignatura_en_fila = self.normalizar_texto(fila[3])
                    
                    if nombre_en_fila == nombre_normalizado:
                        num_pruebas += 1
                        if asignatura_en_fila == asignatura_normalizada:
                            tiene_esta_asignatura = True
            
            prueba_seria = num_pruebas + 1
            
            if num_pruebas >= 2:
                return {
                    'valido': False,
                    'num_pruebas': num_pruebas,
                    'mensaje': f'❌ RECHAZADO ({prueba_seria}/2) - LÍMITE EXCEDIDO'
                }
            elif tiene_esta_asignatura:
                return {
                    'valido': True,
                    'num_pruebas': num_pruebas,
                    'mensaje': f'✅ VÁLIDO ({prueba_seria}/2) - Reemplazará {asignatura}'
                }
            else:
                return {
                    'valido': True,
                    'num_pruebas': num_pruebas,
                    'mensaje': f'✅ VÁLIDO ({prueba_seria}/2) - Prueba {prueba_seria}'
                }
        
        except Exception as e:
            return {
                'valido': False,
                'num_pruebas': 0,
                'mensaje': f'❌ ERROR: {str(e)}'
            }


class ResponderEmails:
    def __init__(self, email_usuario, password):
        self.email_usuario = email_usuario
        self.password = password
    
    def enviar_confirmacion_inscripcion(self, destinatario, nombre_estudiante, curso, asignatura, fecha_hoja):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_usuario
            msg['To'] = destinatario
            msg['Subject'] = f"✅ Inscripción exitosa - {nombre_estudiante} - {asignatura}"
            
            cuerpo = f"""
Estimado/a profesor/a:

La inscripción de la prueba atrasada ha sido procesada exitosamente:

• Estudiante: {nombre_estudiante}
• Curso: {curso}
• Asignatura: {asignatura}
• Fecha programada: {fecha_hoja}

El estudiante ha sido inscrito en el sistema.

Saludos cordiales,
Sistema Automatizado de Pruebas Atrasadas
            """
            
            msg.attach(MIMEText(cuerpo, 'plain'))
            
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(self.email_usuario, self.password)
            server.send_message(msg)
            server.quit()
            
            return True
        
        except Exception as e:
            print(f"    Error al enviar confirmación: {e}")
            return False
    
    def enviar_rechazo_limite(self, destinatario, nombre_estudiante, curso, asignatura, num_pruebas):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_usuario
            msg['To'] = destinatario
            msg['Subject'] = f"❌ Inscripción rechazada - {nombre_estudiante} - Límite excedido"
            
            cuerpo = f"""
Estimado/a profesor/a:

La inscripción de la prueba atrasada NO pudo ser procesada:

• Estudiante: {nombre_estudiante}
• Curso: {curso}
• Asignatura: {asignatura}

MOTIVO: El estudiante ya tiene {num_pruebas} pruebas inscritas para esa fecha.
Según reglamento, el límite máximo es de 2 pruebas por día.

Por favor, coordine una fecha alternativa o comuníquese con el Director Academico o la Dirección de ciclo respectiva.

Saludos cordiales,
Sistema Automatizado de Pruebas Atrasadas
            """
            
            msg.attach(MIMEText(cuerpo, 'plain'))
            
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(self.email_usuario, self.password)
            server.send_message(msg)
            server.quit()
            
            return True
        
        except Exception as e:
            print(f"    Error al enviar rechazo: {e}")
            return False


# ============================================================================
# FUNCIONES
# ============================================================================

def conectar_gmail():
    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(EMAIL_COLEGIO, EMAIL_PASSWORD)
        return imap
    except Exception as e:
        print(f"ERROR conectando a Gmail: {e}")
        return None


def leer_emails_pruebas(limite=10):
    imap = conectar_gmail()
    if not imap:
        return []
    
    try:
        imap.select("INBOX")
        status, messages = imap.search(None, 'SUBJECT "PRUEBA ATRASADA"', 'UNSEEN')
        email_ids = messages[0].split()
        
        print(f"Emails no leidos: {len(email_ids)}")
        
        emails = []
        for email_id in email_ids[-limite:]:
            status, msg_data = imap.fetch(email_id, "(BODY.PEEK[])")
            msg = email.message_from_bytes(msg_data[0][1])
            
            asunto = decode_header(msg["Subject"])[0][0]
            if isinstance(asunto, bytes):
                asunto = asunto.decode()
            
            cuerpo = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        cuerpo = part.get_payload(decode=True).decode()
                        break
            else:
                cuerpo = msg.get_payload(decode=True).decode()
            
            emails.append({'asunto': asunto, 'cuerpo': cuerpo})
        
        imap.close()
        imap.logout()
        return emails
    
    except Exception as e:
        print(f"ERROR: {e}")
        return []


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 80)
    print(f"EJECUCIÓN AUTOMÁTICA - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Conectar Google Sheets
    try:
        gc = gspread.oauth(
            credentials_filename='credentials.json',
            authorized_user_filename='token.json'
        )
        spreadsheet = gc.open_by_key(GOOGLE_SHEETS_ID)
        print(f"✅ Conectado a Google Sheets")
    except Exception as e:
        print(f"❌ ERROR conectando a Google Sheets: {e}")
        return
    
    # Leer emails
    emails = leer_emails_pruebas(limite=10)
    
    if not emails:
        print("\nNo hay emails nuevos para procesar")
        return
    
    # Procesar
    validador = ValidadorPruebas(spreadsheet)
    respondedor = ResponderEmails(EMAIL_COLEGIO, EMAIL_PASSWORD)
    
    for i, email_data in enumerate(emails, 1):
        print(f"\n[{i}/{len(emails)}] {email_data['asunto'][:50]}...")
        
        parser = EmailParser(email_data['cuerpo'], email_data['asunto'])
        datos = parser.parsear()
        
        print(f"  Estudiante: {datos['nombre_estudiante']}")
        print(f"  Curso: {datos['curso']}")
        print(f"  Asignatura: {datos['asignatura']}")
        print(f"  Hoja: {datos['nombre_hoja']}")
        
        validacion = validador.contar_pruebas_estudiante(
            datos['nombre_hoja'],
            datos['nombre_estudiante'],
            datos['asignatura']
        )
        
        print(f"  {validacion['mensaje']}")
        
        if validacion['valido']:
            try:
                worksheet = spreadsheet.worksheet(datos['nombre_hoja'])
                
                nueva_fila = [
                    datos['ciclo'],
                    datos['curso'],
                    datos['nombre_estudiante'],
                    datos['asignatura'],
                    datos['asistencia'],
                    datos['observaciones']
                ]
                
                worksheet.append_row(nueva_fila)
                print(f"  ✅ INSCRITO en Google Sheets")
                
                respondedor.enviar_confirmacion_inscripcion(
                    EMAIL_COLEGIO,
                    datos['nombre_estudiante'],
                    datos['curso'],
                    datos['asignatura'],
                    datos['nombre_hoja']
                )
                print(f"  📧 Email de confirmación enviado")
                
            except Exception as e:
                print(f"  ❌ ERROR al insertar: {e}")
        
        else:
            print(f"  ⛔ NO SE INSCRIBE - Límite excedido")
            
            respondedor.enviar_rechazo_limite(
                EMAIL_COLEGIO,
                datos['nombre_estudiante'],
                datos['curso'],
                datos['asignatura'],
                validacion['num_pruebas']
            )
            print(f"  📧 Email de rechazo enviado")
    
    print(f"\n=" * 80)
    print(f"COMPLETADO: {len(emails)} emails procesados")
    print(f"=" * 80)


if __name__ == "__main__":
    main()
