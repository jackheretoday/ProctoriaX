#!/usr/bin/env python3
"""Database backup script"""
import sys
import os
import subprocess
from datetime import datetime
import gzip
import shutil

# Add app to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import Config


def parse_database_url(url):
    """Parse DATABASE_URL into components"""
    # Format: mysql://user:password@host:port/database
    # or postgresql://user:password@host:port/database
    
    if not url:
        return None
    
    parts = url.split('://')
    if len(parts) != 2:
        return None
    
    db_type = parts[0]  # mysql or postgresql
    rest = parts[1]
    
    # Split credentials and host/db
    if '@' in rest:
        creds, host_db = rest.split('@')
        user, password = creds.split(':')
    else:
        return None
    
    # Split host and database
    if '/' in host_db:
        host, database = host_db.split('/', 1)
    else:
        return None
    
    # Handle port
    if ':' in host:
        host, port = host.split(':')
    else:
        port = '3306' if db_type == 'mysql' else '5432'
    
    return {
        'type': db_type,
        'user': user,
        'password': password,
        'host': host,
        'port': port,
        'database': database
    }


def backup_mysql(db_info, backup_file):
    """Backup MySQL database"""
    cmd = [
        'mysqldump',
        '-h', db_info['host'],
        '-P', db_info['port'],
        '-u', db_info['user'],
        f"-p{db_info['password']}",
        db_info['database']
    ]
    
    print(f"Backing up MySQL database: {db_info['database']}")
    
    with open(backup_file, 'w') as f:
        result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE)
    
    if result.returncode != 0:
        raise Exception(f"Backup failed: {result.stderr.decode()}")
    
    return backup_file


def backup_postgresql(db_info, backup_file):
    """Backup PostgreSQL database"""
    cmd = [
        'pg_dump',
        '-h', db_info['host'],
        '-p', db_info['port'],
        '-U', db_info['user'],
        '-d', db_info['database'],
        '-F', 'c',  # Custom format
        '-f', backup_file
    ]
    
    print(f"Backing up PostgreSQL database: {db_info['database']}")
    
    env = os.environ.copy()
    env['PGPASSWORD'] = db_info['password']
    
    result = subprocess.run(cmd, env=env, stderr=subprocess.PIPE)
    
    if result.returncode != 0:
        raise Exception(f"Backup failed: {result.stderr.decode()}")
    
    return backup_file


def compress_backup(backup_file):
    """Compress backup file with gzip"""
    compressed_file = f"{backup_file}.gz"
    
    print(f"Compressing backup...")
    
    with open(backup_file, 'rb') as f_in:
        with gzip.open(compressed_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    # Remove uncompressed file
    os.remove(backup_file)
    
    return compressed_file


def cleanup_old_backups(backup_dir, days=7):
    """Delete backups older than specified days"""
    print(f"\nCleaning up backups older than {days} days...")
    
    if not os.path.exists(backup_dir):
        return
    
    now = datetime.now()
    deleted = 0
    
    for filename in os.listdir(backup_dir):
        filepath = os.path.join(backup_dir, filename)
        
        if not os.path.isfile(filepath):
            continue
        
        # Check file age
        file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
        age_days = (now - file_time).days
        
        if age_days > days:
            os.remove(filepath)
            deleted += 1
            print(f"  Deleted: {filename} (age: {age_days} days)")
    
    if deleted == 0:
        print("  No old backups to delete")
    else:
        print(f"  ✓ Deleted {deleted} old backup(s)")


def main():
    """Main backup function"""
    print("="*50)
    print("Database Backup Script")
    print("="*50)
    
    # Get database URL from config
    database_url = os.getenv('DATABASE_URL') or Config.SQLALCHEMY_DATABASE_URI
    
    if not database_url or 'sqlite' in database_url:
        print("\n⚠️  SQLite database detected.")
        print("For SQLite, simply copy the .db file.")
        return
    
    # Parse database info
    db_info = parse_database_url(database_url)
    
    if not db_info:
        print("\n❌ Error: Could not parse DATABASE_URL")
        return
    
    # Create backup directory
    backup_dir = os.path.join(os.path.dirname(__file__), '..', 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    
    # Generate backup filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_dir, f"backup_{timestamp}.sql")
    
    try:
        # Perform backup based on database type
        if db_info['type'] == 'mysql':
            backup_file = backup_mysql(db_info, backup_file)
        elif db_info['type'] == 'postgresql':
            backup_file = backup_postgresql(db_info, backup_file)
        else:
            print(f"\n❌ Error: Unsupported database type: {db_info['type']}")
            return
        
        # Compress backup
        compressed_file = compress_backup(backup_file)
        
        # Get file size
        size_mb = os.path.getsize(compressed_file) / (1024 * 1024)
        
        print(f"\n✓ Backup completed successfully!")
        print(f"  File: {compressed_file}")
        print(f"  Size: {size_mb:.2f} MB")
        
        # Cleanup old backups
        cleanup_old_backups(backup_dir, days=7)
        
        print("\n" + "="*50)
        print("Backup process completed!")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ Error during backup: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()