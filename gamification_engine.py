"""
Gamification Engine for SecureWipe India
Tracks user achievements, scores, and environmental impact
"""
import json
import os
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

class AchievementType(Enum):
    ECO_WARRIOR = "eco_warrior"
    DATA_GUARDIAN = "data_guardian"
    RECYCLING_CHAMP = "recycling_champ"
    SECURITY_EXPERT = "security_expert"

class GamificationEngine:
    def __init__(self, db_path: str = "gamification.db"):
        self.db_path = db_path
        self._init_database()
        
        # Environmental impact constants (per device)
        self.ECO_IMPACT = {
            'co2_saved_kg': 50,  # kg CO2 saved per device recycled
            'ewaste_saved_kg': 2,  # kg e-waste prevented
            'water_saved_liters': 1000,  # liters water saved
            'energy_saved_kwh': 200  # kWh energy saved
        }
        
        # Achievement definitions
        self.ACHIEVEMENTS = {
            'first_wipe': {
                'name': 'First Step',
                'description': 'Complete your first secure wipe',
                'points': 100,
                'icon': '🚀'
            },
            'eco_saver_10': {
                'name': 'Eco Saver',
                'description': 'Securely wipe 10 devices',
                'points': 500,
                'icon': '🌱'
            },
            'data_guardian_50': {
                'name': 'Data Guardian',
                'description': 'Wipe 50 devices securely',
                'points': 1000,
                'icon': '🛡️'
            },
            'recycling_champ_100': {
                'name': 'Recycling Champion',
                'description': 'Reach 100 devices wiped',
                'points': 2000,
                'icon': '🏆'
            },
            'carbon_neutral': {
                'name': 'Carbon Neutral Hero',
                'description': 'Save 1000kg CO2 through recycling',
                'points': 1500,
                'icon': '🌍'
            }
        }

    def _init_database(self):
        """Initialize gamification database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # User stats table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_stats (
                user_id TEXT PRIMARY KEY,
                total_devices_wiped INTEGER DEFAULT 0,
                total_files_wiped INTEGER DEFAULT 0,
                total_co2_saved_kg REAL DEFAULT 0,
                total_ewaste_saved_kg REAL DEFAULT 0,
                total_points INTEGER DEFAULT 0,
                current_level INTEGER DEFAULT 1,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        # Achievements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                achievement_id TEXT,
                achieved_at TEXT,
                points_earned INTEGER
            )
        ''')
        
        # Wipe sessions table for tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wipe_sessions_gamified (
                session_id TEXT PRIMARY KEY,
                user_id TEXT,
                device_count INTEGER DEFAULT 0,
                file_count INTEGER DEFAULT 0,
                co2_saved_kg REAL DEFAULT 0,
                ewaste_saved_kg REAL DEFAULT 0,
                session_date TEXT,
                method_used TEXT
            )
        ''')
        
        conn.commit()
        conn.close()

    def record_wipe_session(self, user_id: str, device_count: int = 0, 
                          file_count: int = 0, method: str = "unknown") -> Dict:
        """Record a wipe session and calculate impact"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Calculate environmental impact
        co2_saved = device_count * self.ECO_IMPACT['co2_saved_kg']
        ewaste_saved = device_count * self.ECO_IMPACT['ewaste_saved_kg']
        
        # Store session
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO wipe_sessions_gamified 
            (session_id, user_id, device_count, file_count, co2_saved_kg, ewaste_saved_kg, session_date, method_used)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session_id, user_id, device_count, file_count, co2_saved, ewaste_saved, 
              datetime.now().isoformat(), method))
        
        # Update user stats
        cursor.execute('''
            INSERT OR REPLACE INTO user_stats 
            (user_id, total_devices_wiped, total_files_wiped, total_co2_saved_kg, 
             total_ewaste_saved_kg, total_points, updated_at)
            VALUES (?, 
                    COALESCE((SELECT total_devices_wiped FROM user_stats WHERE user_id = ?), 0) + ?,
                    COALESCE((SELECT total_files_wiped FROM user_stats WHERE user_id = ?), 0) + ?,
                    COALESCE((SELECT total_co2_saved_kg FROM user_stats WHERE user_id = ?), 0) + ?,
                    COALESCE((SELECT total_ewaste_saved_kg FROM user_stats WHERE user_id = ?), 0) + ?,
                    COALESCE((SELECT total_points FROM user_stats WHERE user_id = ?), 0),
                    ?)
        ''', (user_id, user_id, device_count, user_id, file_count, user_id, co2_saved, 
              user_id, ewaste_saved, user_id, datetime.now().isoformat()))
        
        # Set created_at for new users
        cursor.execute('''
            UPDATE user_stats SET created_at = COALESCE(created_at, ?) WHERE user_id = ?
        ''', (datetime.now().isoformat(), user_id))
        
        conn.commit()
        conn.close()
        
        # Check for new achievements
        new_achievements = self._check_achievements(user_id)
        
        return {
            'session_id': session_id,
            'co2_saved_kg': co2_saved,
            'ewaste_saved_kg': ewaste_saved,
            'points_earned': device_count * 10 + file_count * 1,
            'new_achievements': new_achievements
        }

    def _check_achievements(self, user_id: str) -> List[Dict]:
        """Check and award new achievements"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get user stats
        cursor.execute('SELECT total_devices_wiped, total_co2_saved_kg FROM user_stats WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        
        if not result:
            return []
            
        devices_wiped, co2_saved = result
        
        # Check existing achievements
        cursor.execute('SELECT achievement_id FROM user_achievements WHERE user_id = ?', (user_id,))
        existing_achievements = [row[0] for row in cursor.fetchall()]
        
        new_achievements = []
        
        # Check each achievement condition
        if 'first_wipe' not in existing_achievements and devices_wiped >= 1:
            achievement = self._award_achievement(user_id, 'first_wipe')
            if achievement:
                new_achievements.append(achievement)
                
        if 'eco_saver_10' not in existing_achievements and devices_wiped >= 10:
            achievement = self._award_achievement(user_id, 'eco_saver_10')
            if achievement:
                new_achievements.append(achievement)
                
        if 'data_guardian_50' not in existing_achievements and devices_wiped >= 50:
            achievement = self._award_achievement(user_id, 'data_guardian_50')
            if achievement:
                new_achievements.append(achievement)
                
        if 'carbon_neutral' not in existing_achievements and co2_saved >= 1000:
            achievement = self._award_achievement(user_id, 'carbon_neutral')
            if achievement:
                new_achievements.append(achievement)
        
        conn.close()
        return new_achievements

    def _award_achievement(self, user_id: str, achievement_id: str) -> Optional[Dict]:
        """Award an achievement to user"""
        if achievement_id not in self.ACHIEVEMENTS:
            return None
            
        achievement = self.ACHIEVEMENTS[achievement_id]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if already awarded
        cursor.execute('SELECT 1 FROM user_achievements WHERE user_id = ? AND achievement_id = ?', 
                      (user_id, achievement_id))
        if cursor.fetchone():
            return None
        
        # Award achievement
        cursor.execute('''
            INSERT INTO user_achievements (user_id, achievement_id, achieved_at, points_earned)
            VALUES (?, ?, ?, ?)
        ''', (user_id, achievement_id, datetime.now().isoformat(), achievement['points']))
        
        # Update user points
        cursor.execute('''
            UPDATE user_stats SET total_points = total_points + ? WHERE user_id = ?
        ''', (achievement['points'], user_id))
        
        conn.commit()
        conn.close()
        
        return {
            'id': achievement_id,
            'name': achievement['name'],
            'description': achievement['description'],
            'points': achievement['points'],
            'icon': achievement['icon']
        }

    def get_user_stats(self, user_id: str) -> Dict:
        """Get comprehensive user statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT total_devices_wiped, total_files_wiped, total_co2_saved_kg, 
                   total_ewaste_saved_kg, total_points, current_level
            FROM user_stats WHERE user_id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        
        if not result:
            return {
                'total_devices_wiped': 0,
                'total_files_wiped': 0,
                'total_co2_saved_kg': 0,
                'total_ewaste_saved_kg': 0,
                'total_points': 0,
                'current_level': 1,
                'achievements': []
            }
        
        stats = {
            'total_devices_wiped': result[0],
            'total_files_wiped': result[1],
            'total_co2_saved_kg': result[2],
            'total_ewaste_saved_kg': result[3],
            'total_points': result[4],
            'current_level': result[5],
            'achievements': []
        }
        
        # Get achievements
        cursor.execute('''
            SELECT ua.achievement_id, ua.achieved_at, ua.points_earned
            FROM user_achievements ua
            WHERE ua.user_id = ?
            ORDER BY ua.achieved_at DESC
        ''', (user_id,))
        
        for row in cursor.fetchall():
            achievement_id, achieved_at, points = row
            if achievement_id in self.ACHIEVEMENTS:
                achievement = self.ACHIEVEMENTS[achievement_id].copy()
                achievement['achieved_at'] = achieved_at
                achievement['points_earned'] = points
                stats['achievements'].append(achievement)
        
        conn.close()
        return stats

    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get top users leaderboard"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, total_devices_wiped, total_co2_saved_kg, total_points
            FROM user_stats 
            ORDER BY total_points DESC 
            LIMIT ?
        ''', (limit,))
        
        leaderboard = []
        for rank, row in enumerate(cursor.fetchall(), 1):
            user_id, devices, co2_saved, points = row
            leaderboard.append({
                'rank': rank,
                'user_id': user_id,
                'devices_wiped': devices,
                'co2_saved_kg': co2_saved,
                'points': points
            })
        
        conn.close()
        return leaderboard
