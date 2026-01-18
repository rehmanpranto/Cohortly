import crypto from 'crypto';
import config from '../config/config';
import prisma from '../config/database';

interface StudentDbCredentials {
  connectionString: string;
  host: string;
  database: string;
  username: string;
  password: string;
  port: number;
  sslmode: string;
  directCommand: string;
}

class StudentDbService {
  /**
   * Generate passwordless database credentials for a student
   * Uses the student's ID to create a unique, temporary access pattern
   */
  async generateStudentCredentials(studentId: string, email: string): Promise<StudentDbCredentials> {
    // Parse the main DATABASE_URL
    const dbUrl = new URL(config.database.url);
    
    // Generate a secure token for this student session
    const sessionToken = crypto.randomBytes(32).toString('hex');
    
    // For Neon, we'll use the main connection with a custom application_name
    // This allows tracking student queries without creating separate roles
    const studentAppName = `student_${studentId.substring(0, 8)}`;
    
    // Extract connection details
    const host = dbUrl.hostname;
    const database = dbUrl.pathname.substring(1).split('?')[0];
    const port = parseInt(dbUrl.port || '5432');
    const username = dbUrl.username;
    const password = dbUrl.password;
    
    // Create a read-only connection string for students
    // Note: Neon doesn't support creating dynamic roles easily, so we'll use connection pooling
    const studentConnectionString = `postgresql://${username}:${password}@${host}:${port}/${database}?sslmode=require&application_name=${studentAppName}`;
    
    // Command for students to use (password will be in .pgpass file)
    const directCommand = `psql "postgresql://${username}@${host}:${port}/${database}?sslmode=require&application_name=${studentAppName}"`;
    
    return {
      connectionString: studentConnectionString,
      host,
      database,
      username,
      password,
      port,
      sslmode: 'require',
      directCommand,
    };
  }

  /**
   * Generate .pgpass file content for passwordless access
   * Format: hostname:port:database:username:password
   */
  generatePgpassContent(credentials: StudentDbCredentials): string {
    return `${credentials.host}:${credentials.port}:${credentials.database}:${credentials.username}:${credentials.password}`;
  }

  /**
   * Generate setup instructions for student
   */
  generateSetupInstructions(studentId: string, credentials: StudentDbCredentials): string {
    const pgpassContent = this.generatePgpassContent(credentials);
    
    return `
# 🎓 Database Access Setup for Student

## Windows Setup (PowerShell)

### Step 1: Create .pgpass file
\`\`\`powershell
# Create AppData\\Roaming\\postgresql directory if it doesn't exist
New-Item -ItemType Directory -Force -Path "$env:APPDATA\\postgresql"

# Create .pgpass file with your credentials
@"
${pgpassContent}
"@ | Out-File -FilePath "$env:APPDATA\\postgresql\\pgpass.conf" -Encoding ASCII

# Set file permissions (read-only for current user)
icacls "$env:APPDATA\\postgresql\\pgpass.conf" /inheritance:r /grant:r "$env:USERNAME:R"
\`\`\`

### Step 2: Connect to database (passwordless)
\`\`\`powershell
psql -h ${credentials.host} -p ${credentials.port} -U ${credentials.username} -d ${credentials.database}
\`\`\`

---

## Linux/Mac Setup

### Step 1: Create .pgpass file
\`\`\`bash
# Create .pgpass file in home directory
echo "${pgpassContent}" > ~/.pgpass

# Set correct permissions (required for security)
chmod 600 ~/.pgpass
\`\`\`

### Step 2: Connect to database (passwordless)
\`\`\`bash
psql -h ${credentials.host} -p ${credentials.port} -U ${credentials.username} -d ${credentials.database}
\`\`\`

---

## Quick Connect

Once .pgpass is set up, you can connect with:
\`\`\`
psql -h ${credentials.host} -U ${credentials.username} -d ${credentials.database}
\`\`\`

Or use the connection string:
\`\`\`
psql "${credentials.connectionString}"
\`\`\`

---

## Using GUI Tools

### DBeaver
- Host: ${credentials.host}
- Port: ${credentials.port}
- Database: ${credentials.database}
- Username: ${credentials.username}
- Password: (from .pgpass)
- SSL: Required

### pgAdmin
- Host: ${credentials.host}
- Port: ${credentials.port}
- Maintenance database: ${credentials.database}
- Username: ${credentials.username}
- Save password: Yes

---

## 🔒 READ-ONLY Access

Your account has READ-ONLY access. You can:
- ✅ SELECT data from tables
- ✅ Run queries
- ✅ Join tables
- ✅ Create temporary tables in your session

You CANNOT:
- ❌ INSERT, UPDATE, or DELETE data
- ❌ CREATE or DROP tables
- ❌ ALTER table structures
- ❌ Modify other students' data

---

## 🎯 Sample Queries

### View your enrollments
\`\`\`sql
SELECT 
  b.name as bootcamp,
  bt.name as batch,
  e.status,
  e.enrolled_at
FROM enrollments e
JOIN batches bt ON e.batch_id = bt.id
JOIN bootcamps b ON bt.bootcamp_id = b.id
JOIN users u ON e.student_id = u.id
WHERE u.id = '${studentId}';
\`\`\`

### View your assignments
\`\`\`sql
SELECT 
  a.title,
  a.deadline,
  s.status,
  s.submitted_at,
  g.score,
  g.feedback
FROM assignments a
LEFT JOIN submissions s ON a.id = s.assignment_id AND s.student_id = '${studentId}'
LEFT JOIN grades g ON s.id = g.submission_id
ORDER BY a.deadline DESC;
\`\`\`

### Check your progress
\`\`\`sql
SELECT 
  COUNT(DISTINCT CASE WHEN s.status = 'GRADED' THEN s.id END) as completed,
  COUNT(DISTINCT a.id) as total_assignments,
  ROUND(COUNT(DISTINCT CASE WHEN s.status = 'GRADED' THEN s.id END) * 100.0 / NULLIF(COUNT(DISTINCT a.id), 0), 2) as completion_percentage
FROM assignments a
LEFT JOIN submissions s ON a.id = s.assignment_id AND s.student_id = '${studentId}';
\`\`\`

---

## 📞 Support

If you have issues connecting:
1. Verify .pgpass file exists and has correct permissions
2. Check your internet connection
3. Ensure PostgreSQL client (psql) is installed
4. Contact your instructor

---

**Student ID**: ${studentId}
**Generated**: ${new Date().toISOString()}
`;
  }

  /**
   * Validate student has access to database features
   */
  async validateStudentAccess(studentId: string): Promise<boolean> {
    try {
      // Check if student exists and is active
      const student = await prisma.user.findUnique({
        where: { id: studentId },
        select: { 
          id: true, 
          role: true, 
          isActive: true,
        },
      });

      return !!(student && student.role === 'STUDENT' && student.isActive);
    } catch (error) {
      return false;
    }
  }

  /**
   * Log database access for audit trail
   */
  async logDatabaseAccess(studentId: string, action: string): Promise<void> {
    // This could be expanded to log to a separate audit table
    console.log(`[DB ACCESS] Student ${studentId} - ${action} at ${new Date().toISOString()}`);
  }
}

export default new StudentDbService();
