"""
Zero Trace Enhanced - E-Waste Data Sanitization Interface
With improved loading bar and status indicators
"""

import os
import json
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from file_secure_wipe_optimized import FileSecureWipe
from chatbot3 import ChatbotWindow

class LoadingStatusBar(QStatusBar):
    """Enhanced status bar with loading animation"""
    
    def __init__(self):
        super().__init__()
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.setMaximumHeight(15)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()
        
        self.status_label = QLabel("Ready")
        self.addWidget(self.status_label)
        self.addPermanentWidget(self.progress_bar)
        self.chatbot_window = None



    def show_chatbot(self):
    
        try:
            if self.chatbot_window is None:
                from chatbot3 import ChatbotWindow   # import here to avoid circular issues
                self.chatbot_window = ChatbotWindow()
                self.chatbot_window.setAttribute(Qt.WA_DeleteOnClose)
                # Reset the reference when window is closed
                self.chatbot_window.destroyed.connect(lambda: setattr(self, 'chatbot_window', None))

            self.chatbot_window.show()
            self.chatbot_window.raise_()
            self.chatbot_window.activateWindow()
        except Exception as e:
            QMessageBox.critical(self, "Chatbot Error", f"Failed to open chatbot:\n{e}")


        
    def show_loading(self, message="Processing..."):
        """Show loading animation"""
        self.status_label.setText(f"⏳ {message}")
        self.progress_bar.show()
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        
    def show_progress(self, value, message=""):
        """Show specific progress"""
        self.progress_bar.show()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(value)
        if message:
            self.status_label.setText(message)
            
    def show_success(self, message="Operation completed"):
        """Show success status with green background"""
        self.progress_bar.hide()
        self.setStyleSheet("QStatusBar { background-color: #4CAF50; color: white; font-weight: bold; }")
        self.status_label.setText(f"✅ {message}")
        QTimer.singleShot(3000, self.reset_style)
        
    def show_error(self, message="Operation failed"):
        """Show error status with red background"""
        self.progress_bar.hide()
        self.setStyleSheet("QStatusBar { background-color: #F44336; color: white; font-weight: bold; }")
        self.status_label.setText(f"❌ {message}")
        QTimer.singleShot(3000, self.reset_style)
        
    def show_warning(self, message="Warning"):
        """Show warning status with orange background"""
        self.progress_bar.hide()
        self.setStyleSheet("QStatusBar { background-color: #FFA500; color: white; font-weight: bold; }")
        self.status_label.setText(f"⚠️ {message}")
        QTimer.singleShot(3000, self.reset_style)
        
    def reset_style(self):
        """Reset to default style"""
        self.setStyleSheet("")
        self.status_label.setText("Ready")
        self.progress_bar.hide()

# Import the rest of the ZeroTraceGUI class from zero_trace_gui.py
# and modify it to use LoadingStatusBar
from zero_trace_gui import WipeThread, ZeroTraceGUI as BaseZeroTraceGUI

class ZeroTraceEnhanced(BaseZeroTraceGUI):
    """Enhanced version with improved status bar"""
    
    def init_ui(self):
        """Override to use enhanced status bar"""
        super().init_ui()
        
        # Replace the standard status bar with our enhanced one
        self.status_bar = LoadingStatusBar()
        self.setStatusBar(self.status_bar)

    def show_chatbot(self):
    
        try:
            if self.chatbot_window is None:
                from chatbot3 import ChatbotWindow   # import here to avoid circular issues
                self.chatbot_window = ChatbotWindow()
                self.chatbot_window.setAttribute(Qt.WA_DeleteOnClose)
                # Reset the reference when window is closed
                self.chatbot_window.destroyed.connect(lambda: setattr(self, 'chatbot_window', None))

            self.chatbot_window.show()
            self.chatbot_window.raise_()
            self.chatbot_window.activateWindow()
        except Exception as e:
            QMessageBox.critical(self, "Chatbot Error", f"Failed to open chatbot:\n{e}")

        
    def start_wipe(self):
        """Override to show loading animation"""
        super().start_wipe()
        self.status_bar.show_loading("Secure wipe in progress...")
        
    def update_progress(self, message):
        """Override to update loading bar"""
        self.log_message(message)
        self.status_bar.show_loading(message)
        
    def wipe_completed(self, result):
        """Override to show completion status"""
        self.last_result = result
        
        self.wipe_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if result['status'] == 'completed':
            if result['type'] == 'device':
                msg = f"Successfully wiped {result.get('files_deleted', 0)} files"
                self.log_message(f"✅ Device wipe completed: {result.get('files_deleted', 0)} files processed")
            else:
                msg = f"Successfully deleted {result['successful']} files"
                self.log_message(f"✅ File deletion completed: {result['successful']} successful, {result['failed']} failed")
            
            self.pdf_cert_btn.setEnabled(True)
            self.json_cert_btn.setEnabled(True)
            self.status_bar.show_success(msg)
            
        elif result['status'] == 'cancelled':
            self.log_message("⚠️ Operation cancelled by user")
            self.status_bar.show_warning("Operation cancelled")
        else:
            self.log_message(f"❌ Operation failed: {result.get('error', 'Unknown error')}")
            self.status_bar.show_error("Operation failed")
        
        if self.files_radio.isChecked():
            self.clear_files()
        self.selected_device = None
        self.update_ui_state()

# Alias for compatibility
ZeroTraceGUI = ZeroTraceEnhanced
