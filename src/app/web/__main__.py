"""
Run web interface for managing credentials
"""
import ssl
from ssl import SSLContext

import pywebio
from aiohttp import web
from aiohttp.web import Application
from pywebio.platform.aiohttp import webio_handler

from app import app_config, app_utils
from app.web.tradetron import change_password, create_task


def landing_page() -> None:
    """
    web app's landing page
    """
    pywebio.output.put_grid(
        content = [
            [pywebio.output.put_markdown("# Welcome to auto-login service!")],
            [pywebio.output.put_markdown("## Available Options")],
            [
                pywebio.output.put_markdown("### Add Credentials"),
                pywebio.output.put_link(name = 'Add Credentials', url = '/add_credentials')
            ],
            [
                pywebio.output.put_markdown("### Change Password"),
                pywebio.output.put_link(name = 'Change Password', url = '/change_password')
            ],
        ]
    )
    return

def build_web_app() -> web.Application:
    """
    prepare web app

    :return: web app
    :rtype: web.Application
    """
    app: Application = web.Application()
    app.add_routes(
        routes = [
            web.get('/', webio_handler(landing_page)),
            web.get('/add_credentials', webio_handler(create_task.main)),
            web.get('/change_password', webio_handler(change_password.main)),
        ]
    )
    return app

def configure_ssl(ssl_config: Dict[Any, Any]) -> SSLContext:
    """
    ssl config
    See: https://stackoverflow.com/questions/51645324/how-to-setup-a-aiohttp-https-server-and-client

    :return: _description_
    :rtype: ssl.SSLContext
    """
    ssl_context: SSLContext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(
        certfile = ssl_config['certfile'],
        keyfile = ssl_config['keyfile'], 
        password = bytes(str(ssl_config['keyfile_password']), encoding = 'utf-8')
    )
    return ssl_context

def main() -> None:
    """
    run web app
    """
    web_server_config: Dict[Any, Any] = app_utils.read_config(file_path = f"{app_config.paths['config_path']}/web_server.json")
    app: Application = build_web_app()
    ssl_context: SSLContext = configure_ssl(ssl_config = web_server_config['ssl_config'])

    # serve app
    web.run_app(app, host = web_server_config['host'], port = web_server_config['port'], ssl_context = ssl_context)
    return

if __name__ == '__main__':
    main()
