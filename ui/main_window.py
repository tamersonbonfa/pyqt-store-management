from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QStackedWidget
)

from services.config_service import get_config, set_config
from ui.themes import qss_light, qss_dark

from ui.tela_produtos import TelaProdutos
from ui.tela_clientes import TelaClientes
from ui.tela_vendas import TelaVendas
from ui.tela_usuarios import TelaUsuarios
from ui.tela_relatorios import TelaRelatorios


class MainWindow(QMainWindow):
    def __init__(self, usuario_id: int, username: str, nome: str, is_admin: bool):
        super().__init__()
        self.usuario_id = usuario_id
        self.username = username
        self.nome = nome
        self.is_admin = is_admin

        self.setWindowTitle("AngelaStore - Sistema de Estoque e Vendas")
        self.resize(1200, 720)

        self.central = QWidget()
        self.setCentralWidget(self.central)

        root = QHBoxLayout(self.central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # --- SIDEBAR (Barra Lateral) ---
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        sb = QVBoxLayout(self.sidebar)
        sb.setContentsMargins(14, 14, 14, 14)
        sb.setSpacing(10)

        logo = QLabel("AngelaStore")
        logo.setStyleSheet("font-size: 20px; font-weight: 900; margin-bottom: 5px;")
        sb.addWidget(logo)

        user_info = QLabel(f"Usuário: {self.nome}")
        user_info.setStyleSheet("opacity: 0.85; font-size: 12px; margin-bottom: 10px;")
        sb.addWidget(user_info)

        # Botões de Navegação Comuns
        self.btn_vendas = QPushButton("🧾 Frente de Vendas")
        self.btn_produtos = QPushButton("📦 Produtos / Estoque")
        self.btn_clientes = QPushButton("👤 Clientes")
        
        sb.addWidget(self.btn_vendas)
        sb.addWidget(self.btn_produtos)
        sb.addWidget(self.btn_clientes)

        # Botões Exclusivos para Admin
        if self.is_admin:
            sb.addSpacing(10)
            line = QWidget()
            line.setFixedHeight(1)
            line.setStyleSheet("background-color: rgba(255,255,255,0.1);")
            sb.addWidget(line)
            sb.addSpacing(5)

            self.btn_relatorios = QPushButton("📊 Relatórios Gerenciais")
            self.btn_usuarios = QPushButton("🔑 Gestão de Usuários")
            sb.addWidget(self.btn_relatorios)
            sb.addWidget(self.btn_usuarios)

        # Botão de Tema no rodapé da Sidebar
        self.btn_tema = QPushButton("🌙 Tema: Escuro")
        self.btn_tema.setObjectName("Primary")
        sb.addStretch(1)
        sb.addWidget(self.btn_tema)

        # --- ÁREA DE CONTEÚDO (QStackedWidget) ---
        self.stack = QStackedWidget()
        
        # Inicializando as Telas
        self.tela_vendas = TelaVendas(usuario_id=self.usuario_id)
        self.tela_produtos = TelaProdutos(usuario_id=self.usuario_id)
        self.tela_clientes = TelaClientes()
        
        # Adicionando telas ao Stack
        self.stack.addWidget(self.tela_vendas)   # Index 0
        self.stack.addWidget(self.tela_produtos) # Index 1
        self.stack.addWidget(self.tela_clientes) # Index 2

        # Adicionando telas de Admin ao Stack
        if self.is_admin:
            self.tela_relatorios = TelaRelatorios()
            self.tela_usuarios = TelaUsuarios()
            self.stack.addWidget(self.tela_relatorios) # Index 3
            self.stack.addWidget(self.tela_usuarios)   # Index 4

        root.addWidget(self.sidebar)
        root.addWidget(self.stack, 1)

        # --- EVENTOS (Cliques dos Botões) ---
        self.btn_vendas.clicked.connect(lambda: self.stack.setCurrentWidget(self.tela_vendas))
        self.btn_produtos.clicked.connect(lambda: self.stack.setCurrentWidget(self.tela_produtos))
        self.btn_clientes.clicked.connect(lambda: self.stack.setCurrentWidget(self.tela_clientes))

        if self.is_admin:
            self.btn_relatorios.clicked.connect(lambda: self.stack.setCurrentWidget(self.tela_relatorios))
            self.btn_usuarios.clicked.connect(lambda: self.stack.setCurrentWidget(self.tela_usuarios))

        self.btn_tema.clicked.connect(self.toggle_theme)

        # Aplicar Tema Inicial Salvo
        self.apply_theme(get_config("theme", "dark"))

    def apply_theme(self, theme: str):
        theme = (theme or "dark").lower()
        if theme == "light":
            self.setStyleSheet(qss_light())
            self.btn_tema.setText("🌙 Tema: Escuro")
            set_config("theme", "light")
        else:
            self.setStyleSheet(qss_dark())
            self.btn_tema.setText("☀️ Tema: Claro")
            set_config("theme", "dark")

    def toggle_theme(self):
        current = get_config("theme", "dark").lower()
        new_theme = "light" if current == "dark" else "dark"
        self.apply_theme(new_theme)