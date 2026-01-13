"""
Enhanced Main Entry Point for SecureWipe India - Zero Trace Edition
Professional Gamification Integration with Environmental Impact Dashboard
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class GamifiedZeroTraceApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Zero Trace - Professional E-Waste Data Sanitization")
        self.app.setStyle('Fusion')
        self.main_window = None
        self.dashboard = None
        
    def initialize_main_window(self):
        """Initialize the main Zero Trace window with gamification integration"""
        # Check if required backend exists
        if not os.path.exists('file_secure_wipe_optimized.py'):
            QMessageBox.critical(None, "Missing Backend", 
                               "file_secure_wipe_optimized.py not found!\n"
                               "Please ensure the optimized backend is in the same directory.")
            return False
        
        try:
            # Try to import the enhanced GUI with loading bar first
            try:
                from zero_trace_enhanced import ZeroTraceEnhanced as ZeroTraceGUI
                print("Using enhanced GUI with loading bar")
            except ImportError:
                # Fall back to standard GUI
                from zero_trace_gui import ZeroTraceGUI
                print("Using standard GUI")
            
            # Create the main window
            self.main_window = ZeroTraceGUI()
            
            # Add professional dashboard integration
            self.integrate_professional_dashboard()
            
            return True
            
        except ImportError as e:
            QMessageBox.critical(None, "Import Error", 
                               f"Failed to import Zero Trace GUI:\n{str(e)}\n\n"
                               "Please ensure zero_trace_gui.py exists and is properly configured.")
            return False
        except Exception as e:
            QMessageBox.critical(None, "Initialization Error", 
                               f"Failed to initialize application:\n{str(e)}")
            return False
    
    def integrate_professional_dashboard(self):
        """Integrate professional environmental impact dashboard"""
        try:
            from professional_gamification import ProfessionalImpactDashboard
            from gamification_engine import GamificationEngine
            
            # Initialize gamification system
            self.gamification = GamificationEngine()
            
            # Create dashboard button with professional styling
            dashboard_btn = QPushButton("🌍 Environmental Impact Dashboard")
            dashboard_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #28a745, stop:1 #20c997);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 20px;
                    font-weight: bold;
                    font-size: 13px;
                    margin: 5px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #20c997, stop:1 #17a2b8);
                    transform: translateY(-1px);
                }
                QPushButton:pressed {
                    background: #17a2b8;
                }
            """)
            dashboard_btn.clicked.connect(self.show_professional_dashboard)
            
            # Add button to the main window layout
            if hasattr(self.main_window, 'centralWidget'):
                central_widget = self.main_window.centralWidget()
                if central_widget and hasattr(central_widget, 'layout'):
                    layout = central_widget.layout()
                    if layout:
                        # Insert dashboard button before the chatbot button
                        button_index = layout.count() - 2  # Before status bar
                        layout.insertWidget(button_index, dashboard_btn)
            
            # Connect wipe completion to gamification tracking
            self.connect_wipe_tracking()
            
            print("✅ Professional gamification dashboard integrated successfully")
            
        except ImportError as e:
            print(f"⚠️ Gamification features not available: {e}")
            # Continue without gamification if modules are missing
        except Exception as e:
            print(f"⚠️ Failed to integrate gamification: {e}")
    
    def connect_wipe_tracking(self):
        """Connect wipe operations to gamification tracking"""
        try:
            # Store original wipe_completed method
            if hasattr(self.main_window, 'wipe_completed'):
                original_wipe_completed = self.main_window.wipe_completed
                
                def enhanced_wipe_completed(result):
                    # Call original method
                    original_wipe_completed(result)
                    
                    # Track in gamification system
                    self.track_wipe_operation(result)
                
                # Replace with enhanced version
                self.main_window.wipe_completed = enhanced_wipe_completed
                
        except Exception as e:
            print(f"⚠️ Failed to connect wipe tracking: {e}")
    
    def track_wipe_operation(self, result):
        """Track wipe operation in gamification system"""
        try:
            if result.get('status') == 'completed':
                device_count = 1 if result.get('type') == 'device' else 0
                file_count = result.get('files_deleted', 0) if result.get('type') == 'device' else result.get('successful', 0)
                method = result.get('method', 'Unknown')
                
                # Record in gamification system
                gamification_result = self.gamification.record_wipe_session(
                    user_id="default_user",
                    device_count=device_count,
                    file_count=file_count,
                    method=method
                )
                
                # Show achievement notifications
                if gamification_result.get('new_achievements'):
                    self.show_achievement_notifications(gamification_result['new_achievements'])
                
        except Exception as e:
            print(f"⚠️ Failed to track wipe operation: {e}")
    
    def show_achievement_notifications(self, achievements):
        """Show professional achievement notifications"""
        for achievement in achievements:
            msg = QMessageBox(self.main_window)
            msg.setWindowTitle("🏆 Sustainability Achievement Unlocked!")
            msg.setIcon(QMessageBox.Information)
            
            # Professional achievement message
            achievement_text = f"""
            <div style="text-align: center; padding: 10px;">
                <h2 style="color: #28a745;">{achievement['icon']} {achievement['name']}</h2>
                <p style="font-size: 14px; color: #495057;">{achievement['description']}</p>
                <p style="font-weight: bold; color: #007bff;">
                    Sustainability Points Earned: +{achievement['points']}
                </p>
                <p style="font-size: 12px; color: #6c757d;">
                    Your contribution to environmental sustainability has been recognized!
                </p>
            </div>
            """
            
            msg.setText(achievement_text)
            msg.setStandardButtons(QMessageBox.Ok)
            
            # Style the message box
            msg.setStyleSheet("""
                QMessageBox {
                    background: white;
                    font-family: 'Segoe UI', Arial, sans-serif;
                }
                QMessageBox QPushButton {
                    background: #28a745;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QMessageBox QPushButton:hover {
                    background: #20c997;
                }
            """)
            
            msg.exec_()
    
    def show_professional_dashboard(self):
        """Show the professional environmental impact dashboard"""
        try:
            from professional_gamification import ProfessionalImpactDashboard
            
            if not self.dashboard:
                self.dashboard = ProfessionalImpactDashboard("default_user", self.main_window)
            
            self.dashboard.show()
            self.dashboard.raise_()
            self.dashboard.activateWindow()
            
        except Exception as e:
            QMessageBox.critical(self.main_window, "Dashboard Error", 
                               f"Failed to open environmental impact dashboard:\n{str(e)}")
    
    def show_startup_message(self):
        """Show professional startup message"""
        startup_msg = QMessageBox(self.main_window)
        startup_msg.setWindowTitle("SecureWipe India - Professional Edition")
        startup_msg.setIcon(QMessageBox.Information)
        
        startup_text = """
        <div style="text-align: center; padding: 15px;">
            <h2 style="color: #28a745;">🌍 SecureWipe India - Professional Edition</h2>
            <p style="font-size: 14px; margin: 10px 0;">
                <strong>Enterprise-Grade Data Sanitization with Environmental Impact Tracking</strong>
            </p>
            
            <div style="text-align: left; margin: 15px 0;">
                <h3 style="color: #007bff;">🔒 Available Algorithms:</h3>
                <ul style="margin: 5px 0;">
                    <li>NIST SP 800-88 Clear (3 passes) - Industry Standard</li>
                    <li>DoD 5220.22-M 3-Pass - Military Standard</li>
                    <li>DoD 5220.22-M 7-Pass - High Security</li>
                    <li>Gutmann 35-Pass - Maximum Security</li>
                </ul>
                
                <h3 style="color: #28a745;">🌱 Environmental Features:</h3>
                <ul style="margin: 5px 0;">
                    <li>Real-time CO₂ emissions tracking</li>
                    <li>E-waste prevention calculations</li>
                    <li>Sustainability achievement system</li>
                    <li>Professional impact reporting</li>
                </ul>
                
                <h3 style="color: #ffc107;">📜 Professional Documentation:</h3>
                <ul style="margin: 5px 0;">
                    <li>PDF and JSON certificates with QR codes</li>
                    <li>Compliance documentation</li>
                    <li>Environmental impact reports</li>
                </ul>
            </div>
            
            <p style="color: #dc3545; font-weight: bold; margin-top: 15px;">
                ⚠️ WARNING: This performs ACTUAL data destruction!<br>
                Data will be permanently destroyed and cannot be recovered.
            </p>
            
            <p style="color: #6c757d; font-size: 12px; margin-top: 10px;">
                Click the "🌍 Environmental Impact Dashboard" button to track your sustainability impact!
            </p>
        </div>
        """
        
        startup_msg.setText(startup_text)
        startup_msg.setStandardButtons(QMessageBox.Ok)
        
        # Professional styling
        startup_msg.setStyleSheet("""
            QMessageBox {
                background: white;
                font-family: 'Segoe UI', Arial, sans-serif;
                min-width: 500px;
            }
            QMessageBox QPushButton {
                background: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QMessageBox QPushButton:hover {
                background: #0056b3;
            }
        """)
        
        startup_msg.exec_()
    
    def run(self):
        """Run the gamified Zero Trace application"""
        if not self.initialize_main_window():
            return 1
        
        # Show the main window
        self.main_window.show()
        
        # Show professional startup message
        self.show_startup_message()
        
        # Run the application
        return self.app.exec_()

def main():
    """Main entry point for the gamified Zero Trace application"""
    try:
        app = GamifiedZeroTraceApp()
        return app.run()
    except Exception as e:
        print(f"❌ Critical error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())