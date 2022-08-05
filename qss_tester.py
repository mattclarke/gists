import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget, QTabWidget, QListView, QListWidget,
)

QSS_EXAMPLE = """QLineEdit {
  background-color: white;
  border: 1px solid #a9a9a9;
  border-radius: 5px;
}

QLineEdit:!enabled {
  background-color: gainsboro;
  color: gray;
  border: 1px solid #a9a9a9;
  border-radius: 5px;
}"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QSS Tester")
        self.editor = QPlainTextEdit()
        self.editor.textChanged.connect(self.update_styles)
        self.editor.setPlainText(QSS_EXAMPLE)
        layout = QVBoxLayout()
        layout.addWidget(self.editor)

        # Define a set of widgets.
        bar = self.menuBar()
        file = bar.addMenu("File")
        file.addAction("Something")
        file.addAction("Something")

        tb = self.addToolBar("File")
        tb.addAction("toolbar 1")
        tb.addAction("toolbar 2")
        tb.addAction("toolbar 3")

        tabs = QTabWidget()
        for color in ["one", "two", "three"]:
            view = QListWidget()
            view.addItems(["QListWidget 1", "Something", "Blah"])
            tabs.addTab(view, color)
        layout.addWidget(tabs)

        cb = QCheckBox("Checkbox")
        layout.addWidget(cb)

        combo = QComboBox()
        combo.setObjectName("thecombo")
        combo.addItems(["First", "Second", "Third", "Fourth"])
        layout.addWidget(combo)

        sb = QSpinBox()
        sb.setRange(0, 99999)
        layout.addWidget(sb)

        l = QLabel("This is a label")
        layout.addWidget(l)

        le = QLineEdit()
        le.setObjectName("mylineedit")
        le.setText("this is a line edit")
        layout.addWidget(le)

        lero = QLineEdit()
        lero.setObjectName("mylineedit_ro")
        lero.setText("this is a disabled line edit")
        lero.setEnabled(False)
        layout.addWidget(lero)

        qpte = QPlainTextEdit()
        layout.addWidget(qpte)
        qpte.setPlainText("QPlainTextEdit")

        pb = QPushButton("Push me!")
        layout.addWidget(pb)

        self.container = QWidget()
        self.container.setLayout(layout)
        self.setCentralWidget(self.container)

    def update_styles(self):
        qss = self.editor.toPlainText()
        self.setStyleSheet(qss)


app = QApplication(sys.argv)
app.setApplicationName("QSS Tester")
app.setStyle("Fusion")

w = MainWindow()
w.show()
app.exec_()