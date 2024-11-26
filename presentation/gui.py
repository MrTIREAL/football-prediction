from PyQt6.QtWidgets import (
    QMainWindow,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
    QMenu
)
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction, QIcon

from business.controllers.settings_controller import SettingsController
from presentation.analysis_result_widget import AnalysisResultWidget
from presentation.matchday_widget import MatchdayWidget
from presentation.info_status_widget import InfoStatusWidget
from presentation.homepage_widget import HomepageWidget
from presentation.settings_widget import SettingsWidget
from presentation.league_table_widget import LeagueTableWidget
from presentation.single_predict_widget import SinglePredictWidget
from presentation.toto_result_widget import TotoResultWidget
from presentation.toto_widget import TotoWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = SettingsController()
        self._get_league_info()
        self._createLayout()
        self._createActions()
        self._createMenuBar()
        self._createStatusBar()
        self._connectActions()

    def _createMenuBar(self):
        menuBar = self.menuBar()

        # File menu
        file_menu = QMenu("&Fájl", self)
        menuBar.addMenu(file_menu)
        file_menu.addAction(self.homeAction)
        file_menu.addAction(self.settingsAction)
        file_menu.addSeparator()
        file_menu.addAction(self.exitAction)

        # League menu
        league_menu = QMenu("Liga", self)
        menuBar.addMenu(league_menu)
        league_menu.addAction(self.leagueTableAction)

        # Analysis menu
        analysis_menu = QMenu("Analízis", self)
        menuBar.addMenu(analysis_menu)
        analysis_menu.addAction(self.analysisMatchday)
        analysis_menu.addAction(self.analysisSinglePredictAction)
        analysis_menu.addAction(self.analysisResultAction)

        # Toto menu
        toto_menu = QMenu("Toto", self)
        menuBar.addMenu(toto_menu)
        toto_menu.addAction(self.totoGameAction)
        toto_menu.addAction(self.totoResultAction)

    def _createActions(self):
        # File menu
        self.homeAction = QAction("&Főoldal", self)
        self.settingsAction = QAction("&Beállítások", self)
        self.exitAction = QAction("&Kilépés", self)

        # League menu
        self.leagueTableAction = QAction("&Liga állás", self)

        # Analysis menu
        self.analysisMatchday = QAction("&Napi elemzés", self)
        self.analysisSinglePredictAction = QAction("&Egyszeri elemzés", self)
        self.analysisResultAction = QAction("&Elemzések eredménye", self)

        # Toto menu
        self.totoGameAction = QAction("&Játék", self)
        self.totoResultAction = QAction("&Eredmény", self)

        # Shortcuts
        self.homeAction.setShortcut("Ctrl+H")
        self.settingsAction.setShortcut("Ctrl+C")
        self.exitAction.setShortcut("Ctrl+Q")
        self.leagueTableAction.setShortcut("Ctrl+T")

        # Status tips
        self.homeAction.setStatusTip("Főoldal megjelenítése")
        self.settingsAction.setStatusTip("Beállítások megjelenítése")
        self.exitAction.setStatusTip("Kilépés a programból")
        self.leagueTableAction.setStatusTip("Liga megjelenítése")
        self.analysisMatchday.setStatusTip("Napi elemzés megjelenítése")
        self.analysisSinglePredictAction.setStatusTip(
            "Egyszeri elemzés megjelenítése")
        self.analysisResultAction.setStatusTip(
            "Elemzett mérkőzések megjelenítése")
        self.totoGameAction.setStatusTip("Totó generálása")
        self.totoResultAction.setStatusTip("Tótó eredmények")

    def _connectActions(self):
        self.homeAction.triggered.connect(self.activate_Homepage)
        self.settingsAction.triggered.connect(self.activate_Settings)
        self.leagueTableAction.triggered.connect(self.activate_LeagueTable)
        self.analysisMatchday.triggered.connect(self.activate_Matchday)
        self.analysisSinglePredictAction.triggered.connect(
            self.activate_SinglePredict)
        self.analysisResultAction.triggered.connect(
            self.activate_AnalysisResult)
        self.totoGameAction.triggered.connect(self.activate_TotoWidget)
        self.totoResultAction.triggered.connect(self.activate_TotoResult)
        self.exitAction.triggered.connect(self.close)

    def _createStatusBar(self):
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Ready", 3000)

    def _createLayout(self):
        self.setWindowTitle("Football mérkőzések elemzése")
        self.setWindowIcon(QIcon("./presentation/assets/football.ico"))
        self.resize(QSize(400, 350))
        pagelayout = QVBoxLayout()
        self.stacklayout = QStackedLayout()
        pagelayout.addLayout(self.stacklayout)
        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

        # Create widgets
        self._create_HomepageWidget()
        self._create_SettingsWidget()
        self._create_LeagueTableWidget()
        self._create_MatchdayWidget()
        self._create_SinglePredict()
        self._create_AnalysisResult()
        self._create_TotoWidget()
        self._create_TotoResult()

    def _create_HomepageWidget(self):
        self.homepage_widget = HomepageWidget(
            self.display_league, self.league_date)
        self.homepage_widget.calendarBtn.clicked.connect(
            self.activate_Matchday)
        self.homepage_widget.leagueTableBtn.clicked.connect(
            self.activate_LeagueTable)
        self.homepage_widget.resultButton.clicked.connect(
            self.activate_AnalysisResult)
        self.stacklayout.addWidget(self.homepage_widget)

    def _create_SettingsWidget(self):
        self.settings_info_statusbar = InfoStatusWidget(
            self.display_league, self.league_date, self.current_mode)
        self.settings_widget = SettingsWidget()
        self.settings_widget.dateClicked.connect(self.change_date)
        self.settings_widget.leagueSeasonClicked.connect(
            self.change_display_league)
        self.settings_widget.modeClicked.connect(self.change_mode)
        self.settings_widget.cInfoStatusLayout.addWidget(
            self.settings_info_statusbar)
        self.stacklayout.addWidget(self.settings_widget)

    def _create_LeagueTableWidget(self):
        self.table_info_statusbar = InfoStatusWidget(
            self.display_league, self.league_date, self.current_mode)
        self.league_table_widget = LeagueTableWidget()
        self.league_table_widget.ltInfoStatusLayout.addWidget(
            self.table_info_statusbar)
        self.stacklayout.addWidget(self.league_table_widget)

    def _create_MatchdayWidget(self):
        self.matchday_info_statusbar = InfoStatusWidget(
            self.display_league, self.league_date, self.current_mode)
        self.matchday_widget = MatchdayWidget(
            self.current_league, self.current_season, self.current_mode)
        self.matchday_widget.cInfoStatusLayout.addWidget(
            self.matchday_info_statusbar)
        self.stacklayout.addWidget(self.matchday_widget)

    def _create_SinglePredict(self):
        self.single_predict_statusbar = InfoStatusWidget(
            self.display_league, self.league_date, self.current_mode)
        self.single_predict_widget = SinglePredictWidget(
            self.league_date, self.current_league, self.current_season, self.current_mode)
        self.single_predict_widget.spInfoStatusLayout.addWidget(
            self.single_predict_statusbar)
        self.stacklayout.addWidget(self.single_predict_widget)

    def _create_AnalysisResult(self):
        self.analysis_result_statusbar = InfoStatusWidget(
            self.display_league, self.league_date, self.current_mode)
        self.analysis_result_widget = AnalysisResultWidget()
        self.analysis_result_widget.arInfoStatusLayout.addWidget(
            self.analysis_result_statusbar)
        self.stacklayout.addWidget(self.analysis_result_widget)

    def _create_TotoWidget(self):
        self.toto_statusbar = InfoStatusWidget(
            self.display_league, self.league_date, self.current_mode)
        self.toto_widget = TotoWidget(
            self.current_league, self.current_season, self.current_mode)
        self.toto_widget.tInfoStatusLayout.addWidget(self.toto_statusbar)
        self.stacklayout.addWidget(self.toto_widget)

    def _create_TotoResult(self):
        self.toto_result_statusbar = InfoStatusWidget(
            self.display_league, self.league_date, self.current_mode)
        self.toto_result = TotoResultWidget()
        self.toto_result.arInfoStatusLayout.addWidget(
            self.toto_result_statusbar)
        self.stacklayout.addWidget(self.toto_result)

    def activate_Homepage(self):
        self.stacklayout.setCurrentIndex(0)

    def activate_Settings(self):
        self.stacklayout.setCurrentIndex(1)

    def activate_LeagueTable(self):
        self.league_table_widget.update_model(
            self.current_league, self.current_season, self.league_date)
        self.stacklayout.setCurrentIndex(2)

    def activate_Matchday(self):
        self.stacklayout.setCurrentIndex(3)

    def activate_SinglePredict(self):
        self.stacklayout.setCurrentIndex(4)

    def activate_AnalysisResult(self):
        self.analysis_result_widget.update_model()
        self.stacklayout.setCurrentIndex(5)

    def activate_TotoWidget(self):
        self.stacklayout.setCurrentIndex(6)

    def activate_TotoResult(self):
        self.toto_result.update_model()
        self.stacklayout.setCurrentIndex(7)

    def change_date(self, date):
        self.league_date = date
        self.settings_info_statusbar.currentDateLbl.setText(date)
        self.table_info_statusbar.currentDateLbl.setText(date)
        self.matchday_info_statusbar.currentDateLbl.setText(date)
        self.single_predict_statusbar.currentDateLbl.setText(date)
        self.analysis_result_statusbar.currentDateLbl.setText(date)
        self.toto_statusbar.currentDateLbl.setText(date)
        self.toto_result_statusbar.currentDateLbl.setText(date)

        self.homepage_widget.update_date(date)
        self.single_predict_widget.update_date(date)
        self.matchday_widget.set_current_date()
        self.toto_widget.set_current_date()
        self.league_table_widget.update_model(
            self.current_league, self.current_season, date)

    def change_display_league(self, list):
        self.display_league = list[0] + ' ' + list[1]
        self.current_league = list[0]
        self.current_season = list[1]

        self.settings_info_statusbar.currentTableLbl.setText(
            self.display_league)
        self.table_info_statusbar.currentTableLbl.setText(self.display_league)
        self.matchday_info_statusbar.currentTableLbl.setText(
            self.display_league)
        self.single_predict_statusbar.currentTableLbl.setText(
            self.display_league)
        self.analysis_result_statusbar.currentTableLbl.setText(
            self.display_league)
        self.toto_statusbar.currentTableLbl.setText(self.display_league)
        self.toto_result_statusbar.currentTableLbl.setText(self.display_league)

        self.homepage_widget.update_display_league(self.display_league)
        self.matchday_widget.update_league(
            self.current_league, self.current_season)
        self.single_predict_widget.update_league(
            self.current_league, self.current_season)
        self.toto_widget.update_league(
            self.current_league, self.current_season)
        self.league_table_widget.update_model(
            self.current_league, self.current_season, self.league_date)
        self.single_predict_widget.set_comboboxes()

    def change_mode(self, mode):
        self.settings_info_statusbar.modeLbl.setText(mode)
        self.table_info_statusbar.modeLbl.setText(mode)
        self.matchday_info_statusbar.modeLbl.setText(mode)
        self.single_predict_statusbar.modeLbl.setText(mode)
        self.analysis_result_statusbar.modeLbl.setText(mode)
        self.toto_statusbar.modeLbl.setText(mode)
        self.toto_result_statusbar.modeLbl.setText(mode)

        self.single_predict_widget.update_mode(mode)
        self.matchday_widget.update_mode(mode)
        self.toto_widget.update_mode(mode)

    def _get_league_info(self):
        self.league_date = self.controller.get_selected_date()
        self.current_league = self.controller.get_current_league()
        self.current_season = self.controller.get_current_season()
        self.current_mode = self.controller.get_current_mode()
        self.display_league = self.current_league + ' ' + self.current_season
