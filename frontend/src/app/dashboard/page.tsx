'use client';

import { useAuth } from '@/hooks/useAuth';
import { useAuthStore } from '@/store/authStore';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import Link from 'next/link';
import CohortlyLogo from '@/components/CohortlyLogo';
import { 
  Users, 
  BookOpen, 
  GraduationCap, 
  FileText, 
  DollarSign, 
  Calendar,
  LogOut,
  UserCircle
} from 'lucide-react';

export default function DashboardPage() {
  const { user } = useAuth();
  const router = useRouter();
  const logout = useAuthStore((state) => state.logout);

  // Redirect students to their dedicated portal
  useEffect(() => {
    if (user && user.role === 'STUDENT') {
      router.push('/student-portal');
    }
  }, [user, router]);

  const handleLogout = () => {
    logout();
    window.location.href = '/login';
  };

  const getRoleBadgeColor = (role: string) => {
    const colors: Record<string, string> = {
      ADMIN: 'bg-purple-100 text-purple-800',
      SALES: 'bg-green-100 text-green-800',
      INSTRUCTOR: 'bg-blue-100 text-blue-800',
      MENTOR: 'bg-yellow-100 text-yellow-800',
      STUDENT: 'bg-pink-100 text-pink-800',
    };
    return colors[role] || 'bg-gray-100 text-gray-800';
  };

  const stats = [
    { name: 'Total Students', value: '156', icon: Users, color: 'bg-sky-500' },
    { name: 'Active Bootcamps', value: '8', icon: BookOpen, color: 'bg-cyan-500' },
    { name: 'Assignments', value: '24', icon: FileText, color: 'bg-teal-500' },
    { name: 'Revenue', value: '$45,231', icon: DollarSign, color: 'bg-blue-500' },
  ];

  const quickLinks = [
    { name: 'Manage Leads', icon: Users, href: '/leads', show: ['ADMIN', 'SALES'] },
    { name: 'Bootcamps', icon: BookOpen, href: '/bootcamps', show: ['ADMIN', 'INSTRUCTOR'] },
    { name: 'Enrollments', icon: GraduationCap, href: '/enrollments', show: ['ADMIN', 'SALES'] },
    { name: 'Assignments', icon: FileText, href: '/assignments', show: ['ADMIN', 'INSTRUCTOR', 'MENTOR'] },
    { name: 'Schedule', icon: Calendar, href: '/schedule', show: ['ADMIN', 'INSTRUCTOR', 'STUDENT'] },
    { name: 'Students', icon: Users, href: '/students', show: ['ADMIN', 'INSTRUCTOR', 'MENTOR'] },
  ];

  // Show loading while redirecting students
  if (user && user.role === 'STUDENT') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-sky-500"></div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-sky-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50">
      {/* Header */}
      <nav className="bg-white/80 backdrop-blur-md shadow-sm border-b border-sky-100 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <CohortlyLogo size="sm" showText={true} />
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-3 bg-gradient-to-r from-sky-50 to-cyan-50 px-4 py-2 rounded-xl">
                <UserCircle className="h-8 w-8 text-sky-500" />
                <div className="text-sm">
                  <p className="font-semibold text-gray-900">{user.fullName}</p>
                  <p className="text-gray-600 text-xs">{user.email}</p>
                </div>
                <span className={`px-3 py-1 text-xs font-bold rounded-full ${getRoleBadgeColor(user.role)} shadow-sm`}>
                  {user.role}
                </span>
              </div>
              <button
                onClick={handleLogout}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-semibold rounded-xl text-white bg-gradient-to-r from-sky-500 to-cyan-500 hover:from-sky-600 hover:to-cyan-600 transition-all duration-200 shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
              >
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8 animate-fade-in">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-sky-600 to-cyan-600 bg-clip-text text-transparent">
            Welcome back, {user.fullName}! 👋
          </h1>
          <p className="mt-2 text-lg text-gray-600">Here's what's happening with your bootcamps today.</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-8">
          {stats.map((stat, index) => (
            <div 
              key={stat.name} 
              className="bg-white overflow-hidden shadow-lg rounded-2xl transform transition-all duration-300 hover:shadow-2xl hover:-translate-y-1 border border-gray-100"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <div className="p-6">
                <div className="flex items-center justify-between">
                  <div className={`${stat.color} rounded-xl p-4 shadow-md`}>
                    <stat.icon className="h-7 w-7 text-white" />
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-500 uppercase tracking-wide">{stat.name}</p>
                    <p className="text-3xl font-bold bg-gradient-to-r from-sky-600 to-cyan-600 bg-clip-text text-transparent mt-1">
                      {stat.value}
                    </p>
                  </div>
                </div>
              </div>
              <div className="bg-gradient-to-r from-sky-50 to-cyan-50 px-6 py-3">
                <p className="text-xs text-sky-700 font-medium">↗ View Details</p>
              </div>
            </div>
          ))}
        </div>

        {/* Quick Links */}
        <div className="bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl border border-gray-100">
          <div className="px-6 py-5 border-b border-gray-100 bg-gradient-to-r from-sky-50 to-cyan-50">
            <h2 className="text-xl font-bold text-gray-900">🚀 Quick Actions</h2>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 p-6">
              {quickLinks
                .filter((link) => link.show.includes(user.role))
                .map((link, index) => (
                  <Link
                    key={link.name}
                    href={link.href}
                    className="group relative bg-gradient-to-br from-white to-gray-50 p-6 rounded-2xl border-2 border-gray-200 hover:border-sky-400 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 overflow-hidden"
                    style={{ animationDelay: `${index * 50}ms` }}
                  >
                    <div className="absolute top-0 right-0 -mt-4 -mr-4 w-24 h-24 bg-gradient-to-br from-sky-400 to-cyan-400 rounded-full opacity-10 group-hover:opacity-20 transition-opacity duration-300"></div>
                    <div className="relative">
                      <span className="rounded-xl inline-flex p-4 bg-gradient-to-br from-sky-50 to-cyan-50 text-sky-600 ring-4 ring-white shadow-md group-hover:scale-110 transition-transform duration-300">
                        <link.icon className="h-7 w-7" />
                      </span>
                    </div>
                    <div className="mt-5 relative">
                      <h3 className="text-lg font-bold text-gray-900 group-hover:text-sky-600 transition-colors duration-200">
                        {link.name}
                      </h3>
                      <p className="mt-2 text-sm text-gray-600">
                        Manage and track {link.name.toLowerCase()}
                      </p>
                      <div className="mt-4 flex items-center text-sky-600 font-medium text-sm">
                        <span className="group-hover:translate-x-1 transition-transform duration-200">Go to {link.name}</span>
                        <span className="ml-1 group-hover:translate-x-1 transition-transform duration-200">→</span>
                      </div>
                    </div>
                  </Link>
                ))}
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="mt-8 bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl border border-gray-100">
          <div className="px-6 py-5 border-b border-gray-100 bg-gradient-to-r from-sky-50 to-cyan-50">
            <h2 className="text-xl font-bold text-gray-900">📊 Recent Activity</h2>
          </div>
          <div className="p-6">
            <div className="flow-root">
              <ul className="-my-5 divide-y divide-gray-100">
                <li className="py-5 hover:bg-sky-50 px-4 rounded-lg transition-colors duration-200">
                  <div className="flex items-center space-x-4">
                    <div className="flex-shrink-0">
                      <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-green-400 to-emerald-500 flex items-center justify-center shadow-md">
                        <Users className="h-6 w-6 text-white" />
                      </div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900">New student enrolled</p>
                      <p className="text-sm text-gray-500">John Doe joined Web Development Bootcamp</p>
                    </div>
                    <div className="text-sm text-gray-500">2 hours ago</div>
                  </div>
                </li>
                <li className="py-5 hover:bg-sky-50 px-4 rounded-lg transition-colors duration-200">
                  <div className="flex items-center space-x-4">
                    <div className="flex-shrink-0">
                      <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-blue-400 to-sky-500 flex items-center justify-center shadow-md">
                        <FileText className="h-6 w-6 text-white" />
                      </div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900">Assignment submitted</p>
                      <p className="text-sm text-gray-500">15 new submissions to review</p>
                    </div>
                    <div className="text-sm text-gray-500">5 hours ago</div>
                  </div>
                </li>
                <li className="py-5 hover:bg-sky-50 px-4 rounded-lg transition-colors duration-200">
                  <div className="flex items-center space-x-4">
                    <div className="flex-shrink-0">
                      <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-purple-400 to-fuchsia-500 flex items-center justify-center shadow-md">
                        <DollarSign className="h-6 w-6 text-white" />
                      </div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900">Payment received</p>
                      <p className="text-sm text-gray-500">$2,500 from Jane Smith</p>
                    </div>
                    <div className="text-sm text-gray-500">1 day ago</div>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
