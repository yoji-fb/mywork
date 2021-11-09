"""
2021/11/08 Last modified
"""
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import sys

from Image_processing_functions import *


class MainWindow(qtw.QWidget):
    # Store settings
    settings = qtc.QSettings('my_python', 'Image_processing_GUI')
    print('settings file directory: ', settings.fileName())
    # Clear settings
    # settings.clear()

    # SETTINGS #
    path = settings.value('path')
    dpi = settings.value('dpi')
    format = settings.value('format')
    filename0 = settings.value('filename0')
    filename1 = settings.value('filename1')
    grayscale = settings.value('grayscale')
    page_off = settings.value('page_off')
    page_length = settings.value('page_length')
    separation = settings.value('separation')
    direct_exe0 = settings.value('direct_exe0')
    b0, g0, r0 = settings.value('b0'), settings.value('g0'), settings.value('r0')
    direct_exe1 = settings.value('direct_exe1')
    b1, g1, r1 = settings.value('b1'), settings.value('g1'), settings.value('r1')
    regional_exe0 = settings.value('regional_exe0')
    b0_from, g0_from, r0_from = settings.value('b0_from'), settings.value('g0_from'), settings.value('r0_from')
    b0_to, g0_to, r0_to = settings.value('b0_to'), settings.value('g0_to'), settings.value('r0_to')
    regional_exe1 = settings.value('regional_exe1')
    b1_from, g1_from, r1_from = settings.value('b1_from'), settings.value('g1_from'), settings.value('r1_from')
    b1_to, g1_to, r1_to = settings.value('b1_to'), settings.value('g1_to'), settings.value('r1_to')
    direct_dic, from_dir, to_dic = {}, {}, {}

    def __init__(self):
        """MainWindow constructor"""
        super().__init__()

        # Configure the window -------------------------------------------------------
        self.setWindowTitle('IMAGE PROCESSING APP')
        self.resize(800, 600)

        # Create widgets -------------------------------------------------------------
        # ---- #
        # tab0 #
        self.path_ent = qtw.QLineEdit(self.path, self, maxLength=99, placeholderText='Enter file path...')
        self.dpi_spn = qtw.QSpinBox(self, value=self.dpi, maximum=300, minimum=100, singleStep=50)
        self.filename0_ent = qtw.QLineEdit(self.filename0, self, placeholderText='Enter filename...')
        self.filename1_ent = qtw.QLineEdit(self.filename1, self, placeholderText='Enter filename...')
        self.format_ent = qtw.QComboBox(self)
        self.grayscale_chk = qtw.QCheckBox('grayscale', self)
        self.page_off_chk = qtw.QCheckBox('page_off', self)
        self.page_length_spn = qtw.QSpinBox(self, value=self.page_length)
        self.separation_spn = qtw.QSpinBox(self, value=self.separation)
        self.pdf2image_btn = qtw.QPushButton(
            'pdf2image',
            clicked=self.pdf2image_exe
        )
        self.pdf2image_dir_btn = qtw.QPushButton(
            'pdf2image_dir',
            clicked=self.pdf2image_dir_exe
        )
        self.add_image_tif_btn = qtw.QPushButton(
            'add_image_tif',
            clicked=self.add_image_tif_exe
        )
        # ---- #
        # tab1 #
        self.image2image_btn = qtw.QPushButton(
            'image2image',
            clicked=self.image2image_exe
        )
        self.input = qtw.QComboBox(self)
        self.output = qtw.QComboBox(self)
        self.direct_exe0_chk = qtw.QCheckBox('Execute', self)
        self.b0_spn = qtw.QSpinBox(self, value=self.b0, minimum=0, maximum=255)
        self.g0_spn = qtw.QSpinBox(self, value=self.g0, minimum=0, maximum=255)
        self.r0_spn = qtw.QSpinBox(self, value=self.r0, minimum=0, maximum=255)
        self.direct_exe1_chk = qtw.QCheckBox('Execute', self)
        self.b1_spn = qtw.QSpinBox(self, value=self.b1, minimum=0, maximum=255)
        self.g1_spn = qtw.QSpinBox(self, value=self.g1, minimum=0, maximum=255)
        self.r1_spn = qtw.QSpinBox(self, value=self.r1, minimum=0, maximum=255)
        self.regional_exe0_chk = qtw.QCheckBox('Execute', self)
        self.b0_from_spn = qtw.QSpinBox(self, value=self.b0_from, minimum=0, maximum=255)
        self.g0_from_spn = qtw.QSpinBox(self, value=self.g0_from, minimum=0, maximum=255)
        self.r0_from_spn = qtw.QSpinBox(self, value=self.r0_from, minimum=0, maximum=255)
        self.b0_to_spn = qtw.QSpinBox(self, value=self.b0_to, minimum=0, maximum=255)
        self.g0_to_spn = qtw.QSpinBox(self, value=self.g0_to, minimum=0, maximum=255)
        self.r0_to_spn = qtw.QSpinBox(self, value=self.r0_to, minimum=0, maximum=255)
        self.regional_exe1_chk = qtw.QCheckBox('Execute', self)
        self.b1_from_spn = qtw.QSpinBox(self, value=self.b1_from, minimum=0, maximum=255)
        self.g1_from_spn = qtw.QSpinBox(self, value=self.g1_from, minimum=0, maximum=255)
        self.r1_from_spn = qtw.QSpinBox(self, value=self.r1_from, minimum=0, maximum=255)
        self.b1_to_spn = qtw.QSpinBox(self, value=self.b1_to, minimum=0, maximum=255)
        self.g1_to_spn = qtw.QSpinBox(self, value=self.g1_to, minimum=0, maximum=255)
        self.r1_to_spn = qtw.QSpinBox(self, value=self.r1_to, minimum=0, maximum=255)

        # Configure widgets -------------------------------------------------------------
        # ---- #
        # tab0 #
        # Add event categories
        self.format_ent.addItems(['.tif', '.jpg', '.png', '.bmp'])
        # ---- #
        # tab1 #
        self.input.addItems(['.tif', '.jpg', '.png', '.bmp'])
        self.output.addItems(['.tif', '.jpg', '.png', '.bmp'])

        # Arrange the widgets -----------------------------------------------------------
        # Create main_layout
        main_layout = qtw.QHBoxLayout()
        self.setLayout(main_layout)

        self.tabs = qtw.QTabWidget()
        self.tab0 = qtw.QWidget()
        self.tab1 = qtw.QWidget()

        self.tabs.addTab(self.tab0, 'pdf2image')
        self.tabs.addTab(self.tab1, 'image2image')

        # Tab layout ---------------------------------------------------------------------
        # ---- #
        # tab0 #
        self.tab0.layout = qtw.QVBoxLayout()
        self.tab0.layout.addWidget(qtw.QLabel('Image_processing_functions.py\n'
                                              'Image_processing_GUI.py'))
        # Execute box #
        execute_form = qtw.QGroupBox('Execute')
        self.tab0.layout.addWidget(execute_form)
        # execute_form_layout
        execute_form_layout = qtw.QGridLayout()
        execute_form_layout.addWidget(qtw.QLabel('# execute_form', self), 1, 1, 1, 10)
        execute_form_layout.addWidget(self.pdf2image_btn, 2, 1, 1, 1)
        execute_form_layout.addWidget(qtw.QLabel(
            '<b># pdf2image()</b> :pdf -> image (jpg/png/tif)', self), 2, 2, 1, 1)
        execute_form_layout.addWidget(self.pdf2image_dir_btn, 3, 1, 1, 1)
        execute_form_layout.addWidget(qtw.QLabel(
            '<b># pdf2image_dir()</b> :Convert all pdf files to images in the path.', self), 3, 2, 1, 1)
        execute_form_layout.addWidget(self.add_image_tif_btn, 4, 1, 1, 1)
        execute_form_layout.addWidget(qtw.QLabel(
            '<b># add_image_tif()</b> :Add filename1 on filename0 (tif -> tif).', self), 4, 2, 1, 1)
        # Set GridLayout to execute_form_layout
        execute_form.setLayout(execute_form_layout)
        # Settings box #
        settings_form = qtw.QGroupBox('Settings')
        self.tab0.layout.addWidget(settings_form)
        # settings_form_layout
        settings_form_layout = qtw.QGridLayout()
        settings_form_layout.addWidget(qtw.QLabel('# settings_form', self), 1, 1, 1, 10)
        settings_form_layout.addWidget(self.path_ent, 2, 1, 1, 9)  # (row, column, row span, column span)
        settings_form_layout.addWidget(qtw.QLabel('<b># path</b>', self), 2, 10, 1, 1)
        settings_form_layout.addWidget(self.dpi_spn, 3, 1, 1, 1)
        settings_form_layout.addWidget(qtw.QLabel('<b># dpi</b>', self), 3, 2, 1, 1)
        settings_form_layout.addWidget(self.format_ent, 3, 3, 1, 1)
        settings_form_layout.addWidget(qtw.QLabel('<b># format</b>', self), 3, 4, 1, 1)
        settings_form_layout.addWidget(self.filename0_ent, 4, 1, 1, 3)
        settings_form_layout.addWidget(qtw.QLabel('<b># filename0</b>', self), 4, 4, 1, 1)
        settings_form_layout.addWidget(self.filename1_ent, 4, 5, 1, 3)
        settings_form_layout.addWidget(qtw.QLabel('<b># filename1</b>', self), 4, 8, 1, 1)
        # Set GridLayout to settings_form_layout
        settings_form.setLayout(settings_form_layout)
        # Optional box #
        optional_form = qtw.QGroupBox('Optional')
        self.tab0.layout.addWidget(optional_form)

        # optional_form_layout
        optional_form_layout = qtw.QGridLayout()
        optional_form_layout.addWidget(qtw.QLabel('# optional_form', self), 1, 1, 1, 10)
        optional_form_layout.addWidget(self.grayscale_chk, 2, 1, 1, 1)
        optional_form_layout.addWidget(self.page_off_chk, 2, 2, 1, 1)
        optional_form_layout.addWidget(self.page_length_spn, 3, 2, 1, 1)
        optional_form_layout.addWidget(qtw.QLabel('<b># page_length</b>', self), 3, 3, 1, 1)
        optional_form_layout.addWidget(self.separation_spn, 3, 4, 1, 1)
        optional_form_layout.addWidget(qtw.QLabel('<b># separation</b>', self), 3, 5, 1, 1)
        # Set GridLayout to optional_form_layout
        optional_form.setLayout(optional_form_layout)

        # Set tab0.layout to tab0
        self.tab0.setLayout(self.tab0.layout)
        # ---- #
        # tab1 #
        self.tab1.layout = qtw.QVBoxLayout()
        self.tab1.layout.addWidget(qtw.QLabel('Image_processing_functions.py\n'
                                              'Image_processing_GUI.py'))
        # Set tab1.layout
        self.tab1.setLayout(self.tab1.layout)

        # image2image_layout
        image2image_layout = qtw.QGridLayout()
        # qtw.addWidget(self, row, column, row span, column span)
        image2image_layout.addWidget(self.image2image_btn, 1, 1, 1, 1)
        image2image_layout.addWidget(qtw.QLabel('# Convert all the image in the directory to arbitrary format'),
                                     1, 2, 1, 9)
        image2image_layout.addWidget(qtw.QLabel('from', self, margin=40), 2, 1, 1, 1)
        image2image_layout.addWidget(self.input, 2, 2, 1, 1)
        image2image_layout.addWidget(qtw.QLabel('to', self, margin=42), 2, 3, 1, 1)
        image2image_layout.addWidget(self.output, 2, 4, 1, 1)
        # Set image2image_layout to tab1.layout
        self.tab1.layout.addLayout(image2image_layout)

        # direct_form
        direct_form = qtw.QGroupBox('Direct Exclusion')
        self.tab1.layout.addWidget(direct_form)
        # direct_form_layout
        direct_form_layout = qtw.QGridLayout()
        # qtw.addWidget(self, row, column, row span, column span)
        direct_form_layout.addWidget(self.direct_exe0_chk, 1, 1, 1, 1)
        direct_form_layout.addWidget(self.b0_spn, 1, 2, 1, 1)
        direct_form_layout.addWidget(qtw.QLabel('B', self), 1, 3, 1, 1)
        direct_form_layout.addWidget(self.g0_spn, 1, 4, 1, 1)
        direct_form_layout.addWidget(qtw.QLabel('G', self), 1, 5, 1, 1)
        direct_form_layout.addWidget(self.r0_spn, 1, 6, 1, 1)
        direct_form_layout.addWidget(qtw.QLabel('R', self), 1, 7, 1, 1)
        direct_form_layout.addWidget(self.direct_exe1_chk, 2, 1, 1, 1)
        direct_form_layout.addWidget(self.b1_spn, 2, 2, 1, 1)
        direct_form_layout.addWidget(qtw.QLabel('B', self), 2, 3, 1, 1)
        direct_form_layout.addWidget(self.g1_spn, 2, 4, 1, 1)
        direct_form_layout.addWidget(qtw.QLabel('G', self), 2, 5, 1, 1)
        direct_form_layout.addWidget(self.r1_spn, 2, 6, 1, 1)
        direct_form_layout.addWidget(qtw.QLabel('R', self), 2, 7, 1, 1)
        # Set direct_form_layout to direct_form
        direct_form.setLayout(direct_form_layout)

        # Connect Events --------------------------------------------------------------
        # ---- #
        # tab0 #
        # grayscale_chk -> True
        self.grayscale_chk.setChecked(True)
        # page_off_chk -> True
        self.page_off_chk.setChecked(True)
        self.page_off_chk.toggled.connect(self.page_length_spn.setDisabled)
        self.page_off_chk.toggled.connect(self.separation_spn.setDisabled)
        # page_length_spn -> False
        self.page_length_spn.setDisabled(True)
        # separation_spn -> False
        self.separation_spn.setDisabled(True)
        # ---- #
        # tab1 #


        # Loaded settings info ---------------------------------------------------------
        print('* Loaded info *')
        print("cwd is", self.settings.value('path'))
        print('filename0 is', self.settings.value('filename0'))
        print('filename1 is', self.settings.value('filename1'))
        print('grayscale is', self.settings.value('grayscale'))
        print('page_off is', self.settings.value('page_off'))

        # Set tabs to main_layout ------------------------------------------------------
        main_layout.addWidget(self.tabs)
        # End main UI code -------------------------------------------------------------
        self.show()

    # Functions -------------------------------------------------------------------------
    def pdf2image_exe(self):
        # LOG #
        print('path:', self.path_ent.text())
        print('dpi:', self.dpi_spn.text())
        print('filename:', self.filename0_ent.text())
        print('format:', self.format_ent.currentText())
        print('page_off:', self.page_off_chk.isChecked())
        print('page_length:', self.page_length_spn.text())
        print('separation:', self.separation_spn.text())
        print('grayscale:', self.grayscale_chk.isChecked())

        pdf2image(
            path=self.path_ent.text(),
            dpi=self.dpi_spn.text(),
            filename=self.filename0_ent.text(),
            format=self.format_ent.currentText(),
            page_off=self.page_off_chk.isChecked(),
            page_length=self.page_length_spn.text(),
            separation=self.separation_spn.text(),
            grayscale=self.grayscale_chk.isChecked()
        )

    def pdf2image_dir_exe(self):
        # LOG #
        print('path:', self.path_ent.text())
        print('dpi:', self.dpi_spn.text())
        print('format:', self.format_ent.currentText())
        print('page_off:', self.page_off_chk.isChecked())
        print('grayscale:', self.grayscale_chk.isChecked())

        pdf2image_dir(
            path=self.path_ent.text(),
            dpi=self.dpi_spn.text(),
            format=self.format_ent.currentText(),
            page_off=self.page_off_chk.isChecked(),
            grayscale=self.grayscale_chk.isChecked()
        )

    def add_image_tif_exe(self):
        # LOG #
        print('path:', self.path_ent.text())
        print('filename0', self.filename0_ent.text())
        print('filename1', self.filename1_ent.text())
        print('grayscale:', self.grayscale_chk.isChecked())

        add_image_tif(
            path=self.path_ent.text(),
            filename0=self.filename0_ent.text(),
            filename1=self.filename1_ent.text(),
            grayscale=self.grayscale_chk.isChecked()
        )

    def image2image_exe(self):
        if self.direct_exe0_chk:
            self.direct_dic['b0'] = self.b0_spn.value()
            self.direct_dic['g0'] = self.g0_spn.value()
            self.direct_dic['r0'] = self.r0_spn.value()
        if self.direct_exe1_chk:
            self.direct_dic['b1'] = self.b1_spn.value()
            self.direct_dic['g1'] = self.g1_spn.value()
            self.direct_dic['r1'] = self.r1_spn.value()
        print('direct_dic: ', self.direct_dic)
        # if self.regional_exe0_chk:


    def closeEvent(self, e):
        self.saveSettings()

    # Save settings info
    def saveSettings(self):
        # settings = qtc.QSettings('my_python', 'Image_processing_GUI')
        # (tab0)
        self.settings.setValue('path', self.path_ent.text())
        self.settings.setValue('dpi', self.dpi_spn.text())
        self.settings.setValue('format', self.format_ent.currentText())
        self.settings.setValue('filename0', self.filename0_ent.text())
        self.settings.setValue('filename1', self.filename1_ent.text())
        self.settings.setValue('grayscale', self.grayscale_chk.isChecked())
        self.settings.setValue('page_off', self.page_off_chk.isChecked())
        self.settings.setValue('page_length', self.page_length_spn.text())
        self.settings.setValue('separation', self.separation_spn.text())
        # (tab1)
        self.settings.setValue('direct_exe0', self.direct_exe0_chk.isChecked())
        self.settings.setValue('b0', self.b0_spn.text())
        self.settings.setValue('g0', self.g0_spn.text())
        self.settings.setValue('r0', self.r0_spn.text())
        self.settings.setValue('direct_exe1', self.direct_exe1_chk.isChecked())
        self.settings.setValue('b1', self.b1_spn.text())
        self.settings.setValue('g1', self.g1_spn.text())
        self.settings.setValue('r1', self.r1_spn.text())
        self.settings.setValue('regional_exe0', self.regional_exe0_chk.isChecked())
        self.settings.setValue('b0_from', self.b0_from_spn.text())
        self.settings.setValue('g0_from', self.g0_from_spn.text())
        self.settings.setValue('r0_from', self.r0_from_spn.text())
        self.settings.setValue('b0_to', self.b0_to_spn.text())
        self.settings.setValue('g0_to', self.g0_to_spn.text())
        self.settings.setValue('r0_to', self.r0_to_spn.text())
        self.settings.setValue('regional_exe1', self.regional_exe1_chk.isChecked())
        self.settings.setValue('b1_from', self.b1_from_spn.text())
        self.settings.setValue('g1_from', self.g1_from_spn.text())
        self.settings.setValue('r1_from', self.r1_from_spn.text())
        self.settings.setValue('b1_to', self.b1_to_spn.text())
        self.settings.setValue('g1_to', self.g1_to_spn.text())
        self.settings.setValue('r1_to', self.r1_to_spn.text())


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())





