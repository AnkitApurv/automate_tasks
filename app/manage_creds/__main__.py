from aiohttp import web
from pywebio.platform.aiohttp import webio_handler
import pywebio

from app.manage_creds import add_credentials, change_password, auth_user_pywebio

def landing_page():
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

app = web.Application()

app.add_routes(
    [
        web.get('/', webio_handler(landing_page)),
        web.get('/add_credentials', webio_handler(add_credentials.main_pywebio)),
        web.get('/change_password', webio_handler(change_password.main_pywebio)),
    ]
)


web.run_app(app, host='localhost', port=48251)