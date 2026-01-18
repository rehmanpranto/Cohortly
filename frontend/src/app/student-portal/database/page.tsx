'use client';

import { useAuth } from '@/hooks/useAuth';
import { useRouter } from 'next/navigation';
import { ArrowLeft, Database, Download, Copy, CheckCircle, Terminal, Book, AlertCircle } from 'lucide-react';
import { useState, useEffect } from 'react';
import { studentDbService, DbSetupResponse } from '@/services/studentDb.service';

export default function DatabaseAccessPage() {
  const { user } = useAuth();
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [credentials, setCredentials] = useState<DbSetupResponse | null>(null);
  const [copied, setCopied] = useState<string | null>(null);
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState<{ success: boolean; message: string } | null>(null);

  useEffect(() => {
    if (user && user.role !== 'STUDENT') {
      router.push('/dashboard');
      return;
    }
    fetchCredentials();
  }, [user]);

  const fetchCredentials = async () => {
    try {
      setLoading(true);
      const data = await studentDbService.getCredentials();
      setCredentials(data);
    } catch (error) {
      console.error('Failed to fetch credentials:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = async (text: string, label: string) => {
    const success = await studentDbService.copyToClipboard(text);
    if (success) {
      setCopied(label);
      setTimeout(() => setCopied(null), 2000);
    }
  };

  const handleTestConnection = async () => {
    try {
      setTesting(true);
      setTestResult(null);
      const result = await studentDbService.testConnection();
      setTestResult({
        success: true,
        message: `Connected successfully at ${new Date(result.timestamp).toLocaleString()}`,
      });
    } catch (error: any) {
      setTestResult({
        success: false,
        message: error.message || 'Connection test failed',
      });
    } finally {
      setTesting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-sky-500"></div>
      </div>
    );
  }

  if (!credentials) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50">
        <div className="text-center">
          <AlertCircle className="h-16 w-16 text-red-500 mx-auto mb-4" />
          <p className="text-lg text-gray-700">Failed to load database credentials</p>
          <button
            onClick={fetchCredentials}
            className="mt-4 px-6 py-2 bg-sky-500 text-white rounded-xl hover:bg-sky-600"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50">
      {/* Header */}
      <nav className="bg-white/80 backdrop-blur-md shadow-sm border-b border-sky-100 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => router.push('/student-portal')}
                className="p-2 rounded-lg hover:bg-sky-50 transition-colors"
              >
                <ArrowLeft className="h-5 w-5 text-gray-600" />
              </button>
              <Database className="h-6 w-6 text-sky-500" />
              <h1 className="text-xl font-bold bg-gradient-to-r from-sky-600 to-cyan-600 bg-clip-text text-transparent">
                Database Access 💾
              </h1>
            </div>
            <div className="flex items-center">
              <button
                onClick={handleTestConnection}
                disabled={testing}
                className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-300 ${
                  testing
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    : 'bg-gradient-to-r from-green-500 to-emerald-500 text-white hover:shadow-lg hover:-translate-y-0.5'
                }`}
              >
                {testing ? 'Testing...' : '🔌 Test Connection'}
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Test Result */}
        {testResult && (
          <div
            className={`mb-6 p-4 rounded-2xl border-2 ${
              testResult.success
                ? 'bg-green-50 border-green-200 text-green-800'
                : 'bg-red-50 border-red-200 text-red-800'
            }`}
          >
            <div className="flex items-center">
              {testResult.success ? (
                <CheckCircle className="h-5 w-5 mr-2" />
              ) : (
                <AlertCircle className="h-5 w-5 mr-2" />
              )}
              <span className="font-medium">{testResult.message}</span>
            </div>
          </div>
        )}

        {/* Introduction */}
        <div className="bg-white rounded-2xl shadow-xl p-6 mb-6 border border-sky-100">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">📚 Passwordless PostgreSQL Access</h2>
          <p className="text-gray-600 mb-4">
            As a student, you have <strong className="text-sky-600">read-only</strong> access to the bootcamp database.
            Follow the steps below to set up passwordless authentication using <code className="bg-gray-100 px-2 py-1 rounded">.pgpass</code> file.
          </p>
          <div className="bg-gradient-to-r from-sky-50 to-cyan-50 rounded-xl p-4 border border-sky-200">
            <p className="text-sm text-gray-700">
              <strong>✓ You can:</strong> SELECT data, run queries, create temporary tables
              <br />
              <strong>✗ You cannot:</strong> INSERT, UPDATE, DELETE, or modify table structures
            </p>
          </div>
        </div>

        {/* Quick Setup Cards */}
        <div className="grid md:grid-cols-2 gap-6 mb-6">
          {/* Windows Setup */}
          <div className="bg-white rounded-2xl shadow-xl p-6 border border-gray-100">
            <div className="flex items-center mb-4">
              <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-blue-400 to-sky-500 flex items-center justify-center mr-4">
                <Terminal className="h-6 w-6 text-white" />
              </div>
              <div>
                <h3 className="font-bold text-lg text-gray-900">Windows Setup</h3>
                <p className="text-sm text-gray-500">PowerShell script</p>
              </div>
            </div>
            <p className="text-gray-600 mb-4 text-sm">
              Download and run the setup script to configure .pgpass automatically
            </p>
            <button
              onClick={() => studentDbService.downloadWindowsSetupScript(credentials.pgpassContent)}
              className="w-full px-4 py-3 bg-gradient-to-r from-blue-500 to-sky-500 text-white rounded-xl font-medium hover:shadow-lg hover:-translate-y-0.5 transition-all duration-300 flex items-center justify-center"
            >
              <Download className="h-4 w-4 mr-2" />
              Download setup-postgres.ps1
            </button>
            <div className="mt-4 p-3 bg-gray-50 rounded-lg">
              <p className="text-xs text-gray-600 mb-2">Then run in PowerShell:</p>
              <code className="text-xs text-sky-600 block">.\setup-postgres.ps1</code>
            </div>
          </div>

          {/* Linux/Mac Setup */}
          <div className="bg-white rounded-2xl shadow-xl p-6 border border-gray-100">
            <div className="flex items-center mb-4">
              <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-green-400 to-emerald-500 flex items-center justify-center mr-4">
                <Terminal className="h-6 w-6 text-white" />
              </div>
              <div>
                <h3 className="font-bold text-lg text-gray-900">Linux/Mac Setup</h3>
                <p className="text-sm text-gray-500">Bash script</p>
              </div>
            </div>
            <p className="text-gray-600 mb-4 text-sm">
              Download and run the setup script to configure .pgpass automatically
            </p>
            <button
              onClick={() => studentDbService.downloadUnixSetupScript(credentials.pgpassContent)}
              className="w-full px-4 py-3 bg-gradient-to-r from-green-500 to-emerald-500 text-white rounded-xl font-medium hover:shadow-lg hover:-translate-y-0.5 transition-all duration-300 flex items-center justify-center"
            >
              <Download className="h-4 w-4 mr-2" />
              Download setup-postgres.sh
            </button>
            <div className="mt-4 p-3 bg-gray-50 rounded-lg">
              <p className="text-xs text-gray-600 mb-2">Then run in terminal:</p>
              <code className="text-xs text-emerald-600 block">chmod +x setup-postgres.sh && ./setup-postgres.sh</code>
            </div>
          </div>
        </div>

        {/* Connection Details */}
        <div className="bg-white rounded-2xl shadow-xl p-6 mb-6 border border-gray-100">
          <h3 className="text-xl font-bold text-gray-900 mb-4">🔗 Connection Details</h3>
          
          <div className="space-y-4">
            {/* Host */}
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
              <div>
                <p className="text-sm text-gray-500 font-medium">Host</p>
                <p className="text-gray-900 font-mono">{credentials.credentials.host}</p>
              </div>
              <button
                onClick={() => handleCopy(credentials.credentials.host, 'host')}
                className="p-2 hover:bg-gray-200 rounded-lg transition-colors"
              >
                {copied === 'host' ? (
                  <CheckCircle className="h-5 w-5 text-green-500" />
                ) : (
                  <Copy className="h-5 w-5 text-gray-500" />
                )}
              </button>
            </div>

            {/* Database */}
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
              <div>
                <p className="text-sm text-gray-500 font-medium">Database</p>
                <p className="text-gray-900 font-mono">{credentials.credentials.database}</p>
              </div>
              <button
                onClick={() => handleCopy(credentials.credentials.database, 'database')}
                className="p-2 hover:bg-gray-200 rounded-lg transition-colors"
              >
                {copied === 'database' ? (
                  <CheckCircle className="h-5 w-5 text-green-500" />
                ) : (
                  <Copy className="h-5 w-5 text-gray-500" />
                )}
              </button>
            </div>

            {/* Username */}
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
              <div>
                <p className="text-sm text-gray-500 font-medium">Username</p>
                <p className="text-gray-900 font-mono">{credentials.credentials.username}</p>
              </div>
              <button
                onClick={() => handleCopy(credentials.credentials.username, 'username')}
                className="p-2 hover:bg-gray-200 rounded-lg transition-colors"
              >
                {copied === 'username' ? (
                  <CheckCircle className="h-5 w-5 text-green-500" />
                ) : (
                  <Copy className="h-5 w-5 text-gray-500" />
                )}
              </button>
            </div>

            {/* Port */}
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
              <div>
                <p className="text-sm text-gray-500 font-medium">Port</p>
                <p className="text-gray-900 font-mono">{credentials.credentials.port}</p>
              </div>
              <button
                onClick={() => handleCopy(credentials.credentials.port.toString(), 'port')}
                className="p-2 hover:bg-gray-200 rounded-lg transition-colors"
              >
                {copied === 'port' ? (
                  <CheckCircle className="h-5 w-5 text-green-500" />
                ) : (
                  <Copy className="h-5 w-5 text-gray-500" />
                )}
              </button>
            </div>

            {/* Connection String */}
            <div className="p-4 bg-gradient-to-r from-sky-50 to-cyan-50 rounded-xl border-2 border-sky-200">
              <div className="flex items-center justify-between mb-2">
                <p className="text-sm text-sky-700 font-bold">Full Connection String</p>
                <button
                  onClick={() => handleCopy(credentials.credentials.connectionString, 'connection')}
                  className="p-2 hover:bg-sky-100 rounded-lg transition-colors"
                >
                  {copied === 'connection' ? (
                    <CheckCircle className="h-5 w-5 text-green-500" />
                  ) : (
                    <Copy className="h-5 w-5 text-sky-600" />
                  )}
                </button>
              </div>
              <p className="text-xs text-gray-700 font-mono break-all">
                {credentials.credentials.connectionString}
              </p>
            </div>
          </div>
        </div>

        {/* Sample Queries */}
        <div className="bg-white rounded-2xl shadow-xl p-6 border border-gray-100">
          <div className="flex items-center mb-4">
            <Book className="h-6 w-6 text-purple-500 mr-2" />
            <h3 className="text-xl font-bold text-gray-900">📝 Sample Queries</h3>
          </div>
          <p className="text-gray-600 mb-4">Try these queries after connecting:</p>
          
          <div className="space-y-4">
            <div className="p-4 bg-gray-50 rounded-xl">
              <p className="text-sm font-medium text-gray-700 mb-2">View your enrollments:</p>
              <pre className="text-xs bg-gray-900 text-green-400 p-3 rounded-lg overflow-x-auto">
{`SELECT b.name, bt.name as batch, e.status
FROM enrollments e
JOIN batches bt ON e.batch_id = bt.id
JOIN bootcamps b ON bt.bootcamp_id = b.id
WHERE e.student_id = '<your-user-id>';`}
              </pre>
            </div>

            <div className="p-4 bg-gray-50 rounded-xl">
              <p className="text-sm font-medium text-gray-700 mb-2">Check your assignment progress:</p>
              <pre className="text-xs bg-gray-900 text-green-400 p-3 rounded-lg overflow-x-auto">
{`SELECT 
  COUNT(CASE WHEN s.status = 'GRADED' THEN 1 END) as completed,
  COUNT(*) as total
FROM assignments a
LEFT JOIN submissions s ON a.id = s.assignment_id
WHERE s.student_id = '<your-user-id>';`}
              </pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
