from __future__ import annotations


def qss_light() -> str:
    return """
    QWidget { font-size: 14px; color: #111827; }
    QMainWindow { background: #f6f7fb; }
    QDialog { background: #f6f7fb; }


    QLabel { color: #111827; }
    QLabel#Title { font-size: 22px; font-weight: 800; color: #0f172a; }

    QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {
        background: white;
        border: 1px solid #d7d9e0;
        border-radius: 10px;
        padding: 8px;
        color: #111827;
    }

    QTableWidget {
        background: white;
        border: 1px solid #d7d9e0;
        border-radius: 12px;
        color: #111827;
        gridline-color: #e5e7eb;
    }

    QHeaderView::section {
        background: #f1f5f9;
        color: #0f172a;
        padding: 6px;
        border: 0px;
        border-bottom: 1px solid #d7d9e0;
    }

    QPushButton {
        border: 1px solid #d7d9e0;
        border-radius: 12px;
        padding: 10px 12px;
        background: white;
        color: #111827;
    }

    QPushButton:hover { background: #f0f1f6; }

    QPushButton#Primary {
        background: #2563eb;
        color: white;
        border: 0px;
        font-weight: 700;
    }
    QPushButton#Primary:hover { background: #1d4ed8; }

    #Sidebar {
        background: white;
        border-right: 1px solid #d7d9e0;
    }
    /* Limpar fundo das tabelas para remover cantos pretos */
    QTableWidget {
        background-color: white;
        border: 1px solid #d7d9e0;
        border-radius: 12px;
        gridline-color: #e5e7eb;
        /* Força o fundo transparente nos cantos */
        outline: none;
    }

    /* Remove o fundo preto atrás dos cabeçalhos nos cantos */
    QTableWidget QHeaderView {
        background-color: transparent;
        border-radius: 12px;
    }

    QHeaderView::section {
        background-color: #f1f5f9;
        border: none;
        border-bottom: 1px solid #d7d9e0;
        padding: 6px;
    }

    /* Remove o botão do canto superior esquerdo que costuma ficar preto */
    QTableCornerButton::section {
        background-color: #f1f5f9;
        border-top-left-radius: 12px;
        border: none;
        border-bottom: 1px solid #d7d9e0;
    }
    
    /* Corrigir o fundo da lista de seleção (Completer / ComboBox Popup) */
    QAbstractItemView {
        background-color: white;
        color: #111827;
        selection-background-color: #2563eb;
        selection-color: white;
        border: 1px solid #d7d9e0;
        outline: 0px;
    }
    
    """



def qss_dark() -> str:
    return """
    QWidget { font-size: 14px; color: #e5e7eb; }
    QMainWindow { background: #0f172a; }
    QDialog { background: #0f172a; }


    QLabel#Title { font-size: 22px; font-weight: 800; color: white; }

    QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {
        background: #111827;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 8px;
        color: #e5e7eb;
    }

    QTableWidget {
        background: #111827;
        border: 1px solid #334155;
        border-radius: 12px;
        color: #e5e7eb;
    }

    QPushButton {
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 10px 12px;
        background: #111827;
        color: #e5e7eb;
    }

    QPushButton:hover { background: #1f2937; }

    QPushButton#Primary {
        background: #2563eb;
        color: white;
        border: 0px;
        font-weight: 700;
    }
    QPushButton#Primary:hover { background: #1d4ed8; }

    #Sidebar {
        background: #111827;
        border-right: 1px solid #334155;
    }
    
    QAbstractItemView {
        background-color: #1e293b;
        color: #e5e7eb;
        selection-background-color: #2563eb;
        selection-color: white;
        border: 1px solid #334155;
        outline: 0px;
    }
    
    QListView {
        background-color: #1e293b;
        border: 1px solid #334155;
    }
    
    QListView::item:selected {
        background-color: #2563eb;
    }
    
    QHeaderView::section {
        background: #1e293b;
        color: #f8fafc;
        padding: 8px;
        border: none;
        border-bottom: 1px solid #334155;
    }
    
    /* Remove o fundo preto do quadrado do canto */
    QTableCornerButton::section {
        background: #1e293b;
        border: none;
    }
    
    """
