"""
instruct_pix2pix_pyqt5UI - A PyQt5 GUI for InstructPix2Pix
Copyright (C) 2023 Liu Yuan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

This project is based on InstructPix2Pix, which is licensed under the MIT License.
Original InstructPix2Pix Copyright (c) 2023 Timothy Brooks, Aleksander Holynski, Alexei A. Efros
"""

import sys
import PIL
import torch
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLineEdit, QFileDialog, QSpinBox, QDoubleSpinBox, QGroupBox, 
                             QMessageBox, QGridLayout)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from diffusers import StableDiffusionInstructPix2PixPipeline, EulerAncestralDiscreteScheduler

class ImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('InstructPix2Pix Image Editor')
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()

        # Image selection
        image_layout = QHBoxLayout()
        self.select_button = QPushButton('Select Image')
        self.select_button.clicked.connect(self.select_image)
        image_layout.addWidget(self.select_button)
        self.image_label = QLabel('No image selected')
        self.image_label.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(self.image_label)
        main_layout.addLayout(image_layout)

        # Prompt input
        prompt_layout = QHBoxLayout()
        prompt_layout.addWidget(QLabel('Edit instruction:'))
        self.prompt_entry = QLineEdit()
        prompt_layout.addWidget(self.prompt_entry)
        main_layout.addLayout(prompt_layout)

        # Parameters
        params_group = QGroupBox('Parameters')
        params_layout = QGridLayout()

        # Number of inference steps
        params_layout.addWidget(QLabel('Number of inference steps:'), 0, 0)
        self.steps_spinbox = QSpinBox()
        self.steps_spinbox.setRange(1, 100)
        self.steps_spinbox.setValue(10)
        params_layout.addWidget(self.steps_spinbox, 0, 1)
        params_layout.addWidget(QLabel('Default: 10, Range: 1-100'), 0, 2)
        params_layout.addWidget(QLabel('Higher values may improve quality but increase processing time.'), 1, 0, 1, 3)

        # Image guidance scale
        params_layout.addWidget(QLabel('Image guidance scale:'), 2, 0)
        self.image_guidance_spinbox = QDoubleSpinBox()
        self.image_guidance_spinbox.setRange(0.0, 5.0)
        self.image_guidance_spinbox.setSingleStep(0.1)
        self.image_guidance_spinbox.setValue(1.0)
        params_layout.addWidget(self.image_guidance_spinbox, 2, 1)
        params_layout.addWidget(QLabel('Default: 1.0, Range: 0.0-5.0'), 2, 2)
        params_layout.addWidget(QLabel('Higher values make the result more similar to the input image.'), 3, 0, 1, 3)

        # Guidance scale
        params_layout.addWidget(QLabel('Guidance scale:'), 4, 0)
        self.guidance_spinbox = QDoubleSpinBox()
        self.guidance_spinbox.setRange(0.0, 20.0)
        self.guidance_spinbox.setSingleStep(0.1)
        self.guidance_spinbox.setValue(7.5)
        params_layout.addWidget(self.guidance_spinbox, 4, 1)
        params_layout.addWidget(QLabel('Default: 7.5, Range: 0.0-20.0'), 4, 2)
        params_layout.addWidget(QLabel('Higher values make the image adhere more closely to the text prompt.'), 5, 0, 1, 3)

        params_group.setLayout(params_layout)
        main_layout.addWidget(params_group)

        # Process button
        self.process_button = QPushButton('Edit Image')
        self.process_button.clicked.connect(self.process_image)
        main_layout.addWidget(self.process_button)

        # Result display
        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.result_label)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def select_image(self):
        self.image_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.bmp)")
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)

    def process_image(self):
        if not hasattr(self, 'image_path'):
            QMessageBox.warning(self, "Warning", "Please select an image first.")
            return
        prompt = self.prompt_entry.text()
        if not prompt:
            QMessageBox.warning(self, "Warning", "Please enter an edit instruction.")
            return

        num_inference_steps = self.steps_spinbox.value()
        image_guidance_scale = self.image_guidance_spinbox.value()
        guidance_scale = self.guidance_spinbox.value()

        QMessageBox.information(self, "Processing", "Processing... This may take a while.")
        try:
            edited_image = self.edit_image(self.image_path, prompt, num_inference_steps, image_guidance_scale, guidance_scale)
            q_image = QImage(edited_image.tobytes(), edited_image.width, edited_image.height, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.result_label.setPixmap(pixmap)
            edited_image.save("edited_image.jpg")
            QMessageBox.information(self, "Success", "Image edited successfully and saved as 'edited_image.jpg'")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def edit_image(self, image_path, prompt, num_inference_steps, image_guidance_scale, guidance_scale):
        model_id = "timbrooks/instruct-pix2pix"
        pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(model_id, torch_dtype=torch.float16, safety_checker=None)
        pipe.to("cuda")
        pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)

        image = PIL.Image.open(image_path).convert("RGB")
        images = pipe(prompt, image=image, num_inference_steps=num_inference_steps, 
                      image_guidance_scale=image_guidance_scale, guidance_scale=guidance_scale).images
        return images[0]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageEditor()
    ex.show()
    sys.exit(app.exec_())
