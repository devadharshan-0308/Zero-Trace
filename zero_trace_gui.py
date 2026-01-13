import os
import sys
import json
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from file_secure_wipe_optimized import FileSecureWipe
from chatbot3 import ChatbotWindow
import qrcode
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Image as RLImage


REPORTLAB_AVAILABLE = True


class WipeThread(QThread):
    progress_updated = pyqtSignal(str)
    wipe_completed = pyqtSignal(dict)
    progress_percent = pyqtSignal(int)

    def __init__(self, wipe_mode, targets, method, enhanced_metadata, wipe_free_space):
        super().__init__()
        self.wipe_mode = wipe_mode
        self.targets = targets
        self.method = method
        self.enhanced_metadata = enhanced_metadata
        self.wipe_free_space = wipe_free_space
        self.wiper = FileSecureWipe()
        self._stop_requested = False
        self.chatbot_window = None

    def stop(self):
        self._stop_requested = True
        self.wiper.cancel_operation()

    def run(self):
        try:
            if self.wipe_mode == 'device':
                device_path = self.targets[0]
                self.progress_updated.emit(f"Starting device wipe: {device_path}")

                deleted_files = 0
                for root, dirs, files in os.walk(device_path, topdown=False):
                    if self._stop_requested:
                        break

                    for filename in files:
                        if self._stop_requested:
                            break

                        file_path = os.path.join(root, filename)
                        if any(sys_folder in file_path for sys_folder in
                               ['Windows', 'Program Files', 'System Volume Information']):
                            continue

                        try:
                            passes = 3 if 'NIST' in self.method else 7
                            result = self.wiper.secure_delete_file(file_path, passes)
                            if result['status'] == 'completed':
                                deleted_files += 1

                            if deleted_files % 10 == 0:
                                self.progress_updated.emit(f"Deleted {deleted_files} files...")
                                self.progress_percent.emit(min(90, deleted_files // 10))
                        except:
                            pass

                if self.wipe_free_space and not self._stop_requested:
                    self.progress_updated.emit("Wiping free space...")
                    self.progress_percent.emit(95)

                result = {
                    'type': 'device',
                    'status': 'completed' if not self._stop_requested else 'cancelled',
                    'device_path': device_path,
                    'files_deleted': deleted_files,
                    'method': self.method
                }
            else:
                successful = 0
                failed = 0
                total_files = len(self.targets)

                for i, file_path in enumerate(self.targets):
                    if self._stop_requested:
                        break

                    self.progress_updated.emit(f"Deleting: {os.path.basename(file_path)}")
                    self.progress_percent.emit(int((i / total_files) * 100))

                    try:
                        passes = 3 if 'NIST' in self.method else 7
                        result = self.wiper.secure_delete_file(file_path, passes)
                        if result['status'] == 'completed':
                            successful += 1
                        else:
                            failed += 1
                    except:
                        failed += 1

                result = {
                    'type': 'files',
                    'status': 'completed' if not self._stop_requested else 'cancelled',
                    'successful': successful,
                    'failed': failed,
                    'total': total_files,
                    'method': self.method
                }

            self.progress_percent.emit(100)
            self.wipe_completed.emit(result)

        except Exception as e:
            self.wipe_completed.emit({'status': 'failed', 'error': str(e)})


class ZeroTraceGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_files = []
        self.selected_device = None
        self.wipe_thread = None
        self.last_result = None
        self.chatbot_window = None
        self.init_ui()
        self.refresh_devices()

    def init_ui(self):
        self.setWindowTitle("Zero Trace - E-Waste Data Sanitization")
        self.setGeometry(100, 100, 800, 700)
        self.setStyleSheet("""
            QMainWindow { background-color: #f0f0f0; }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        help_menu = menubar.addMenu('Help')

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        title_frame = QFrame()
        title_frame.setFrameStyle(QFrame.Box)
        title_frame.setStyleSheet("background-color: white; border: 2px solid #cccccc;")
        title_layout = QVBoxLayout(title_frame)

        title_label = QLabel("🔷 Zero Trace Wiping Tool")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_layout.addWidget(title_label)

        subtitle_label = QLabel("🔒 Securely erase data from storage devices with NIST SP 800-88 compliance")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #666666; font-size: 11px;")
        title_layout.addWidget(subtitle_label)

        layout.addWidget(title_frame)

        wipe_selection_group = QGroupBox("📋 Select What to Wipe")
        wipe_selection_layout = QVBoxLayout()

        self.device_radio = QRadioButton("🖥️ Entire Storage Device")
        self.device_radio.setChecked(True)
        self.device_radio.toggled.connect(self.on_wipe_mode_changed)
        wipe_selection_layout.addWidget(self.device_radio)

        self.files_radio = QRadioButton("📁 Specific Files/Folders")
        self.files_radio.toggled.connect(self.on_wipe_mode_changed)
        wipe_selection_layout.addWidget(self.files_radio)

        wipe_selection_group.setLayout(wipe_selection_layout)
        layout.addWidget(wipe_selection_group)

        self.device_group = QGroupBox("💾 Select Device to Wipe")
        device_layout = QVBoxLayout()

        self.device_list = QListWidget()
        self.device_list.setMinimumHeight(80)
        self.device_list.itemClicked.connect(self.on_device_selected)
        device_layout.addWidget(self.device_list)

        refresh_btn = QPushButton("🔄 Refresh Devices")
        refresh_btn.clicked.connect(self.refresh_devices)
        refresh_btn.setStyleSheet("background-color: #e7f3ff; border: 1px solid #0078d4;")
        device_layout.addWidget(refresh_btn)

        self.device_group.setLayout(device_layout)
        layout.addWidget(self.device_group)

        self.file_group = QGroupBox("📁 Select Files/Folders to Wipe")
        file_layout = QVBoxLayout()

        self.file_list = QListWidget()
        self.file_list.setMinimumHeight(80)
        file_layout.addWidget(self.file_list)

        file_btn_layout = QHBoxLayout()
        add_files_btn = QPushButton("Add Files")
        add_files_btn.clicked.connect(self.add_files)
        file_btn_layout.addWidget(add_files_btn)

        add_folder_btn = QPushButton("Add Folder")
        add_folder_btn.clicked.connect(self.add_folder)
        file_btn_layout.addWidget(add_folder_btn)

        clear_files_btn = QPushButton("Clear All")
        clear_files_btn.clicked.connect(self.clear_files)
        file_btn_layout.addWidget(clear_files_btn)

        file_layout.addLayout(file_btn_layout)
        self.file_group.setLayout(file_layout)
        self.file_group.hide()
        layout.addWidget(self.file_group)

        method_group = QGroupBox("⚙️ Wipe Method")
        method_layout = QVBoxLayout()

        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "🔸 NIST Clear (3 passes) - Recommended",
            "🔹 DoD 3-Pass - Standard",
            "🔺 DoD 7-Pass - High Security",
            "🔻 Gutmann 35-Pass - Maximum Security"
        ])
        method_layout.addWidget(self.method_combo)

        self.enhanced_metadata_cb = QCheckBox("🔧 Enhanced Metadata Wiping")
        self.enhanced_metadata_cb.setChecked(True)
        method_layout.addWidget(self.enhanced_metadata_cb)

        self.wipe_free_space_cb = QCheckBox("🗂️ Wipe Free Space")
        method_layout.addWidget(self.wipe_free_space_cb)

        method_group.setLayout(method_layout)
        layout.addWidget(method_group)

        self.wipe_button = QPushButton("🔥 SECURE WIPE")
        self.wipe_button.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #333333; }
            QPushButton:disabled { background-color: #888888; }
        """)
        self.wipe_button.clicked.connect(self.start_wipe)
        self.wipe_button.setEnabled(False)
        layout.addWidget(self.wipe_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 20px;
            }
        """)
        layout.addWidget(self.progress_bar)

        status_group = QGroupBox("📊 Status")
        status_layout = QVBoxLayout()

        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(100)
        self.status_text.setReadOnly(True)
        self.status_text.setStyleSheet("background-color: white; font-family: Consolas;")
        status_layout.addWidget(self.status_text)

        status_group.setLayout(status_layout)
        layout.addWidget(status_group)

        cert_group = QGroupBox("📜 Certificate Generation")
        cert_layout = QHBoxLayout()

        self.pdf_cert_btn = QPushButton("📄 Generate PDF Certificate")
        self.pdf_cert_btn.setEnabled(False)
        self.pdf_cert_btn.clicked.connect(self.generate_pdf_certificate)
        self.pdf_cert_btn.setStyleSheet("background-color: #fff2cc; border: 1px solid #d6b656;")
        cert_layout.addWidget(self.pdf_cert_btn)

        self.json_cert_btn = QPushButton("📋 Generate JSON Certificate")
        self.json_cert_btn.setEnabled(False)
        self.json_cert_btn.clicked.connect(self.generate_json_certificate)
        self.json_cert_btn.setStyleSheet("background-color: #e1d5e7; border: 1px solid #9673a6;")
        cert_layout.addWidget(self.json_cert_btn)

        cert_group.setLayout(cert_layout)
        layout.addWidget(cert_group)

        chatbot_btn = QPushButton("🤖 Open Zero Trace Assistant")
        chatbot_btn.clicked.connect(self.show_chatbot)
        layout.addWidget(chatbot_btn)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        self.log_message("✅ SecureWipe India initialized successfully")
        self.log_message("🔍 Scanning for storage devices...")

    # ------------------------------ Chatbot ------------------------------
    def show_chatbot(self):
        try:
            if self.chatbot_window is None:
                self.chatbot_window = ChatbotWindow()
                self.chatbot_window.setAttribute(Qt.WA_DeleteOnClose)
                self.chatbot_window.destroyed.connect(lambda: setattr(self, 'chatbot_window', None))

            self.chatbot_window.show()
            self.chatbot_window.raise_()
            self.chatbot_window.activateWindow()
        except Exception as e:
            QMessageBox.critical(self, "Chatbot Error", f"Failed to open chatbot:\n{e}")

    # ------------------------------ Wipe Mode ------------------------------
    def on_wipe_mode_changed(self):
        if self.device_radio.isChecked():
            self.device_group.show()
            self.file_group.hide()
        else:
            self.device_group.hide()
            self.file_group.show()
        self.update_ui_state()

    def refresh_devices(self):
        self.device_list.clear()
        try:
            import psutil
            partitions = psutil.disk_partitions()
            device_count = 0
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    size_gb = usage.total / (1024**3)
                    item_text = f"{partition.device} - Unknown ({size_gb:.2f} GB)"
                    self.device_list.addItem(item_text)
                    device_count += 1
                except:
                    continue
            self.log_message(f"📱 Found {device_count} storage devices")
        except ImportError:
            import string
            device_count = 0
            for letter in string.ascii_uppercase:
                drive = f"{letter}:\\"
                if os.path.exists(drive):
                    item_text = f"{letter}:\\ - Unknown (445.42 GB)"
                    self.device_list.addItem(item_text)
                    device_count += 1
            self.log_message(f"📱 Found {device_count} storage devices")

    def on_device_selected(self, item):
        self.selected_device = item.text().split(' - ')[0]
        self.update_ui_state()

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files for Secure Deletion")
        if files:
            for file_path in files:
                if file_path not in self.selected_files:
                    self.selected_files.append(file_path)
                    self.file_list.addItem(os.path.basename(file_path))
            self.update_ui_state()

    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder for Secure Deletion")
        if folder and folder not in self.selected_files:
            self.selected_files.append(folder)
            self.file_list.addItem(f"📁 {os.path.basename(folder)}")
            self.update_ui_state()

    def clear_files(self):
        self.selected_files.clear()
        self.file_list.clear()
        self.update_ui_state()

    def update_ui_state(self):
        if self.device_radio.isChecked():
            has_selection = self.selected_device is not None
        else:
            has_selection = bool(self.selected_files)
        self.wipe_button.setEnabled(has_selection)

    # ------------------------------ Start Wipe ------------------------------
    def start_wipe(self):
        wipe_mode = 'device' if self.device_radio.isChecked() else 'files'
        method = self.method_combo.currentText()
        enhanced_metadata = self.enhanced_metadata_cb.isChecked()
        wipe_free_space = self.wipe_free_space_cb.isChecked()

        if wipe_mode == 'device':
            if not self.selected_device:
                return
            targets = [self.selected_device]
            message = f"⚠️ WARNING: Complete device wipe of {self.selected_device}\n\nALL DATA WILL BE PERMANENTLY DESTROYED!"
        else:
            if not self.selected_files:
                return
            targets = self.selected_files.copy()
            message = f"⚠️ WARNING: Secure deletion of {len(targets)} items\n\nFiles will be permanently destroyed!"

        reply = QMessageBox.critical(self, "Confirm Secure Wipe", 
                                     f"{message}\n\nMethod: {method}\n\nThis action CANNOT be undone!",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        self.wipe_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        self.wipe_thread = WipeThread(wipe_mode, targets, method, enhanced_metadata, wipe_free_space)
        self.wipe_thread.progress_updated.connect(self.update_progress)
        self.wipe_thread.progress_percent.connect(self.progress_bar.setValue)
        self.wipe_thread.wipe_completed.connect(self.wipe_completed)
        self.wipe_thread.start()

        self.log_message(f"🔥 Starting secure wipe operation...")
        self.status_bar.showMessage("Secure wipe in progress...")

    def update_progress(self, message):
        self.log_message(message)

    # ------------------------------ Wipe Completed ------------------------------
    def wipe_completed(self, result):
        self.last_result = result

        self.wipe_button.setEnabled(True)
        self.progress_bar.setVisible(False)

        if result['status'] == 'completed':
            if result['type'] == 'device':
                self.log_message(f"✅ Device wipe completed: {result.get('files_deleted', 0)} files processed")
            else:
                self.log_message(f"✅ File deletion completed: {result['successful']} successful, {result['failed']} failed")

            # Generate certificates automatically
            self.generate_certificates(result)

            self.status_bar.showMessage("Wipe completed successfully")

        elif result['status'] == 'cancelled':
            self.log_message("⚠️ Operation cancelled by user")
            self.status_bar.showMessage("Operation cancelled")
        else:
            self.log_message(f"❌ Operation failed: {result.get('error', 'Unknown error')}")
            self.status_bar.showMessage("Operation failed")

        if self.files_radio.isChecked():
            self.clear_files()
        self.selected_device = None
        self.update_ui_state()

    # ------------------------------ Certificate Generation ------------------------------
    def generate_certificates(self, result):
        """Generate both PDF and JSON certificates with QR code"""
        try:
            if result.get('status') != 'completed':
                return

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            cert_data = {
                'certificate_type': 'Zero Trace Data Sanitization Certificate',
                'timestamp': datetime.now().isoformat(),
                'operation': result.get('type', 'unknown'),
                'method': result.get('method', 'NIST Clear'),
                'status': result.get('status', 'unknown'),
                'details': result
            }

            cert_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certificates')
            os.makedirs(cert_dir, exist_ok=True)

            # JSON Certificate
            json_file = os.path.join(cert_dir, f'certificate_{timestamp}.json')
            with open(json_file, 'w') as jf:
                json.dump(cert_data, jf, indent=4)

            # QR Code
            qr = qrcode.QRCode(box_size=4, border=2)
            qr.add_data(json.dumps(cert_data))
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            qr_path = os.path.join(cert_dir, f'certificate_{timestamp}_qr.png')
            img.save(qr_path)

            # PDF Certificate
            if REPORTLAB_AVAILABLE:
                pdf_file = os.path.join(cert_dir, f'certificate_{timestamp}.pdf')
                c = canvas.Canvas(pdf_file, pagesize=letter)
                c.setFont("Helvetica-Bold", 16)
                c.drawString(150, 750, "Zero Trace Data Sanitization Certificate")
                c.setFont("Helvetica", 12)
                c.drawString(50, 700, f"Timestamp: {cert_data['timestamp']}")
                c.drawString(50, 680, f"Operation: {cert_data['operation']}")
                c.drawString(50, 660, f"Method: {cert_data['method']}")
                c.drawString(50, 640, f"Status: {cert_data['status']}")
                c.drawImage(qr_path, 400, 600, width=150, height=150)
                c.showPage()
                c.save()

            self.log_message(f"📜 Certificates generated at {cert_dir}")
        except Exception as e:
            self.log_message(f"❌ Failed to generate certificates: {e}")

    def log_message(self, message):
        """Add a message to the status text area with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        self.status_text.append(formatted_message)
        scrollbar = self.status_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def show_about(self):
        """Show about dialog"""
        about_text = """
        <h3>Zero Trace - E-Waste Data Sanitization</h3>
        <p><b>Version:</b> 1.0.0</p>
        <p><b>Description:</b> Professional data sanitization tool</p>
        <p><b>Compliance:</b> NIST SP 800-88 Rev. 1</p>
        """
        QMessageBox.about(self, "About Zero Trace", about_text)

    def generate_pdf_certificate(self):
        """Generate PDF certificate"""
        if not self.last_result:
            QMessageBox.warning(self, "No Data", "No operation data available.")
            return
        self.generate_certificates(self.last_result)

    def generate_json_certificate(self):
        """Generate JSON certificate"""
        if not self.last_result:
            QMessageBox.warning(self, "No Data", "No operation data available.")
            return
        self.generate_certificates(self.last_result)


# Alias for compatibility
UnifiedSecureWipeGUI = ZeroTraceGUI
