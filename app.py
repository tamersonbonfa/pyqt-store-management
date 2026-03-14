import sys

from PySide6.QtWidgets import QApplication

from database.db import init_db
from services.auth_service import ensure_admin_user
from services.config_service import get_config
from ui.themes import qss_dark, qss_light
from ui.login_dialog import LoginDialog


def main():
    init_db()
    ensure_admin_user()  # <-- CRIA admin/admin automaticamente

    app = QApplication(sys.argv)

    theme = get_config("theme", "dark").lower()
    if theme == "light":
        app.setStyleSheet(qss_light())
    else:
        app.setStyleSheet(qss_dark())

    w = LoginDialog()
    w.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
