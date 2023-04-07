import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QVBoxLayout, \
    QHBoxLayout, QListWidget, QListWidgetItem, QMessageBox, QAbstractItemView, QDialog
from PyQt5.QtGui import QImage, QPixmap
import thecampy

class AddLetterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.title_edit = QLineEdit()
        self.content_edit = QTextEdit()
        self.content_edit.textChanged.connect(self.show_char_count)
        self.file_button = QPushButton('이미지 파일 로드')
        self.file_button.setFixedWidth(200)
        self.file_button.clicked.connect(self.load_image)
        self.add_button = QPushButton('편지 추가하기')
        font = self.add_button.font()
        font.setPointSize(30)
        self.add_button.setFont(font)
        self.add_button.setFixedWidth(self.width())
        self.add_button.setFixedHeight(80)
        self.add_button.clicked.connect(self.dialog_close)
        self.file_label = QLabel()
        self.char_count_label = QLabel('0 characters')

        layout = QVBoxLayout()
        layout.addWidget(QLabel('제목:'))
        layout.addWidget(self.title_edit)
        layout.addWidget(QLabel('내용:'))
        layout.addWidget(self.content_edit)
        layout.addStretch()
        layout.addWidget(self.char_count_label)
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel('사진 추가 (10 MB 제한):'))
        file_layout.addWidget(self.file_label)
        file_layout.addStretch()
        file_layout.addWidget(self.file_button)
        layout.addLayout(file_layout)
        layout.addWidget(self.add_button)
        self.setLayout(layout)
        self.setWindowTitle("편지 작성하기")
        self.setGeometry(400, 400, 600, 400)

        self.image_path=""

    def load_image(self):
        # 이미지 파일 필터 설정
        filters = "Image Files (*.jpg *.jpeg *.png);;"
        # 파일 대화상자 생성
        file_dialog = QFileDialog(self, "이미지 열기", filter=filters)
        file_dialog.setAcceptMode(QFileDialog.AcceptOpen)
        # 파일 대화상자 실행
        if file_dialog.exec_() == QFileDialog.Accepted:
            # 선택된 파일 경로 가져오기
            file_path = file_dialog.selectedFiles()[0]
            # 파일 크기가 10MB 이하인 경우에만 이미지 불러오기
            if os.path.getsize(file_path) <= 10 * 1024 * 1024:
                image = QImage(file_path)
                # 이미지 불러오기가 성공한 경우
                if not image.isNull():
                    pixmap = QPixmap.fromImage(image)
                    self.image_path = file_path
                    self.file_label.setText(file_path.split('/')[-1])
                    return pixmap
                else:
                    QMessageBox.critical(self, "이미지 열기 오류", "이미지를 열지 못했습니다.")
            else:
                QMessageBox.warning(self, "이미지 열기 경고", "이미지 크기가 10MB를 초과합니다.")

    def dialog_close(self):
        self.accept()

    def show_char_count(self):
        content = self.content_edit.toPlainText()
        char_count = len(content)
        self.char_count_label.setText(f'{char_count} characters')

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # UI 요소 생성
        self.name_label = QLabel("훈련병 이름:", self)
        self.name_edit = QLineEdit(self)
        self.name_edit.setFixedWidth(250)

        self.id_label = QLabel("더캠프 ID:", self)
        self.id_edit = QLineEdit(self)
        self.id_edit.setFixedWidth(250)

        self.pw_label = QLabel("더캠프 PW:", self)
        self.pw_edit = QLineEdit(self)
        self.pw_edit.setFixedWidth(250)
        self.pw_edit.setEchoMode(QLineEdit.Password)

        self.load_btn = QPushButton("txt 불러오기", self)
        self.load_btn.setFixedWidth(180)
        self.load_btn.clicked.connect(self.load_txt)

        self.add_btn = QPushButton("편지 추가", self)
        self.add_btn.setFixedWidth(180)
        self.add_btn.clicked.connect(self.add_letter)

        self.send_btn = QPushButton("전송", self)
        self.send_btn.clicked.connect(self.send_email)

        self.title_label = QLabel("제목:", self)
        self.title_edit = QListWidget(self)
        self.title_edit.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 다중 항목 선택 모드로 설정
        self.title_edit.itemClicked.connect(self.show_content)

        self.msg_label = QLabel("내용:", self)
        self.msg_edit = QTextEdit(self)
        self.msg_edit.textChanged.connect(self.update_msg_list)

        # 전체 레이아웃 생성
        vbox = QVBoxLayout()

        # 첫 번째 행
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.name_label)
        hbox1.addWidget(self.name_edit)
        vbox.addLayout(hbox1)

        # 두 번째 행
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.id_label)
        hbox2.addWidget(self.id_edit)
        vbox.addLayout(hbox2)

        # 세 번째 행
        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.pw_label)
        hbox3.addWidget(self.pw_edit)
        vbox.addLayout(hbox3)

        # 네 번째 행
        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.load_btn)
        hbox4.addWidget(self.add_btn)
        vbox.addLayout(hbox4)

        # 다섯 번째 행
        vbox.addWidget(self.title_label)
        vbox.addWidget(self.title_edit)

        # 여섯 번째 행
        vbox.addWidget(self.msg_label)
        vbox.addWidget(self.msg_edit)

        vbox.addStretch()
        vbox.addWidget(self.send_btn)

        self.setLayout(vbox)
        self.setWindowTitle("더캠프 위문편지 보내기 Ver1.0.0")
        self.setGeometry(300, 300, 400, 500)

        self.show()

        self.title_list = []
        self.msg_list = []
        self.img_list = []
        self.change_context_flag = False

    def load_txt(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text files (*.txt)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()

                    msg_list = [text[i:i + 1500] for i in range(0, len(text), 1500)]
                    for i, msg in enumerate(msg_list):
                        title = f"{os.path.basename(file_path)}_{i + 1}"
                        item = QListWidgetItem(title)
                        #item.path = temp_path
                        self.msg_list.append(msg)
                        self.title_list.append(title)
                        self.img_list.append("")
                        self.title_edit.addItem(item)
            except Exception as e:
                QMessageBox.warning(self, "Warning", "utf-8 형식의 txt 파일만 불러올 수 있습니다. ")
                return


    def load_image(self):
        return

    def show_content(self):
        text = self.msg_list[self.title_edit.currentRow()]
        self.change_context_flag = True
        self.msg_edit.setText(text)

    def update_msg_list(self):
        if self.change_context_flag == True:
            self.change_context_flag = False
            return

        if self.title_edit.count() == 0 and self.msg_edit.toPlainText() != "":
            QMessageBox.warning(self, "Warning", "텍스트 파일이나 편지를 추가해주세요.")
            self.msg_edit.clear()
            return

        text = self.msg_edit.toPlainText()

        if len(text) > 1500:
            QMessageBox.warning(self, "Warning", "1500자를 초과하는 메시지는 전송할 수 없습니다.")
            self.show_content()
            return

        for i in range(self.title_edit.count()):
            item = self.title_edit.item(i)
            if item is not None and item.isSelected():
                index = i + 1
                self.msg_list[index - 1] = text
                break


    def add_letter(self):
        dialog = AddLetterDialog()
        if dialog.exec_() == QDialog.Accepted:
            title = dialog.title_edit.text()
            content = dialog.content_edit.toPlainText()
            image_path = dialog.image_path

            if title == "" or content == "":
                return

            # content가 1500자 이상이면 분리해서 저장
            contents = [content[i:i + 1500] for i in range(0, len(content), 1500)]
            titles = [f"{title}_{i+1}" for i in range(len(contents))] if contents else ['']

            # 받아온 정보로 제목, 내용, 파일 경로를 리스트에 추가하는 코드 작성

            self.title_list.extend(titles)
            self.msg_list.extend(contents)
            for i in range(0,len(contents)):
                if i == 0:
                    self.img_list.append(image_path)
                else:
                    self.img_list.append("")

            self.title_edit.clear()
            for item in self.title_list:
                self.title_edit.addItem(item)

    def send_email(self):
        name = self.name_edit.text()
        id = self.id_edit.text()
        pw = self.pw_edit.text()

        if name=="" or id=="" or pw=="" :
            QMessageBox.information(self, "전송 실패", "이름, ID, PW를 모두 입력해주세요.")
            return

        my_soldier = thecampy.Soldier(name)
        tc = thecampy.Client(id, pw)

        if tc.cookie.iuid == "":
            QMessageBox.information(self, "전송 실패", "훈련병 카페 로그인 실패")
            return


        tc.get_soldier(my_soldier) # returns soldier_code

        #for i,title in enumerate(self.title_list):
        #    msg = thecampy.Message(title, self.msg_list[i])
        #    tc.send_message(my_soldier, msg)
        selected_items = self.title_edit.selectedIndexes()
        selected_indexes = [index.row() for index in selected_items]
        selected_indexes.sort()

        for i in selected_indexes:
            title = self.title_list[i]
            text = self.msg_list[i]
            img = self.img_list[i]
            msg = thecampy.Message(title, text)
            #print(msg.title, msg.content)

            if img == "":
                try:
                    tc.send_message(my_soldier, msg)
                except Exception as e:
                    QMessageBox.information(self, "전송 실패", "메시지 전송에 실패하였습니다.")
            else:
                try:
                    tc.send_message(my_soldier, msg, img)
                except Exception as e:
                    QMessageBox.information(self, "전송 실패", "이미지를 제외하고 전송합니다.")
                    tc.send_message(my_soldier, msg)


        QMessageBox.information(self, "전송 성공", "메시지 전송에 성공하였습니다. ")
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())

