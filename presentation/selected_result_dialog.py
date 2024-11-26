import os
import pathlib
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.uic import loadUi

from business.controllers.poisson_controller import PoissonController
from business.utils.common import CommonUtil
from business.utils.constants import ANALYSIS_MODE_PREFIX


class SelectedResultDialog(QDialog):
    def __init__(self, parent, poisson_id):
        super().__init__(parent)
        loadUi("./presentation/ui/selected_result_dialog.ui", self)
        self.poisson = PoissonController()
        self.data = self.poisson.get_data_for_dialog(poisson_id)
        self.mode = self.data[15]
        self.home_team = self.data[4]
        self.away_team = self.data[5]

        self.setWindowTitle(self.home_team + ' - ' + self.away_team)
        self.matchLbl.setText(self.home_team + ' - ' + self.away_team)
        self.dateLbl.setText(self.data[1])
        self.leagueLbl.setText(self.data[2])
        self.seasonLbl.setText(self.data[3])
        self.modeLbl.setText(self.mode)

        self.plotBtn.clicked.connect(self.on_plotBtn_Clicked)
        self.excelBtn.clicked.connect(self.on_excelBtn_Clicked)
        self.closeBtn.clicked.connect(self.close)

    def on_plotBtn_Clicked(self):
        self.close()
        self.poisson.show_result_plot_goal_given(
            self.home_team, self.away_team, self.data[6], self.data[7])

    def on_excelBtn_Clicked(self):
        is_ok = self.poisson.save_to_excel_from_result(self.data)
        if is_ok:
            self.excel_dialog()
        else:
            self.error_dialog()

    def excel_dialog(self):
        excel_path = f"output/match_results/{self.home_team}-{self.away_team}_{
            CommonUtil.excel_datetime()}_{ANALYSIS_MODE_PREFIX[self.mode]}.xlsx"
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Információ")
        dlg.setText(f"A mérkőzés sikeresen elmentésre került a következő néven: \n{
                    self.home_team}-{self.away_team}_{CommonUtil.excel_datetime()}_{ANALYSIS_MODE_PREFIX[self.mode]}.xlsx")
        dlg.setStandardButtons(
            QMessageBox.StandardButton.Open | QMessageBox.StandardButton.Cancel
        )
        dlg.setIcon(QMessageBox.Icon.Information)
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Open:
            project_path = pathlib.Path().resolve()
            file_path = os.path.join(project_path, excel_path)
            os.startfile(file_path)

    def error_dialog(self):
        QMessageBox.critical(
            self,
            "Hiba",
            "Nem sikerült elmenti az eredményeket."
        )
