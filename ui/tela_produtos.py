from __future__ import annotations
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QFormLayout, QDialog,
    QSpinBox, QDoubleSpinBox, QCheckBox, QTextEdit, QSplitter, QComboBox
)
from services.produtos_service import (
    listar_produtos,
    buscar_produtos_por_nome,
    criar_produto,
    atualizar_produto,
    registrar_entrada_estoque,
    registrar_ajuste_estoque,
    listar_movimentacoes,
)


def _money(v: float) -> str:
    try:
        return f"R$ {float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "R$ 0,00"


def _format_tamanho(v: float, unidade: str) -> str:
    return f"{int(v)}" if v.is_integer() else f"{v}"


class ProdutoDialog(QDialog):
    def __init__(self, parent=None, produto: dict | None = None):
        super().__init__(parent)
        self.setWindowTitle("Produto")
        self.setMinimumWidth(520)
        self.produto = produto

        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.setSpacing(10)

        self.ed_nome = QLineEdit()
        self.ed_marca = QLineEdit()
        self.cb_categoria = QComboBox()
        self.cb_categoria.addItems(["Body Splash", "Condicionador", "Desodorante", "Máscara", "Perfume", "Sabonete", "Shampo", "Outro"])

        self.sp_tamanho = QDoubleSpinBox()
        self.sp_tamanho.setRange(0, 99999)
        self.sp_tamanho.setDecimals(2)
        self.sp_tamanho.setValue(100)
        self.cb_unidade = QComboBox()
        self.cb_unidade.addItems(["ml", "g", "un"])

        self.sp_custo = QDoubleSpinBox()
        self.sp_custo.setRange(0, 999999)
        self.sp_custo.setDecimals(2)

        self.sp_preco = QDoubleSpinBox()
        self.sp_preco.setRange(0, 999999)
        self.sp_preco.setDecimals(2)

        self.sp_qtd = QSpinBox()
        self.sp_qtd.setRange(0, 999999)
        self.sp_min = QSpinBox()
        self.sp_min.setRange(0, 999999)

        self.ck_ativo = QCheckBox("Produto ativo")
        self.ck_ativo.setChecked(True)
        self.ed_codigo = QLineEdit()
        self.ed_codigo.setPlaceholderText("Código de barras")

        form.addRow("Nome*", self.ed_nome)
        form.addRow("Marca", self.ed_marca)
        form.addRow("Categoria", self.cb_categoria)
        form.addRow("Tamanho", self.sp_tamanho)
        form.addRow("Unidade", self.cb_unidade)
        form.addRow("Custo (R$)", self.sp_custo)
        form.addRow("Preço venda (R$)", self.sp_preco)
        form.addRow("Quantidade", self.sp_qtd)
        form.addRow("Estoque mínimo", self.sp_min)
        form.addRow("", self.ck_ativo)
        form.addRow("Código de barras", self.ed_codigo)
        layout.addLayout(form)

        row = QHBoxLayout()
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_save = QPushButton("Salvar")
        self.btn_save.setObjectName("Primary")
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self.accept)
        row.addWidget(self.btn_cancel)
        row.addWidget(self.btn_save)
        layout.addLayout(row)

        if produto:
            self._fill(produto)
            self.sp_qtd.setEnabled(False)

    def _fill(self, p: dict):
        self.ed_nome.setText(str(p.get("nome") or ""))
        self.ed_marca.setText(str(p.get("marca") or ""))
        categoria = p.get("categoria") or "Outro"
        idx = self.cb_categoria.findText(categoria)
        if idx >= 0:
            self.cb_categoria.setCurrentIndex(idx)
        self.sp_tamanho.setValue(float(p.get("tamanho") or 0))
        unidade = p.get("unidade") or "ml"
        idx = self.cb_unidade.findText(unidade)
        if idx >= 0:
            self.cb_unidade.setCurrentIndex(idx)
        self.sp_custo.setValue(float(p.get("custo") or 0))
        self.sp_preco.setValue(float(p.get("preco_venda") or 0))
        self.sp_qtd.setValue(int(p.get("quantidade") or 0))
        self.sp_min.setValue(int(p.get("estoque_minimo") or 0))
        self.ck_ativo.setChecked(int(p.get("ativo") or 0) == 1)
        codigo = p.get("codigo_barras")
        self.ed_codigo.setText("" if codigo is None else str(codigo))

    def get_data(self) -> dict:
        return {
            "nome": self.ed_nome.text().strip(),
            "marca": self.ed_marca.text().strip(),
            "categoria": self.cb_categoria.currentText(),
            "tamanho": float(self.sp_tamanho.value()),
            "unidade": self.cb_unidade.currentText(),
            "custo": float(self.sp_custo.value()),
            "preco_venda": float(self.sp_preco.value()),
            "quantidade": int(self.sp_qtd.value()),
            "estoque_minimo": int(self.sp_min.value()),
            "codigo_barras": self.ed_codigo.text().strip(),
            "ativo": bool(self.ck_ativo.isChecked()),
        }


class EstoqueDialog(QDialog):
    def __init__(self, parent=None, titulo="Movimentação", modo="ENTRADA"):
        super().__init__(parent)
        self.setWindowTitle(titulo)
        self.setMinimumWidth(520)
        self.modo = modo

        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.setSpacing(10)

        self.sp_qtd = QSpinBox()
        self.sp_qtd.setRange(1, 999999)
        self.sp_nova = QSpinBox()
        self.sp_nova.setRange(0, 999999)
        self.ed_obs = QTextEdit()
        self.ed_obs.setFixedHeight(90)

        if modo == "ENTRADA":
            form.addRow("Quantidade (entrada)", self.sp_qtd)
        else:
            form.addRow("Nova quantidade", self.sp_nova)

        form.addRow("Observação", self.ed_obs)
        layout.addLayout(form)

        row = QHBoxLayout()
        btn_cancel = QPushButton("Cancelar")
        btn_ok = QPushButton("Confirmar")
        btn_ok.setObjectName("Primary")
        btn_cancel.clicked.connect(self.reject)
        btn_ok.clicked.connect(self.accept)
        row.addWidget(btn_cancel)
        row.addWidget(btn_ok)
        layout.addLayout(row)

    def get_data(self) -> dict:
        return {
            "quantidade": int(self.sp_qtd.value()),
            "nova_quantidade": int(self.sp_nova.value()),
            "observacao": self.ed_obs.toPlainText().strip(),
        }


class TelaProdutos(QWidget):
    def __init__(self, usuario_id: int):
        super().__init__()
        self.usuario_id = usuario_id
        self.produtos_cache: list[dict] = []

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Cabeçalho
        header = QHBoxLayout()
        title = QLabel("📦 Produtos / Controle de Estoque")
        title.setObjectName("Title")
        self.ed_busca = QLineEdit()
        self.ed_busca.setPlaceholderText("Buscar por nome, marca ou categoria...")
        self.btn_novo = QPushButton("➕ Novo Produto")
        self.btn_novo.setObjectName("Primary")
        self.btn_refresh = QPushButton("🔄 Atualizar")
        header.addWidget(title, 1)
        header.addWidget(self.ed_busca, 1)
        header.addWidget(self.btn_refresh)
        header.addWidget(self.btn_novo)
        layout.addLayout(header)

        # Splitter para tabela e movimentações
        splitter = QSplitter(Qt.Vertical)

        # Tabela de produtos
        self.tbl = QTableWidget(0, 12)
        self.tbl.setHorizontalHeaderLabels([
            "ID", "Nome", "Marca", "Categoria", "Tamanho", "Unidade",
            "Custo", "Preço", "Qtd", "Mínimo", "Status", "Código de barras"
        ])
        self.tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbl.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tbl.setAlternatingRowColors(True)

        # Botões de ações
        actions = QHBoxLayout()
        self.btn_editar = QPushButton("✏️ Editar")
        self.btn_entrada = QPushButton("⬆️ Entrada Estoque")
        self.btn_ajuste = QPushButton("🛠️ Ajustar Estoque")
        self.btn_mov = QPushButton("📜 Ver Movimentações")
        actions.addWidget(self.btn_editar)
        actions.addWidget(self.btn_entrada)
        actions.addWidget(self.btn_ajuste)
        actions.addWidget(self.btn_mov)
        actions.addStretch(1)

        top = QWidget()
        top_l = QVBoxLayout(top)
        top_l.setContentsMargins(0, 0, 0, 0)
        top_l.addWidget(self.tbl)
        top_l.addLayout(actions)

        # Tabela de movimentações
        self.tbl_mov = QTableWidget(0, 11)
        self.tbl_mov.setHorizontalHeaderLabels([
            "Data", "Tipo", "Produto", "Qtd", "Tamanho", "Unidade", "Obs", "Venda", "Usuário", "Valor", "Desconto"
        ])
        self.tbl_mov.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tbl_mov.setAlternatingRowColors(True)

        bottom = QWidget()
        bottom_l = QVBoxLayout(bottom)
        bottom_l.setContentsMargins(0, 0, 0, 0)
        bottom_l.addWidget(QLabel("📜 Histórico de movimentações (últimas 200)"))
        bottom_l.addWidget(self.tbl_mov)

        splitter.addWidget(top)
        splitter.addWidget(bottom)
        splitter.setSizes([420, 220])
        layout.addWidget(splitter, 1)

        # Eventos
        self.btn_novo.clicked.connect(self.novo_produto)
        self.btn_refresh.clicked.connect(self.carregar)
        self.ed_busca.textChanged.connect(self.buscar)
        self.btn_editar.clicked.connect(self.editar)
        self.btn_entrada.clicked.connect(self.entrada)
        self.btn_ajuste.clicked.connect(self.ajuste)
        self.btn_mov.clicked.connect(self.carregar_movimentacoes)
        self.tbl.doubleClicked.connect(self.editar)

        self.carregar()
        self.carregar_movimentacoes()

    def _selected_produto(self) -> dict | None:
        row = self.tbl.currentRow()
        if row < 0:
            return None
        pid = int(self.tbl.item(row, 0).text())
        return next((p for p in self.produtos_cache if int(p["id"]) == pid), None)

    def carregar(self):
        self.produtos_cache = listar_produtos(apenas_ativos=False)
        self._render_tabela(self.produtos_cache)

    def buscar(self):
        texto = self.ed_busca.text().strip()
        self.produtos_cache = buscar_produtos_por_nome(texto, apenas_ativos=False)
        self._render_tabela(self.produtos_cache)

    def _render_tabela(self, data: list[dict]):
        self.tbl.setRowCount(0)
        for p in data:
            r = self.tbl.rowCount()
            self.tbl.insertRow(r)
            qtd = int(p.get("quantidade") or 0)
            minimo = int(p.get("estoque_minimo") or 0)
            ativo = int(p.get("ativo") or 0) == 1
            status = "ATIVO" if ativo else "INATIVO"
            if ativo and minimo > 0 and qtd <= minimo:
                status = "⚠️ ESTOQUE BAIXO"

            values = [
                str(p["id"]),
                str(p.get("nome") or ""),
                str(p.get("marca") or ""),
                str(p.get("categoria") or ""),
                _format_tamanho(float(p.get("tamanho") or 0), p.get("unidade") or "ml"),
                str(p.get("unidade") or ""),
                _money(float(p.get("custo") or 0)),
                _money(float(p.get("preco_venda") or 0)),
                str(qtd),
                str(minimo),
                status,
                str(p.get("codigo_barras") or "")
            ]
            for c, v in enumerate(values):
                it = QTableWidgetItem(v)
                if c in (0, 4, 7, 8, 9):
                    it.setTextAlignment(Qt.AlignCenter)
                self.tbl.setItem(r, c, it)
        self.tbl.resizeColumnsToContents()

    def novo_produto(self):
        dlg = ProdutoDialog(self, produto=None)
        if dlg.exec() != QDialog.Accepted:
            return
        d = dlg.get_data()
        try:
            criar_produto(**d)
            self.carregar()
            self.carregar_movimentacoes()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def editar(self):
        p = self._selected_produto()
        if not p:
            QMessageBox.information(self, "Aviso", "Selecione um produto.")
            return
        dlg = ProdutoDialog(self, produto=p)
        if dlg.exec() != QDialog.Accepted:
            return
        d = dlg.get_data()
        try:
            atualizar_produto(produto_id=int(p["id"]), **d)
            self.carregar()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def entrada(self):
        p = self._selected_produto()
        if not p:
            QMessageBox.information(self, "Aviso", "Selecione um produto.")
            return
        dlg = EstoqueDialog(self, titulo="Entrada de estoque", modo="ENTRADA")
        if dlg.exec() != QDialog.Accepted:
            return
        d = dlg.get_data()
        try:
            registrar_entrada_estoque(
                produto_id=int(p["id"]),
                quantidade=int(d["quantidade"]),
                observacao=d["observacao"] or "Reposição",
                usuario_id=self.usuario_id,
            )
            self.carregar()
            self.carregar_movimentacoes()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def ajuste(self):
        p = self._selected_produto()
        if not p:
            QMessageBox.information(self, "Aviso", "Selecione um produto.")
            return
        dlg = EstoqueDialog(self, titulo="Ajuste de estoque", modo="AJUSTE")
        if dlg.exec() != QDialog.Accepted:
            return
        d = dlg.get_data()
        try:
            registrar_ajuste_estoque(
                produto_id=int(p["id"]),
                nova_quantidade=int(d["nova_quantidade"]),
                observacao=d["observacao"] or "Ajuste manual",
                usuario_id=self.usuario_id,
            )
            self.carregar()
            self.carregar_movimentacoes()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def carregar_movimentacoes(self):
        movs = listar_movimentacoes(produto_id=None, limite=200)
        self.tbl_mov.setRowCount(0)
        for m in movs:
            r = self.tbl_mov.rowCount()
            self.tbl_mov.insertRow(r)
            values = [
                str(m.get("data") or ""),
                str(m.get("tipo") or ""),
                str(m.get("produto_nome") or ""),
                str(m.get("quantidade") or 0),
                _format_tamanho(float(m.get("tamanho") or 0), m.get("unidade") or "un"),
                str(m.get("unidade") or ""),
                str(m.get("observacao") or ""),
                str(m.get("venda_id") or ""),
                str(m.get("usuario_nome") or ""),
                _money(float(m.get("valor_venda") or 0)),
                f"{float(m.get('desconto') or 0):.2f}%"
            ]
            for c, v in enumerate(values):
                it = QTableWidgetItem(v)
                if c in (1, 3, 4, 5, 7, 9, 10):
                    it.setTextAlignment(Qt.AlignCenter)
                self.tbl_mov.setItem(r, c, it)
        self.tbl_mov.resizeColumnsToContents()
