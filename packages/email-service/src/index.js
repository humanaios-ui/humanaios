const nodemailer = require('nodemailer');

class EmailService {
  constructor(config = {}) {
    this.config = {
      sendgridApiKey: config.sendgridApiKey || process.env.SENDGRID_API_KEY,
      frontendUrl: config.frontendUrl || process.env.FRONTEND_URL,
      emailFrom: config.emailFrom || process.env.EMAIL_FROM || 'noreply@humanaios.com',
    };

    // Only create transporter if API key is provided
    if (this.config.sendgridApiKey) {
      this.transporter = nodemailer.createTransport({
        host: 'smtp.sendgrid.net',
        port: 587,
        auth: {
          user: 'apikey',
          pass: this.config.sendgridApiKey,
        },
      });
    } else {
      console.log('⚠️  Email service disabled (no SENDGRID_API_KEY)');
      this.transporter = null;
    }
  }

  async sendPasswordResetEmail(email, resetToken, firstName) {
    if (!this.transporter) {
      console.log('⚠️  Email not sent (email service not configured)');
      console.log(`Reset token for ${email}: ${resetToken}`);
      return;
    }

    const resetLink = `${this.config.frontendUrl}/reset-password?token=${resetToken}`;

    const mailOptions = {
      from: this.config.emailFrom,
      to: email,
      subject: 'Password Reset Request - HumanAIOS',
      html: `
        <h2>Password Reset Request</h2>
        <p>Hi ${firstName || 'there'},</p>
        <p>Click the link below to reset your password:</p>
        <p><a href="${resetLink}">${resetLink}</a></p>
        <p>This link expires in 1 hour.</p>
      `,
    };

    try {
      await this.transporter.sendMail(mailOptions);
      console.log(`✅ Password reset email sent to ${email}`);
    } catch (error) {
      console.error('❌ Error sending email:', error);
      throw new Error('Failed to send password reset email');
    }
  }
}

module.exports = EmailService;
