# 🛍️ Desktop Management System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PySide-6-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PySide6">
  <img src="https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/UI-Dark_Premium-222222?style=for-the-badge" alt="UI Dark">
</p>

Sistema de Gestão Comercial Desktop de alta performance desenvolvido em **Python**. Uma solução robusta com arquitetura modular, suporte a temas e persistência de dados segura, ideal para automação comercial de pequeno e médio porte.

---

## 🚀 Funcionalidades Principais

| Recurso | Descrição |
| :--- | :--- |
| **📦 Gestão de Inventário** | Cadastro completo de produtos com controle de tamanho, unidade e estoque mínimo. |
| **💳 PDV Otimizado** | Fluxo de caixa ágil com suporte a múltiplas formas de pagamento: PIX, Cartão e Dinheiro. |
| **📊 Dashboard Gerencial** | Relatórios em tempo real com métricas de faturamento, ticket médio e lucro estimado. |
| **📑 Histórico Total** | Rastreabilidade completa de entradas e saídas de estoque com logs detalhados de usuário. |
| **🎨 Interface Premium** | UI moderna em **PySide6** com tema Dark, focada em usabilidade e redução de fadiga visual. |

---

## 🛠️ Stack Tecnológica

* **Core:** Python 3.x
* **GUI:** PySide6 (Qt for Python) com widgets customizados
* **Database:** SQLite com suporte a transações ACID
* **Arquitetura:** Separação modular entre `services/` (lógica) e `ui/` (interface)

---

## 📁 Estrutura do Projeto

```bash
├── 🗄️ database/    # Configurações e inicialização do SQLite (angelastore.db)
├── ⚙️ services/    # Lógica de negócio (Relatórios, Estoque, Vendas)
├── 🖼️ ui/          # Camada de visualização (Main, Relatórios, Login)
├── 🎨 assets/      # Ícones, logotipos e recursos visuais
└── 🚀 main.py      # Ponto de entrada da aplicação

</details>

<details>
<summary>⚙️ <strong>Configuração e Instalação</strong></summary>