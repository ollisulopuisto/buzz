from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QPlainTextEdit,
    QDialogButtonBox,
)

from buzz.locale import _


class TranscriptionLogDialog(QDialog):
    def __init__(
        self,
        logs: str,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)

        self.setWindowTitle(_("Transcription Log"))
        self.setMinimumSize(700, 500)

        layout = QVBoxLayout(self)

        self.text_edit = QPlainTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlainText(logs)
        # Scroll to bottom
        self.text_edit.moveCursor(self.text_edit.textCursor().MoveOperation.End)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Close, self
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(self.text_edit)
        layout.addWidget(button_box)

        self.setLayout(layout)
