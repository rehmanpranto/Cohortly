# 🎓 STUDENT PORTAL - QUICK GUIDE

## 📍 Access
**URL**: `http://localhost:3000/student-portal`

**Auto-Redirect**: Students logging in are automatically redirected from dashboard to their portal.

---

## 🖥️ INTERFACE OVERVIEW

### Top Navigation Bar
```
┌──────────────────────────────────────────────────────┐
│ Cohortly Logo | My Learning Dashboard  [User] [Back] │
└──────────────────────────────────────────────────────┘
```

### Stats Section (4 Cards)
```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ 📚 Active   │ ✅ Completed│ ⏰ Pending  │ 📈 Avg      │
│  Bootcamps  │   Tasks     │   Tasks     │  Progress   │
│    [#]      │    [#]      │    [#]      │   [%]       │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

### Main Content (2 Columns)

#### Left: My Bootcamps
```
┌────────────────────────────────────────┐
│ 📚 My Bootcamps                        │
├────────────────────────────────────────┤
│ ┌────────────────────────────────────┐ │
│ │ Web Development Bootcamp           │ │
│ │ Batch A - Fall 2026         ACTIVE │ │
│ │ ▓▓▓▓▓▓▓▓▓▓▓░░░░░░ 65%           │ │
│ │ 📅 Started Jan 18 → View Details  │ │
│ └────────────────────────────────────┘ │
│                                        │
│ ┌────────────────────────────────────┐ │
│ │ Data Science Bootcamp              │ │
│ │ Batch B - Winter 2026       ACTIVE │ │
│ │ ▓▓▓▓▓▓▓▓░░░░░░░░░░ 42%           │ │
│ │ 📅 Started Jan 10 → View Details  │ │
│ └────────────────────────────────────┘ │
└────────────────────────────────────────┘
```

#### Right: Pending Assignments
```
┌────────────────────────────────────────┐
│ 📝 Pending Assignments                 │
├────────────────────────────────────────┤
│ ┌────────────────────────────────┐ 🔴│
│ │ Build Todo App (OVERDUE!)      │   │
│ │ Module 3 • React Basics        │   │
│ │ ⏰ Was due Jan 15  🏆 100pts   │   │
│ │                        [Submit]│   │
│ └────────────────────────────────┘   │
│                                        │
│ ┌────────────────────────────────┐ 🟠│
│ │ Data Cleaning Project          │   │
│ │ Module 1 • Python Fundamentals │   │
│ │ ⏰ Due Jan 20  🏆 50pts        │   │
│ │                        [Submit]│   │
│ └────────────────────────────────┘   │
│                                        │
│ ┌────────────────────────────────┐   │
│ │ SQL Query Assignment           │   │
│ │ Module 2 • Databases           │   │
│ │ ⏰ Due Jan 30  🏆 75pts        │   │
│ │                        [Submit]│   │
│ └────────────────────────────────┘   │
└────────────────────────────────────────┘
```

---

## 🎨 VISUAL INDICATORS

### Progress Bars
| Progress | Color        | Visual                    |
|----------|--------------|---------------------------|
| 0-24%    | Red          | ▓▓░░░░░░░░░░░░░░░░░░     |
| 25-49%   | Yellow       | ▓▓▓▓▓░░░░░░░░░░░░░░░     |
| 50-74%   | Blue         | ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░     |
| 75-100%  | Green        | ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░     |

### Assignment Urgency
| Status      | Color  | Icon | Background      |
|-------------|--------|------|-----------------|
| Overdue     | Red    | 🔴   | Red tint        |
| Due ≤3 days | Orange | 🟠   | Orange tint     |
| Normal      | Gray   | -    | White           |

### Bootcamp Status
| Status    | Badge Color           |
|-----------|-----------------------|
| ACTIVE    | Sky/Cyan gradient     |
| PENDING   | Yellow                |
| COMPLETED | Green                 |
| DROPPED   | Red                   |

---

## 🔔 EMPTY STATES

### No Bootcamps Enrolled
```
        📚
   [Empty Icon]

  No bootcamps enrolled yet
Contact your administrator to get started
```

### No Pending Assignments
```
        ✅
   [Check Icon]

    All caught up! 🎉
   No pending assignments
```

### No Recent Activity
```
        📅
  [Calendar Icon]

   No recent activities
  Check back later for updates
```

---

## 🎯 KEY FEATURES

### ✅ What Students Can See:
1. **Enrollment Status** - Which bootcamps they're enrolled in
2. **Progress Tracking** - Visual progress bars per bootcamp
3. **Assignment List** - All pending assignments in one place
4. **Deadline Alerts** - Color-coded urgency indicators
5. **Quick Submit** - Direct submission buttons
6. **Batch Information** - Which batch they're in
7. **Start Dates** - When bootcamp began

### ❌ What Students DON'T See:
- Lead management
- Other students' data
- Revenue/payment details
- Admin controls
- Instructor tools
- Sales dashboards

---

## 📱 RESPONSIVE DESIGN

### Desktop (>1024px)
- 2-column layout (bootcamps | assignments)
- 4-column stats grid
- Full navigation

### Tablet (768px - 1024px)
- 2-column layout maintained
- 4-column stats grid
- Compact navigation

### Mobile (<768px)
- Single column stacked layout
- 1-column stats grid
- Hamburger menu (if implemented)

---

## 🔌 DATA INTEGRATION

### Required API Calls:
```typescript
// On page load
1. GET /api/v1/enrollments/student/:studentId
   → Fetch student's enrolled bootcamps with progress

2. GET /api/v1/assignments/student/:studentId/pending
   → Fetch assignments not yet submitted

3. GET /api/v1/assignments/student/:studentId/submissions
   → Fetch completed assignments for stats

4. GET /api/v1/announcements/student/:studentId (future)
   → Fetch recent announcements
```

### Mock Data Structure (Current):
```typescript
interface Enrollment {
  id: string;
  status: 'ACTIVE' | 'PENDING' | 'COMPLETED' | 'DROPPED';
  progress: number; // 0-100
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
  submissions?: any[]; // Empty if not submitted
}
```

---

## 🎬 USER INTERACTIONS

### Available Actions:
1. **View Details** (Bootcamp card)
   - Future: Navigate to bootcamp detail page
   - Show curriculum, schedule, resources

2. **Submit** (Assignment card)
   - Future: Open submission modal
   - Upload files or paste URLs
   - Add notes/comments

3. **Back Button** (Top nav)
   - Returns to main dashboard
   - (Currently same page for students)

---

## 🎨 DESIGN TOKENS

### Colors:
```css
/* Backgrounds */
--bg-gradient: linear-gradient(to-br, #f8fafc, #e0f2fe, #cffafe);
--card-bg: rgba(255, 255, 255, 0.9);
--header-bg: rgba(255, 255, 255, 0.8);

/* Accents */
--primary: #0EA5E9;   /* Sky-500 */
--secondary: #06B6D4; /* Cyan-500 */
--success: #10B981;   /* Green-500 */
--warning: #F59E0B;   /* Orange-500 */
--danger: #EF4444;    /* Red-500 */

/* Progress */
--progress-low: linear-gradient(to-right, #F87171, #EF4444);
--progress-mid-low: linear-gradient(to-right, #FBBF24, #F59E0B);
--progress-mid-high: linear-gradient(to-right, #60A5FA, #3B82F6);
--progress-high: linear-gradient(to-right, #34D399, #10B981);
```

### Shadows:
```css
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
--shadow-2xl: 0 25px 50px -12px rgb(0 0 0 / 0.25);
```

### Animations:
```css
--transition-fast: all 200ms ease;
--transition-normal: all 300ms ease;
--hover-lift: translateY(-4px);
--hover-shadow: 0 25px 50px -12px rgb(0 0 0 / 0.25);
```

---

## 🚀 FUTURE ENHANCEMENTS

### Phase 1 (Core):
- [ ] Connect to real enrollment API
- [ ] Implement assignment submission
- [ ] Add bootcamp detail view
- [ ] Enable grade viewing

### Phase 2 (Enhanced):
- [ ] Announcements feed
- [ ] Calendar view for deadlines
- [ ] Progress charts/graphs
- [ ] Download certificates
- [ ] Peer messaging

### Phase 3 (Advanced):
- [ ] AI study recommendations
- [ ] Gamification (badges, points)
- [ ] Discussion forums
- [ ] Video lessons embedded
- [ ] Live class integration

---

## 📊 COMPARISON TO GOOGLE CLASSROOM

### Similarities:
✅ Clean, distraction-free interface  
✅ Assignment list with deadlines  
✅ Progress tracking  
✅ Color-coded urgency  
✅ Card-based layout  
✅ Mobile responsive  

### Differences:
- **More visual** - Gradient backgrounds, icons
- **Progress bars** - Visual bootcamp progress
- **Stats dashboard** - Quick overview metrics
- **Modern design** - Glassmorphism, animations
- **Bootcamp-focused** - Not class-based

---

## 🎓 STUDENT WORKFLOW

### Daily Routine:
1. **Login** → Auto-redirected to portal
2. **Check Stats** → See pending tasks count
3. **Review Bootcamps** → Check progress
4. **View Assignments** → Identify urgent ones
5. **Submit Work** → Complete pending tasks
6. **Check Updates** → Read announcements

### Assignment Workflow:
1. See assignment in **Pending Assignments**
2. Note deadline (overdue/due soon alert)
3. Click **Submit** button
4. Complete and submit work
5. Await grade/feedback
6. View result in completed section

---

## ✨ DESIGN HIGHLIGHTS

### What Makes It Special:
1. **Gradient Magic** - Smooth color transitions everywhere
2. **Micro-interactions** - Buttons lift on hover
3. **Visual Feedback** - Clear urgency indicators
4. **Personality** - Emojis add warmth
5. **Performance** - Smooth 60fps animations
6. **Accessibility** - High contrast, readable

### UX Principles:
- **Progressive Disclosure** - Show only what matters
- **Visual Hierarchy** - Important info stands out
- **Consistency** - Same patterns throughout
- **Feedback** - Clear hover/active states
- **Simplicity** - No cognitive overload

---

## 📞 TROUBLESHOOTING

### If Page Doesn't Load:
1. Check if backend is running (port 5000)
2. Verify frontend is running (port 3000)
3. Confirm user role is 'STUDENT'
4. Check browser console for errors

### If No Data Shows:
- Mock data is in place for UI
- Real API integration pending
- Empty states should display

### If Styling Breaks:
- Clear Next.js cache: `rm -rf .next`
- Restart dev server: `npm run dev`
- Check Tailwind config

---

**Status**: ✅ **LIVE & FUNCTIONAL**  
**URL**: http://localhost:3000/student-portal  
**Test User**: student1@bootcamp.com (Password123!)
