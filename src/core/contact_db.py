"""
联系人数据库管理模块
使用 SQLite 存储联系人和分组
"""
import sqlite3
import os
from datetime import datetime
from typing import List, Optional, Dict, Any


class ContactDatabase:
    """联系人数据库管理"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # 默认保存在用户数据目录
            data_dir = os.path.expanduser("~/.eason")
            os.makedirs(data_dir, exist_ok=True)
            db_path = os.path.join(data_dir, "contacts.db")
        
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 分组表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                color TEXT DEFAULT '#4F46E5',
                icon TEXT DEFAULT '📁',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 联系人表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                name TEXT DEFAULT '',
                group_id INTEGER,
                notes TEXT DEFAULT '',
                interaction_count INTEGER DEFAULT 0,
                last_contact TIMESTAMP,
                first_contact TIMESTAMP,
                send_count INTEGER DEFAULT 0,
                last_send TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE SET NULL
            )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_contacts_email ON contacts(email)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_contacts_group ON contacts(group_id)')
        
        # 插入默认分组
        cursor.execute("SELECT COUNT(*) FROM groups")
        if cursor.fetchone()[0] == 0:
            default_groups = [
                ('全部联系人', '#6B7280', '📋'),
                ('客户', '#10B981', '👥'),
                ('供应商', '#F59E0B', '🏢'),
                ('同事', '#3B82F6', '👔'),
                ('其他', '#8B5CF6', '📌'),
            ]
            # 注意：'全部联系人' 是虚拟分组，不实际存储
            for name, color, icon in default_groups[1:]:
                cursor.execute(
                    "INSERT OR IGNORE INTO groups (name, color, icon) VALUES (?, ?, ?)",
                    (name, color, icon)
                )
        
        conn.commit()
        conn.close()
    
    # ========== 分组管理 ==========
    
    def get_groups(self) -> List[Dict]:
        """获取所有分组"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT g.*, COUNT(c.id) as contact_count 
            FROM groups g 
            LEFT JOIN contacts c ON g.id = c.group_id
            GROUP BY g.id
            ORDER BY g.id
        ''')
        
        groups = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return groups
    
    def create_group(self, name: str, color: str = '#4F46E5', icon: str = '📁') -> int:
        """创建分组"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO groups (name, color, icon) VALUES (?, ?, ?)",
            (name, color, icon)
        )
        group_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        return group_id
    
    def rename_group(self, group_id: int, new_name: str) -> bool:
        """重命名分组"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE groups SET name = ? WHERE id = ?",
            (new_name, group_id)
        )
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        return success
    
    def delete_group(self, group_id: int) -> bool:
        """删除分组（联系人会变成未分组）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 先将该分组的联系人设为未分组
        cursor.execute("UPDATE contacts SET group_id = NULL WHERE group_id = ?", (group_id,))
        cursor.execute("DELETE FROM groups WHERE id = ?", (group_id,))
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        return success
    
    # ========== 联系人管理 ==========
    
    def get_contacts(self, group_id: Optional[int] = None, search: str = '') -> List[Dict]:
        """获取联系人列表"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = '''
            SELECT c.*, g.name as group_name, g.color as group_color
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            WHERE 1=1
        '''
        params = []
        
        if group_id is not None:
            query += ' AND c.group_id = ?'
            params.append(group_id)
        
        if search:
            query += ' AND (c.email LIKE ? OR c.name LIKE ?)'
            params.extend([f'%{search}%', f'%{search}%'])
        
        query += ' ORDER BY c.interaction_count DESC, c.created_at DESC'
        
        cursor.execute(query, params)
        contacts = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return contacts
    
    def get_contact_count(self, group_id: Optional[int] = None) -> int:
        """获取联系人数量"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if group_id is None:
            cursor.execute("SELECT COUNT(*) FROM contacts")
        else:
            cursor.execute("SELECT COUNT(*) FROM contacts WHERE group_id = ?", (group_id,))
        
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def add_contact(self, email: str, name: str = '', group_id: Optional[int] = None,
                    interaction_count: int = 0, last_contact: str = '', 
                    first_contact: str = '') -> int:
        """添加联系人"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO contacts (email, name, group_id, interaction_count, last_contact, first_contact)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (email, name, group_id, interaction_count, 
                  last_contact or None, first_contact or None))
            contact_id = cursor.lastrowid
            conn.commit()
        except sqlite3.IntegrityError:
            # 邮箱已存在，更新信息
            cursor.execute('''
                UPDATE contacts 
                SET name = COALESCE(NULLIF(?, ''), name),
                    interaction_count = interaction_count + ?,
                    last_contact = COALESCE(?, last_contact)
                WHERE email = ?
            ''', (name, interaction_count, last_contact or None, email))
            cursor.execute("SELECT id FROM contacts WHERE email = ?", (email,))
            contact_id = cursor.fetchone()[0]
            conn.commit()
        
        conn.close()
        return contact_id
    
    def update_contact(self, contact_id: int, **kwargs) -> bool:
        """更新联系人信息"""
        if not kwargs:
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in ('email', 'name', 'group_id', 'notes', 'interaction_count', 
                      'last_contact', 'send_count', 'last_send'):
                fields.append(f"{key} = ?")
                values.append(value)
        
        if not fields:
            conn.close()
            return False
        
        values.append(contact_id)
        query = f"UPDATE contacts SET {', '.join(fields)} WHERE id = ?"
        
        cursor.execute(query, values)
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        return success
    
    def delete_contact(self, contact_id: int) -> bool:
        """删除联系人"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        return success
    
    def delete_contacts(self, contact_ids: List[int]) -> int:
        """批量删除联系人"""
        if not contact_ids:
            return 0
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        placeholders = ','.join(['?' for _ in contact_ids])
        cursor.execute(f"DELETE FROM contacts WHERE id IN ({placeholders})", contact_ids)
        deleted = cursor.rowcount
        
        conn.commit()
        conn.close()
        return deleted
    
    def move_contacts_to_group(self, contact_ids: List[int], group_id: Optional[int]) -> int:
        """批量移动联系人到分组"""
        if not contact_ids:
            return 0
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        placeholders = ','.join(['?' for _ in contact_ids])
        cursor.execute(
            f"UPDATE contacts SET group_id = ? WHERE id IN ({placeholders})",
            [group_id] + contact_ids
        )
        updated = cursor.rowcount
        
        conn.commit()
        conn.close()
        return updated
    
    def import_contacts(self, contacts: List[Dict], group_id: Optional[int] = None) -> int:
        """批量导入联系人"""
        count = 0
        for c in contacts:
            self.add_contact(
                email=c.get('email', ''),
                name=c.get('name', ''),
                group_id=group_id,
                interaction_count=c.get('count', 0),
                last_contact=c.get('last_contact', ''),
                first_contact=c.get('first_contact', '')
            )
            count += 1
        return count
    
    def get_contacts_by_group_for_send(self, group_id: int) -> List[Dict]:
        """获取分组联系人用于发送（返回简化格式）"""
        contacts = self.get_contacts(group_id=group_id)
        return [{'email': c['email'], 'name': c['name']} for c in contacts]
    
    def record_send(self, email: str):
        """记录发送"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE contacts 
            SET send_count = send_count + 1, last_send = ?
            WHERE email = ?
        ''', (datetime.now().strftime('%Y-%m-%d %H:%M'), email))
        
        conn.commit()
        conn.close()
