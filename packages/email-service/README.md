# @humanaios/email-service

Email service module for HumanAIOS using SendGrid and Nodemailer.

## Installation

```bash
npm install @humanaios/email-service
```

## Configuration

Set environment variables:
- `SENDGRID_API_KEY` - SendGrid API key
- `FRONTEND_URL` - Base URL for password reset links
- `EMAIL_FROM` - Sender email address (default: noreply@humanaios.com)

Or pass config object to constructor:

```javascript
const EmailService = require('@humanaios/email-service');

const emailService = new EmailService({
  sendgridApiKey: 'your-api-key',
  frontendUrl: 'https://app.humanaios.com',
  emailFrom: 'support@humanaios.com',
});
```

## API

### sendPasswordResetEmail(email, resetToken, firstName)

Send password reset email to user.

**Parameters:**
- `email` (string) - User's email address
- `resetToken` (string) - Password reset token
- `firstName` (string, optional) - User's first name

**Returns:** Promise<void>

**Example:**

```javascript
await emailService.sendPasswordResetEmail(
  'user@example.com',
  'reset-token-xyz',
  'John'
);
```

## Dependencies

- nodemailer ^6.9.0 - Email sending library

## License

MIT
