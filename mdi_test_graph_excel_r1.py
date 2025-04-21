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

        # 한글 폰트 설정 (예: Windows 기준)
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

        # 사용자 입력 영역 (새 데이터 추가용)
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

        # 필터 입력 UI: 시작날짜/종료날짜 및 버튼
        filterLayout = QHBoxLayout()
        self.startDateEdit = QDateEdit()
        self.startDateEdit.setCalendarPopup(True)
        self.startDateEdit.setDisplayFormat("yyyy-MM-dd")
        filterLayout.addWidget(QLabel("시작날짜:"))
        filterLayout.addWidget(self.startDateEdit)
        
        self.endDateEdit = QDateEdit()
        self.endDateEdit.setCalendarPopup(True)
        self.endDateEdit.setDisplayFormat("yyyy-MM-dd")
        filterLayout.addWidget(QLabel("종료날짜:"))
        filterLayout.addWidget(self.endDateEdit)
        
        # 필터 적용 버튼
        filterButton = QPushButton("필터 적용")
        filterButton.clicked.connect(self.plot_data_custom)
        filterLayout.addWidget(filterButton)
        
        # 전체 데이터 보기 버튼 추가: 전체 데이터를 보여주도록 필터를 초기화
        fullDataButton = QPushButton("전체 데이터 보기")
        fullDataButton.clicked.connect(self.resetFilter)
        filterLayout.addWidget(fullDataButton)

        layout.addLayout(filterLayout)

        # 데이터 테이블 위젯 생성
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(4)
        self.data_table.setHorizontalHeaderLabels(["날짜", "온도", "습도", "이슬점"])
        self.data_table.horizontalHeader().setStretchLastSection(True)
        self.data_table.cellChanged.connect(self.table_cell_changed)

        # 데이터 테이블 및 엑셀 관련 버튼을 담는 위젯 생성
        dataWidget = QWidget()
        dataLayout = QVBoxLayout(dataWidget)
        dataLayout.setContentsMargins(0, 0, 0, 0)
        dataLayout.addWidget(self.data_table)

        excelWidget = QWidget()
        excelLayout = QHBoxLayout(excelWidget)
        excelLayout.setContentsMargins(0, 0, 0, 0)
        loadExcelButton = QPushButton("엑셀에서 불러오기")
        loadExcelButton.clicked.connect(self.loadFromExcel)
        excelLayout.addWidget(loadExcelButton)
        saveExcelButton = QPushButton("엑셀로 저장하기")
        saveExcelButton.clicked.connect(self.exportToExcel)
        excelLayout.addWidget(saveExcelButton)
        dataLayout.addWidget(excelWidget)

        # 그래프용 캔버스 생성 (고정 크기: 예시 1200 x 900)
        self.canvas = FigureCanvas(plt.Figure(figsize=(12, 9)))
        self.canvas.setFixedSize(1200, 900)

        # QScrollArea에 캔버스 추가 (필요시 스크롤바 표시)
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(False)
        scrollArea.setWidget(self.canvas)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # QSplitter로 데이터 영역과 그래프 영역 분할 (수직)
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(dataWidget)
        splitter.addWidget(scrollArea)
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
            # QDateEdit에서 날짜를 "yyyy-MM-dd" 문자열로 변환 후 to_datetime 사용
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
        
        # 데이터 저장
        self.custom_data["dates"].append(date_val)
        self.custom_data["temperatures"].append(temp_val)
        self.custom_data["humidities"].append(hum_val)
        self.custom_data["dew_points"].append(dew_val)
        
        # 입력 필드 초기화 및 날짜 입력 필드에 포커스 설정
        self.tempEdit.clear()
        self.humEdit.clear()
        self.dewEdit.clear()
        self.dateEdit.setFocus()
        
        # 테이블과 그래프 갱신
        self.update_table()
        self.plot_data_custom()

    def update_table(self, dates=None, temperatures=None, humidities=None, dew_points=None):
        """매개변수가 있으면 전달받은 데이터를, 없으면 self.custom_data의 전체 데이터를 사용하여 테이블 갱신"""
        self.table_updating = True
        if dates is None:
            dates = self.custom_data["dates"]
            temperatures = self.custom_data["temperatures"]
            humidities = self.custom_data["humidities"]
            dew_points = self.custom_data["dew_points"]

        rows = len(dates)
        self.data_table.setRowCount(rows)
        for i in range(rows):
            # 날짜
            date_str = dates[i].strftime("%Y-%m-%d")
            date_item = QTableWidgetItem(date_str)
            date_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)
            self.data_table.setItem(i, 0, date_item)

            # 온도
            temp_val = str(temperatures[i])
            temp_item = QTableWidgetItem(temp_val)
            temp_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)
            self.data_table.setItem(i, 1, temp_item)

            # 습도
            hum_val = str(humidities[i])
            hum_item = QTableWidgetItem(hum_val)
            hum_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)
            self.data_table.setItem(i, 2, hum_item)

            # 이슬점
            dew_val = str(dew_points[i])
            dew_item = QTableWidgetItem(dew_val)
            dew_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)
            self.data_table.setItem(i, 3, dew_item)

        self.data_table.resizeColumnsToContents()
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

    def plot_data_custom(self):
        """사용자 입력 및 선택한 시작/종료 날짜에 해당하는 데이터를 기반으로
           데이터 테이블과 그래프(온도, 습도, 이슬점 및 평균선)를 갱신하는 함수"""
        self.canvas.figure.clf()  # 이전 축 지우기

        if not self.custom_data["dates"]:
            self.canvas.draw()
            return

        # QDateEdit에서 선택한 날짜를 Python의 date 객체로 추출
        start_date = self.startDateEdit.date().toPyDate()
        end_date = self.endDateEdit.date().toPyDate()

        # 선택한 기간에 해당하는 데이터만 필터링 (pandas Timestamp의 date()와 비교)
        filtered_dates = []
        filtered_temps = []
        filtered_hums = []
        filtered_dew = []
        for d, t, h, dp in zip(self.custom_data["dates"],
                               self.custom_data["temperatures"],
                               self.custom_data["humidities"],
                               self.custom_data["dew_points"]):
            if start_date <= d.date() <= end_date:
                filtered_dates.append(d)
                filtered_temps.append(t)
                filtered_hums.append(h)
                filtered_dew.append(dp)

        # 필터링된 데이터를 기준으로 데이터 테이블 업데이트 (테이블에도 필터링 결과만 반영)
        self.update_table(filtered_dates, filtered_temps, filtered_hums, filtered_dew)

        if not filtered_dates:
            self.canvas.draw()
            return

        import matplotlib.dates as mdates
        from matplotlib.ticker import MaxNLocator, FixedLocator

        num_dates = mdates.date2num(filtered_dates)

        # x축 범위: 최소/최대 값에 10%의 여백 추가
        x_min = min(num_dates)
        x_max = max(num_dates)
        margin = (x_max - x_min) * 0.1 if x_max > x_min else 1
        x_left = x_min - margin
        x_right = x_max + margin

        # 서브플롯 1: 온도 그래프
        ax1 = self.canvas.figure.add_subplot(311)
        ax1.plot(filtered_dates, filtered_temps, 'r-', label='온도 (°C)')
        if filtered_temps:
            temp_mean = sum(filtered_temps) / len(filtered_temps)
            ax1.axhline(y=temp_mean, color='r', linestyle='--', label=f'평균: {temp_mean:.2f}°C')
        ax1.set_xlabel('날짜 (월-시)', fontsize=10)
        ax1.set_ylabel('온도 (°C)', color='r', fontsize=10)
        ax1.tick_params(axis='y', labelcolor='r', labelsize=9)
        ax1.xaxis.set_major_locator(FixedLocator(num_dates))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%H'))
        ax1.set_xlim(x_left, x_right)
        ax1.tick_params(axis='x', labelrotation=45, labelsize=9)
        ax1.set_title('온도 변화', pad=15, fontsize=12)
        ax1.legend(loc='upper left', fontsize=9)
        ax1.yaxis.set_major_locator(MaxNLocator(nbins=5))
        ax1.minorticks_on()
        ax1.grid(which='both', linestyle='--', linewidth=0.5, alpha=0.7)

        # 서브플롯 2: 습도 그래프
        ax2 = self.canvas.figure.add_subplot(312)
        ax2.plot(filtered_dates, filtered_hums, 'b-', label='습도 (%)')
        if filtered_hums:
            hum_mean = sum(filtered_hums) / len(filtered_hums)
            ax2.axhline(y=hum_mean, color='b', linestyle='--', label=f'평균: {hum_mean:.2f}%')
        ax2.set_xlabel('날짜 (월-시)', fontsize=10)
        ax2.set_ylabel('습도 (%)', color='b', fontsize=10)
        ax2.tick_params(axis='y', labelcolor='b', labelsize=9)
        ax2.xaxis.set_major_locator(FixedLocator(num_dates))
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%H'))
        ax2.set_xlim(x_left, x_right)
        ax2.tick_params(axis='x', labelrotation=45, labelsize=9)
        ax2.set_title('습도 변화', pad=15, fontsize=12)
        ax2.legend(loc='upper left', fontsize=9)
        ax2.yaxis.set_major_locator(MaxNLocator(nbins=5))
        ax2.minorticks_on()
        ax2.grid(which='both', linestyle='--', linewidth=0.5, alpha=0.7)

        # 서브플롯 3: 이슬점 그래프
        ax3 = self.canvas.figure.add_subplot(313)
        try:
            # 빈 문자열은 제외하고 숫자로 변환
            dew_points_numeric = [float(dp) for dp in filtered_dew if dp != ""]
        except Exception:
            dew_points_numeric = filtered_dew
        ax3.plot(filtered_dates, dew_points_numeric, 'g-', label='이슬점 (°C)')
        if dew_points_numeric:
            dew_mean = sum(dew_points_numeric) / len(dew_points_numeric)
            ax3.axhline(y=dew_mean, color='g', linestyle='--', label=f'평균: {dew_mean:.2f}°C')
        ax3.set_xlabel('날짜 (월-시)', fontsize=10)
        ax3.set_ylabel('이슬점 (°C)', color='g', fontsize=10)
        ax3.tick_params(axis='y', labelcolor='g', labelsize=9)
        ax3.xaxis.set_major_locator(FixedLocator(num_dates))
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m-%H'))
        ax3.set_xlim(x_left, x_right)
        ax3.tick_params(axis='x', labelrotation=45, labelsize=9)
        ax3.set_title('이슬점 변화', pad=15, fontsize=12)
        ax3.legend(loc='upper left', fontsize=9)
        ax3.yaxis.set_major_locator(MaxNLocator(nbins=5))
        ax3.minorticks_on()
        ax3.grid(which='both', linestyle='--', linewidth=0.5, alpha=0.7)

        self.canvas.figure.tight_layout()
        self.canvas.draw()

    def loadFromExcel(self):
        """엑셀 파일에서 날짜, 온도, 습도, 이슬점 데이터를 불러와 custom_data를 갱신하는 함수"""
        fileName, _ = QFileDialog.getOpenFileName(
            self, "엑셀 파일 불러오기", "", "Excel Files (*.xlsx *.xls);;모든 파일 (*.*)"
        )
        if not fileName:
            return

            # 파일 확장자에 따라 적절한 엔진 사용 (xlsx 파일의 경우 openpyxl 필요)
            if fileName.lower().endswith('.xlsx'):
                df = pd.read_excel(fileName, engine='openpyxl')
            else:
                df = pd.read_excel(fileName)
            
            # 엑셀 파일 헤더의 앞뒤 공백을 제거
            df.columns = df.columns.str.strip()
            n = len(df)

            self.custom_data["dates"] = list(pd.to_datetime(df["날짜"]))
            self.custom_data["temperatures"] = list(df["온도"])
            self.custom_data["humidities"] = list(df["습도"])
            self.custom_data["dew_points"] = list(df["이슬점"])
        
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

    def resetFilter(self):
        """전체 데이터를 보여주도록 필터를 초기화하고 테이블과 그래프를 갱신하는 함수"""
        from PyQt5.QtCore import QDate
        if self.custom_data["dates"]:
            # 전체 데이터 범위에서 최소/최대 날짜 구하기
            first_date = min(self.custom_data["dates"])
            last_date = max(self.custom_data["dates"])
            # QDateEdit에 설정
            self.startDateEdit.setDate(first_date)
            self.endDateEdit.setDate(last_date)
            self.plot_data_custom()


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
