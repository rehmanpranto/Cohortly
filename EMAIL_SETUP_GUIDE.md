# 📧 SendGrid Email Integration Setup Guide

## 🎯 Overview
This guide will help you set up SendGrid email integration for Cohortly, including DNS configuration for domain authentication.

---

## 📋 Prerequisites

- SendGrid account (Free tier: 100 emails/day)
- Access to your domain DNS settings (cohortly.com)
- Domain ownership verification

---

## 🔧 Step 1: DNS Configuration

### Required DNS Records

Add the following DNS records to your domain registrar (GoDaddy, Namecheap, Cloudflare, etc.):

#### 1. CNAME Record - Email Subdomain
```
Type:  CNAME
Host:  em5173.cohortly.com
Value: u59037209.wl210.sendgrid.net
TTL:   3600 (or automatic)
```

#### 2. CNAME Record - DKIM Key 1
```
Type:  CNAME
Host:  s1._domainkey.cohortly.com
Value: s1.domainkey.u59037209.wl210.sendgrid.net
TTL:   3600 (or automatic)
```

#### 3. CNAME Record - DKIM Key 2
```
Type:  CNAME
Host:  s2._domainkey.cohortly.com
Value: s2.domainkey.u59037209.wl210.sendgrid.net
TTL:   3600 (or automatic)
```

#### 4. TXT Record - DMARC Policy
```
Type:  TXT
Host:  _dmarc.cohortly.com
Value: v=DMARC1; p=none;
TTL:   3600 (or automatic)
```

---

## 🌐 DNS Setup by Provider

### Option 1: Cloudflare (Recommended)
1. Log in to Cloudflare dashboard
2. Select your domain `cohortly.com`
3. Go to **DNS** > **Records**
4. Click **Add record** for each entry above
5. Enter Type, Name, and Target/Content
6. Click **Save**

### Option 2: GoDaddy
1. Log in to GoDaddy account
2. Go to **My Products** > **DNS**
3. Click **Add** in the DNS Records section
4. Select record type (CNAME or TXT)
5. Enter Host and Points to/Value
6. Click **Save**

### Option 3: Namecheap
1. Log in to Namecheap
2. Go to **Domain List** > Select domain
3. Go to **Advanced DNS** tab
4. Click **Add New Record**
5. Enter record details
6. Click checkmark to save

### Option 4: AWS Route 53
1. Open Route 53 console
2. Select hosted zone for `cohortly.com`
3. Click **Create record**
4. Enter record details
5. Click **Create records**

---

## ⏱️ DNS Propagation

- **Typical time:** 1-4 hours
- **Maximum time:** 24-48 hours
- **Check status:** Use [DNS Checker](https://dnschecker.org/)

---

## 🔑 Step 2: Get SendGrid API Key

1. Log in to [SendGrid](https://app.sendgrid.com/)
2. Go to **Settings** > **API Keys**
3. Click **Create API Key**
4. Name: `Cohortly-Production`
5. Permissions: **Full Access** (or Restricted with Mail Send permissions)
6. Click **Create & View**
7. **COPY THE API KEY** (you won't see it again!)

---

## 💻 Step 3: Backend Implementation

### 3.1 Install Dependencies

```bash
cd backend
npm install @sendgrid/mail
```

### 3.2 Update Environment Variables

Add to `backend/.env`:

```bash
# SendGrid Configuration
SENDGRID_API_KEY="SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
SENDGRID_FROM_EMAIL="noreply@cohortly.com"
SENDGRID_FROM_NAME="Cohortly Bootcamp"
SENDGRID_VERIFIED_SENDER="noreply@cohortly.com"
```

### 3.3 Create Email Service

Create `backend/src/services/email.service.ts`:

```typescript
import sgMail from '@sendgrid/mail';
import { config } from '../config/config';
import { logger } from '../config/logger';

// Initialize SendGrid
sgMail.setApiKey(config.sendgrid.apiKey);

interface EmailOptions {
  to: string | string[];
  subject: string;
  text?: string;
  html: string;
  from?: {
    email: string;
    name: string;
  };
}

class EmailService {
  private defaultFrom = {
    email: config.sendgrid.fromEmail,
    name: config.sendgrid.fromName,
  };

  /**
   * Send a single email
   */
  async sendEmail(options: EmailOptions): Promise<boolean> {
    try {
      const msg = {
        to: options.to,
        from: options.from || this.defaultFrom,
        subject: options.subject,
        text: options.text || '',
        html: options.html,
      };

      await sgMail.send(msg);
      logger.info(`Email sent successfully to ${options.to}`);
      return true;
    } catch (error: any) {
      logger.error('SendGrid email error:', error);
      if (error.response) {
        logger.error(error.response.body);
      }
      return false;
    }
  }

  /**
   * Send welcome email to new student
   */
  async sendWelcomeEmail(email: string, fullName: string): Promise<boolean> {
    const html = `
      <!DOCTYPE html>
      <html>
      <head>
        <style>
          body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
          .container { max-width: 600px; margin: 0 auto; padding: 20px; }
          .header { background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
          .content { background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }
          .button { display: inline-block; padding: 12px 30px; background: #0ea5e9; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }
          .footer { text-align: center; margin-top: 20px; color: #666; font-size: 12px; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1>Welcome to Cohortly! 🎉</h1>
          </div>
          <div class="content">
            <h2>Hi ${fullName},</h2>
            <p>Welcome to Cohortly - your journey to success starts here!</p>
            <p>We're excited to have you as part of our learning community. Here's what you can do now:</p>
            <ul>
              <li>Browse available bootcamps</li>
              <li>Enroll in courses that interest you</li>
              <li>Track your progress</li>
              <li>Connect with instructors and mentors</li>
            </ul>
            <a href="http://localhost:3000/student-portal" class="button">Go to Dashboard</a>
            <p>If you have any questions, feel free to reach out to our support team.</p>
            <p>Happy learning!</p>
            <p><strong>The Cohortly Team</strong></p>
          </div>
          <div class="footer">
            <p>© 2026 Cohortly. All rights reserved.</p>
            <p>You received this email because you signed up for Cohortly.</p>
          </div>
        </div>
      </body>
      </html>
    `;

    return this.sendEmail({
      to: email,
      subject: 'Welcome to Cohortly! 🎉',
      html,
    });
  }

  /**
   * Send enrollment confirmation
   */
  async sendEnrollmentConfirmation(
    email: string,
    fullName: string,
    bootcampName: string
  ): Promise<boolean> {
    const html = `
      <!DOCTYPE html>
      <html>
      <head>
        <style>
          body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
          .container { max-width: 600px; margin: 0 auto; padding: 20px; }
          .header { background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
          .content { background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }
          .bootcamp-card { background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #10b981; }
          .button { display: inline-block; padding: 12px 30px; background: #10b981; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1>Enrollment Confirmed! ✅</h1>
          </div>
          <div class="content">
            <h2>Hi ${fullName},</h2>
            <p>Great news! You're now enrolled in:</p>
            <div class="bootcamp-card">
              <h3>${bootcampName}</h3>
            </div>
            <p>You can now access all course materials, assignments, and resources.</p>
            <a href="http://localhost:3000/student-portal" class="button">View My Courses</a>
            <p>Let's get started on your learning journey!</p>
            <p><strong>The Cohortly Team</strong></p>
          </div>
        </div>
      </body>
      </html>
    `;

    return this.sendEmail({
      to: email,
      subject: `Enrollment Confirmed: ${bootcampName}`,
      html,
    });
  }

  /**
   * Send assignment notification
   */
  async sendAssignmentNotification(
    email: string,
    fullName: string,
    assignmentTitle: string,
    dueDate: string,
    bootcampName: string
  ): Promise<boolean> {
    const html = `
      <!DOCTYPE html>
      <html>
      <head>
        <style>
          body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
          .container { max-width: 600px; margin: 0 auto; padding: 20px; }
          .header { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
          .content { background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }
          .assignment-card { background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #f59e0b; }
          .due-date { color: #d97706; font-weight: bold; }
          .button { display: inline-block; padding: 12px 30px; background: #f59e0b; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1>New Assignment Posted! 📝</h1>
          </div>
          <div class="content">
            <h2>Hi ${fullName},</h2>
            <p>A new assignment has been posted in <strong>${bootcampName}</strong>:</p>
            <div class="assignment-card">
              <h3>${assignmentTitle}</h3>
              <p class="due-date">Due: ${dueDate}</p>
            </div>
            <a href="http://localhost:3000/student-portal" class="button">View Assignment</a>
            <p>Don't forget to submit before the deadline!</p>
            <p><strong>The Cohortly Team</strong></p>
          </div>
        </div>
      </body>
      </html>
    `;

    return this.sendEmail({
      to: email,
      subject: `New Assignment: ${assignmentTitle}`,
      html,
    });
  }

  /**
   * Send password reset email
   */
  async sendPasswordResetEmail(
    email: string,
    fullName: string,
    resetToken: string
  ): Promise<boolean> {
    const resetUrl = `http://localhost:3000/reset-password?token=${resetToken}`;
    
    const html = `
      <!DOCTYPE html>
      <html>
      <head>
        <style>
          body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
          .container { max-width: 600px; margin: 0 auto; padding: 20px; }
          .header { background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
          .content { background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }
          .button { display: inline-block; padding: 12px 30px; background: #ef4444; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }
          .warning { background: #fef2f2; border-left: 4px solid #ef4444; padding: 15px; margin: 20px 0; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1>Password Reset Request 🔒</h1>
          </div>
          <div class="content">
            <h2>Hi ${fullName},</h2>
            <p>We received a request to reset your password. Click the button below to create a new password:</p>
            <a href="${resetUrl}" class="button">Reset Password</a>
            <div class="warning">
              <strong>⚠️ Important:</strong>
              <ul>
                <li>This link expires in 1 hour</li>
                <li>If you didn't request this, please ignore this email</li>
                <li>Never share this link with anyone</li>
              </ul>
            </div>
            <p>If the button doesn't work, copy and paste this link:</p>
            <p style="word-break: break-all; color: #0ea5e9;">${resetUrl}</p>
            <p><strong>The Cohortly Team</strong></p>
          </div>
        </div>
      </body>
      </html>
    `;

    return this.sendEmail({
      to: email,
      subject: 'Reset Your Password - Cohortly',
      html,
    });
  }
}

export const emailService = new EmailService();
```

### 3.4 Update Config File

Add to `backend/src/config/config.ts`:

```typescript
export const config = {
  // ...existing config...
  
  sendgrid: {
    apiKey: process.env.SENDGRID_API_KEY || '',
    fromEmail: process.env.SENDGRID_FROM_EMAIL || 'noreply@cohortly.com',
    fromName: process.env.SENDGRID_FROM_NAME || 'Cohortly',
  },
};
```

### 3.5 Integrate with Auth Service

Update `backend/src/services/auth.service.ts`:

```typescript
import { emailService } from './email.service';

class AuthService {
  async register(data: RegisterData) {
    // ...existing registration code...

    // Send welcome email
    await emailService.sendWelcomeEmail(user.email, user.fullName);

    return { user, accessToken, refreshToken };
  }
}
```

---

## ✅ Step 4: Verify Setup

### 4.1 Check DNS Records

```bash
# Check CNAME records
nslookup -type=CNAME em5173.cohortly.com
nslookup -type=CNAME s1._domainkey.cohortly.com
nslookup -type=CNAME s2._domainkey.cohortly.com

# Check TXT record
nslookup -type=TXT _dmarc.cohortly.com
```

### 4.2 Verify in SendGrid Dashboard

1. Go to **Settings** > **Sender Authentication**
2. Check **Domain Authentication** status
3. Should show ✅ **Verified**

### 4.3 Test Email Sending

Create a test endpoint in your backend:

```typescript
// backend/src/routes/test.routes.ts
import { Router } from 'express';
import { emailService } from '../services/email.service';

const router = Router();

router.post('/test-email', async (req, res) => {
  const { email } = req.body;
  
  const success = await emailService.sendWelcomeEmail(
    email,
    'Test User'
  );
  
  res.json({ success, message: success ? 'Email sent!' : 'Failed to send email' });
});

export default router;
```

Test with curl:
```bash
curl -X POST http://localhost:5000/api/v1/test/test-email \
  -H "Content-Type: application/json" \
  -d '{"email":"your-email@example.com"}'
```

---

## 🔒 DMARC Policy Explanation

**Current setting:** `v=DMARC1; p=none;`

- `v=DMARC1` - DMARC version 1
- `p=none` - Monitor mode (no action on failures)

### Upgrade DMARC (After Testing)

After confirming emails work properly, upgrade to:

```
v=DMARC1; p=quarantine; pct=100; rua=mailto:dmarc@cohortly.com;
```

- `p=quarantine` - Move suspicious emails to spam
- `pct=100` - Apply to 100% of emails
- `rua=mailto:dmarc@cohortly.com` - Receive aggregate reports

Or strict mode:
```
v=DMARC1; p=reject; pct=100; rua=mailto:dmarc@cohortly.com;
```

---

## 📊 SendGrid Dashboard Features

### Monitor Email Activity
1. Go to **Activity**
2. View sent emails, opens, clicks, bounces, spam reports
3. Filter by date, recipient, status

### Email Templates
1. Go to **Email API** > **Dynamic Templates**
2. Create reusable templates
3. Use handlebars syntax for variables

### Webhook Setup (Optional)
1. Go to **Settings** > **Mail Settings** > **Event Webhook**
2. Set webhook URL: `https://api.cohortly.com/webhooks/sendgrid`
3. Select events: Delivered, Opened, Clicked, Bounced, etc.

---

## 🚨 Troubleshooting

### Problem: DNS records not propagating
**Solution:** Wait 24-48 hours, clear DNS cache:
```bash
# Windows
ipconfig /flushdns

# Mac
sudo dscacheutil -flushcache

# Linux
sudo systemd-resolve --flush-caches
```

### Problem: SendGrid authentication failed
**Solution:** 
- Verify API key is correct
- Check API key permissions (Full Access or Mail Send)
- Regenerate API key if needed

### Problem: Emails going to spam
**Solution:**
- Verify domain authentication (SPF, DKIM, DMARC)
- Add plain text version to emails
- Avoid spam trigger words
- Warm up your sending domain gradually

### Problem: API rate limits exceeded
**Solution:**
- Free tier: 100 emails/day
- Upgrade to paid plan
- Implement email queue with Bull/Redis

---

## 📈 Best Practices

1. **Test in development first** - Use Mailtrap or SendGrid sandbox
2. **Use templates** - Create reusable email templates
3. **Queue emails** - Don't send synchronously in API requests
4. **Monitor deliverability** - Check bounce rates, spam reports
5. **Personalize emails** - Use recipient names, relevant content
6. **Mobile-friendly** - Test emails on mobile devices
7. **Unsubscribe link** - Always include (legal requirement)
8. **Track engagement** - Monitor opens and clicks

---

## 🔗 Useful Resources

- [SendGrid Documentation](https://docs.sendgrid.com/)
- [SendGrid Node.js Library](https://github.com/sendgrid/sendgrid-nodejs)
- [DNS Checker Tool](https://dnschecker.org/)
- [DMARC Guide](https://dmarc.org/)
- [Email Testing Tool](https://www.mail-tester.com/)

---

## 📝 Next Steps

- [ ] Add DNS records to domain registrar
- [ ] Wait for DNS propagation (1-24 hours)
- [ ] Verify domain in SendGrid dashboard
- [ ] Get SendGrid API key
- [ ] Update backend .env file
- [ ] Install @sendgrid/mail package
- [ ] Create email service
- [ ] Test email sending
- [ ] Monitor email deliverability
- [ ] Upgrade DMARC policy after testing

---

**Last Updated:** January 19, 2026  
**Status:** Ready for Implementation  
**Priority:** High (Phase 1 Feature)
