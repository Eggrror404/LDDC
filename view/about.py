# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright (c) 2024 沉默の金
import time

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QWidget

from ui.about_ui import Ui_about
from utils.version import __version__

from .update import check_update


class AboutWidget(QWidget, Ui_about):
    def __init__(self, version: str) -> None:
        super().__init__()
        self.version = version
        self.setupUi(self)
        self.connect_signals()

    def init_ui(self) -> None:
        html = self.label.text()
        year = time.strftime("%Y", time.localtime())
        if year != "2024":
            year = "2024-" + year
        self.label.setText(html.replace("{year}", year))
        self.version_label.setText(self.version_label.text() + self.version)

    def connect_signals(self) -> None:
        self.github_pushButton.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/chenmozhijin/LDDC")))
        self.githubissues_pushButton.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/chenmozhijin/LDDC/issues")))
        self.checkupdate_pushButton.clicked.connect(lambda: check_update(False, self.tr("LDDC主程序"), "chenmozhijin/LDDC", __version__))

    def retranslateUi(self, about: QWidget) -> None:
        super().retranslateUi(about)
        self.init_ui()
