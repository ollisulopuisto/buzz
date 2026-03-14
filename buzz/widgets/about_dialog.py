import json
from typing import Optional
from platformdirs import user_log_dir

from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon, QPixmap, QDesktopServices
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt6.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QDialogButtonBox,
    QMessageBox,
)

from buzz.__version__ import VERSION
from buzz.widgets.icon import BUZZ_ICON_PATH, BUZZ_LARGE_ICON_PATH
from buzz.locale import _
from buzz.settings.settings import APP_NAME


class AboutDialog(QDialog):
    GITHUB_API_LATEST_RELEASE_URL = (
        "https://api.github.com/repos/chidiwilliams/buzz/releases/latest"
    )
    GITHUB_LATEST_RELEASE_URL = "https://github.com/chidiwilliams/buzz/releases/latest"

    def __init__(
        self,
        network_access_manager: Optional[QNetworkAccessManager] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)

        self.setWindowIcon(QIcon(BUZZ_ICON_PATH))
        self.setWindowTitle(f'{_("About")} {APP_NAME}')

        if network_access_manager is None:
            network_access_manager = QNetworkAccessManager()

        self.network_access_manager = network_access_manager
        self.network_access_manager.finished.connect(self.on_latest_release_reply)

        main_layout = QVBoxLayout(self)
        content_layout = QHBoxLayout()

        image_label = QLabel()
        pixmap = QPixmap(BUZZ_LARGE_ICON_PATH).scaled(
            128,
            128,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        image_label.setPixmap(pixmap)
        image_label.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        details_layout = QVBoxLayout()

        buzz_label = QLabel(APP_NAME)
        buzz_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        )
        buzz_label_font = QtGui.QFont()
        buzz_label_font.setBold(True)
        buzz_label_font.setPointSize(24)
        buzz_label.setFont(buzz_label_font)

        version_label = QLabel(f"{_('Version')} {VERSION}")
        version_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        )
        version_label.setStyleSheet("color: gray;")

        self.check_updates_button = QPushButton(_("Check for updates"), self)
        self.check_updates_button.clicked.connect(self.on_click_check_for_updates)

        self.show_logs_button = QPushButton(_("Show logs"), self)
        self.show_logs_button.clicked.connect(self.on_click_show_logs)

        details_layout.addWidget(buzz_label)
        details_layout.addWidget(version_label)
        details_layout.addSpacing(10)
        details_layout.addWidget(self.check_updates_button)
        details_layout.addWidget(self.show_logs_button)
        details_layout.addStretch()

        content_layout.addWidget(image_label)
        content_layout.addSpacing(20)
        content_layout.addLayout(details_layout)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton(QDialogButtonBox.StandardButton.Close), self
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout.addLayout(content_layout)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)
        self.setMinimumWidth(450)
        self.setMinimumHeight(250)

    def on_click_check_for_updates(self):
        url = QUrl(self.GITHUB_API_LATEST_RELEASE_URL)
        self.network_access_manager.get(QNetworkRequest(url))
        self.check_updates_button.setDisabled(True)

    def on_click_show_logs(self):
        log_dir = user_log_dir(appname="Buzz")
        QDesktopServices.openUrl(QUrl.fromLocalFile(log_dir))

    def on_latest_release_reply(self, reply: QNetworkReply):
        if reply.error() == QNetworkReply.NetworkError.NoError:
            response = json.loads(reply.readAll().data())
            tag_name = response.get("name")
            if self.is_version_lower(VERSION, tag_name[1:]):
                QDesktopServices.openUrl(QUrl(self.GITHUB_LATEST_RELEASE_URL))
            else:
                QMessageBox.information(self, "", _("You're up to date!"))
        self.check_updates_button.setEnabled(True)

    @staticmethod
    def is_version_lower(version_a: str, version_b: str):
        return version_a.replace(".", "") < version_b.replace(".", "")
