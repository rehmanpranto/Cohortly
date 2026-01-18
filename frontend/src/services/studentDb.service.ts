import api from '@/lib/api';

export interface DbCredentials {
  host: string;
  database: string;
  username: string;
  port: number;
  sslmode: string;
  connectionString: string;
}

export interface DbSetupResponse {
  credentials: DbCredentials;
  pgpassContent: string;
  setupInstructions: string;
}

export interface DbSetupInstructionsResponse {
  instructions: string;
  quickStart: {
    windows: string;
    linux: string;
    manual: string;
  };
}

export const studentDbService = {
  /**
   * Get database connection credentials for student
   */
  getCredentials: async (): Promise<DbSetupResponse> => {
    const response = await api.get('/student/db-credentials');
    return response.data.data;
  },

  /**
   * Get setup instructions only
   */
  getSetupInstructions: async (): Promise<DbSetupInstructionsResponse> => {
    const response = await api.get('/student/db-setup');
    return response.data.data;
  },

  /**
   * Test database connection
   */
  testConnection: async (): Promise<{ connected: boolean; timestamp: string }> => {
    const response = await api.get('/student/db-test');
    return response.data.data;
  },

  /**
   * Download .pgpass file for Windows
   */
  downloadPgpassWindows: (pgpassContent: string) => {
    const blob = new Blob([pgpassContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'pgpass.conf';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  },

  /**
   * Download .pgpass file for Linux/Mac
   */
  downloadPgpassUnix: (pgpassContent: string) => {
    const blob = new Blob([pgpassContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = '.pgpass';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  },

  /**
   * Copy connection string to clipboard
   */
  copyToClipboard: async (text: string): Promise<boolean> => {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch (err) {
      console.error('Failed to copy:', err);
      return false;
    }
  },

  /**
   * Download setup script for Windows PowerShell
   */
  downloadWindowsSetupScript: (pgpassContent: string) => {
    const script = `# PostgreSQL Passwordless Setup for Windows
# Run this script in PowerShell as Administrator

Write-Host "Setting up PostgreSQL passwordless authentication..." -ForegroundColor Green

# Create postgresql directory
$pgDir = "$env:APPDATA\\postgresql"
New-Item -ItemType Directory -Force -Path $pgDir | Out-Null

# Create pgpass.conf file
$pgpassFile = "$pgDir\\pgpass.conf"
@"
${pgpassContent}
"@ | Out-File -FilePath $pgpassFile -Encoding ASCII -Force

# Set file permissions (read-only for current user)
icacls $pgpassFile /inheritance:r /grant:r "$env:USERNAME:R" | Out-Null

Write-Host "✓ Setup complete!" -ForegroundColor Green
Write-Host "You can now connect to PostgreSQL without password:" -ForegroundColor Cyan
Write-Host "  psql -h [host] -U [username] -d [database]" -ForegroundColor Yellow
`;

    const blob = new Blob([script], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'setup-postgres.ps1';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  },

  /**
   * Download setup script for Linux/Mac
   */
  downloadUnixSetupScript: (pgpassContent: string) => {
    const script = `#!/bin/bash
# PostgreSQL Passwordless Setup for Linux/Mac

echo "Setting up PostgreSQL passwordless authentication..."

# Create .pgpass file
PGPASS_FILE="$HOME/.pgpass"
cat > "$PGPASS_FILE" << 'EOF'
${pgpassContent}
EOF

# Set correct permissions
chmod 600 "$PGPASS_FILE"

echo "✓ Setup complete!"
echo "You can now connect to PostgreSQL without password:"
echo "  psql -h [host] -U [username] -d [database]"
`;

    const blob = new Blob([script], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'setup-postgres.sh';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  },
};
