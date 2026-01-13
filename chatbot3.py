"""
Zero Trace AI Assistant - Chatbot Window
Provides help and guidance for secure data sanitization operations
"""

import sys
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, 
                             QPushButton, QLabel, QFrame, QScrollArea)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QTextCursor

class ChatbotThread(QThread):
    """Thread for processing chatbot responses"""
    response_ready = pyqtSignal(str)
    
    def __init__(self, user_message):
        super().__init__()
        self.user_message = user_message
    
    def run(self):
        """Generate response to user message"""
        response = self.generate_response(self.user_message)
        self.response_ready.emit(response)
    
    def generate_response(self, message):
        """Generate appropriate response based on user input"""
        message_lower = message.lower()
        
        # Security algorithm responses
        if any(keyword in message_lower for keyword in ['nist', 'algorithm', 'method', 'security']):
            return """🔒 **Security Algorithms Available:**

• **NIST SP 800-88 Clear** (3 passes) - Industry standard, recommended for most use cases
• **DoD 5220.22-M 3-Pass** - Military standard with 3 overwrite passes  
• **DoD 5220.22-M 7-Pass** - High security with 7 overwrite passes
• **Gutmann 35-Pass** - Maximum security for highly sensitive data

**Recommendation:** Use NIST Clear for standard compliance and best performance."""
        
        # Environmental impact responses
        elif any(keyword in message_lower for keyword in ['environmental', 'impact', 'co2', 'green', 'eco']):
            return """🌍 **Environmental Impact Tracking:**

Every secure wipe operation contributes to sustainability:

• **CO₂ Savings:** Each device wiped saves ~50kg CO₂ emissions
• **E-waste Prevention:** Prevents ~2kg e-waste from landfills  
• **Water Conservation:** Saves ~1000L water consumption
• **Energy Savings:** Prevents ~200kWh energy usage

Track your impact in the Environmental Dashboard!"""
        
        # Certificate responses
        elif any(keyword in message_lower for keyword in ['certificate', 'report', 'documentation', 'compliance']):
            return """📜 **Certificate Generation:**

Zero-Trace automatically generates:

• **PDF Certificates** with QR codes for verification
• **JSON Reports** for audit trails
• **Environmental Impact Reports** for sustainability reporting
• **Compliance Documentation** for regulatory requirements

All certificates include operation details, timestamps, and verification codes."""
        
        # Achievement responses
        elif any(keyword in message_lower for keyword in ['achievement', 'badge', 'points', 'gamification']):
            return """🏆 **Achievement System:**

Earn sustainability badges and points:

• **First Step** - Complete first wipe (100 points)
• **Eco Saver** - Wipe 10 devices (500 points)  
• **Data Guardian** - Wipe 50 devices (1000 points)
• **Recycling Champion** - Wipe 100 devices (2000 points)
• **Carbon Neutral Hero** - Save 1000kg CO₂ (1500 points)

Track your progress in the Environmental Dashboard!"""
        
        # Help and guidance
        elif any(keyword in message_lower for keyword in ['help', 'how', 'what', 'guide']):
            return """🤖 **Zero-Trace Assistant - How Can I Help?**

I can help you with:
• Security algorithm recommendations
• Environmental impact information  
• Certificate and compliance details
• Achievement system guidance
• General usage instructions

**Quick Start:**
1. Choose files or device to wipe
2. Select security method (NIST recommended)
3. Start the secure wipe process
4. View your environmental impact

What would you like to know more about?"""
        
        # Default response
        else:
            return """🤖 **Zero-Trace Assistant**

I'm here to help with your secure data sanitization needs!

**Common Topics:**
• Security algorithms and methods
• Environmental impact tracking
• Certificate generation
• Achievement system
• Usage guidance

Type 'help' for more information or ask me anything about Zero-Trace features!"""

class ChatbotWindow(QDialog):
    """AI Assistant window for Zero-Trace application"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🤖 Zero-Trace AI Assistant")
        self.setFixedSize(500, 600)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
            QTextEdit {
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 8px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton {
                background: #007bff;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #0056b3;
            }
            QPushButton:pressed {
                background: #004085;
            }
            QLabel {
                color: #495057;
                font-weight: bold;
            }
        """)
        
        self.init_ui()
        self.add_welcome_message()
    
    def init_ui(self):
        """Initialize the chatbot UI"""
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Header
        header = QLabel("🤖 Zero-Trace AI Assistant")
        header.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #007bff;
                padding: 10px;
                background: white;
                border-radius: 8px;
                margin-bottom: 5px;
            }
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.chat_display)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.input_field = QTextEdit()
        self.input_field.setMaximumHeight(80)
        self.input_field.setPlaceholderText("Ask me about Zero-Trace features...")
        self.input_field.setFont(QFont("Segoe UI", 10))
        input_layout.addWidget(self.input_field)
        
        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setMaximumWidth(80)
        input_layout.addWidget(self.send_button)
        
        layout.addLayout(input_layout)
        
        # Quick action buttons
        quick_actions_layout = QHBoxLayout()
        
        quick_help_btn = QPushButton("Quick Help")
        quick_help_btn.clicked.connect(lambda: self.send_quick_message("help"))
        
        algorithms_btn = QPushButton("Security Info")
        algorithms_btn.clicked.connect(lambda: self.send_quick_message("security algorithms"))
        
        impact_btn = QPushButton("Environmental")
        impact_btn.clicked.connect(lambda: self.send_quick_message("environmental impact"))
        
        quick_actions_layout.addWidget(quick_help_btn)
        quick_actions_layout.addWidget(algorithms_btn)
        quick_actions_layout.addWidget(impact_btn)
        
        layout.addLayout(quick_actions_layout)
        
        self.setLayout(layout)
        
        # Connect enter key to send
        self.input_field.keyPressEvent = self.handle_key_press
    
    def handle_key_press(self, event):
        """Handle key press events for input field"""
        if event.key() == Qt.Key_Return and event.modifiers() == Qt.ShiftModifier:
            # Shift+Enter for new line
            super().keyPressEvent(event)
        elif event.key() == Qt.Key_Return:
            # Enter to send message
            self.send_message()
        else:
            super().keyPressEvent(event)
    
    def add_welcome_message(self):
        """Add welcome message to chat"""
        welcome = """🤖 **Zero-Trace AI Assistant**

Hello! I'm your AI assistant for secure data sanitization. I can help you with:

• Security algorithm recommendations
• Environmental impact information  
• Certificate and compliance details
• Achievement system guidance
• General usage instructions

How can I assist you today?"""
        
        self.add_message("Assistant", welcome)
    
    def send_message(self):
        """Send user message and get response"""
        user_text = self.input_field.toPlainText().strip()
        if not user_text:
            return
        
        # Add user message
        self.add_message("You", user_text)
        
        # Clear input
        self.input_field.clear()
        
        # Disable input while processing
        self.input_field.setEnabled(False)
        self.send_button.setEnabled(False)
        
        # Start chatbot thread
        self.chatbot_thread = ChatbotThread(user_text)
        self.chatbot_thread.response_ready.connect(self.handle_response)
        self.chatbot_thread.finished.connect(self.enable_input)
        self.chatbot_thread.start()
    
    def send_quick_message(self, message):
        """Send a predefined quick message"""
        self.input_field.setPlainText(message)
        self.send_message()
    
    def handle_response(self, response):
        """Handle chatbot response"""
        self.add_message("Assistant", response)
    
    def enable_input(self):
        """Re-enable input field"""
        self.input_field.setEnabled(True)
        self.send_button.setEnabled(True)
        self.input_field.setFocus()
    
    def add_message(self, sender, message):
        """Add a message to the chat display"""
        self.chat_display.moveCursor(QTextCursor.End)
        
        # Add sender with formatting
        if sender == "You":
            self.chat_display.insertHtml(f"""
                <div style="margin: 10px 0;">
                    <span style="color: #007bff; font-weight: bold;">{sender}:</span>
                </div>
            """)
        else:
            self.chat_display.insertHtml(f"""
                <div style="margin: 10px 0;">
                    <span style="color: #28a745; font-weight: bold;">{sender}:</span>
                </div>
            """)
        
        # Add message with formatting
        formatted_message = message.replace('\n', '<br>')
        self.chat_display.insertHtml(f"""
            <div style="margin: 5px 0 15px 20px; padding: 10px; 
                        background: white; border-radius: 8px; 
                        border-left: 4px solid #007bff;">
                {formatted_message}
            </div>
        """)
        
        # Auto-scroll to bottom
        self.chat_display.moveCursor(QTextCursor.End)
        self.chat_display.ensureCursorVisible()

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    chatbot = ChatbotWindow()
    chatbot.show()
    sys.exit(app.exec_())
