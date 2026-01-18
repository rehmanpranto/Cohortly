'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';

export function useAuth(requiredRole?: string[]) {
  const router = useRouter();
  const { isAuthenticated, user } = useAuthStore();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    if (requiredRole && user && !requiredRole.includes(user.role)) {
      router.push('/unauthorized');
    }
  }, [isAuthenticated, user, requiredRole, router]);

  return { isAuthenticated, user };
}
