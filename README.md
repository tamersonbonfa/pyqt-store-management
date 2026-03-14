# pyqt-store-management
Sistema de Gestão Comercial Desktop desenvolvido em Python e PyQt. Arquitetura modular, suporte a temas e banco de dados SQLite. Pronto para personalização e rebranding.

# Desktop Store Management System (Template)

Este é um projeto de código aberto de um sistema de gestão comercial desktop, desenvolvido com foco em modularidade e facilidade de personalização. O sistema foi projetado para ser uma solução "White Label", permitindo que você altere o nome, logotipos e cores para atender a qualquer tipo de comércio.

## 🚀 Funcionalidades Principal
* **Gestão de Clientes e Produtos:** Cadastro completo com persistência em SQLite.
* **Sistema de Vendas:** Fluxo de caixa com registro de itens e geração de recibos.
* **Interface Moderna:** Desenvolvida em PyQt/PySide com suporte a temas customizáveis.
* **Relatórios:** Geração de relatórios de vendas e serviços.
* **Segurança:** Sistema de autenticação e diferentes níveis de acesso.

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.x
* **Interface Gráfica:** PyQt / PySide
* **Banco de Dados:** SQLite (com scripts de inicialização automática)
* **Relatórios:** ReportLab / PDF Service

## ⚙️ Como Personalizar
Para adaptar este projeto para o seu próprio negócio (ex: "Minha Loja", "Angela Store", etc.):
1. Altere o nome e identidade visual no arquivo `ui/themes.py`.
2. Configure o título da janela principal em `ui/main_window.py`.
3. Substitua os ícones na pasta `assets/`.

## 📦 Instalação
1. Clone o repositório.
2. Crie um ambiente virtual: `python -m venv .venv`
3. Instale as dependências: `pip install -r requirements.txt`
4. Execute o arquivo principal: `python main.py`
