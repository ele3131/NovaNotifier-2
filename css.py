def window():
    return """
    QApplication{
        background-color: #000000;
    }
    """


def btn():
    return """
    QPushButton{
    background-color: transparent;
    border-style:solid;
    border-radius:5px;
    border-color:#FFD500;
    border-width:2px;
    color: #FFD500;
    font:12px;
    font-weight:bold;
    padding:6px;
    min-width:6em;
    }

    QPushButton::hover{
        color:black;
        background:#FFD500;
    }
    """


def btn_main(img):
    return f'''
    QPushButton{{
    qproperty-icon:{img};
    background-color: transparent;
    border-style:outset;
    border-radius:5px;
    font:12px;
    font-weight:bold;
    padding:6px;
    min-width:6em;
    }}
    '''


def tbl():
    return """
    QTableView{
    background-color:#141414;
    border-top-style:solid;
    border-bottom-style:solid;
    border-width:3px;
    border-radius:0px;
    border-color:#FFD500;
    color:#d9d9d9;
    font:10px;
    font-weight:bold;
    padding:0px;
    margin-bottom:0px;
    min-height:0px;
    }
    QTableView::item{
        selection-background-color:#FFD500;
    }
    """


def scrollbar():
    return """
        QScrollBar:vertical{
            background-color: #141414;
            width: 14px
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{
            background-color: #141414;
        }
        QScrollBar::handle:vertical{
            background-color: #FFD500;
            border-radius: 6px;
            margin-top: 1px;
            margin-bottom: 1px;
        }
        QScrollBar::add-line:vertical {
            height: 0px;
        }
        QScrollBar::sub-line:vertical {
            height: 0px;
        }

        QScrollBar:horizontal{
            background-color: #141414;
        }
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal{
            background-color: #141414;
        }
        QScrollBar::handle:horizontal{
            background-color: #FFD500;
            border-radius: 2px;
            margin-left: 1px;
            margin-right: 1px;
        }
        QScrollBar::add-line:horizontal{
            height: 0px;
        }
        QScrollBar::sub-line:horizontal{
            height: 0px;
        }
    """


def lbl():
    return """
        QLabel{
        font:12px;
        color:white;
        border-width:0px;
        border-radius:0px;
        font-weight:bold;
        margin-top:10px;
        margin-bottom:10px;
        }
        """


def lbl_acc():
    return """
    QLabel{
    font:12px;
    color:#e32037;
    border-width:0px;
    border-radius:0px;
    }
    """


def lbl_refresh():
    return """
    QLabel{
    font:12px;
    font-weight:bold;
    color:#2ED03C;
    border-width:0px;
    border-radius:0px;
    }
    """


def header():
    return """
    QHeaderView::section{
        background-color:#141414;
        color:#FFD500;
        font:10px;
        font-weight:bold;
    }
    """


def container():
    return """
    background-color:#141414;
    border-right-style:none;
    border-width:3px;
    border-radius:4px;
    border-color:#FFD500;
    """


def popup():
    return """
    QWidget{
    background-color: #141414;
    }
    """


def line_edit():
    return """
    QLineEdit{
    background-color: #141414;
    color:#d9d9d9;
    border-bottom-style:outset;
    border-width:2px;
    border-radius:0px;
    padding:4px;
    border-color:#FFD500;
    font-weight:bold;
    }

    QToolTip{
    background-color: #141414;
    color: white;
    border: 2px;
    border-color:#ffd500;
    font-weight:bold;
    }
    """


def rbtn():
    return """
    QRadioButton{
    background-color: #141414;
    color: #d9d9d9;
    font-weight:bold;
    padding:4px;
    }

    QRadioButton::indicator::unchecked{
    border: 1px solid #FFD500;
    background-color: #141414;
    border-radius: 2px;
    }

    QRadioButton::indicator::checked{
    border: 1px solid #FFD500;
    background-color: #FFD500;
    border-radius: 2px;
    }
    """


def checkbox():
    return """
    QCheckBox{
    background-color: #141414;
    color: #d9d9d9;
    font-weight:bold;
    padding:4px;
    }

    QCheckBox::indicator::unchecked{
    border: 1px solid #FFD500;
    background-color: #141414;
    border-radius: 2px;
    }

    QCheckBox::indicator::checked{
    border: 1px solid #FFD500;
    background-color: #FFD500;
    border-radius: 2px;
    }
    """


def menu():
    return """
    QMenu {
    background-color: #141414;
    }

    QMenu::item{
        color: white;
        font-weight:bold;
    }

    QMenu::item:selected{
        color: #ffd500;
        font-weight:bold;
    }
    """
