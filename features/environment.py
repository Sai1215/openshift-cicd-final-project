from threading import Thread

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from werkzeug.serving import make_server

from app import app
from service import db


def before_all(context):
    with app.app_context():
        db.create_all()

    context.server = make_server("127.0.0.1", 5000, app)
    context.server_thread = Thread(
        target=context.server.serve_forever,
        daemon=True,
    )
    context.server_thread.start()

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    context.driver = webdriver.Chrome(options=options)
    context.base_url = "http://127.0.0.1:5000"


def after_all(context):
    if getattr(context, "driver", None):
        context.driver.quit()
    if getattr(context, "server", None):
        context.server.shutdown()
        context.server_thread.join(timeout=5)
