# Zero Trace - Secure Data Sanitization System

A comprehensive data sanitization and secure file wiping application built for the Smart India Hackathon 2024. Zero Trace provides military-grade data deletion capabilities with an intuitive GUI interface, environmental impact tracking, and gamification features.

## Features

### Core Functionality
- **Secure File Wiping**: Multiple data sanitization methods (DoD 5220.22-M, Gutmann, Random)
- **Device Sanitization**: Complete drive wiping capabilities
- **Free Space Cleaning**: Securely wipe unused disk space
- **Real-time Progress Tracking**: Visual progress bars and status updates
- **Audit Logging**: Comprehensive operation logs for compliance

### User Interface
- **Modern GUI**: Built with PyQt5 for a professional user experience
- **Enhanced Status Bar**: Loading animations and real-time feedback
- **Chatbot Assistant**: Integrated help system for user guidance
- **Certificate Generation**: PDF certificates for completed operations

### Gamification & Environmental Impact
- **Achievement System**: Track user accomplishments and milestones
- **Environmental Dashboard**: Monitor ecological impact of data sanitization
- **Professional Analytics**: Detailed statistics and reporting
- **Leaderboards**: Competitive elements for engagement

## Installation

### Prerequisites
- Python 3.8 or higher
- Windows, Linux, or macOS

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/zero-trace.git
   cd zero-trace
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python zero_trace_gui.py
   ```

## Usage

### Basic Operations
1. Launch the application using `zero_trace_gui.py`
2. Select files, folders, or drives to sanitize
3. Choose your preferred wiping method
4. Configure additional options (free space wiping, enhanced metadata)
5. Start the secure wipe process
6. Monitor progress and receive completion certificates

### Advanced Features
- **Gamification**: Access the environmental impact dashboard to track your achievements
- **Chatbot**: Use the integrated assistant for help and guidance
- **Audit Logs**: Review detailed operation history in the audit system

## Security Methods

- **DoD 5220.22-M**: 3-pass Department of Defense standard
- **Gutmann Method**: 35-pass maximum security wiping
- **Random Data**: Customizable passes with random data patterns
- **Zero Fill**: Single-pass zero overwrite for quick sanitization

## Project Structure

```
zero-trace/
├── zero_trace_gui.py              # Main GUI application
├── zero_trace_enhanced.py         # Enhanced version with improved UI
├── file_secure_wipe_optimized.py  # Core wiping engine
├── chatbot3.py                    # Help system
├── gamification_engine.py         # Achievement system
├── professional_gamification.py   # Environmental dashboard
├── audit_logger.py                # Compliance and logging
├── main_fixed.py                  # Alternative entry point
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Security Notice

⚠️ **WARNING**: This software permanently deletes data. Always backup important files before use. The developers are not responsible for accidental data loss.

## Support

For support and questions:
- Create an issue on GitHub
- Use the in-app chatbot assistant
- Review the comprehensive audit logs for troubleshooting

## Acknowledgments

- Smart India Hackathon 2025
- PyQt5 development team
- Open-source security community
