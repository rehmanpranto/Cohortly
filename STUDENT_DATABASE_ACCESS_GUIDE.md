# 🔐 Student Database Access - Complete Guide

## Overview

As a student in Cohortly, you have **passwordless read-only access** to the PostgreSQL database. This allows you to practice SQL queries, explore data structures, and analyze your own academic data.

---

## 🎯 Quick Start

### 1. **Access Your Credentials**
- Log in to your student portal
- Click "Database Access" card
- Your credentials will be displayed

### 2. **Choose Your Setup Method**

#### Option A: Automatic Setup (Recommended)
**Windows:**
```powershell
# Download setup-postgres.ps1 from portal
.\setup-postgres.ps1
```

**Linux/Mac:**
```bash
# Download setup-postgres.sh from portal
chmod +x setup-postgres.sh
./setup-postgres.sh
```

#### Option B: Manual Setup
See detailed instructions below

---

## 📋 What You Can Access

### ✅ Allowed Operations:
- `SELECT` - Query all tables
- `VIEW` - See table structures
- `EXPLAIN` - Analyze query plans
- `CREATE TEMPORARY TABLE` - Session-only tables
- `WITH` (CTE) - Common table expressions

### ❌ Restricted Operations:
- `INSERT`, `UPDATE`, `DELETE` - No data modification
- `CREATE TABLE` - No permanent tables
- `DROP`, `ALTER` - No schema changes
- `GRANT`, `REVOKE` - No permission changes

---

## 🪟 Windows Setup

### Automatic Method

1. **Download Script**
   - Go to Student Portal → Database Access
   - Click "Download setup-postgres.ps1"

2. **Run Script**
   ```powershell
   # Open PowerShell
   cd Downloads
   .\setup-postgres.ps1
   ```

3. **Connect**
   ```powershell
   psql -h pg.neon.tech -U <your-username> -d neondb
   ```

### Manual Method

1. **Create PostgreSQL Directory**
   ```powershell
   New-Item -ItemType Directory -Force -Path "$env:APPDATA\postgresql"
   ```

2. **Create pgpass.conf File**
   ```powershell
   # Replace with your actual credentials
   @"
   pg.neon.tech:5432:neondb:your-username:your-password
   "@ | Out-File -FilePath "$env:APPDATA\postgresql\pgpass.conf" -Encoding ASCII
   ```

3. **Set Permissions**
   ```powershell
   icacls "$env:APPDATA\postgresql\pgpass.conf" /inheritance:r /grant:r "$env:USERNAME:R"
   ```

4. **Verify Setup**
   ```powershell
   # Should connect without asking for password
   psql -h pg.neon.tech -U your-username -d neondb
   ```

---

## 🐧 Linux/Mac Setup

### Automatic Method

1. **Download Script**
   ```bash
   # From Student Portal, download setup-postgres.sh
   cd ~/Downloads
   ```

2. **Run Script**
   ```bash
   chmod +x setup-postgres.sh
   ./setup-postgres.sh
   ```

3. **Connect**
   ```bash
   psql -h pg.neon.tech -U <your-username> -d neondb
   ```

### Manual Method

1. **Create .pgpass File**
   ```bash
   # Replace with your actual credentials
   echo "pg.neon.tech:5432:neondb:your-username:your-password" > ~/.pgpass
   ```

2. **Set Correct Permissions**
   ```bash
   chmod 600 ~/.pgpass
   ```

3. **Verify Setup**
   ```bash
   # Should connect without asking for password
   psql -h pg.neon.tech -U your-username -d neondb
   ```

---

## 🔧 Troubleshooting

### "Password required" error
**Problem:** `.pgpass` file not set up correctly

**Solution:**
- **Windows:** Check `%APPDATA%\postgresql\pgpass.conf` exists
- **Linux/Mac:** Check `~/.pgpass` exists and has `600` permissions
  ```bash
  ls -la ~/.pgpass  # Should show: -rw------- (owner read/write only)
  chmod 600 ~/.pgpass  # Fix if needed
  ```

### "Connection refused" error
**Problem:** Network or firewall issue

**Solution:**
- Check internet connection
- Verify you're using correct host: `pg.neon.tech`
- Try with explicit port: `-p 5432`

### "psql: command not found"
**Problem:** PostgreSQL client not installed

**Solution:**

**Windows:**
```powershell
# Install via Chocolatey
choco install postgresql

# Or download from: https://www.postgresql.org/download/windows/
```

**Mac:**
```bash
brew install postgresql
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install postgresql-client
```

### "Permission denied for table"
**Problem:** Trying to modify data (you have read-only access)

**Solution:**
- Use only `SELECT` queries
- Cannot `INSERT`, `UPDATE`, or `DELETE`
- This is intentional for data safety

---

## 📊 Sample Queries

### View Your Enrollments
```sql
SELECT 
  b.name AS bootcamp,
  bt.name AS batch,
  e.status,
  e.enrolled_at,
  e.progress
FROM enrollments e
JOIN batches bt ON e.batch_id = bt.id
JOIN bootcamps b ON bt.bootcamp_id = b.id
JOIN users u ON e.student_id = u.id
WHERE u.email = 'your-email@example.com';
```

### Check Your Assignments
```sql
SELECT 
  a.title,
  a.deadline,
  a.max_score,
  s.status AS submission_status,
  s.submitted_at,
  g.score,
  g.feedback
FROM assignments a
LEFT JOIN submissions s ON a.id = s.assignment_id
LEFT JOIN grades g ON s.id = g.submission_id
WHERE s.student_id IN (
  SELECT id FROM users WHERE email = 'your-email@example.com'
)
ORDER BY a.deadline DESC;
```

### Calculate Your Progress
```sql
SELECT 
  COUNT(DISTINCT CASE WHEN s.status = 'GRADED' THEN s.id END) AS completed,
  COUNT(DISTINCT a.id) AS total_assignments,
  ROUND(
    COUNT(DISTINCT CASE WHEN s.status = 'GRADED' THEN s.id END) * 100.0 / 
    NULLIF(COUNT(DISTINCT a.id), 0), 
    2
  ) AS completion_percentage,
  AVG(g.score) AS average_score
FROM assignments a
LEFT JOIN submissions s ON a.id = s.assignment_id 
  AND s.student_id IN (SELECT id FROM users WHERE email = 'your-email@example.com')
LEFT JOIN grades g ON s.id = g.submission_id;
```

### View Attendance History
```sql
SELECT 
  a.session_date,
  a.present,
  bt.name AS batch,
  b.name AS bootcamp
FROM attendance a
JOIN enrollments e ON a.enrollment_id = e.id
JOIN batches bt ON e.batch_id = bt.id
JOIN bootcamps b ON bt.bootcamp_id = b.id
WHERE e.student_id IN (
  SELECT id FROM users WHERE email = 'your-email@example.com'
)
ORDER BY a.session_date DESC;
```

### Explore Database Schema
```sql
-- List all tables
\dt

-- Describe a specific table
\d users
\d enrollments
\d assignments

-- View table relationships
SELECT 
  tc.table_name, 
  kcu.column_name, 
  ccu.table_name AS foreign_table_name,
  ccu.column_name AS foreign_column_name 
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY';
```

---

## 🛠️ Using GUI Tools

### DBeaver (Cross-platform, Free)

1. **Download:** https://dbeaver.io/download/
2. **Create Connection:**
   - Database: PostgreSQL
   - Host: `pg.neon.tech`
   - Port: `5432`
   - Database: `neondb`
   - Username: (from portal)
   - Password: (leave empty if .pgpass is set up)
   - SSL: Required
3. **Test Connection**
4. **Save**

### pgAdmin (Cross-platform, Free)

1. **Download:** https://www.pgadmin.org/download/
2. **Add New Server:**
   - General → Name: "Cohortly DB"
   - Connection → Host: `pg.neon.tech`
   - Connection → Port: `5432`
   - Connection → Database: `neondb`
   - Connection → Username: (from portal)
   - Connection → Password: (from portal)
   - Connection → Save password: Yes
   - SSL → Mode: Require
3. **Save**

### TablePlus (Mac/Windows, Paid with Trial)

1. **Download:** https://tableplus.com/
2. **Create Connection:**
   - Type: PostgreSQL
   - Name: Cohortly
   - Host: `pg.neon.tech`
   - Port: `5432`
   - User: (from portal)
   - Password: (from portal)
   - Database: `neondb`
   - SSL Mode: require
3. **Test & Save**

---

## 💡 Best Practices

### 1. **Use Meaningful Aliases**
```sql
-- Good
SELECT u.full_name, b.name AS bootcamp_name
FROM users u
JOIN enrollments e ON u.id = e.student_id
JOIN batches bt ON e.batch_id = bt.id
JOIN bootcamps b ON bt.bootcamp_id = b.id;

-- Less clear
SELECT u.full_name, b.name
FROM users u, enrollments e, batches bt, bootcamps b
WHERE u.id = e.student_id AND e.batch_id = bt.id AND bt.bootcamp_id = b.id;
```

### 2. **Use EXPLAIN to Understand Queries**
```sql
EXPLAIN ANALYZE
SELECT * FROM enrollments WHERE student_id = 'your-id';
```

### 3. **Limit Large Result Sets**
```sql
-- Always use LIMIT when exploring
SELECT * FROM users LIMIT 10;
```

### 4. **Use CTEs for Complex Queries**
```sql
WITH student_stats AS (
  SELECT 
    e.student_id,
    COUNT(s.id) AS total_submissions
  FROM enrollments e
  LEFT JOIN submissions s ON s.student_id = e.student_id
  GROUP BY e.student_id
)
SELECT * FROM student_stats WHERE total_submissions > 5;
```

---

## 🎓 Learning Resources

### PostgreSQL Documentation
- Official Docs: https://www.postgresql.org/docs/
- Tutorial: https://www.postgresqltutorial.com/

### SQL Practice
- SQLZoo: https://sqlzoo.net/
- HackerRank SQL: https://www.hackerrank.com/domains/sql
- LeetCode Database: https://leetcode.com/problemset/database/

### Video Tutorials
- freeCodeCamp PostgreSQL: https://www.youtube.com/watch?v=qw--VYLpxG4
- Traversy Media SQL Crash Course: https://www.youtube.com/watch?v=p3qvj9hO_Bo

---

## 🔐 Security Reminders

1. **Never share your credentials** - They're unique to you
2. **Don't modify .pgpass permissions** - Must be owner-only readable
3. **Don't commit .pgpass to git** - Add to `.gitignore`
4. **Report suspicious activity** - Contact instructor immediately
5. **Don't try to bypass restrictions** - It's logged and monitored

---

## 📞 Getting Help

### If You're Stuck:
1. **Check this guide** - Most issues are covered here
2. **Test connection** - Use the "Test Connection" button in portal
3. **Ask classmates** - They might have faced the same issue
4. **Contact instructor** - Include error messages and what you tried

### Common Support Requests:
- **"Can't connect"** → Check .pgpass file and permissions
- **"Password still asked"** → Verify .pgpass format (no spaces, correct path)
- **"Permission denied"** → You're trying to modify data (read-only access)
- **"Table not found"** → Check spelling, use `\dt` to list tables

---

## 🎯 Next Steps

1. ✅ Set up passwordless connection
2. ✅ Test connection from portal
3. ✅ Run sample queries
4. ✅ Explore database schema
5. ✅ Practice with your own data
6. ✅ Try GUI tools (DBeaver/pgAdmin)
7. ✅ Complete SQL assignments

---

**Generated for:** Cohortly Students  
**Last Updated:** January 2026  
**Support:** Contact your instructor via student portal
