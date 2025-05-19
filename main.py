import time

from selenium.webdriver import Keys

import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string."""
    import json
    import time
    from selenium.common import WebDriverException

    code = None
    print("Iniciando búsqueda del código...")

    for i in range(20):  # Aumentamos a 20 intentos
        try:
            # Obtener logs de performance
            logs = driver.get_log('performance')
            print(f"\nIntento {i + 1}: {len(logs)} logs encontrados")

            # Filtrar logs relevantes
            filtered_logs = [log["message"] for log in logs if
                             log.get("message") and 'api/v1/number?number' in log.get("message")]
            print(f"Logs filtrados: {len(filtered_logs)}")

            for log in reversed(filtered_logs):
                try:
                    message_data = json.loads(log)["message"]
                    print(f"\nAnalizando log: {message_data.get('method', '')}")

                    if message_data.get("method") == "Network.responseReceived":
                        request_id = message_data["params"]["requestId"]
                        print(f"Request ID encontrado: {request_id}")

                        # Obtener cuerpo de la respuesta
                        body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
                        print(f"Respuesta cruda: {body}")

                        if 'body' in body and body['body']:
                            # Extraer solo dígitos
                            code = ''.join([x for x in body['body'] if x.isdigit()])
                            print(f"Código potencial encontrado: {code}")

                            if code and len(code) == 4:  # Asumiendo que el código es de 4 dígitos
                                print(f"¡Código válido encontrado!: {code}")
                                return code
                except Exception as e:
                    print(f"Error procesando log: {str(e)}")
                    continue

        except WebDriverException as e:
            print(f"Excepción WebDriver: {str(e)}")
            time.sleep(1)
            continue

        print("Esperando 1 segundo antes de reintentar...")
        time.sleep(1)

    raise Exception("No se encontró el código de confirmación del teléfono después de 20 intentos")


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.from_field))
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    order_taxi_button = (By.XPATH, "//button[text()='Pedir un taxi']")
    def select_order_taxi (self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.order_taxi_button))
        self.driver.find_element(*self.order_taxi_button).click()

    comfort_tariff_button = (By.XPATH, '//div[@class="tcard-title" and text()="Comfort"]')
    def select_comfort_tariff_button (self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.comfort_tariff_button))
        self.driver.find_element(*self.comfort_tariff_button).click()

    button_phone_number = (By.XPATH, "//div[text()='Número de teléfono']")
    def select_button_phone_number (self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.button_phone_number))
        self.driver.find_element(*self.button_phone_number).click()

    second_button_phone_number = (By.XPATH, "//label[contains(text(),'Número de teléfono')]")
    def select_second_button_phone_number(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.second_button_phone_number))
        self.driver.find_element(*self.second_button_phone_number).click()

    phone_number = (By.ID, 'phone')
    def set_phone_number (self, phone):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.phone_number))
        self.driver.find_element(*self.phone_number).click()
        self.driver.find_element(*self.phone_number).send_keys(phone)

    button_next_phone = (By.XPATH, "//button[@class='button full' and text()='Siguiente']")
    def select_button_next_phone(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.button_next_phone))
        self.driver.find_element(*self.button_next_phone).click()

    field_code_phone = (By.XPATH, "//label[@class='label' and text()='Introduce el código']")
    def select_field_code_phone(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.field_code_phone))
        self.driver.find_element(*self.field_code_phone).click()

    field_write_code_phone = (By.XPATH, "//input[@placeholder='xxxx' and @type='text']")
    def select_field_write_code_phone(self, code_phone):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.field_write_code_phone))
        self.driver.find_element(*self.field_write_code_phone).send_keys(code_phone)

    button_confirm_code_phone = (By.XPATH, "//button[@class='button full' and text()='Confirmar']")
    def select_button_confirm_code_phone(self):
        self.driver.find_element(*self.button_confirm_code_phone).click()

    payment_method = (By.XPATH, "//div[@class='pp-text' and text()='Método de pago']")
    def select_payment_method (self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.payment_method))
        self.driver.find_element(*self.payment_method).click()

    button_add_card = (By.XPATH, "//div[@class='pp-title' and text()='Agregar tarjeta']")
    def select_button_add_card (self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.button_add_card))
        self.driver.find_element(*self.button_add_card).click()

    field_number_card = (By.ID,"number")
    def select_field_number_card(self, credit_card):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.field_number_card))
        self.driver.find_element(*self.field_number_card).click()
        self.driver.find_element(*self.field_number_card).send_keys(credit_card)

    field_cvv_card = (By.XPATH,"//input[@id='code' and contains(@class, 'card-input')]")
    def select_field_cvv_card(self, code):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.field_cvv_card))
        self.driver.find_element(*self.field_cvv_card).click()
        self.driver.find_element(*self.field_cvv_card).send_keys(code)
        self.driver.find_element(*self.field_cvv_card).send_keys(Keys.TAB)

    button_add = (By.XPATH, "//button[@type='submit' and text()='Agregar']")
    def select_button_add(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.button_add))
        self.driver.find_element(*self.button_add).click()

    button_close_card = (By.XPATH, "(//button[@class='close-button section-close'])[3]")
    def select_button_close_card(self):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(self.button_close_card))
        self.driver.find_element(*self.button_close_card).click()

    field_driving_message = (By.XPATH, "//label[@for='comment' and @class='label']")
    def select_field_driving_message(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.field_driving_message))
        self.driver.find_element(*self.field_driving_message).click()

    field_message = (By.XPATH, "//input[@name='comment']")
    def select_field_message(self, message):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.field_message))
        self.driver.find_element(*self.field_message).send_keys(message)

    button_blanket_scarves = (By.XPATH, "(//span[@class='slider round'])[1]")
    def select_button_blanket_scarves(self):
        self.driver.find_element(*self.button_blanket_scarves).click()

    button_add_ice_cream = (By.XPATH, "(//div[@class='counter-plus'])[1]")
    def select_button_add_ice_cream(self):
        self.driver.find_element(*self.button_add_ice_cream).click()
        time.sleep(1)
        self.driver.find_element(*self.button_add_ice_cream).click()

    button_reserve_taxi = (By.XPATH, "//button//span[@class='smart-button-secondary']")
    def select_button_reserve_taxi(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.button_reserve_taxi))
        self.driver.find_element(*self.button_reserve_taxi).click()
        time.sleep(38)

class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()

    def setup_method(self):
        self.page = UrbanRoutesPage(self.driver)
        self.driver.get(data.urban_routes_url)

    def test_enter_route(self):
        self.page.set_route(data.address_from, data.address_to)
        assert self.page.get_from() == data.address_from
        assert self.page.get_to() == data.address_to

    def test_choose_tariff(self):
        self.page.set_route(data.address_from, data.address_to)
        self.page.select_order_taxi()
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.page.comfort_tariff_button)
        )
        assert "Comfort" in element.text
        self.page.select_comfort_tariff_button()

    def test_enter_phone_number_and_code(self):
        self.page.set_route(data.address_from, data.address_to)
        self.page.select_order_taxi()
        self.page.select_comfort_tariff_button()
        self.page.select_button_phone_number()
        title_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='head' and text()='Introduce tu número de teléfono']")))
        assert "Introduce tu número de teléfono" in title_element.text
        self.page.select_second_button_phone_number()
        self.page.set_phone_number(data.phone_number)
        self.page.select_button_next_phone()
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(self.page.field_code_phone))
        code = retrieve_phone_code(self.driver)
        print("Código recibido:", code)
        self.page.select_field_code_phone()
        self.page.select_field_write_code_phone(code)
        self.page.select_button_confirm_code_phone()
        telefono = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[text()='+1 123 123 12 12']")))
        assert telefono.text == "+1 123 123 12 12"


    def test_add_payment_method(self):
        self.page.set_route(data.address_from, data.address_to)
        self.page.select_order_taxi()
        self.page.select_comfort_tariff_button()
        self.page.select_payment_method()
        self.page.select_button_add_card()
        title_element = self.driver.find_element(By.XPATH, "//div[@class='card-number-label' and text()='Número de tarjeta (no la tuya):']")
        assert title_element.is_displayed()
        self.page.select_field_number_card(data.card_number)
        self.page.select_field_cvv_card(data.card_code)
        self.page.select_button_add()
        self.page.select_button_close_card()
        tarjeta_text = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='pp-value-text' and text()='Tarjeta']")))
        assert tarjeta_text.text == "Tarjeta"

    def test_customize_order(self):
        self.page.set_route(data.address_from, data.address_to)
        self.page.select_order_taxi()
        self.page.select_comfort_tariff_button()
        self.page.select_field_driving_message()
        placeholder = self.driver.find_element(By.ID, "comment").get_attribute("placeholder")
        assert placeholder == "Traiga un aperitivo"
        self.page.select_field_message(data.message_for_driver)

    def test_add_blanket_scarves(self):
        self.page.set_route(data.address_from, data.address_to)
        self.page.select_order_taxi()
        self.page.select_comfort_tariff_button()
        self.page.select_button_blanket_scarves()
        element = self.driver.find_element(By.XPATH, "//div[@class='r-sw-label' and text()='Manta y pañuelos']")
        assert element.text == "Manta y pañuelos"

    def test_add_ice_cream(self):
        self.page.set_route(data.address_from, data.address_to)
        self.page.select_order_taxi()
        self.page.select_comfort_tariff_button()
        self.page.select_button_add_ice_cream()
        element = self.driver.find_element(By.XPATH, "//div[@class='r-group-title' and text()='Cubeta de helado']")
        assert element.text == "Cubeta de helado"

    def test_confirm_reservation(self):
        self.page.set_route(data.address_from, data.address_to)
        self.page.select_order_taxi()
        self.page.select_comfort_tariff_button()
        self.page.select_button_phone_number()
        self.page.select_second_button_phone_number()
        self.page.set_phone_number(data.phone_number)
        self.page.select_button_next_phone()
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(self.page.field_code_phone))
        code = retrieve_phone_code(self.driver)
        self.page.select_field_code_phone()
        self.page.select_field_write_code_phone(code)
        self.page.select_button_confirm_code_phone()
        self.page.select_payment_method()
        self.page.select_button_add_card()
        self.page.select_field_number_card(data.card_number)
        self.page.select_field_cvv_card(data.card_code)
        self.page.select_button_add()
        self.page.select_button_close_card()
        self.page.select_field_driving_message()
        self.page.select_field_message(data.message_for_driver)
        self.page.select_button_blanket_scarves()
        self.page.select_button_add_ice_cream()
        self.page.select_button_reserve_taxi()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

        """Esta ultima prueba, solo queda correcta si se ponen todas las demás pruebas, 
                no funciona solo poniendo el telefono, da click al boton de reserva
                y solo abre el cronometro un instante y vuelve a cerrar. Por eso la pongo completa y queda extensa."""
