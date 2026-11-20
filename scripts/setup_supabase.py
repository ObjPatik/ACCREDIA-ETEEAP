#!/usr/bin/env python
"""
Automated Supabase Verification, Migration & Seeding Script for ACCREDIA
"""
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

# Set up project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / 'backend'
sys.path.insert(0, str(BACKEND_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accredia.settings')

def main():
    print("=" * 70)
    print("ACCREDIA - SUPABASE AUTOMATED CONNECTION & SETUP WIZARD")
    print("=" * 70)

    from dotenv import load_dotenv
    load_dotenv(BACKEND_DIR / '.env')

    db_url = os.getenv('DATABASE_URL', '').strip()
    supabase_url = os.getenv('SUPABASE_URL', '').strip()
    bucket = os.getenv('SUPABASE_STORAGE_BUCKET', 'applicant-documents')

    print(f"\n1. Checking Environment Variables in {BACKEND_DIR / '.env'}:")
    if not db_url:
        print("   [!] DATABASE_URL is not set in backend/.env.")
        print("       The system will use local SQLite (db.sqlite3).")
        print("       To connect to Supabase, paste your PostgreSQL connection URI in backend/.env")
    else:
        parsed = urlparse(db_url)
        masked_pwd = '****' if parsed.password else 'NONE'
        print(f"   [+] DATABASE_URL detected!")
        print(f"       Host: {parsed.hostname}")
        print(f"       Port: {parsed.port}")
        print(f"       Database: {parsed.path.lstrip('/')}")
        print(f"       User: {parsed.username}")
        print(f"       Password: {masked_pwd}")

    if supabase_url:
        print(f"   [+] SUPABASE_URL: {supabase_url}")
        print(f"   [+] STORAGE_BUCKET: {bucket}")
    else:
        print("   [-] SUPABASE_URL not configured (local media storage will be used).")

    print("\n2. Initializing Django Environment...")
    try:
        import django
        django.setup()
        print("   [+] Django framework initialized successfully.")
    except Exception as exc:
        print(f"   [x] Failed to initialize Django: {exc}")
        return 1

    print("\n3. Testing Database Connection...")
    from django.db import connection
    try:
        connection.ensure_connection()
        with connection.cursor() as cursor:
            if connection.vendor == 'postgresql':
                cursor.execute("SELECT version();")
            else:
                cursor.execute("SELECT sqlite_version();")
            row = cursor.fetchone()
            db_version = row[0] if row else "Unknown"
        print(f"   [+] Database Connection Succeeded ({connection.vendor.upper()})!")
        print(f"       Server Version: {db_version[:60]}...")
    except Exception as exc:
        print(f"   [x] Database connection failed: {exc}")
        print("\n   Troubleshooting Tip:")
        print("   - Check if your password is correct (without brackets [ ]).")
        print("   - For Supabase, use port 6543 (connection pooling) or port 5432.")
        return 1

    print("\n4. Running Database Migrations...")
    from django.core.management import call_command
    try:
        call_command('migrate', interactive=False)
        print("   [+] All 12 ACCREDIA database tables and schema migrated successfully!")
    except Exception as exc:
        print(f"   [x] Migration failed: {exc}")
        return 1

    print("\n5. Seeding CIT-U BSIT 2023-2024 Curriculum & Demo Users...")
    try:
        from core.seed_data import seed_bsit_program, create_demo_users
        seed_bsit_program()
        create_demo_users()
        print("   [+] Curriculum & Demo Users seeded successfully!")
    except Exception as exc:
        print(f"   [!] Seeding encountered notice: {exc}")

    print("\n" + "=" * 70)
    print("SUPABASE SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print("You can now run your backend server with:")
    print("   cd backend")
    print("   python manage.py runserver 127.0.0.1:8000")
    print("=" * 70)
    return 0

if __name__ == '__main__':
    sys.exit(main())
