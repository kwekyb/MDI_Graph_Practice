import sys  # 시스템 관련 기능을 사용하기 위한 모듈
import requests  # HTTP 요청을 보내기 위한 모듈
import pandas as pd  # 데이터 분석 및 처리에 사용되는 라이브러리
import matplotlib.pyplot as plt  # 데이터 시각화를 위한 라이브러리
from PyQt5.QtWidgets import *  # PyQt5의 위젯 모듈 전체를 가져옴
from PyQt5 import QtWidgets, QtCore, QtGui  # PyQt5의 핵심 모듈 가져오기
from PyQt5.QtCore import *  # PyQt5의 코어 기능을 가져옴
from PyQt5.QtGui import *  # PyQt5의 GUI 기능을 가져옴
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  # PyQt5에서 Matplotlib 그래프를 표시하기 위한 모듈

class MainWindow(QMainWindow):  # 메인 윈도우 클래스를 정의 (QMainWindow를 상속)
    def __init__(self):  # 생성자 함수
        super().__init__()  # 부모 클래스(QMainWindow)의 생성자를 호출
        self.window1 = None  # 첫 번째 서브윈도우의 참조를 저장할 변수 (초기값은 None)
        self.initUI()  # UI 초기화 함수 호출

    def initUI(self):  # UI 설정을 위한 함수
        self.mdi = QMdiArea()  # MDI(Multiple Document Interface) 영역 생성
        self.mdi.setViewMode(QMdiArea.SubWindowView)  # 서브윈도우 뷰 모드 설정
        self.mdi.setOption(QMdiArea.DontMaximizeSubWindowOnActivation)  # 서브윈도우 활성화 시 자동 최대화 방지
        self.setCentralWidget(self.mdi)  # MDI 영역을 메인 윈도우의 중앙 위젯으로 설정

        menubar = self.menuBar()  # 메뉴바 생성
        menu = menubar.addMenu('메뉴')  # "메뉴" 항목 추가
        
        menuAction1 = QAction('창 1', self)  # "창 1" 서브메뉴 생성
        menuAction1.triggered.connect(self.createWindow1)  # 클릭 시 새 창 1 생성 함수 호출
        menu.addAction(menuAction1)  # 메뉴에 추가
        
        menuAction2 = QAction('창 2', self)  # "창 2" 서브메뉴 생성
        menuAction2.triggered.connect(self.createWindow2)  # 클릭 시 새 창 2 생성 함수 호출
        menu.addAction(menuAction2)  # 메뉴에 추가
        
        menuAction3 = QAction('창 3', self)  # "창 3" 서브메뉴 생성
        menuAction3.triggered.connect(self.createWindow3)  # 클릭 시 새 창 3 생성 함수 호출
        menu.addAction(menuAction3)  # 메뉴에 추가

        menuAction3 = QAction('닫기', self)  # "닫기" 서브메뉴 생성
        menuAction3.triggered.connect(self.close)  # 클릭 시 전체프로그램 닫기 호출
        menu.addAction(menuAction3)  # 메뉴에 추가
        
        viewMenu = menubar.addMenu('보기')  # "보기" 메뉴 추가
        
        tileAction = QAction('바둑판 배열', self)  # 바둑판 배열 액션 생성
        tileAction.triggered.connect(self.mdi.tileSubWindows)  # 클릭 시 서브윈도우 바둑판 배열
        viewMenu.addAction(tileAction)  # 보기 메뉴에 추가
        
        cascadeAction = QAction('계단식 배열', self)  # 계단식 배열 액션 생성
        cascadeAction.triggered.connect(self.mdi.cascadeSubWindows)  # 클릭 시 서브윈도우 계단식 배열
        viewMenu.addAction(cascadeAction)  # 보기 메뉴에 추가
        
        self.setWindowTitle('MDI 애플리케이션')  # 메인 윈도우 제목 설정
        self.setGeometry(100, 100, 800, 600)  # 윈도우 위치 및 크기 설정

    def createWindow1(self):  # 새 창 1을 생성하는 함수
        sub = QMdiSubWindow()  # MDI 서브윈도우 생성
        widget = QWidget()  # QWidget 생성
        widget.setMinimumSize(400, 300)  # 최소 크기 설정
        layout = QGridLayout()  # 그리드 레이아웃 설정
        widget.setLayout(layout)  # 위젯에 레이아웃 설정

        label = QLabel('이름:')  # 라벨 생성
        layout.addWidget(label, 0, 0)  # 그리드 위치 설정 (행, 열)

        textbox = QLineEdit()  # 입력창 생성
        textbox.setFixedWidth(100)  # 입력창 가로 크기 조정
        layout.addWidget(textbox, 0, 1, 1, 1)  # 입력창을 넓게 배치

        memoLabel = QLabel('메모:')  # 메모 라벨 생성
        layout.addWidget(memoLabel, 1, 0)
        memo = QTextEdit()  # 텍스트 입력 가능한 메모장 생성
        memo.setFixedWidth(250)  # 메모 입력창 가로 크기 조정
        layout.addWidget(memo, 1, 1, 1, 2)  # 넓은 칸 배치

        comboLabel = QLabel('선택:')  # 콤보박스 라벨 생성
        layout.addWidget(comboLabel, 2, 0)
        combo = QComboBox()  # 콤보박스 생성
        combo.addItems(['옵션 1', '옵션 2', '옵션 3'])  # 옵션 추가
        combo.setFixedWidth(150)  # 콤보박스 가로 크기 조정
        layout.addWidget(combo, 2, 1, 1, 2)

        radio1 = QRadioButton('옵션 A')  # 옵션 단추 생성
        radio2 = QRadioButton('옵션 B')
        layout.addWidget(radio1, 3, 1)
        layout.addWidget(radio2, 3, 2)

        button = QPushButton('확인')  # 버튼 생성
        button.setFixedWidth(100)  # 버튼 가로 크기 조정
        layout.addWidget(button, 4, 1, 1, 2)  # 버튼을 넓게 배치

        sub.setWidget(widget)  # 서브윈도우에 위젯 추가
        sub.setWindowTitle('새 창 1')  # 서브윈도우 제목 설정
        self.mdi.addSubWindow(sub)  # MDI에 서브윈도우 추가
        sub.resize(400, 300)  # 서브윈도우 크기 설정
        sub.show()  # 서브윈도우 표시
        self.window1 = widget  # 첫 번째 창의 참조 저장
        textbox.setFocus()  # 텍스트박스에 포커스 설정
    
    def createWindow2(self):  # 새 창 2를 생성하는 함수
        sub = QMdiSubWindow()  # MDI 서브윈도우 생성
        widget = QWidget()  # QWidget 생성
        widget.setMinimumSize(300, 200)  # 최소 크기 설정
        layout = QVBoxLayout()  # 수직 레이아웃 설정
        widget.setLayout(layout)  # 위젯에 레이아웃 설정
    
        label = QLabel('창 2 - 내용')  # 라벨 생성
        layout.addWidget(label)  # 레이아웃에 추가
    
        sub.setWidget(widget)  # 서브윈도우에 위젯 추가
        sub.setWindowTitle('새 창 2')  # 서브윈도우 제목 설정
        self.mdi.addSubWindow(sub)  # MDI에 서브윈도우 추가
        sub.show()  # 서브윈도우 표시

    def createWindow3(self):  # 새 창 3을 생성하는 함수
        sub = QMdiSubWindow()  # MDI 서브윈도우 생성
        widget = QWidget()  # QWidget 생성
        widget.setMinimumSize(300, 200)  # 최소 크기 설정
        layout = QVBoxLayout()  # 수직 레이아웃 설정
        widget.setLayout(layout)  # 위젯에 레이아웃 설정
    
        label = QLabel('창 3 - 내용')  # 라벨 생성
        layout.addWidget(label)  # 레이아웃에 추가
    
        sub.setWidget(widget)  # 서브윈도우에 위젯 추가
        sub.setWindowTitle('새 창 3')  # 서브윈도우 제목 설정
        self.mdi.addSubWindow(sub)  # MDI에 서브윈도우 추가
        sub.show()  # 서브윈도우 표시

if __name__ == '__main__':  # 프로그램 실행 시
    app = QApplication(sys.argv)  # PyQt5 애플리케이션 객체 생성
    ex = MainWindow()  # MainWindow 인스턴스 생성
    ex.show()  # 메인 윈도우 표시
    sys.exit(app.exec_())  # 애플리케이션 실행