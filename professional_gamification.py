"""
Professional Gamification Integration for SecureWipe India
Enterprise-grade environmental impact tracking and achievement system
"""
import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from gamification_engine import GamificationEngine

class ProfessionalImpactDashboard(QDialog):
    """Professional Environmental Impact Dashboard"""
    
    def __init__(self, user_id="default_user", parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.gamification = GamificationEngine()
        self.init_professional_ui()
        self.load_data()
        
        # Auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.load_data)
        self.refresh_timer.start(3000)  # Refresh every 3 seconds
        
    def init_professional_ui(self):
        """Initialize professional dashboard UI"""
        self.setWindowTitle("SecureWipe India - Environmental Impact Dashboard")
        self.setFixedSize(900, 700)
        self.setModal(True)
        
        # Professional styling
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 15px;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                color: #495057;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #007bff, stop:1 #0056b3);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0056b3, stop:1 #004085);
            }
            QPushButton:pressed {
                background: #004085;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Header Section
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #28a745, stop:1 #20c997);
                border-radius: 10px;
                margin: 5px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        
        title_label = QLabel("🌍 Environmental Impact Dashboard")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white; font-size: 22px; font-weight: bold; padding: 15px;")
        header_layout.addWidget(title_label)
        
        subtitle_label = QLabel("SecureWipe India - Making E-Waste Management Sustainable")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: white; font-size: 12px; padding-bottom: 10px;")
        header_layout.addWidget(subtitle_label)
        
        layout.addWidget(header_frame)
        
        # Main Content Area
        content_scroll = QScrollArea()
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        # Key Metrics Section
        metrics_group = QGroupBox("📊 Key Environmental Metrics")
        metrics_layout = QGridLayout()
        
        # Create professional metric cards
        self.devices_card = self.create_metric_card("Devices Processed", "0", "💾", "#17a2b8")
        self.co2_card = self.create_metric_card("CO₂ Emissions Saved", "0 kg", "🌱", "#28a745")
        self.ewaste_card = self.create_metric_card("E-Waste Prevented", "0 kg", "♻️", "#ffc107")
        self.points_card = self.create_metric_card("Sustainability Points", "0", "⭐", "#6f42c1")
        
        metrics_layout.addWidget(self.devices_card, 0, 0)
        metrics_layout.addWidget(self.co2_card, 0, 1)
        metrics_layout.addWidget(self.ewaste_card, 1, 0)
        metrics_layout.addWidget(self.points_card, 1, 1)
        
        metrics_group.setLayout(metrics_layout)
        content_layout.addWidget(metrics_group)
        
        # Progress & Achievements Section
        progress_group = QGroupBox("🏆 Achievement Progress")
        progress_layout = QVBoxLayout()
        
        # Level Progress
        level_frame = QFrame()
        level_frame.setStyleSheet("background: #f8f9fa; border-radius: 5px; padding: 10px;")
        level_layout = QHBoxLayout(level_frame)
        
        level_layout.addWidget(QLabel("Sustainability Level:"))
        self.level_bar = QProgressBar()
        self.level_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #dee2e6;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #28a745, stop:1 #20c997);
                border-radius: 3px;
            }
        """)
        level_layout.addWidget(self.level_bar)
        self.level_label = QLabel("Level 1")
        self.level_label.setStyleSheet("font-weight: bold; color: #495057;")
        level_layout.addWidget(self.level_label)
        
        progress_layout.addWidget(level_frame)
        
        # Next Achievement
        self.next_achievement = QLabel("Next Milestone: Complete your first secure wipe operation")
        self.next_achievement.setStyleSheet("""
            padding: 12px; 
            background: #fff3cd; 
            border: 1px solid #ffeaa7;
            border-radius: 6px;
            color: #856404;
            font-weight: bold;
        """)
        self.next_achievement.setWordWrap(True)
        progress_layout.addWidget(self.next_achievement)
        
        progress_group.setLayout(progress_layout)
        content_layout.addWidget(progress_group)
        
        # Recent Achievements
        achievements_group = QGroupBox("🎖️ Recent Achievements")
        achievements_layout = QVBoxLayout()
        
        self.achievements_display = QLabel("No achievements unlocked yet. Start your first secure wipe to begin earning sustainability badges!")
        self.achievements_display.setWordWrap(True)
        self.achievements_display.setStyleSheet("padding: 15px; background: #f8f9fa; border-radius: 5px;")
        achievements_layout.addWidget(self.achievements_display)
        
        achievements_group.setLayout(achievements_layout)
        content_layout.addWidget(achievements_group)
        
        # Environmental Impact Comparison
        impact_group = QGroupBox("🌍 Environmental Impact Equivalents")
        impact_layout = QVBoxLayout()
        
        impact_info = QLabel("💡 Your environmental contribution is equivalent to:")
        impact_info.setStyleSheet("font-weight: bold; color: #495057; margin-bottom: 8px;")
        impact_layout.addWidget(impact_info)
        
        self.impact_equivalents = QLabel("""
        🌳 Planting 0 trees for one year
        🚗 Preventing 0 km of car emissions  
        🏠 Powering 0 homes for one day
        💧 Saving 0 liters of water
        """)
        self.impact_equivalents.setStyleSheet("padding: 12px; background: #e8f5e9; border-radius: 5px; line-height: 1.6;")
        impact_layout.addWidget(self.impact_equivalents)
        
        impact_group.setLayout(impact_layout)
        content_layout.addWidget(impact_group)
        
        content_scroll.setWidget(content_widget)
        content_scroll.setWidgetResizable(True)
        layout.addWidget(content_scroll)
        
        # Action Buttons
        button_layout = QHBoxLayout()
        
        share_btn = QPushButton("📱 Share Impact")
        share_btn.clicked.connect(self.share_impact)
        button_layout.addWidget(share_btn)
        
        export_btn = QPushButton("📊 Export Report")
        export_btn.clicked.connect(self.export_report)
        button_layout.addWidget(export_btn)
        
        refresh_btn = QPushButton("🔄 Refresh Data")
        refresh_btn.clicked.connect(self.load_data)
        button_layout.addWidget(refresh_btn)
        
        close_btn = QPushButton("✖️ Close")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6c757d, stop:1 #495057);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #495057, stop:1 #343a40);
            }
        """)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
    def create_metric_card(self, title, value, icon, color):
        """Create a professional metric card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: white;
                border-left: 4px solid {color};
                border-radius: 8px;
                padding: 15px;
                margin: 5px;
            }}
            QFrame:hover {{
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }}
        """)
        
        layout = QVBoxLayout(card)
        
        # Icon and value
        top_layout = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        top_layout.addWidget(icon_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {color};")
        value_label.setAlignment(Qt.AlignRight)
        top_layout.addWidget(value_label)
        
        layout.addLayout(top_layout)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #6c757d; font-size: 11px; font-weight: bold;")
        layout.addWidget(title_label)
        
        card.value_label = value_label  # Store reference for updates
        return card
        
    def load_data(self):
        """Load and update dashboard data"""
        stats = self.gamification.get_user_stats(self.user_id)
        
        # Update metric cards
        self.devices_card.value_label.setText(str(stats['total_devices_wiped']))
        self.co2_card.value_label.setText(f"{stats['total_co2_saved_kg']:.1f} kg")
        self.ewaste_card.value_label.setText(f"{stats['total_ewaste_saved_kg']:.1f} kg")
        self.points_card.value_label.setText(str(stats['total_points']))
        
        # Update progress
        level_progress = min((stats['total_devices_wiped'] % 10) * 10, 100)
        self.level_bar.setValue(level_progress)
        current_level = (stats['total_devices_wiped'] // 10) + 1
        self.level_label.setText(f"Level {current_level}")
        
        # Update next achievement
        next_goal = self.get_next_milestone(stats)
        self.next_achievement.setText(f"Next Milestone: {next_goal}")
        
        # Update achievements
        if stats['achievements']:
            achievements_text = "\n".join([
                f"🏆 {ach['icon']} {ach['name']} - {ach['description']} (+{ach['points']} pts)"
                for ach in stats['achievements'][:3]
            ])
            self.achievements_display.setText(achievements_text)
        
        # Update environmental equivalents
        self.update_impact_equivalents(stats)
        
    def get_next_milestone(self, stats):
        """Get next achievement milestone"""
        devices = stats['total_devices_wiped']
        co2 = stats['total_co2_saved_kg']
        
        if devices == 0:
            return "Complete your first secure wipe operation"
        elif devices < 10:
            return f"Process {10 - devices} more devices to become an Eco Saver"
        elif devices < 50:
            return f"Process {50 - devices} more devices to become a Data Guardian"
        elif co2 < 1000:
            return f"Save {1000 - co2:.0f}kg more CO₂ to become a Carbon Neutral Hero"
        else:
            return "Reach 100 devices to become a Recycling Champion"
            
    def update_impact_equivalents(self, stats):
        """Update environmental impact equivalents"""
        co2_kg = stats['total_co2_saved_kg']
        ewaste_kg = stats['total_ewaste_saved_kg']
        
        trees = co2_kg / 21.77
        km_driven = co2_kg / 0.12
        homes_powered = co2_kg / 5.0
        water_saved = stats['total_devices_wiped'] * 1000  # 1000L per device
        
        equivalents = f"""
        🌳 Planting {trees:.0f} trees for one year
        🚗 Preventing {km_driven:.0f} km of car emissions  
        🏠 Powering {homes_powered:.0f} homes for one day
        💧 Saving {water_saved:,.0f} liters of water
        """
        
        self.impact_equivalents.setText(equivalents)
        
    def share_impact(self):
        """Share environmental impact on social media"""
        # Generate simple shareable content without the deleted module
        user_data = self.gamification.get_user_stats(self.user_id)
        content = f"""
🌍 My Zero-Trace Environmental Impact:
📊 Files Wiped: {user_data.get('total_files', 0)}
🏆 Achievements: {len(user_data.get('achievements', []))}
💚 CO₂ Saved: {user_data.get('total_co2_saved', 0):.1f} kg
♻️ E-waste Prevented: {user_data.get('total_ewaste_prevented', 0):.1f} kg

#ZeroTrace #Sustainability #DataSecurity
        """.strip()
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Share Your Environmental Impact")
        dialog.setFixedSize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        layout.addWidget(QLabel("📱 Ready to share on social media:"))
        
        message_text = QTextEdit()
        message_text.setPlainText(f"{content['message']}\n\n{content['hashtags']}")
        message_text.setStyleSheet("padding: 10px; border: 1px solid #dee2e6; border-radius: 5px;")
        layout.addWidget(message_text)
        
        stats_label = QLabel(f"""
        📊 Your Impact Statistics:
        • Devices processed: {content['stats']['devices_wiped']}
        • CO₂ saved: {content['stats']['co2_saved']:.1f}kg
        • E-waste prevented: {content['stats']['ewaste_prevented']:.1f}kg
        • Achievements unlocked: {content['stats']['achievements_count']}
        """)
        stats_label.setStyleSheet("background: #f8f9fa; padding: 10px; border-radius: 5px;")
        layout.addWidget(stats_label)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec_()
        
    def export_report(self):
        """Export environmental impact report"""
        stats = self.gamification.get_user_stats(self.user_id)
        
        filename = f"environmental_impact_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        try:
            with open(filepath, 'w') as f:
                f.write("SECUREWIPE INDIA - ENVIRONMENTAL IMPACT REPORT\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"User ID: {self.user_id}\n\n")
                
                f.write("KEY METRICS:\n")
                f.write(f"• Devices Processed: {stats['total_devices_wiped']}\n")
                f.write(f"• Files Wiped: {stats['total_files_wiped']}\n")
                f.write(f"• CO₂ Emissions Saved: {stats['total_co2_saved_kg']:.1f} kg\n")
                f.write(f"• E-Waste Prevented: {stats['total_ewaste_saved_kg']:.1f} kg\n")
                f.write(f"• Sustainability Points: {stats['total_points']}\n")
                f.write(f"• Current Level: {stats['current_level']}\n\n")
                
                if stats['achievements']:
                    f.write("ACHIEVEMENTS UNLOCKED:\n")
                    for ach in stats['achievements']:
                        f.write(f"• {ach['name']}: {ach['description']} (+{ach['points']} pts)\n")
                
            QMessageBox.information(self, "Report Exported", f"Environmental impact report saved to:\n{filepath}")
            
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export report:\n{str(e)}")
            
    def record_wipe_operation(self, device_count=1, file_count=0, method="NIST Clear"):
        """Record a wipe operation and show achievements"""
        result = self.gamification.record_wipe_session(
            self.user_id, device_count, file_count, method
        )
        
        # Show achievement notifications
        if result['new_achievements']:
            for achievement in result['new_achievements']:
                QMessageBox.information(
                    self,
                    "🏆 Achievement Unlocked!",
                    f"{achievement['icon']} {achievement['name']}\n\n"
                    f"{achievement['description']}\n\n"
                    f"Sustainability Points Earned: +{achievement['points']}"
                )
        
        self.load_data()
        return result
