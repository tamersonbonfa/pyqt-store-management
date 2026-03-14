🛍️ Desktop Management System
Sistema de Gestão Comercial Desktop de alta performance desenvolvido em Python. Uma solução robusta com arquitetura modular, suporte a temas e persistência de dados segura, ideal para automação comercial de pequeno e médio porte.

🚀 Funcionalidades Principais
Gestão de Inventário: Cadastro detalhado de produtos com controle de tamanho, unidade e estoque mínimo.

PDV (Ponto de Venda): Fluxo de caixa otimizado com suporte a múltiplas formas de pagamento (PIX, Cartão, Dinheiro).

Dashboard Gerencial: Relatórios em tempo real com métricas de faturamento, ticket médio e lucro estimado.

Histórico de Movimentação: Rastreabilidade total de entradas e saídas de estoque com logs de usuário.

Interface Dark Premium: UI moderna desenvolvida em PySide6 com foco em usabilidade e redução de fadiga visual.

🛠️ Stack Tecnológica
Core: Python 3.x

GUI: PySide6 (Qt for Python) com widgets customizados

Database: SQLite com suporte a transações ACID

Serviços: Arquitetura separada em services/ para lógica de negócio e ui/ para interface

📁 Estrutura do Projeto
Plaintext

├── database/        # Configurações e inicialização do SQLite (angelastore.db)
├── services/        # Lógica de negócio (Relatórios, Estoque, Vendas)
├── ui/              # Telas (Main, Relatórios, Produtos, Login)
├── assets/          # Ícones e recursos visuais
└── main.py          # Ponto de entrada da aplicação

⚙️ Configuração e Instalação
Clone o repositório:

Bash

git clone https://github.com/tamersonbonfa/pyqt-store-management.git
Ambiente Virtual:

Bash

python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
Dependências:

Bash

pip install -r requirements.txt
Banco de Dados:
O sistema inicializa automaticamente o arquivo angelastore.db ao ser executado pela primeira vez, criando todas as tabelas e índices necessários.

🧪 Ferramentas de Desenvolvimento
O projeto inclui um script utilitário para testes de estresse e preenchimento de banco de dados:

injetor_dados.py: Gera movimentações de estoque e vendas fictícias para validar os gráficos e relatórios gerenciais.

Desenvolvido por Tamerson Bonfa