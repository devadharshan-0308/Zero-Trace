"""
Comprehensive Logging and Audit Trail System
Maintains detailed logs of all wipe operations for compliance and auditing
"""

import logging
import json
import os
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
import hashlib
import threading

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    AUDIT = "AUDIT"

class AuditLogger:
    """Comprehensive audit logging system for secure wipe operations"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        self.db_path = os.path.join(log_dir, "audit_trail.db")
        self._lock = threading.Lock()
        
        # Create log directory
        os.makedirs(log_dir, exist_ok=True)
        
        # Initialize database
        self._init_database()
        
        # Setup file logging
        self._setup_file_logging()
        
        # Setup audit logging
        self._setup_audit_logging()
    
    def _init_database(self):
        """Initialize audit database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Audit events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                session_id TEXT,
                user_id TEXT,
                device_path TEXT,
                event_data TEXT,
                checksum TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Wipe sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wipe_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                device_path TEXT NOT NULL,
                device_serial TEXT,
                wipe_method TEXT,
                start_time TEXT,
                end_time TEXT,
                status TEXT,
                verification_hash TEXT,
                certificate_id TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # System events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                level TEXT NOT NULL,
                component TEXT,
                message TEXT,
                details TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _setup_file_logging(self):
        """Setup file-based logging"""
        # Main application log
        self.app_logger = logging.getLogger('securewipe_app')
        self.app_logger.setLevel(logging.DEBUG)
        
        app_handler = logging.FileHandler(
            os.path.join(self.log_dir, 'application.log'),
            encoding='utf-8'
        )
        app_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        app_handler.setFormatter(app_formatter)
        self.app_logger.addHandler(app_handler)
        
        # Error log
        self.error_logger = logging.getLogger('securewipe_errors')
        self.error_logger.setLevel(logging.ERROR)
        
        error_handler = logging.FileHandler(
            os.path.join(self.log_dir, 'errors.log'),
            encoding='utf-8'
        )
        error_handler.setFormatter(app_formatter)
        self.error_logger.addHandler(error_handler)
    
    def _setup_audit_logging(self):
        """Setup audit-specific logging"""
        self.audit_logger = logging.getLogger('securewipe_audit')
        self.audit_logger.setLevel(logging.INFO)
        
        audit_handler = logging.FileHandler(
            os.path.join(self.log_dir, 'audit_trail.log'),
            encoding='utf-8'
        )
        audit_formatter = logging.Formatter(
            '%(asctime)s - AUDIT - %(message)s'
        )
        audit_handler.setFormatter(audit_formatter)
        self.audit_logger.addHandler(audit_handler)
    
    def log_system_event(self, level: LogLevel, component: str, message: str, details: Dict = None):
        """Log system events"""
        with self._lock:
            timestamp = datetime.now().isoformat()
            
            # Log to file
            if level == LogLevel.ERROR or level == LogLevel.CRITICAL:
                self.error_logger.error(f"{component}: {message}")
            
            self.app_logger.log(
                getattr(logging, level.value),
                f"{component}: {message}"
            )
            
            # Store in database
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO system_events (timestamp, level, component, message, details)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    timestamp,
                    level.value,
                    component,
                    message,
                    json.dumps(details) if details else None
                ))
                
                conn.commit()
                conn.close()
                
            except Exception as e:
                print(f"Failed to log system event: {e}")
    
    def log_audit_event(self, event_type: str, session_id: str = None, 
                       user_id: str = None, device_path: str = None, 
                       event_data: Dict = None):
        """Log audit events with tamper-proof checksum"""
        with self._lock:
            timestamp = datetime.now().isoformat()
            
            # Create event record
            event_record = {
                'timestamp': timestamp,
                'event_type': event_type,
                'session_id': session_id,
                'user_id': user_id,
                'device_path': device_path,
                'event_data': event_data or {}
            }
            
            # Generate checksum for tamper detection
            event_json = json.dumps(event_record, sort_keys=True)
            checksum = hashlib.sha256(event_json.encode()).hexdigest()
            
            # Log to audit file
            audit_message = f"{event_type} - Session: {session_id} - Device: {device_path}"
            self.audit_logger.info(audit_message)
            
            # Store in database
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO audit_events 
                    (timestamp, event_type, session_id, user_id, device_path, event_data, checksum)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    timestamp,
                    event_type,
                    session_id,
                    user_id,
                    device_path,
                    json.dumps(event_data) if event_data else None,
                    checksum
                ))
                
                conn.commit()
                conn.close()
                
            except Exception as e:
                self.log_system_event(
                    LogLevel.ERROR, 
                    "AuditLogger", 
                    f"Failed to store audit event: {e}"
                )
    
    def log_wipe_session(self, session_data: Dict):
        """Log complete wipe session"""
        with self._lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                device_info = session_data.get('device_info', {})
                
                cursor.execute('''
                    INSERT OR REPLACE INTO wipe_sessions 
                    (session_id, device_path, device_serial, wipe_method, 
                     start_time, end_time, status, verification_hash, certificate_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    session_data.get('session_id'),
                    session_data.get('device_path'),
                    device_info.get('serial_number'),
                    session_data.get('wipe_method'),
                    session_data.get('start_time'),
                    session_data.get('end_time'),
                    session_data.get('status'),
                    session_data.get('verification_hash'),
                    session_data.get('certificate', {}).get('certificate_id')
                ))
                
                conn.commit()
                conn.close()
                
                # Log audit event
                self.log_audit_event(
                    'WIPE_SESSION_COMPLETED',
                    session_data.get('session_id'),
                    device_path=session_data.get('device_path'),
                    event_data={
                        'status': session_data.get('status'),
                        'method': session_data.get('wipe_method'),
                        'duration': self._calculate_duration(
                            session_data.get('start_time'),
                            session_data.get('end_time')
                        )
                    }
                )
                
            except Exception as e:
                self.log_system_event(
                    LogLevel.ERROR,
                    "AuditLogger",
                    f"Failed to log wipe session: {e}"
                )
    
    def _calculate_duration(self, start_time: str, end_time: str) -> Optional[float]:
        """Calculate duration between timestamps"""
        try:
            if not start_time or not end_time:
                return None
            
            start = datetime.fromisoformat(start_time)
            end = datetime.fromisoformat(end_time)
            
            return (end - start).total_seconds()
            
        except Exception:
            return None
    
    def get_audit_trail(self, session_id: str = None, 
                       start_date: str = None, end_date: str = None,
                       event_type: str = None) -> List[Dict]:
        """Retrieve audit trail with filters"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "SELECT * FROM audit_events WHERE 1=1"
            params = []
            
            if session_id:
                query += " AND session_id = ?"
                params.append(session_id)
            
            if start_date:
                query += " AND timestamp >= ?"
                params.append(start_date)
            
            if end_date:
                query += " AND timestamp <= ?"
                params.append(end_date)
            
            if event_type:
                query += " AND event_type = ?"
                params.append(event_type)
            
            query += " ORDER BY timestamp DESC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            
            audit_trail = []
            for row in rows:
                audit_trail.append({
                    'id': row[0],
                    'timestamp': row[1],
                    'event_type': row[2],
                    'session_id': row[3],
                    'user_id': row[4],
                    'device_path': row[5],
                    'event_data': json.loads(row[6]) if row[6] else {},
                    'checksum': row[7],
                    'created_at': row[8]
                })
            
            return audit_trail
            
        except Exception as e:
            self.log_system_event(
                LogLevel.ERROR,
                "AuditLogger",
                f"Failed to retrieve audit trail: {e}"
            )
            return []
    
    def get_wipe_sessions(self, device_path: str = None, 
                         status: str = None) -> List[Dict]:
        """Retrieve wipe sessions with filters"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "SELECT * FROM wipe_sessions WHERE 1=1"
            params = []
            
            if device_path:
                query += " AND device_path = ?"
                params.append(device_path)
            
            if status:
                query += " AND status = ?"
                params.append(status)
            
            query += " ORDER BY created_at DESC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            
            sessions = []
            for row in rows:
                sessions.append({
                    'id': row[0],
                    'session_id': row[1],
                    'device_path': row[2],
                    'device_serial': row[3],
                    'wipe_method': row[4],
                    'start_time': row[5],
                    'end_time': row[6],
                    'status': row[7],
                    'verification_hash': row[8],
                    'certificate_id': row[9],
                    'created_at': row[10]
                })
            
            return sessions
            
        except Exception as e:
            self.log_system_event(
                LogLevel.ERROR,
                "AuditLogger",
                f"Failed to retrieve wipe sessions: {e}"
            )
            return []
    
    def verify_audit_integrity(self) -> Dict:
        """Verify integrity of audit trail"""
        integrity_result = {
            'valid': True,
            'total_events': 0,
            'corrupted_events': 0,
            'corrupted_ids': []
        }
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM audit_events")
            rows = cursor.fetchall()
            conn.close()
            
            integrity_result['total_events'] = len(rows)
            
            for row in rows:
                # Reconstruct event record
                event_record = {
                    'timestamp': row[1],
                    'event_type': row[2],
                    'session_id': row[3],
                    'user_id': row[4],
                    'device_path': row[5],
                    'event_data': json.loads(row[6]) if row[6] else {}
                }
                
                # Recalculate checksum
                event_json = json.dumps(event_record, sort_keys=True)
                calculated_checksum = hashlib.sha256(event_json.encode()).hexdigest()
                
                # Compare with stored checksum
                if calculated_checksum != row[7]:
                    integrity_result['corrupted_events'] += 1
                    integrity_result['corrupted_ids'].append(row[0])
                    integrity_result['valid'] = False
            
        except Exception as e:
            integrity_result['valid'] = False
            integrity_result['error'] = str(e)
        
        return integrity_result
    
    def generate_compliance_report(self, start_date: str = None, 
                                 end_date: str = None) -> Dict:
        """Generate compliance report for auditing"""
        report = {
            'report_id': hashlib.md5(f"{datetime.now().isoformat()}".encode()).hexdigest()[:8],
            'generated_at': datetime.now().isoformat(),
            'period': {
                'start_date': start_date or '1970-01-01',
                'end_date': end_date or datetime.now().isoformat()
            },
            'summary': {},
            'wipe_sessions': [],
            'audit_events': [],
            'integrity_check': {}
        }
        
        # Get wipe sessions in period
        sessions = self.get_wipe_sessions()
        if start_date or end_date:
            filtered_sessions = []
            for session in sessions:
                session_date = session.get('created_at', '')
                if start_date and session_date < start_date:
                    continue
                if end_date and session_date > end_date:
                    continue
                filtered_sessions.append(session)
            sessions = filtered_sessions
        
        report['wipe_sessions'] = sessions
        
        # Get audit events in period
        audit_events = self.get_audit_trail(start_date=start_date, end_date=end_date)
        report['audit_events'] = audit_events
        
        # Generate summary statistics
        report['summary'] = {
            'total_wipe_sessions': len(sessions),
            'successful_wipes': len([s for s in sessions if s['status'] == 'completed']),
            'failed_wipes': len([s for s in sessions if s['status'] == 'failed']),
            'total_audit_events': len(audit_events),
            'devices_wiped': len(set(s['device_path'] for s in sessions)),
            'compliance_standard': 'NIST SP 800-88'
        }
        
        # Verify audit integrity
        report['integrity_check'] = self.verify_audit_integrity()
        
        return report
    
    def export_logs(self, output_dir: str, format_type: str = 'json') -> bool:
        """Export logs for external analysis"""
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            # Export audit events
            audit_events = self.get_audit_trail()
            audit_file = os.path.join(output_dir, f'audit_events.{format_type}')
            
            with open(audit_file, 'w', encoding='utf-8') as f:
                if format_type == 'json':
                    json.dump(audit_events, f, indent=2, ensure_ascii=False)
                else:
                    # CSV format
                    import csv
                    if audit_events:
                        writer = csv.DictWriter(f, fieldnames=audit_events[0].keys())
                        writer.writeheader()
                        writer.writerows(audit_events)
            
            # Export wipe sessions
            sessions = self.get_wipe_sessions()
            sessions_file = os.path.join(output_dir, f'wipe_sessions.{format_type}')
            
            with open(sessions_file, 'w', encoding='utf-8') as f:
                if format_type == 'json':
                    json.dump(sessions, f, indent=2, ensure_ascii=False)
                else:
                    if sessions:
                        writer = csv.DictWriter(f, fieldnames=sessions[0].keys())
                        writer.writeheader()
                        writer.writerows(sessions)
            
            self.log_system_event(
                LogLevel.INFO,
                "AuditLogger",
                f"Logs exported to {output_dir}"
            )
            
            return True
            
        except Exception as e:
            self.log_system_event(
                LogLevel.ERROR,
                "AuditLogger",
                f"Failed to export logs: {e}"
            )
            return False
