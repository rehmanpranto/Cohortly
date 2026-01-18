'use client';

import { useAuth } from '@/hooks/useAuth';
import { useRouter } from 'next/navigation';
import { ArrowLeft, BookOpen, FileText, CheckCircle, Clock, AlertCircle, Calendar, TrendingUp, Award } from 'lucide-react';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import CohortlyLogo from '@/components/CohortlyLogo';

interface Enrollment {
  id: string;
  status: string;
  progress: number;
  enrollmentDate: string;
  batch: {
    id: string;
    name: string;
    startDate: string;
    endDate: string;
    bootcamp: {
      id: string;
      name: string;
      description: string;
    };
  };
}

interface Assignment {
  id: string;
  title: string;
  description: string;
  deadline: string;
  maxScore: number;
  lesson: {
    title: string;
    module: {
      name: string;
    };
  };
  submissions?: any[];
}

export default function StudentPortalPage() {
  const { user } = useAuth();
  const router = useRouter();
  const [enrollments, setEnrollments] = useState<Enrollment[]>([]);
  const [assignments, setAssignments] = useState<Assignment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user && user.role !== 'STUDENT') {
      router.push('/dashboard');
      return;
    }
    fetchStudentData();
  }, [user]);

  const fetchStudentData = async () => {
    try {
      // In production, these would be actual API calls
      // For now, using mock data
      setEnrollments([]);
      setAssignments([]);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching student data:', error);
      setLoading(false);
    }
  };

  const getProgressColor = (progress: number) => {
    if (progress >= 75) return 'from-green-400 to-emerald-500';
    if (progress >= 50) return 'from-blue-400 to-sky-500';
    if (progress >= 25) return 'from-yellow-400 to-orange-500';
    return 'from-red-400 to-rose-500';
  };

  const isDeadlineSoon = (deadline: string) => {
    const daysUntil = Math.ceil((new Date(deadline).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24));
    return daysUntil <= 3 && daysUntil >= 0;
  };

  const isOverdue = (deadline: string) => {
    return new Date(deadline) < new Date();
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <nav className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center space-x-4">
              <CohortlyLogo size="sm" showText={true} />
              <div className="hidden md:block h-6 w-px bg-gray-300"></div>
              <h1 className="hidden md:block text-xl font-semibold text-gray-800">
                Student Portal
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-right">
                <p className="font-medium text-gray-900">{user?.fullName}</p>
                <p className="text-gray-500 text-xs">Student</p>
              </div>
              <button
                onClick={() => router.push('/dashboard')}
                className="p-2 rounded-full hover:bg-gray-100 transition-colors"
              >
                <ArrowLeft className="h-5 w-5 text-gray-600" />
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Overview */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-lg p-4 border border-gray-200 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-2xl font-semibold text-gray-900">{enrollments.length}</p>
                <p className="text-xs text-gray-600 mt-1">Enrolled</p>
              </div>
              <BookOpen className="h-8 w-8 text-blue-600" />
            </div>
          </div>

          <div className="bg-white rounded-lg p-4 border border-gray-200 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-2xl font-semibold text-gray-900">
                  {assignments.filter(a => a.submissions && a.submissions.length > 0).length}
                </p>
                <p className="text-xs text-gray-600 mt-1">Completed</p>
              </div>
              <CheckCircle className="h-8 w-8 text-green-600" />
            </div>
          </div>

          <div className="bg-white rounded-lg p-4 border border-gray-200 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-2xl font-semibold text-gray-900">
                  {assignments.filter(a => !a.submissions || a.submissions.length === 0).length}
                </p>
                <p className="text-xs text-gray-600 mt-1">Pending</p>
              </div>
              <Clock className="h-8 w-8 text-orange-600" />
            </div>
          </div>

          <div className="bg-white rounded-lg p-4 border border-gray-200 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-2xl font-semibold text-gray-900">
                  {enrollments.length > 0 ? Math.round(enrollments.reduce((acc, e) => acc + e.progress, 0) / enrollments.length) : 0}%
                </p>
                <p className="text-xs text-gray-600 mt-1">Progress</p>
              </div>
              <TrendingUp className="h-8 w-8 text-purple-600" />
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* My Bootcamps */}
          <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900 flex items-center">
                <BookOpen className="h-5 w-5 mr-2 text-gray-700" />
                Enrolled Bootcamps
              </h3>
            </div>
            <div className="p-6 space-y-3 max-h-[600px] overflow-y-auto">
              {enrollments.length === 0 ? (
                <div className="text-center py-12">
                  <BookOpen className="h-12 w-12 text-gray-300 mx-auto mb-3" />
                  <p className="text-gray-500 text-sm">No bootcamps enrolled</p>
                  <p className="text-gray-400 text-xs mt-1">Contact your administrator to get started</p>
                </div>
              ) : (
                enrollments.map((enrollment) => (
                  <div
                    key={enrollment.id}
                    className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 hover:border-gray-300 transition-all cursor-pointer"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex-1">
                        <h4 className="font-medium text-gray-900 text-sm">
                          {enrollment.batch.bootcamp.name}
                        </h4>
                        <p className="text-xs text-gray-500 mt-1">{enrollment.batch.name}</p>
                      </div>
                      <span className="px-2 py-1 bg-blue-50 text-blue-700 text-xs font-medium rounded">
                        {enrollment.status}
                      </span>
                    </div>
                    
                    <div className="mb-3">
                      <div className="flex items-center justify-between mb-1.5">
                        <span className="text-xs text-gray-600">Progress</span>
                        <span className="text-xs font-medium text-gray-900">{enrollment.progress}%</span>
                      </div>
                      <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-blue-600 transition-all duration-300 rounded-full"
                          style={{ width: `${enrollment.progress}%` }}
                        ></div>
                      </div>
                    </div>

                    <div className="flex items-center justify-between text-xs text-gray-500">
                      <div className="flex items-center">
                        <Calendar className="h-3.5 w-3.5 mr-1" />
                        <span>{new Date(enrollment.batch.startDate).toLocaleDateString()}</span>
                      </div>
                      <span className="text-blue-600 hover:text-blue-700 font-medium">
                        View →
                      </span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Pending Assignments */}
          <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900 flex items-center">
                <FileText className="h-5 w-5 mr-2 text-gray-700" />
                Pending Assignments
              </h3>
            </div>
            <div className="p-6 space-y-3 max-h-[600px] overflow-y-auto">
              {assignments.filter(a => !a.submissions || a.submissions.length === 0).length === 0 ? (
                <div className="text-center py-12">
                  <CheckCircle className="h-12 w-12 text-green-500 mx-auto mb-3" />
                  <p className="text-gray-500 text-sm font-medium">All caught up!</p>
                  <p className="text-gray-400 text-xs mt-1">No pending assignments</p>
                </div>
              ) : (
                assignments
                  .filter(a => !a.submissions || a.submissions.length === 0)
                  .map((assignment) => {
                    const overdue = isOverdue(assignment.deadline);
                    const dueSoon = isDeadlineSoon(assignment.deadline);
                    
                    return (
                      <div
                        key={assignment.id}
                        className={`border rounded-lg p-4 hover:bg-gray-50 transition-all ${
                          overdue
                            ? 'border-red-300 bg-red-50'
                            : dueSoon
                            ? 'border-orange-300 bg-orange-50'
                            : 'border-gray-200'
                        }`}
                      >
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex-1">
                            <h4 className="font-medium text-gray-900 text-sm">{assignment.title}</h4>
                            <p className="text-xs text-gray-500 mt-1">
                              {assignment.lesson.module.name} • {assignment.lesson.title}
                            </p>
                          </div>
                          {overdue && (
                            <span className="px-2 py-1 bg-red-100 text-red-700 text-xs font-medium rounded flex items-center">
                              <AlertCircle className="h-3 w-3 mr-1" />
                              Overdue
                            </span>
                          )}
                          {dueSoon && !overdue && (
                            <span className="px-2 py-1 bg-orange-100 text-orange-700 text-xs font-medium rounded">
                              Due soon
                            </span>
                          )}
                        </div>

                        <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                          {assignment.description}
                        </p>

                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-3 text-xs text-gray-600">
                            <div className="flex items-center">
                              <Clock className="h-3.5 w-3.5 mr-1" />
                              <span>{new Date(assignment.deadline).toLocaleDateString()}</span>
                            </div>
                            <div className="flex items-center">
                              <Award className="h-3.5 w-3.5 mr-1" />
                              <span>{assignment.maxScore} pts</span>
                            </div>
                          </div>
                          <button className="px-4 py-1.5 bg-blue-600 text-white text-xs font-medium rounded hover:bg-blue-700 transition-colors">
                            Submit
                          </button>
                        </div>
                      </div>
                    );
                  })
              )}
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="mt-6 bg-white rounded-lg border border-gray-200 overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">Recent Activity</h3>
          </div>
          <div className="p-6">
            <div className="text-center py-12">
              <Calendar className="h-12 w-12 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-500 text-sm">No recent activities</p>
              <p className="text-gray-400 text-xs mt-1">Check back later for updates</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
