# Proyecto de Automatización de Pruebas - Urban Routes

Este proyecto contiene pruebas automatizadas para verificar el correcto funcionamiento de la aplicación web **Urban Routes**, simulando acciones de un usuario real al solicitar un servicio de taxi. Las pruebas cubren distintas funcionalidades esenciales de la interfaz.

## Descripción del Proyecto

El objetivo del proyecto es garantizar que las funcionalidades principales del sitio Urban Routes estén operativas, incluyendo:

- Ingreso de direcciones ("Desde" y "Hasta")
- Selección del tipo de tarifa (Comfort)
- Ingreso de datos del usuario (teléfono, tarjeta)
- Confirmación del pedido

Se automatizan flujos completos de principio a fin utilizando Selenium WebDriver y pytest.

## Tecnologías y Herramientas Utilizadas

- Lenguaje: Python 3.x
- Framework de pruebas: pytest
- Automatización web: Selenium WebDriver
- Manejo de esperas: WebDriverWait con ExpectedConditions
- Entorno de desarrollo: PyCharm
- Navegador: Google Chrome
- Dependencias: selenium, pytest

## Estructura del Proyecto
📁 proyecto/

├── main.py # Archivo principal con las clases y tests

├── data.py # Datos de prueba centralizados

├── README.md # Este archivo

## Cómo Ejecutar las Pruebas

1. Clona el repositorio o descarga los archivos.
2. Asegúrate de tener Python instalado (`python --version`).
3. Instala las dependencias si aún no lo has hecho: pip install selenium pytest

4. Ejecuta las pruebas desde la terminal (o desde PyCharm)
