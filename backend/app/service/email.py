import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from env.env import FROM_EMAIL, FROM_PASSWORD, SMTP_SERVER, SMTP_PORT
from env.router import IMAGE_PATH

def send_email(TO_EMAIL: str, SUBJECT: str, BODY: str, IMAGE_PATH: str = None):

    # Crear el mensaje
    message = MIMEMultipart()
    message["From"] = FROM_EMAIL
    message["To"] = TO_EMAIL
    message["SUBJECT"] = SUBJECT

    # Crear el cuerpo del mensaje
    html_BODY = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Correo Electrónico</title>
            <style>
                /* Diseño general del cuerpo */
                BODY {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f7fa;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }}

                /* Contenedor principal */
                .container {{
                    background-color: #ffffff;
                    border-radius: 12px;
                    width: 80%;
                    max-width: 700px;
                    padding: 40px;
                    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
                    text-align: center;
                }}

                /* Título principal */
                h1 {{
                    font-size: 2.5rem;
                    color: #FF5733;
                    margin-bottom: 20px;
                    font-weight: 600;
                }}

                /* Párrafos de texto */
                p {{
                    font-size: 1.1rem;
                    color: #333;
                    margin-bottom: 20px;
                    line-height: 1.6;
                    text-align: left;
                }}

                /* Estilo de la imagen */
                .image {{
                    max-width: 80%;
                    height: auto;
                    margin: 30px 0;
                    border-radius: 10px;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
                }}

                /* Botón de llamada a la acción */
                .cta-button {{
                    display: inline-block;
                    padding: 12px 30px;
                    margin-top: 20px;
                    background-color: #FF5733;
                    color: white;
                    font-size: 1rem;
                    text-decoration: none;
                    border-radius: 6px;
                    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
                    transition: background-color 0.3s;
                }}

                .cta-button:hover {{
                    background-color: #FF3D00;
                }}

                /* Pie de página */
                .footer {{
                    font-size: 0.9rem;
                    color: #888;
                    margin-top: 30px;
                }}

                .footer a {{
                    color: #FF5733;
                    text-decoration: none;
                }}

                /* Estilos para pantallas más pequeñas */
                @media (max-width: 768px) {{
                    .container {{
                        width: 90%;
                        padding: 20px;
                    }}
                    h1 {{
                        font-size: 2rem;
                    }}
                    .image {{
                        max-width: 100%;
                    }}
                }}
            </style>
        </head>
        <BODY>
            <div class="container">
                <h1>{SUBJECT}</h1>
                <p>Estimado/a {BODY},</p>
                <p>Gracias por confiar en nosotros. Aquí tienes la información que solicitaste:</p>
                <img src="cid:image1" class="image" alt="Imagen relacionada" />

                <a href="http://localhost:4200/Home" class="cta-button">Ver más detalles</a>
                <div class="footer">
                    <p>Si tienes alguna pregunta, no dudes en <a href="mailto:lifesnapco@gmail.com">contactarnos</a>.</p>
                </div>
            </div>
        </BODY>
        </html>
        """
        
    
    # Adjuntar el cuerpo HTML al mensaje
    message.attach(MIMEText(html_BODY, "html"))

    # Adjuntar una imagen si se proporciona una ruta
    if IMAGE_PATH:
        with open(IMAGE_PATH, 'rb') as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-ID', '<image1>') 
            message.attach(img)

    try:
        # Establecer conexión con el servidor SMTP
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Iniciar encriptación TLS
        server.login(FROM_EMAIL, FROM_PASSWORD)  # Iniciar sesión con el correo
        text = message.as_string()
        server.sendmail(FROM_EMAIL, TO_EMAIL, text)  # Enviar el correo
        server.quit()
        print("Correo enviado con éxito")
    except Exception as e:
        print(f"Error al enviar el correo: {str(e)}")

# Llamar a la función para enviar un correo con HTML y una imagen
TO_EMAIL = "juandavidmunozsotelo7@gmail.com"
SUBJECT = "Bienvenido a LifeSnap"
BODY = "Gracias por registrarte en LifeSnap. ¡Esperamos que disfrutes de la aplicación!"

# Llamar a la función para enviar un correo con HTML

def servicio_correo():
    send_email(TO_EMAIL, SUBJECT, BODY, IMAGE_PATH)
