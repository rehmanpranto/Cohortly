'use client';

import { useAuth } from '@/hooks/useAuth';
import { useRouter } from 'next/navigation';
import { ArrowLeft, Calendar as CalendarIcon, Clock, MapPin, Video } from 'lucide-react';

export default function SchedulePage() {
  const { user } = useAuth();
  const router = useRouter();

  if (!user) return null;

  const events = [
    {
      id: 1,
      title: 'React Fundamentals - Live Session',
      bootcamp: 'Full Stack Web Development',
      time: '10:00 AM - 12:00 PM',
      date: 'Jan 20, 2026',
      type: 'Online',
      instructor: 'Prof. Sarah Johnson',
      color: 'bg-blue-500'
    },
    {
      id: 2,
      title: 'JavaScript Advanced Concepts',
      bootcamp: 'Full Stack Web Development',
      time: '2:00 PM - 4:00 PM',
      date: 'Jan 21, 2026',
      type: 'Online',
      instructor: 'Prof. Michael Chen',
      color: 'bg-purple-500'
    },
    {
      id: 3,
      title: 'Database Design Workshop',
      bootcamp: 'Full Stack Web Development',
      time: '9:00 AM - 11:00 AM',
      date: 'Jan 22, 2026',
      type: 'Hybrid',
      instructor: 'Prof. Sarah Johnson',
      color: 'bg-green-500'
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => router.push('/dashboard')}
                className="p-2 hover:bg-gray-100 rounded-md"
              >
                <ArrowLeft className="h-5 w-5 text-gray-600" />
              </button>
              <h1 className="text-2xl font-bold text-gray-900">Schedule</h1>
            </div>
            <div className="flex items-center space-x-3">
              <select className="px-4 py-2 border border-gray-300 rounded-md text-sm focus:ring-indigo-500 focus:border-indigo-500">
                <option>All Bootcamps</option>
                <option>Full Stack Web Development</option>
                <option>Data Science & AI</option>
                <option>Mobile App Development</option>
              </select>
              <button className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-md hover:bg-indigo-700">
                Today
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Calendar View (Placeholder) */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold text-gray-900">January 2026</h2>
                <div className="flex space-x-2">
                  <button className="px-3 py-1 text-sm text-gray-700 hover:bg-gray-100 rounded-md">Previous</button>
                  <button className="px-3 py-1 text-sm text-gray-700 hover:bg-gray-100 rounded-md">Next</button>
                </div>
              </div>
              
              {/* Simple Calendar Grid */}
              <div className="grid grid-cols-7 gap-2">
                {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day) => (
                  <div key={day} className="text-center text-sm font-medium text-gray-500 py-2">
                    {day}
                  </div>
                ))}
                {Array.from({ length: 35 }, (_, i) => {
                  const day = i - 2; // Start from day -2 to have some empty cells
                  const isCurrentMonth = day >= 1 && day <= 31;
                  const hasEvent = [20, 21, 22].includes(day);
                  
                  return (
                    <div
                      key={i}
                      className={`aspect-square flex items-center justify-center text-sm rounded-lg cursor-pointer
                        ${isCurrentMonth ? 'hover:bg-gray-100' : 'text-gray-300'}
                        ${hasEvent ? 'bg-indigo-50 text-indigo-600 font-semibold' : ''}
                        ${day === 18 ? 'bg-indigo-600 text-white font-bold' : ''}
                      `}
                    >
                      {isCurrentMonth ? day : ''}
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Upcoming Events */}
            <div className="mt-6 bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Upcoming Events</h2>
              <div className="space-y-4">
                {events.map((event) => (
                  <div key={event.id} className="flex items-start space-x-4 p-4 hover:bg-gray-50 rounded-lg transition-colors">
                    <div className={`flex-shrink-0 w-1 h-16 ${event.color} rounded-full`}></div>
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900">{event.title}</h3>
                      <p className="text-sm text-gray-500 mt-1">{event.bootcamp}</p>
                      <div className="flex items-center space-x-4 mt-2">
                        <div className="flex items-center text-sm text-gray-500">
                          <CalendarIcon className="h-4 w-4 mr-1" />
                          {event.date}
                        </div>
                        <div className="flex items-center text-sm text-gray-500">
                          <Clock className="h-4 w-4 mr-1" />
                          {event.time}
                        </div>
                        <div className="flex items-center text-sm text-gray-500">
                          <Video className="h-4 w-4 mr-1" />
                          {event.type}
                        </div>
                      </div>
                    </div>
                    <button className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-md hover:bg-indigo-700">
                      Join
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Today's Schedule */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Today's Schedule</h2>
              <div className="space-y-3">
                <div className="text-center py-8 text-gray-500">
                  <CalendarIcon className="h-12 w-12 mx-auto mb-2 text-gray-300" />
                  <p className="text-sm">No events scheduled for today</p>
                </div>
              </div>
            </div>

            {/* Quick Stats */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">This Week</h2>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Total Sessions</span>
                  <span className="font-semibold text-gray-900">12</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Hours</span>
                  <span className="font-semibold text-gray-900">24</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Bootcamps</span>
                  <span className="font-semibold text-gray-900">5</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
