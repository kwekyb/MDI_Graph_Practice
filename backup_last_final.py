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
        layout = QVBoxLayout(widget)
        widget.setLayout(layout)

        # 한글이 제대로 표시되도록 matplotlib 폰트 설정 (Windows 기준)
        import matplotlib as mpl
        mpl.rcParams["font.family"] = "Malgun Gothic"
        mpl.rcParams["axes.unicode_minus"] = False

        # 사용자 입력 데이터를 저장할 딕셔너리 초기화 (이슬점 포함)
        self.custom_data = {
            "dates": [],
            "temperatures": [],
            "humidities": [],
            "dew_points": []
        }
        # 전체(원본) 데이터를 저장할 변수 (필터 적용 전 데이터를 보존)
        self.all_custom_data = {
            "dates": [],
            "temperatures": [],
            "humidities": [],
            "dew_points": []
        }

        # 사용자 입력 영역 (날짜, 온도, 습도, 이슬점 입력 필드 및 "데이터 추가" 버튼)
        inputLayout = QHBoxLayout()
        
        self.dateEdit = QDateEdit()
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDisplayFormat("yyyy-MM-dd")
        inputLayout.addWidget(QLabel("날짜:"))
        inputLayout.addWidget(self.dateEdit)
        
        self.tempEdit = QLineEdit()
        self.tempEdit.setPlaceholderText("온도")
        inputLayout.addWidget(QLabel("온도:"))
        inputLayout.addWidget(self.tempEdit)
        
        self.humEdit = QLineEdit()
        self.humEdit.setPlaceholderText("습도")
        inputLayout.addWidget(QLabel("습도:"))
        inputLayout.addWidget(self.humEdit)
        
        self.dewEdit = QLineEdit()
        self.dewEdit.setPlaceholderText("이슬점")
        inputLayout.addWidget(QLabel("이슬점:"))
        inputLayout.addWidget(self.dewEdit)
        
        addButton = QPushButton("데이터 추가")
        addButton.clicked.connect(self.addData)
        inputLayout.addWidget(addButton)
        
        layout.addLayout(inputLayout)

        # -------------------------------
        # 좌측: 데이터 테이블 및 엑셀 버튼 영역
        # -------------------------------
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(4)
        self.data_table.setHorizontalHeaderLabels(["날짜", "온도", "습도", "이슬점"])
        self.data_table.horizontalHeader().setStretchLastSection(True)
        self.data_table.cellChanged.connect(self.table_cell_changed)

        dataLeftWidget = QWidget()
        leftLayout = QVBoxLayout(dataLeftWidget)
        leftLayout.setContentsMargins(0, 0, 0, 0)
        leftLayout.addWidget(self.data_table)

        excelWidget = QWidget()
        excelLayout = QHBoxLayout(excelWidget)
        excelLayout.setContentsMargins(0, 0, 0, 0)
        loadExcelButton = QPushButton("엑셀에서 불러오기")
        loadExcelButton.clicked.connect(self.loadFromExcel)
        excelLayout.addWidget(loadExcelButton)
        saveExcelButton = QPushButton("엑셀로 저장하기")
        saveExcelButton.clicked.connect(self.exportToExcel)
        excelLayout.addWidget(saveExcelButton)
        leftLayout.addWidget(excelWidget)

        # -------------------------------
        # 우측: 필터 패널 영역
        # -------------------------------
        filterWidget = QWidget()
        filterLayout = QVBoxLayout(filterWidget)
        filterLayout.setContentsMargins(10, 10, 10, 10)
        
        filterLabel = QLabel("필터 조건:(날짜1~날짜2)")
        filterLayout.addWidget(filterLabel)
        
        self.filterEdit = QLineEdit()
        filterLayout.addWidget(self.filterEdit)
        
        applyFilterButton = QPushButton("검색")
        applyFilterButton.clicked.connect(lambda: self.applyFilter(self.filterEdit.text()))
        filterLayout.addWidget(applyFilterButton)

        # "전체 데이터 보기" 버튼 추가 (필터 해제)
        resetFilterButton = QPushButton("전체 데이터 보기")
        resetFilterButton.clicked.connect(self.resetFilter)
        filterLayout.addWidget(resetFilterButton)
        
        # "그래프 보기" 버튼 추가 (클릭하면 그래프 패널을 업데이트하여 표시함)
        graphViewButton = QPushButton("그래프 보기")
        graphViewButton.clicked.connect(self.showGraph)
        filterLayout.addWidget(graphViewButton)
        
        filterLayout.addStretch()

        # -------------------------------
        # 좌측과 우측 패널을 수평으로 배치
        # -------------------------------
        combinedDataWidget = QWidget()
        combinedLayout = QHBoxLayout(combinedDataWidget)
        combinedLayout.setContentsMargins(0, 0, 0, 0)
        combinedLayout.addWidget(dataLeftWidget, stretch=3)
        combinedLayout.addWidget(filterWidget, stretch=1)

        # -------------------------------
        # 그래프를 표시할 캔버스 영역 생성
        # -------------------------------
        self.canvas = FigureCanvas(plt.Figure(figsize=(12, 9)))
        self.canvas.setFixedSize(1200, 900)
        # 캔버스를 명시적으로 클리어하여 빈 상태로 유지
        self.canvas.figure.clf()
        self.canvas.draw()
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(False)
        scrollArea.setWidget(self.canvas)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # 이전에는 scrollArea.hide()로 감추었으나,
        # 변경 후엔 그래프 영역은 항상 보이나, 캔버스는 초기에는 그래프가 그려져 있지 않음.
        self.scrollArea = scrollArea

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(combinedDataWidget)
        splitter.addWidget(self.scrollArea)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        layout.addWidget(splitter)

        sub.setWidget(widget)
        sub.setWindowTitle('새 창 3 - 그래프')
        sub.setAttribute(Qt.WA_DeleteOnClose, False)
        sub.setWindowFlags(
            Qt.SubWindow |
            Qt.WindowSystemMenuHint |
            Qt.WindowTitleHint |
            Qt.WindowMinMaxButtonsHint |
            Qt.WindowCloseButtonHint
        )
        self.mdi.addSubWindow(sub)
        sub.resize(800, 600)
        sub.show()

    def addData(self):
        """사용자 입력값을 읽어들여 custom_data에 추가하고, 테이블과 그래프를 갱신하는 함수"""
        try:
            date_val = pd.to_datetime(self.dateEdit.date().toString("yyyy-MM-dd"))
        except Exception as e:
            QMessageBox.warning(self, "입력 오류", f"날짜 변환 오류: {e}")
            return

        temp_str = self.tempEdit.text().strip()
        hum_str = self.humEdit.text().strip()
        dew_str = self.dewEdit.text().strip()
        
        if not (temp_str and hum_str and dew_str):
            QMessageBox.warning(self, "경고", "모든 값(온도, 습도, 이슬점)을 입력해주세요.")
            return
        
        try:
            temp_val = float(temp_str)
            hum_val = float(hum_str)
            dew_val = float(dew_str)
        except Exception as e:
            QMessageBox.warning(self, "입력 오류", f"입력값 오류: {e}")
            return
        
        # 데이터 저장 및 원본 데이터 업데이트
        self.custom_data["dates"].append(date_val)
        self.custom_data["temperatures"].append(temp_val)
        self.custom_data["humidities"].append(hum_val)
        self.custom_data["dew_points"].append(dew_val)
        
        self.all_custom_data["dates"].append(date_val)
        self.all_custom_data["temperatures"].append(temp_val)
        self.all_custom_data["humidities"].append(hum_val)
        self.all_custom_data["dew_points"].append(dew_val)
        
        self.tempEdit.clear()
        self.humEdit.clear()
        self.dewEdit.clear()
        self.dateEdit.setFocus()
        
        self.update_table()
        self.plot_data_custom()

    def update_table(self):
        """self.custom_data의 데이터를 QTableWidget에 갱신하여 표시 (이슬점 포함)"""
        self.table_updating = True  # 셀 변경 신호 처리 중단 플래그
        rows = len(self.custom_data["dates"])
        self.data_table.setRowCount(rows)
        for i in range(rows):
            # 날짜 (예: 2023-10-07)
            date_str = self.custom_data["dates"][i].strftime("%Y-%m-%d")
            date_item = QTableWidgetItem(date_str)
            date_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)
            self.data_table.setItem(i, 0, date_item)
            
            # 온도
            if i < len(self.custom_data["temperatures"]):
                temp_val = str(self.custom_data["temperatures"][i])
            else:
                temp_val = ""
            temp_item = QTableWidgetItem(temp_val)
            temp_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)
            self.data_table.setItem(i, 1, temp_item)
            
            # 습도
            if i < len(self.custom_data["humidities"]):
                hum_val = str(self.custom_data["humidities"][i])
            else:
                hum_val = ""
            hum_item = QTableWidgetItem(hum_val)
            hum_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)
            self.data_table.setItem(i, 2, hum_item)
            
            # 이슬점 (값이 존재하지 않으면 빈 문자열 처리)
            if i < len(self.custom_data["dew_points"]):
                dew_val = str(self.custom_data["dew_points"][i])
            else:
                dew_val = ""
            dew_item = QTableWidgetItem(dew_val)
            dew_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)
            self.data_table.setItem(i, 3, dew_item)
        
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
            elif column == 3:
                new_dew = float(new_value)
                self.custom_data["dew_points"][row] = new_dew
            self.plot_data_custom()
        except Exception as e:
            QMessageBox.warning(self, "입력 오류", f"입력값 오류: {e}")

    def plot_data_custom(self, progress=None):
        """사용자 입력 데이터를 기반으로 온도, 습도, 이슬점을 그리는 함수 (진행바 업데이트 포함)"""
        # 0단계: 초기에 진행바를 0으로 설정
        if progress:
            progress.setValue(0)
            QApplication.processEvents()
        self.canvas.figure.clf()  # 캔버스 클리어

        if not self.custom_data["dates"]:
            self.canvas.draw()
            if progress:
                progress.setValue(100)
            return

        dates = self.custom_data["dates"]
        temps = self.custom_data["temperatures"]
        hums = self.custom_data["humidities"]
        dew_points = self.custom_data["dew_points"]

        import matplotlib.dates as mdates
        from matplotlib.ticker import MaxNLocator, FixedLocator
        import numpy as np

        num_dates = mdates.date2num(dates)

        # 1단계: 온도 그래프
        ax1 = self.canvas.figure.add_subplot(311)
        ax1.plot(dates, temps, 'r-', label='온도 (°C)')
        avg_temp = np.mean(temps)
        ax1.axhline(avg_temp, color='gray', linestyle='--', linewidth=1,
                    label=f'평균: {avg_temp:.2f}°C')
        if progress:
            progress.setValue(40)
            QApplication.processEvents()

        # 2단계: 습도 그래프
        ax2 = self.canvas.figure.add_subplot(312)
        ax2.plot(dates, hums, 'b-', label='습도 (%)')
        avg_hum = np.mean(hums)
        ax2.axhline(avg_hum, color='gray', linestyle='--', linewidth=1,
                    label=f'평균: {avg_hum:.2f}%')
        if progress:
            progress.setValue(70)
            QApplication.processEvents()

        # 3단계: 이슬점 그래프
        ax3 = self.canvas.figure.add_subplot(313)
        # 이슬점 값들을 안전하게 숫자로 변환 (실패 시 np.nan 처리)
        dew_points_numeric = []
        for dp in dew_points:
            try:
                dew_points_numeric.append(float(dp))
            except Exception:
                dew_points_numeric.append(np.nan)
        ax3.plot(dates, dew_points_numeric, 'g-', label='이슬점 (°C)')
        avg_dew = np.nanmean(dew_points_numeric)
        ax3.axhline(avg_dew, color='gray', linestyle='--', linewidth=1,
                    label=f'평균: {avg_dew:.2f}°C')
        if progress:
            progress.setValue(90)
            QApplication.processEvents()

        # 4단계: 서브플롯 공통 서식 및 캔버스 업데이트
        for ax in [ax1, ax2, ax3]:
            ax.xaxis.set_major_locator(FixedLocator(num_dates))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.tick_params(axis='x', labelrotation=45, labelsize=9)
            ax.minorticks_on()
            ax.grid(which='both', linestyle='--', linewidth=0.5, alpha=0.7)

        ax1.set_xlabel('날짜', fontsize=10)
        ax1.set_ylabel('온도 (°C)', color='r', fontsize=10)
        ax1.tick_params(axis='y', labelcolor='r', labelsize=9)
        ax1.set_title('온도 변화', pad=15, fontsize=12)
        ax1.legend(loc='upper left', fontsize=9)
        ax1.yaxis.set_major_locator(MaxNLocator(nbins=5))

        ax2.set_xlabel('날짜', fontsize=10)
        ax2.set_ylabel('습도 (%)', color='b', fontsize=10)
        ax2.tick_params(axis='y', labelcolor='b', labelsize=9)
        ax2.set_title('습도 변화', pad=15, fontsize=12)
        ax2.legend(loc='upper left', fontsize=9)
        ax2.yaxis.set_major_locator(MaxNLocator(nbins=5))

        ax3.set_xlabel('날짜', fontsize=10)
        ax3.set_ylabel('이슬점 (°C)', color='g', fontsize=10)
        ax3.tick_params(axis='y', labelcolor='g', labelsize=9)
        ax3.set_title('이슬점 변화', pad=15, fontsize=12)
        ax3.legend(loc='upper left', fontsize=9)
        ax3.yaxis.set_major_locator(MaxNLocator(nbins=5))

        self.canvas.figure.tight_layout()
        self.canvas.draw()

        if progress:
            progress.setValue(100)
            QApplication.processEvents()

    def loadFromExcel(self):
        """엑셀 파일에서 날짜, 온도, 습도, 이슬점 데이터를 불러와 custom_data를 갱신하는 함수
        (그래프 갱신은 하지 않고 테이블 데이터만 업데이트)"""
        fileName, _ = QFileDialog.getOpenFileName(
            self, "엑셀 파일 불러오기", "", "Excel Files (*.xlsx *.xls);;모든 파일 (*.*)"
        )
        if not fileName:
            return
        try:
            df = pd.read_excel(fileName)
            df.columns = df.columns.str.strip()
            n = len(df)

            self.custom_data["dates"] = list(pd.to_datetime(df["날짜"]))
            self.custom_data["temperatures"] = list(df["온도"])
            self.custom_data["humidities"] = list(df["습도"])
            if "이슬점" in df.columns:
                self.custom_data["dew_points"] = list(df["이슬점"])
            else:
                self.custom_data["dew_points"] = ["" for _ in range(n)]
            # 불러온 데이터를 원본 데이터로 저장
            self.all_custom_data = {
                "dates": list(self.custom_data["dates"]),
                "temperatures": list(self.custom_data["temperatures"]),
                "humidities": list(self.custom_data["humidities"]),
                "dew_points": list(self.custom_data["dew_points"])
            }
        except Exception as e:
            QMessageBox.critical(self, "오류", f"엑셀 파일 불러오기 중 오류 발생: {e}")
            return
        self.update_table()
        # 그래프는 갱신하지 않음.
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

    def applyFilter(self, filter_text):
        """입력된 필터 조건을 기반으로 원본 데이터를 필터링하는 함수.
        
        조건이 'YYYY-MM-DD ~ YYYY-MM-DD'와 같은 범위 형식이면 해당 범위에 포함된 데이터만 필터링합니다.
        그렇지 않으면 기존의 단일 날짜 검색을 수행합니다.
        """
        filter_text = filter_text.strip()
        # 필터 조건이 비어 있으면 전체 데이터를 표시합니다.
        if not filter_text:
            self.resetFilter()
            return

        if "~" in filter_text:
            # 범위 조건: '~'를 구분자로 사용
            parts = filter_text.split("~")
            if len(parts) == 2:
                start_text = parts[0].strip()
                end_text = parts[1].strip()
                try:
                    start_date = pd.to_datetime(start_text)
                    end_date = pd.to_datetime(end_text)
                except Exception as e:
                    QMessageBox.warning(self, "입력 오류", f"날짜 범위 형식 오류: {e}")
                    return
                # 필터: 날짜가 start_date 이상이고 end_date 이하인 경우 선택
                filtered_data = [
                    (date, temp, hum, dew)
                    for date, temp, hum, dew in zip(
                        self.all_custom_data["dates"],
                        self.all_custom_data["temperatures"],
                        self.all_custom_data["humidities"],
                        self.all_custom_data["dew_points"]
                    )
                    if start_date <= date <= end_date
                ]
            else:
                QMessageBox.warning(self, "입력 오류", "날짜 범위 형식이 올바르지 않습니다. 예: 2024-12-22 ~ 2024-12-24")
                return
        else:
            # 단일 날짜 검색: filter_text가 날짜 문자열에 포함된 경우 선택
            filtered_data = [
                (date, temp, hum, dew)
                for date, temp, hum, dew in zip(
                    self.all_custom_data["dates"],
                    self.all_custom_data["temperatures"],
                    self.all_custom_data["humidities"],
                    self.all_custom_data["dew_points"]
                )
                if filter_text.lower() in date.strftime("%Y-%m-%d").lower()
            ]

        self.custom_data["dates"] = [date for date, _, _, _ in filtered_data]
        self.custom_data["temperatures"] = [temp for _, temp, _, _ in filtered_data]
        self.custom_data["humidities"] = [hum for _, _, hum, _ in filtered_data]
        self.custom_data["dew_points"] = [dew for _, _, _, dew in filtered_data]
        self.update_table()
        # self.plot_data_custom()

    def resetFilter(self):
        """전체 데이터를 다시 표시하는 함수"""
        # 원본 데이터(self.all_custom_data)를 복사해서 custom_data를 복원함.
        self.custom_data = {k: list(v) for k, v in self.all_custom_data.items()}
        self.update_table()
        # self.plot_data_custom()

    def showGraph(self):
        """그래프 보기 버튼 클릭 시 진행바를 표시하며 그래프를 그리는 함수"""
        # 결정형 진행바: 최소=0, 최대=100
        progress = QProgressDialog("그래프를 그리는 중...", "취소", 0, 100, self)
        progress.setWindowTitle("진행중")
        progress.setWindowModality(Qt.WindowModal)
        progress.setCancelButton(None)
        progress.setValue(0)  # 초기값을 0으로 설정
        progress.show()
        QApplication.processEvents()
        try:
            # progress 객체를 plot_data_custom에 전달
            self.plot_data_custom(progress)
        finally:
            progress.close()


class CanvasContainer(QWidget):
    """
    캔버스를 감싸는 컨테이너 위젯.
    부모 위젯의 가로 폭에 따라 캔버스는 가로로 늘어나되, 높이는 고정(최소치)을 유지하여
    QScrollArea에서 수직 스크롤바가 나타나도록 합니다.
    """
    def __init__(self, canvas, parent=None):
        super().__init__(parent)
        self.canvas = canvas
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(canvas)

    def resizeEvent(self, event):
        new_width = self.width()
        # 가로폭은 부모 폭에 맞추고, 높이는 최소 높이(예: 800)로 유지합니다.
        self.canvas.resize(new_width, self.canvas.minimumHeight())
        super().resizeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
