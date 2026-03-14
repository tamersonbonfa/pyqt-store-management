# 🛍️ Desktop Management System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PySide-6-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PySide6">
  <img src="https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
</p>

---

<details>
<summary>🚀 <strong>Funcionalidades Principais</strong></summary>
<br>

| Recurso | Descrição |
| :--- | :--- |
| **📦 Gestão de Inventário** | Cadastro completo de produtos com controle de tamanho, unidade e estoque mínimo. |
| **💳 PDV Otimizado** | Fluxo de caixa ágil com suporte a múltiplas formas de pagamento: PIX, Cartão e Dinheiro. |
| **📊 Dashboard Gerencial** | Relatórios em tempo real com métricas de faturamento, ticket médio e lucro estimado. |
| **📑 Histórico Total** | Rastreabilidade completa de entradas e saídas de estoque com logs detalhados de usuário. |
| **🎨 Interface Premium** | UI moderna em **PySide6** com tema Dark, focada em usabilidade e redução de fadiga visual. |

</details>

<details>
<summary>🛠️ <strong>Stack Tecnológica</strong></summary>
<br>

* **Core:** Python 3.x
* **GUI:** PySide6 (Qt for Python) com widgets customizados
* **Database:** SQLite com suporte a transações ACID
* **Arquitetura:** Separação modular entre `services/` e `ui/`

</details>

<details>
<summary>📁 <strong>Estrutura do Projeto</strong></summary>
<br>

```bash
├── 🗄️ database/    # Configurações e inicialização do SQLite (angelastore.db)
├── ⚙️ services/    # Lógica de negócio (Relatórios, Estoque, Vendas)
├── 🖼️ ui/          # Camada de visualização (Main, Relatórios, Login)
├── 🎨 assets/      # Ícones, logotipos e recursos visuais
└── 🚀 main.py      # Ponto de entrada da aplicação

```

</details>

<details>
<summary>⚙️ <strong>Configuração e Instalação</strong></summary>
<br>

1. Clonar o Repositório
```bash

git clone [https://github.com/tamersonbonfa/pyqt-store-management.git](https://github.com/tamersonbonfa/pyqt-store-management.git)

```
```bash

cd pyqt-store-management

```

2. Configurar Ambiente Virtual
```bash

python -m venv .venv

```
# Ativação Windows:
```bash

.venv\Scripts\activate

```

# Ativação Linux/Mac:
```bash

source .venv/bin/activate

```

3. Instalar Dependências
```bash

pip install -r requirements.txt

```

💡 Nota: O sistema inicializa automaticamente o arquivo angelastore.db na primeira execução.

</details>

<details>
<summary>🧪 <strong>Ferramentas de Desenvolvimento</strong></summary>
<br>
O projeto inclui o script utilitário injetor_dados.py para testes de estresse:

Simulação Realista: Gera movimentações de estoque e vendas fictícias.

Validação: Ideal para validar o comportamento dos gráficos e relatórios gerenciais.

</details>
<br>
<br>
<br>

<p align="center">
Desenvolvido por <strong>Tamerson Bonfa</strong>
</p>