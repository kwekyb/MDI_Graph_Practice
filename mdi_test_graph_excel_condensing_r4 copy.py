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

        toolbar = self.addToolBar('도구')  # 툴바 생성
        toolbar.setMovable(False)  # 툴바 위치 고정

        # 새 창 열기 액션 생성 및 툴바에 추가
        newAction1 = QAction('새 창 1', self)  # 새 창 1을 여는 액션 생성
        newAction1.setShortcut('Ctrl+1')  # 단축키 설정
        newAction1.triggered.connect(self.createWindow1)  # 클릭 시 새 창 1 생성 함수 호출
        toolbar.addAction(newAction1)  # 툴바에 추가

        newAction2 = QAction('새 창 2', self)  # 새 창 2를 여는 액션 생성
        newAction2.setShortcut('Ctrl+2')  # 단축키 설정
        newAction2.triggered.connect(self.createWindow2)  # 클릭 시 새 창 2 생성 함수 호출
        toolbar.addAction(newAction2)  # 툴바에 추가

        newAction3 = QAction('새 창 3', self)  # 새 창 3을 여는 액션 생성
        newAction3.setShortcut('Ctrl+3')  # 단축키 설정
        newAction3.triggered.connect(self.createWindow3)  # 클릭 시 새 창 3 생성 함수 호출
        toolbar.addAction(newAction3)  # 툴바에 추가

        toolbar.addSeparator()  # 툴바 구분선 추가

        # 창 배열 액션 생성 및 추가
        tileAction = QAction('바둑판 배열', self)  # 바둑판 배열 액션 생성
        tileAction.triggered.connect(self.mdi.tileSubWindows)  # 클릭 시 서브윈도우 바둑판 배열
        toolbar.addAction(tileAction)  # 툴바에 추가

        cascadeAction = QAction('계단식 배열', self)  # 계단식 배열 액션 생성
        cascadeAction.triggered.connect(self.mdi.cascadeSubWindows)  # 클릭 시 서브윈도우 계단식 배열
        toolbar.addAction(cascadeAction)  # 툴바에 추가

        self.setWindowTitle('MDI 애플리케이션')  # 메인 윈도우 제목 설정
        self.setGeometry(100, 100, 800, 600)  # 윈도우 위치 및 크기 설정

    def createWindow1(self):  # 새 창 1을 생성하는 함수
        sub = QMdiSubWindow()  # MDI 서브윈도우 생성
        widget = QWidget()  # QWidget 생성
        widget.setMinimumSize(300, 200)  # 최소 크기 설정
        layout = QVBoxLayout()  # 수직 레이아웃 설정
        widget.setLayout(layout)  # 위젯에 레이아웃 설정

        label = QLabel('창 1 - 입력하세요:')  # 라벨 생성
        layout.addWidget(label)  # 레이아웃에 추가
        textbox = QLineEdit()  # 입력창 생성
        layout.addWidget(textbox)  # 레이아웃에 추가
        widget.textbox = textbox  # 텍스트박스를 위젯 속성으로 저장

        button = QPushButton('확인')  # 확인 버튼 생성
        button.clicked.connect(lambda: self.addTextToMemo(textbox.text(), memo))  # 버튼 클릭 시 메모에 추가
        layout.addWidget(button)  # 레이아웃에 추가

        memoLabel = QLabel('메모:')  # 메모 라벨 생성
        layout.addWidget(memoLabel)  # 레이아웃에 추가
        memo = QTextEdit()  # 텍스트 입력 가능한 메모장 생성
        memo.setMinimumHeight(100)  # 최소 높이 설정
        layout.addWidget(memo)  # 레이아웃에 추가
        widget.memo = memo  # 메모장을 위젯 속성으로 저장

        sub.setWidget(widget)  # 서브윈도우에 위젯 추가
        sub.setWindowTitle('새 창 1')  # 서브윈도우 제목 설정
        self.mdi.addSubWindow(sub)  # MDI에 서브윈도우 추가
        sub.resize(400, 400)  # 서브윈도우 크기 설정
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
