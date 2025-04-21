import sys
import requests
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window1 = None  # 새창1의 참조를 저장할 변수
        self.initUI()

    def initUI(self):
        # MDI 영역 생성
        self.mdi = QMdiArea()
        self.mdi.setViewMode(QMdiArea.SubWindowView)
        self.mdi.setOption(QMdiArea.DontMaximizeSubWindowOnActivation)
        self.setCentralWidget(self.mdi)

        # 툴바 생성
        toolbar = self.addToolBar('도구')
        toolbar.setMovable(False)  # 툴바 위치 고정

        # 새 창 열기 액션들 생성
        newAction1 = QAction('새 창 1', self)
        newAction1.setShortcut('Ctrl+1')
        newAction1.triggered.connect(self.createWindow1)
        toolbar.addAction(newAction1)

        newAction2 = QAction('새 창 2', self)
        newAction2.setShortcut('Ctrl+2')
        newAction2.triggered.connect(self.createWindow2)
        toolbar.addAction(newAction2)

        newAction3 = QAction('새 창 3', self)
        newAction3.setShortcut('Ctrl+3')
        newAction3.triggered.connect(self.createWindow3)
        toolbar.addAction(newAction3)

        toolbar.addSeparator()  # 구분선 추가

        # 창 배열 액션 추가
        tileAction = QAction('바둑판 배열', self)
        tileAction.triggered.connect(self.mdi.tileSubWindows)
        toolbar.addAction(tileAction)

        cascadeAction = QAction('계단식 배열', self)
        cascadeAction.triggered.connect(self.mdi.cascadeSubWindows)
        toolbar.addAction(cascadeAction)

        # 윈도우 설정
        self.setWindowTitle('MDI 애플리케이션')
        self.setGeometry(100, 100, 800, 600)

    def createWindow1(self):
        # 첫 번째 타입의 서브윈도우 생성
        sub = QMdiSubWindow()
        widget = QWidget()
        widget.setMinimumSize(300, 200)

        layout = QVBoxLayout()
        widget.setLayout(layout)

        label = QLabel('창 1 - 입력하세요:')
        layout.addWidget(label)

        textbox = QLineEdit()
        layout.addWidget(textbox)
        widget.textbox = textbox  # 텍스트박스를 위젯의 속성으로 저장

        button = QPushButton('확인')
        button.clicked.connect(lambda: self.addTextToMemo(textbox.text(), memo))
        layout.addWidget(button)

        # 메모 영역 추가
        memoLabel = QLabel('메모:')
        layout.addWidget(memoLabel)

        memo = QTextEdit()
        memo.setMinimumHeight(100)
        layout.addWidget(memo)
        widget.memo = memo  # 메모장을 위젯의 속성으로 저장

        # 버튼들을 위한 수평 레이아웃
        btnLayout = QHBoxLayout()
        
        saveButton = QPushButton('저장')
        saveButton.clicked.connect(lambda: self.saveMemo(memo))
        btnLayout.addWidget(saveButton)

        loadButton = QPushButton('불러오기')
        loadButton.clicked.connect(lambda: self.loadMemo(memo))
        btnLayout.addWidget(loadButton)

        clearSelectedButton = QPushButton('선택지우기')
        clearSelectedButton.clicked.connect(lambda: self.clearSelectedMemo(memo))
        btnLayout.addWidget(clearSelectedButton)

        clearAllButton = QPushButton('전체지우기')
        clearAllButton.clicked.connect(lambda: self.clearAllMemo(memo))
        btnLayout.addWidget(clearAllButton)

        layout.addLayout(btnLayout)
        layout.addStretch()

        sub.setWidget(widget)
        sub.setWindowTitle('새 창 1')
        sub.setAttribute(Qt.WA_DeleteOnClose, False)
        sub.setWindowFlags(Qt.SubWindow | Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.mdi.addSubWindow(sub)
        sub.resize(400, 400)
        sub.show()
        
        self.window1 = widget
        textbox.setFocus()

    def saveMemo(self, memo):
        """메모장의 내용을 파일로 저장하는 함수"""
        text = memo.toPlainText()
        if not text.strip():  # 메모가 비어있으면 저장하지 않음
            QMessageBox.warning(self, '경고', '저장할 내용이 없습니다.')
            return
            
        fileName, _ = QFileDialog.getSaveFileName(self,
            "메모 저장",
            "",
            "텍스트 파일 (*.txt);;모든 파일 (*.*)")
            
        if fileName:  # 파일명을 선택한 경우
            try:
                with open(fileName, 'w', encoding='utf-8') as file:
                    file.write(text)
                QMessageBox.information(self, '알림', '메모가 저장되었습니다.')
            except Exception as e:
                QMessageBox.critical(self, '오류', f'저장 중 오류가 발생했습니다.\n{str(e)}')

    def loadMemo(self, memo):
        """파일에서 메모 내용을 불러오는 함수"""
        fileName, _ = QFileDialog.getOpenFileName(self,
            "메모 불러오기",
            "",
            "텍스트 파일 (*.txt);;모든 파일 (*.*)")
            
        if fileName:  # 파일을 선택한 경우
            try:
                with open(fileName, 'r', encoding='utf-8') as file:
                    text = file.read()
                memo.setText(text)
                QMessageBox.information(self, '알림', '메모를 불러왔습니다.')
            except Exception as e:
                QMessageBox.critical(self, '오류', f'불러오기 중 오류가 발생했습니다.\n{str(e)}')

    def addTextToMemo(self, text, memo):
        """텍스트박스의 내용을 메모장에 추가하는 함수"""
        if text.strip():  # 빈 텍스트가 아닌 경우에만 추가
            current_text = memo.toPlainText()
            if current_text:  # 기존 텍스트가 있으면 새 줄에 추가
                memo.append(text)
            else:  # 기존 텍스트가 없으면 바로 설정
                memo.setText(text)
            self.window1.textbox.clear()
            self.window1.textbox.setFocus()

    def createWindow2(self):
        sub = QMdiSubWindow()
        widget = QWidget()
        widget.setMinimumSize(300, 200)

        layout = QVBoxLayout()
        widget.setLayout(layout)

        label = QLabel('창 2 - 선택하세요:')
        layout.addWidget(label)

        combo = QComboBox()
        combo.addItems(['항목 1', '항목 2', '항목 3'])
        layout.addWidget(combo)

        button = QPushButton('선택')
        button.clicked.connect(lambda: self.setTextToWindow1(combo.currentText()))  # 버튼 클릭 시 선택된 항목을 새창1로 전달
        layout.addWidget(button)

        layout.addStretch()

        sub.setWidget(widget)
        sub.setWindowTitle('새 창 2')
        sub.setAttribute(Qt.WA_DeleteOnClose, False)
        sub.setWindowFlags(Qt.SubWindow | Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.mdi.addSubWindow(sub)
        sub.resize(400, 300)
        sub.show()

    def setTextToWindow1(self, text):
        """새창2에서 선택한 텍스트를 새창1의 텍스트박스에 설정하는 함수"""
        if self.window1 and hasattr(self.window1, 'textbox'):
            self.window1.textbox.setText(text)

    def createWindow3(self):
        sub = QMdiSubWindow()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # 한글이 제대로 표시되도록 matplotlib 폰트 설정 (Windows 기준)
        import matplotlib as mpl
        mpl.rcParams["font.family"] = "Malgun Gothic"
        mpl.rcParams["axes.unicode_minus"] = False

        # 사용자 입력 데이터를 저장할 딕셔너리 초기화
        self.custom_data = {"dates": [], "temperatures": [], "humidities": []}

        # 사용자 입력 영역 (날짜, 온도, 습도 입력 필드와 "데이터 추가" 버튼)
        inputLayout = QHBoxLayout()
        # 날짜 입력: QDateEdit (마우스로 날짜 선택 가능)
        self.dateEdit = QDateEdit()
        self.dateEdit.setCalendarPopup(True)  # 달력 팝업 활성화
        self.dateEdit.setDisplayFormat("yyyy-MM-dd")
        inputLayout.addWidget(QLabel("날짜:"))
        inputLayout.addWidget(self.dateEdit)
        # 온도 입력 (QLineEdit)
        self.tempEdit = QLineEdit()
        self.tempEdit.setPlaceholderText("온도")
        inputLayout.addWidget(QLabel("온도:"))
        inputLayout.addWidget(self.tempEdit)
        # 습도 입력 (QLineEdit)
        self.humEdit = QLineEdit()
        self.humEdit.setPlaceholderText("습도")
        inputLayout.addWidget(QLabel("습도:"))
        inputLayout.addWidget(self.humEdit)
        # 데이터 추가 버튼
        addButton = QPushButton("데이터 추가")
        addButton.clicked.connect(self.addData)
        inputLayout.addWidget(addButton)
        
        layout.addLayout(inputLayout)
        
        # 테이블 위젯 추가: 입력한 데이터를 표시하고 수정할 수 있도록 함.
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(3)
        self.data_table.setHorizontalHeaderLabels(["날짜", "온도", "습도"])
        self.data_table.horizontalHeader().setStretchLastSection(True)
        # 테이블의 셀 값이 변경되면 자동 처리를 위해 신호 연결
        self.data_table.cellChanged.connect(self.table_cell_changed)
        layout.addWidget(self.data_table)
        
        # 엑셀 관련 버튼 추가 (불러오기 / 엑셀로 저장하기)
        excelLayout = QHBoxLayout()
        loadExcelButton = QPushButton("엑셀에서 불러오기")
        loadExcelButton.clicked.connect(self.loadFromExcel)
        excelLayout.addWidget(loadExcelButton)
        saveExcelButton = QPushButton("엑셀로 저장하기")
        saveExcelButton.clicked.connect(self.exportToExcel)
        excelLayout.addWidget(saveExcelButton)
        layout.addLayout(excelLayout)
        
        # 그래프를 표시할 캔버스 추가
        self.canvas = FigureCanvas(plt.Figure())
        layout.addWidget(self.canvas)

        sub.setWidget(widget)
        sub.setWindowTitle('새 창 3 - 그래프')
        sub.setAttribute(Qt.WA_DeleteOnClose, False)
        sub.setWindowFlags(Qt.SubWindow | Qt.WindowSystemMenuHint | Qt.WindowTitleHint |
                           Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.mdi.addSubWindow(sub)
        sub.resize(800, 600)
        sub.show()

    def addData(self):
        """사용자 입력값을 읽어들여 custom_data에 추가하고, 테이블과 그래프를 갱신하는 함수"""
        try:
            # QDateEdit에서 날짜를 "yyyy-MM-dd" 문자열로 변환 후 to_datetime 사용
            date_val = pd.to_datetime(self.dateEdit.date().toString("yyyy-MM-dd"))
        except Exception as e:
            QMessageBox.warning(self, "입력 오류", f"날짜 변환 오류: {e}")
            return

        temp_str = self.tempEdit.text().strip()
        hum_str = self.humEdit.text().strip()
        
        if not (temp_str and hum_str):
            QMessageBox.warning(self, "경고", "모든 값(온도, 습도)을 입력해주세요.")
            return
        
        try:
            temp_val = float(temp_str)
            hum_val = float(hum_str)
        except Exception as e:
            QMessageBox.warning(self, "입력 오류", f"입력값 오류: {e}")
            return
        
        # 데이터 저장
        self.custom_data["dates"].append(date_val)
        self.custom_data["temperatures"].append(temp_val)
        self.custom_data["humidities"].append(hum_val)
        
        # 입력 필드 초기화 및 날짜 입력 필드에 포커스 설정
        self.tempEdit.clear()
        self.humEdit.clear()
        self.dateEdit.setFocus()
        
        # 테이블과 그래프 갱신
        self.update_table()
        self.plot_data_custom()

    def update_table(self):
        """self.custom_data의 데이터를 QTableWidget에 갱신하여 표시"""
        self.table_updating = True  # 셀 변경 신호 처리 중단 플래그
        rows = len(self.custom_data["dates"])
        self.data_table.setRowCount(rows)
        for i in range(rows):
            # 날짜: 문자열로 표시 (예: 2023-10-07)
            date_str = self.custom_data["dates"][i].strftime("%Y-%m-%d")
            date_item = QTableWidgetItem(date_str)
            date_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)
            self.data_table.setItem(i, 0, date_item)
            
            temp_item = QTableWidgetItem(str(self.custom_data["temperatures"][i]))
            temp_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)
            self.data_table.setItem(i, 1, temp_item)
            
            hum_item = QTableWidgetItem(str(self.custom_data["humidities"][i]))
            hum_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)
            self.data_table.setItem(i, 2, hum_item)
        self.table_updating = False

    def table_cell_changed(self, row, column):
        """테이블 셀 수정 시 custom_data를 업데이트하고 그래프를 갱신하는 함수"""
        if getattr(self, "table_updating", False):
            return
        
        try:
            new_value = self.data_table.item(row, column).text()
            if column == 0:
                # 날짜 수정: 문자열을 날짜로 변환 (YYYY-MM-DD 형식)
                new_date = pd.to_datetime(new_value)
                self.custom_data["dates"][row] = new_date
            elif column == 1:
                new_temp = float(new_value)
                self.custom_data["temperatures"][row] = new_temp
            elif column == 2:
                new_hum = float(new_value)
                self.custom_data["humidities"][row] = new_hum
            self.plot_data_custom()
        except Exception as e:
            QMessageBox.warning(self, "입력 오류", f"입력값 오류: {e}")

    def plot_data_custom(self):
        """사용자 입력 데이터를 기반으로 온도와 습도를 각각의 별도 그래프로 그리는 함수"""
        self.canvas.figure.clf()  # 이전 축 제거
        if not self.custom_data["dates"]:
            self.canvas.draw()
            return

        dates = self.custom_data["dates"]
        temps = self.custom_data["temperatures"]
        hums = self.custom_data["humidities"]

        import matplotlib.dates as mdates
        from matplotlib.ticker import MaxNLocator, FixedLocator

        # 첫 번째 서브플롯: 온도 그래프
        ax1 = self.canvas.figure.add_subplot(211)  # 2행 1열의 첫번째 플롯
        ax1.plot(dates, temps, 'r-', label='온도 (°C)')
        ax1.set_xlabel('날짜', fontsize=10)
        ax1.set_ylabel('온도 (°C)', color='r', fontsize=10)
        ax1.tick_params(axis='y', labelcolor='r', labelsize=9)
        num_dates = mdates.date2num(dates)
        ax1.xaxis.set_major_locator(FixedLocator(num_dates))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1.tick_params(axis='x', labelrotation=45, labelsize=9)
        ax1.set_title('온도 변화', pad=15, fontsize=12)
        ax1.legend(loc='upper left', fontsize=9)
        ax1.yaxis.set_major_locator(MaxNLocator(nbins=5))

        # 두 번째 서브플롯: 습도 그래프
        ax2 = self.canvas.figure.add_subplot(212)  # 2행 1열의 두번째 플롯
        ax2.plot(dates, hums, 'b-', label='습도 (%)')
        ax2.set_xlabel('날짜', fontsize=10)
        ax2.set_ylabel('습도 (%)', color='b', fontsize=10)
        ax2.tick_params(axis='y', labelcolor='b', labelsize=9)
        ax2.xaxis.set_major_locator(FixedLocator(num_dates))
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax2.tick_params(axis='x', labelrotation=45, labelsize=9)
        ax2.set_title('습도 변화', pad=15, fontsize=12)
        ax2.legend(loc='upper left', fontsize=9)
        ax2.yaxis.set_major_locator(MaxNLocator(nbins=5))

        self.canvas.figure.tight_layout()
        self.canvas.draw()

    def loadFromExcel(self):
        """엑셀 파일에서 날짜, 온도, 습도 데이터를 불러와 custom_data를 갱신하는 함수"""
        fileName, _ = QFileDialog.getOpenFileName(self, 
            "엑셀 파일 불러오기", "", "Excel Files (*.xlsx *.xls);;모든 파일 (*.*)")
        if not fileName:
            return
        try:
            df = pd.read_excel(fileName)
            # 파일의 열 이름은 "날짜", "온도", "습도"로 가정합니다.
            self.custom_data["dates"] = list(pd.to_datetime(df["날짜"]))
            self.custom_data["temperatures"] = list(df["온도"])
            self.custom_data["humidities"] = list(df["습도"])
        except Exception as e:
            QMessageBox.critical(self, "오류", f"엑셀 파일 불러오기 중 오류 발생: {e}")
            return
        self.update_table()
        self.plot_data_custom()
        QMessageBox.information(self, "알림", "엑셀 파일 불러오기가 완료되었습니다.")

    def exportToExcel(self):
        """현재 custom_data 데이터를 엑셀 파일로 저장하는 함수"""
        fileName, _ = QFileDialog.getSaveFileName(self, 
            "엑셀로 저장하기", "", "Excel Files (*.xlsx *.xls);;모든 파일 (*.*)")
        if not fileName:
            return
        try:
            df = pd.DataFrame({
                "날짜": [d.strftime("%Y-%m-%d") for d in self.custom_data["dates"]],
                "온도": self.custom_data["temperatures"],
                "습도": self.custom_data["humidities"]
            })
            df.to_excel(fileName, index=False)
            QMessageBox.information(self, "알림", "엑셀로 저장되었습니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"엑셀로 저장 중 오류 발생: {e}")

    def clearSelectedMemo(self, memo):
        """메모장에서 선택된 텍스트를 지우고 나머지 텍스트를 재배치하는 함수"""
        cursor = memo.textCursor()
        if cursor.hasSelection():
            # 선택 영역의 시작점과 끝점을 구합니다.
            start = cursor.selectionStart()
            end = cursor.selectionEnd()
            # 메모장의 전체 텍스트를 가져옵니다.
            full_text = memo.toPlainText()
            # 선택된 영역을 제거한 후 텍스트를 재구성합니다.
            new_text = full_text[:start] + full_text[end:]
            memo.setPlainText(new_text)
            # 커서를 선택이 삭제된 위치로 이동시킵니다.
            new_cursor = memo.textCursor()
            new_cursor.setPosition(start)
            memo.setTextCursor(new_cursor)
        else:
            QMessageBox.information(self, '알림', '선택된 텍스트가 없습니다.')

    def clearAllMemo(self, memo):
        """메모장의 모든 내용을 지우는 함수"""
        if memo.toPlainText().strip():  # 메모장에 내용이 있는 경우
            reply = QMessageBox.question(self, '확인', 
                '모든 내용을 지우시겠습니까?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                memo.clear()
                QMessageBox.information(self, '알림', '모든 내용이 지워졌습니다.')
        else:
            QMessageBox.information(self, '알림', '지울 내용이 없습니다.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
