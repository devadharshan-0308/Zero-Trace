# 🔷 Zero-Trace - Complete Cross-Platform Secure Data Sanitization Suite

Welcome to Zero-Trace, a comprehensive secure data sanitization solution featuring both desktop PyQt5 application and Android companion app. This suite provides enterprise-grade security with environmental impact tracking across all platforms.

**🌟 Dual-Platform Solution:** Desktop Application + Android Companion App

## 🏆 About the Project

Zero-Trace is a complete cross-platform data sanitization suite that includes:

- **🖥️ Desktop Application** - Professional device and file sanitization with gamification
- **📱 Android Companion** - Mobile secure file wiping with USB bridge communication
- **🌍 Environmental Tracking** - Real CO₂ savings and sustainability metrics
- **🏆 Achievement System** - Gamified engagement for best practices
- **📜 Compliance Reporting** - NIST SP 800-88 and DoD 5220.22-M standards

This project combines military-grade security algorithms with modern environmental consciousness and cross-platform functionality.

## 🧩 Problem Statement

Organizations need comprehensive data sanitization across multiple platforms:

🔒 **Desktop secure data destruction** with compliance requirements  
📱 **Mobile device file management** for field operations  
📊 **Environmental impact tracking** for sustainability reporting  
📜 **Professional certification** for audit trails  
🎯 **Cross-platform consistency** for unified security policies

**Our Solution:** Desktop military-grade wiping + Mobile secure deletion + Environmental tracking + Professional gamification

## 📦 Project Distribution

This project is distributed in **two components**:

1. **🖥️ Zero-Trace Desktop** - Distributed as ZIP file (extract and run)
2. **📱 Android Companion** - Source code in `android_companion/` folder (build with Android Studio)

Both components work together via USB bridge for complete cross-platform data sanitization.

## 🌟 Complete Feature Set

### 🖥️ Desktop Application Features

#### Professional Data Sanitization
- **NIST SP 800-88 Clear** (3 passes) - Industry Standard
- **DoD 5220.22-M 3-Pass** - Military Standard  
- **DoD 5220.22-M 7-Pass** - High Security
- **Gutmann 35-Pass** - Maximum Security
- **Entire device wiping** and **selective file deletion**

#### Environmental & Gamification
- **Real-time CO₂ tracking** - Environmental impact calculations
- **Achievement system** - Sustainability badges and points
- **Professional dashboard** - Impact metrics and progress
- **Social sharing** - Certificate sharing capabilities

#### Compliance & Reporting
- **PDF certificates** with QR codes for verification
- **JSON compliance reports** for audit trails
- **Environmental impact reports** for corporate sustainability
- **Automatic documentation** generation

### 📱 Android Companion Features

#### Mobile Secure Deletion
- **3-pass secure wiping** algorithm (Zero → Ones → Random)
- **Text file support** (.txt files) with native file picker
- **Complete file deletion** after secure overwriting
- **Real-time operation logging** with detailed status

#### Cross-Platform Communication
- **TCP socket server** (localhost:5555) for bridge communication
- **USB debugging integration** for seamless laptop connection
- **ADB bridge support** for automated operations
- **Error handling** with comprehensive status reporting

## 🚀 Complete Setup Guide

### Method 1: 🖥️ Desktop Application Setup

#### Step 1: Download and Extract
```bash
# Download Zero-Trace ZIP file from repository
# Extract to your preferred location
unzip Zero-Trace.zip
cd Zero-Trace
```

#### Step 2: Install Python Dependencies
```bash
# Verify Python installation (3.7+ required)
python --version

# Install required packages
pip install PyQt5 psutil qrcode reportlab

# Alternative: Install from requirements file
pip install -r requirements.txt
```

#### Step 3: Run Desktop Application
```bash
# Launch the main application
python main_fixed.py

# For Windows users - alternative methods:
# Method 1: Right-click main_fixed.py → "Open with" → "Python"
# Method 2: Double-click if Python is associated with .py files
```

#### Step 4: Desktop Usage
```bash
# In the GUI application:
1. Select "Entire Storage Device" for complete drive sanitization
2. Choose "Specific Files/Folders" for targeted deletion
3. Pick security method (NIST recommended for compliance)
4. Monitor environmental impact in dashboard
5. Generate certificates after completion
```

### Method 2: 📱 Android Companion Setup

#### Prerequisites
- **Android Studio** installed on your computer
- **Android device** with USB debugging enabled
- **ADB (Android Debug Bridge)** installed and in system PATH
- **USB cable** for device connection

#### Step 1: Prepare Development Environment
```bash
# Install Android Studio from: https://developer.android.com/studio
# Install Android SDK and platform tools
# Add ADB to system PATH

# Verify ADB installation
adb --version
```

#### Step 2: Prepare Android Device
```bash
# Enable Developer Options on Android device:
1. Go to Settings → About Phone
2. Tap "Build Number" 7 times until "Developer mode enabled"
3. Go back to Settings → Developer Options
4. Enable "USB Debugging"
5. Connect device via USB cable
6. Authorize computer when prompted on device screen
```

#### Step 3: Build Android App
```bash
# In Android Studio:
1. Create new project with Kotlin support
2. Set package name: com.example.securewipecompanion
3. Copy files from android_companion/ folder to appropriate locations:
   
   Source Files:
   - MainActivity.kt → app/src/main/java/com/example/securewipecompanion/
   - WipeService.kt → app/src/main/java/com/example/securewipecompanion/
   
   Configuration Files:
   - AndroidManifest.xml → app/src/main/
   - activity_main.xml → app/src/main/res/layout/

4. Build APK: Build → Build Bundle(s)/APK(s) → Build APK(s)
```

#### Step 4: Install Android App
```bash
# Install APK on connected device
adb install app-debug.apk

# Verify installation
adb shell pm list packages | grep securewipe

# Check device connection
adb devices
```

#### Step 5: Android App Usage
```bash
# On Android device:
1. Open "SecureWipe Companion" app
2. Click "Pick File to Wipe"
3. Select any .txt file from device storage
4. Click "Start WipeService (Server)" - this starts TCP server
5. App will show "Service running on port 5555"
```

### Method 3: 🔗 Cross-Platform Bridge Operation

#### Step 1: Connect Devices
```bash
# Ensure Android device is connected and app is running
# Forward TCP port from device to laptop
adb forward tcp:5555 tcp:5555

# Verify port forwarding
adb forward --list
```

#### Step 2: Execute Cross-Platform Wipe
```bash
# On laptop - navigate to Zero-Trace directory
cd Zero-Trace

# Test connection to Android service
python AndroidBridge.py

# Wipe specific file on Android device
python wipe_text_files.py

# When prompted, enter file path (examples):
# /sdcard/Documents/secret.txt
# /sdcard/Downloads/confidential.txt
# /storage/emulated/0/Documents/private.txt

# Confirm deletion by typing 'YES'
# File will be securely wiped with 3-pass algorithm
```

#### Step 3: Verify Operation
```bash
# Check operation logs on Android device (in app)
# Verify file no longer exists:
adb shell ls "/sdcard/Documents/secret.txt"
# Should return "No such file or directory"
```

## 📁 Complete Project Structure

```
📦 Zero-Trace/ (Main Project Directory)
 ┣ 📁 Desktop Application/
 ┃ ┣ 📄 main_fixed.py                    # 🚀 Main entry point
 ┃ ┣ 📄 zero_trace_enhanced.py           # 🎨 Enhanced GUI with loading bar
 ┃ ┣ 📄 zero_trace_gui.py               # 🖥️ Base GUI implementation
 ┃ ┣ 📄 professional_gamification.py     # 🏆 Environmental dashboard
 ┃ ┣ 📄 gamification_engine.py          # 🎮 Achievement system
 ┃ ┣ 📄 file_secure_wipe_optimized.py   # 🔧 Secure wipe backend
 ┃ ┣ 📄 chatbot3.py                     # 🤖 AI assistant
 ┃ ┗ 📄 shareable_certificate.py        # 📱 Social sharing
 ┣ 📁 android_companion/ (Android Source Files)
 ┃ ┣ 📄 MainActivity.kt                  # Android main activity
 ┃ ┣ 📄 WipeService.kt                  # Mobile secure wipe service
 ┃ ┣ 📄 AndroidManifest.xml             # App permissions & configuration
 ┃ ┗ 📄 activity_main.xml               # Mobile UI layout
 ┣ 📁 Cross-Platform Bridge/
 ┃ ┣ 📄 AndroidBridge.py                # 🌉 Desktop-mobile bridge
 ┃ ┗ 📄 wipe_text_files.py             # 📱 Mobile file wiper CLI
 ┣ 📄 requirements.txt                  # 📦 Python dependencies
 ┣ 📄 README.md                         # 📖 This documentation
 ┣ 📁 certificates/                     # 📜 Generated certificates (auto-created)
 ┣ 📄 gamification.db                   # 💾 Achievement database (auto-created)
 ┗ 📄 verification_records.db           # 📊 Audit database (auto-created)
```

## 📌 System Requirements

### Desktop Requirements
- **Operating System**: Windows 10/11 (recommended), Linux, macOS
- **Python**: Version 3.7 or higher
- **Storage**: 100MB free disk space
- **Privileges**: Administrator rights for device-level operations
- **Memory**: 512MB RAM minimum

### Android Development Requirements
- **Android Studio**: Latest version with Kotlin support
- **Android SDK**: API level 21+ (Android 5.0+)
- **Development Machine**: Windows/Mac/Linux with 4GB+ RAM
- **USB Cable**: For device connection and debugging

### Android Device Requirements
- **Android Version**: 5.0+ (API level 21+)
- **Storage**: 10MB for app installation
- **Permissions**: USB debugging capability
- **File System**: Access to internal storage for file selection

### Python Dependencies
```
PyQt5>=5.15.0          # GUI framework
psutil>=5.8.0           # System information
qrcode>=7.3.1           # QR code generation
reportlab>=3.6.0        # PDF generation
```

## 🔧 Technical Implementation Details

### Desktop Security Algorithms
```python
# Multi-pass wiping implementation
SECURITY_METHODS = {
    'NIST_CLEAR': 3,        # Industry standard (recommended)
    'DOD_3_PASS': 3,        # Military standard
    'DOD_7_PASS': 7,        # High security
    'GUTMANN': 35           # Maximum security
}
```

### Android Security Protocol
```kotlin
// 3-pass secure deletion implementation
// Pass 1: Overwrite with zeros (0x00)
// Pass 2: Overwrite with ones (0xFF)
// Pass 3: Overwrite with random data
// Final: Delete file from filesystem with sync
```

### Cross-Platform Communication
```json
// TCP Socket Protocol (localhost:5555)
{
  "ping": {"action": "ping"},
  "wipe": {"action": "wipe", "path": "/sdcard/file.txt"},
  "response": {"status": "success", "message": "File wiped"}
}
```

## 🛠️ Troubleshooting Guide

### Desktop Application Issues

**"Python not found" Error:**
```bash
# Install Python from python.org (3.7+)
# Or install from Microsoft Store
python --version  # Verify installation
```

**"Module not found" Error:**
```bash
# Install missing dependencies
pip install -r requirements.txt
# Or install individually:
pip install PyQt5 psutil qrcode reportlab
```

**"Permission denied" Error:**
- Right-click application and select "Run as Administrator"
- Ensure you have admin privileges for device operations
- Check antivirus software isn't blocking the application

### Android Development Issues

**"ADB not found" Error:**
```bash
# Install Android Platform Tools
# Add ADB to system PATH environment variable
# Verify installation: adb --version
```

**"No device detected" Error:**
- Enable USB debugging on Android device
- Authorize computer when prompted on device
- Try different USB cable or port
- Check device manager for driver issues
- Verify: `adb devices`

**"Build failed in Android Studio":**
- Ensure correct package name: com.example.securewipecompanion
- Check all files are in correct directories
- Verify Android SDK is properly installed
- Clean and rebuild project

### Cross-Platform Communication Issues

**"Connection refused" Error:**
- Ensure SecureWipe Companion app is open on Android
- Click "Start WipeService" button in the app
- Verify port forwarding: `adb forward tcp:5555 tcp:5555`
- Check firewall settings on laptop

**"File not found on Android" Error:**
- Use absolute file paths: `/sdcard/Documents/file.txt`
- Check file exists: `adb shell ls "/path/to/file.txt"`
- Ensure file has .txt extension
- Verify file permissions allow reading

## 🎯 Usage Examples & Workflows

### Desktop-Only Operations
```bash
# Launch desktop application
python main_fixed.py

# Workflow:
1. Select security method (NIST Clear recommended)
2. Choose target (entire device or specific files)
3. Monitor progress in real-time
4. View environmental impact dashboard
5. Generate and save compliance certificates
```

### Mobile-Only Operations
```bash
# On Android device:
1. Open SecureWipe Companion app
2. Tap "Pick File to Wipe"
3. Select .txt file from device storage
4. Tap "Start WipeService"
5. File is automatically wiped with 3-pass algorithm
```

### Cross-Platform Operations
```bash
# Combined desktop-mobile workflow:
1. Connect Android device via USB
2. Enable USB debugging and authorize computer
3. Install and open SecureWipe Companion app
4. Start WipeService on Android
5. Run: python wipe_text_files.py on laptop
6. Enter file path when prompted
7. Confirm with 'YES' for secure deletion
8. Verify operation in desktop dashboard
```

## ⚠️ Security Warnings & Best Practices

### Critical Security Warnings
- **⚠️ Data destruction is permanent** and cannot be undone
- **⚠️ Always backup critical data** before sanitization
- **⚠️ Test on non-production systems** first
- **⚠️ USB debugging poses security risks** - disable after use
- **⚠️ Verify compliance requirements** for your organization

### Best Practices
- **✅ Use NIST Clear method** for standard compliance
- **✅ Generate certificates** for all operations
- **✅ Maintain audit logs** for regulatory compliance
- **✅ Test file paths** before bulk operations
- **✅ Monitor environmental impact** for sustainability reporting

### Current Limitations
- **📱 Mobile wiping supports text files only** (.txt extension)
- **🔗 USB connection required** for cross-platform operations
- **🖥️ Administrator privileges needed** for device-level desktop operations
- **📱 Android 5.0+ required** for companion app

## 💡 Future Development Roadmap

### Short-term Improvements
- **📶 Wireless communication** between desktop and mobile (eliminate USB requirement)
- **📄 Enhanced file type support** on Android (images, documents, videos)
- **🔐 Advanced encryption** for bridge communication
- **📊 Real-time sync** of environmental metrics across platforms

### Long-term Vision
- **☁️ Cloud dashboard integration** for enterprise deployment
- **🔗 Blockchain certificates** for tamper-proof verification
- **🌐 Multi-language support** for global deployment
- **🤖 IoT device integration** for automated e-waste processing
- **📱 iOS companion app** for complete mobile coverage

## 🌍 Environmental Impact & Sustainability

### Real Environmental Benefits
```
Per Device Sanitized:
├── 50kg CO₂ emissions saved
├── 2kg e-waste prevented from landfills
├── 1000L water consumption avoided
└── 200kWh energy usage prevented
```

### Achievement System
- **🚀 First Step** - Complete first wipe (100 points)
- **🌱 Eco Saver** - Wipe 10 devices (500 points)
- **🛡️ Data Guardian** - Wipe 50 devices (1000 points)
- **🏆 Recycling Champion** - Wipe 100 devices (2000 points)
- **🌍 Carbon Neutral Hero** - Save 1000kg CO₂ (1500 points)

## 📱 Cross-Platform Advantages

### Unified Benefits
✅ **Consistent security standards** across desktop and mobile platforms  
✅ **Unified environmental tracking** with combined impact metrics  
✅ **Seamless USB bridge communication** for integrated operations  
✅ **Professional compliance documentation** across all devices  
✅ **Portable deployment** - runs from any directory or USB drive  
✅ **No cloud dependency** - fully offline operation for security

### Enterprise Applications
- **🏢 Corporate IT departments** - Unified device sanitization policy
- **🔒 Security firms** - Cross-platform data destruction services  
- **♻️ E-waste facilities** - Professional sanitization with documentation
- **🏛️ Government agencies** - Compliance-ready data destruction
- **🎓 Educational institutions** - Sustainable technology practices

## ✨ Created By
- Jayasri S
- Devadharshan G
- Krithika S
- J Jeswanth Singh
- Vishal K
- Vishnusairam Raju

## 📜 License & Legal

**MIT License** - Open source for educational and professional use

### Legal Disclaimers
- This software is designed to permanently destroy data - this is its intended function
- Users are responsible for ensuring proper authorization before data destruction
- Always verify compliance requirements for your specific organization and jurisdiction
- The developers are not responsible for any data loss resulting from proper use of this tool

---

**🌍 Environmental Mission:** Every secure wipe across desktop and mobile platforms contributes to reducing e-waste and promoting sustainable technology practices worldwide.

**🔒 Security Promise:** Military-grade data destruction with full compliance documentation and environmental responsibility across all platforms and devices.

**🚀 Innovation Commitment:** Bridging enterprise security between desktop and mobile devices for comprehensive, future-ready data protection solutions.

