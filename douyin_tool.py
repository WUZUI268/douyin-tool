import sys
import os
import struct
import random
import string
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QSpinBox, QCheckBox, QTextEdit, QHBoxLayout
)

# 定义修改视频元数据的函数
def modify_metadata(file_path, duration):
    # 使用 ffmpeg 修改显示时长、元数据、封面帧等
    # 修改文件的显示时长
    cmd = [
        'ffmpeg', '-i', file_path, '-t', str(duration), '-c', 'copy', 
        '-map', '0', file_path
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# 生成随机字符串用于伪装
def random_string(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# 修改视频的封面帧
def change_cover_image(file_path, cover_image_path):
    cmd = [
        'ffmpeg', '-i', file_path, '-i', cover_image_path, '-map', '0', '-map', '1',
        '-c:v', 'copy', '-c:a', 'copy', '-c:s', 'mov_text', file_path
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# 修改视频文件中的 mdhd 和 mvhd atom
def modify_video_header(file_path, new_duration=10):
    with open(file_path, 'rb') as f:
        data = f.read()

    # 定位到 mdhd 和 mvhd atom，并进行修改（伪装）
    # 假设你已经通过分析结构知道如何修改
    # 下面的内容仅做示例，实际操作时需要根据文件格式和结构分析进行调整

    # 修改时长、mdhd、mvhd等字段
    # 这里只是示范伪装逻辑，具体实现需要用到结构解析与二进制修改
    data = data.replace(b'original_data', b'new_fake_data')

    # 写入伪装后的数据到新文件
    with open(file_path, 'wb') as f:
        f.write(data)

# PyQt5 图形界面设计
class VideoTool(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("抖音视频去重工具")
        self.setGeometry(100, 100, 500, 300)

        self.layout = QVBoxLayout()

        # 视频文件路径
        self.label = QLabel("选择视频文件:")
        self.layout.addWidget(self.label)

        self.file_input = QLineEdit(self)
        self.layout.addWidget(self.file_input)

        self.browse_button = QPushButton("浏览", self)
        self.browse_button.clicked.connect(self.browse_file)
        self.layout.addWidget(self.browse_button)

        # 显示时长
        self.duration_label = QLabel("视频显示时长 (秒):")
        self.layout.addWidget(self.duration_label)

        self.duration_spinbox = QSpinBox(self)
        self.duration_spinbox.setMinimum(1)
        self.duration_spinbox.setMaximum(3600)
        self.layout.addWidget(self.duration_spinbox)

        # 修改封面
        self.cover_label = QLabel("选择封面图:")
        self.layout.addWidget(self.cover_label)

        self.cover_input = QLineEdit(self)
        self.layout.addWidget(self.cover_input)

        self.cover_button = QPushButton("浏览", self)
        self.cover_button.clicked.connect(self.browse_cover)
        self.layout.addWidget(self.cover_button)

        # 开始按钮
        self.start_button = QPushButton("开始修改", self)
        self.start_button.clicked.connect(self.start_processing)
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择视频文件", "", "视频文件 (*.mp4 *.mov *.avi)")
        if file_path:
            self.file_input.setText(file_path)

    def browse_cover(self):
        cover_path, _ = QFileDialog.getOpenFileName(self, "选择封面图", "", "图片文件 (*.jpg *.png *.jpeg)")
        if cover_path:
            self.cover_input.setText(cover_path)

    def start_processing(self):
        file_path = self.file_input.text()
        cover_path = self.cover_input.text()
        duration = self.duration_spinbox.value()

        if not file_path:
            self.show_message("错误", "请选择视频文件")
            return

        # 开始处理
        self.show_message("正在处理", "正在修改视频...")
        modify_metadata(file_path, duration)
        if cover_path:
            change_cover_image(file_path, cover_path)
        modify_video_header(file_path, new_duration=duration)
        self.show_message("完成", "视频修改完成!")

    def show_message(self, title, message):
        text_edit = QTextEdit(self)
        text_edit.setText(f"{title}: {message}")
        self.layout.addWidget(text_edit)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoTool()
    window.show()
    sys.exit(app.exec_())
