const { validationResult } = require('express-validator');
const User = require('../models/User');
const TokenService = require('../utils/tokenService');
const emailService = require('../utils/emailService');

class AuthController {
  static async register(req, res) {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          success: false,
          errors: errors.array(),
        });
      }

      const { email, password, firstName, lastName } = req.body;

      const existingUser = await User.findByEmail(email);
      if (existingUser) {
        return res.status(409).json({
          success: false,
          message: 'Email already registered',
        });
      }

      const user = await User.create({ email, password, firstName, lastName });
      const accessToken = TokenService.generateAccessToken(user.id, user.email, user.role);
      const refreshToken = await TokenService.generateRefreshToken(user.id);

      res.status(201).json({
        success: true,
        message: 'User registered successfully',
        data: {
          user: {
            id: user.id,
            email: user.email,
            firstName: user.first_name,
            lastName: user.last_name,
            role: user.role,
          },
          accessToken,
          refreshToken,
        },
      });
    } catch (error) {
      console.error('Registration error:', error);
      res.status(500).json({
        success: false,
        message: 'Registration failed',
        error: error.message,
      });
    }
  }

  static async login(req, res) {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          success: false,
          errors: errors.array(),
        });
      }

      const { email, password } = req.body;

      const isLocked = await User.isAccountLocked(email);
      if (isLocked) {
        return res.status(423).json({
          success: false,
          message: 'Account is temporarily locked due to multiple failed login attempts.',
        });
      }

      const user = await User.findByEmail(email);
      if (!user) {
        return res.status(401).json({
          success: false,
          message: 'Invalid email or password',
        });
      }

      const isValidPassword = await User.verifyPassword(password, user.password_hash);
      if (!isValidPassword) {
        await User.incrementLoginAttempts(email);
        return res.status(401).json({
          success: false,
          message: 'Invalid email or password',
        });
      }

      if (!user.is_active) {
        return res.status(403).json({
          success: false,
          message: 'Account is deactivated',
        });
      }

      await User.resetLoginAttempts(email);

      const accessToken = TokenService.generateAccessToken(user.id, user.email, user.role);
      const refreshToken = await TokenService.generateRefreshToken(user.id);

      res.json({
        success: true,
        message: 'Login successful',
        data: {
          user: {
            id: user.id,
            email: user.email,
            firstName: user.first_name,
            lastName: user.last_name,
            role: user.role,
            isVerified: user.is_verified,
          },
          accessToken,
          refreshToken,
        },
      });
    } catch (error) {
      console.error('Login error:', error);
      res.status(500).json({
        success: false,
        message: 'Login failed',
        error: error.message,
      });
    }
  }

  static async refreshToken(req, res) {
    try {
      const { refreshToken } = req.body;

      if (!refreshToken) {
        return res.status(400).json({
          success: false,
          message: 'Refresh token required',
        });
      }

      const payload = await TokenService.verifyRefreshToken(refreshToken);
      const user = await User.findById(payload.userId);
      
      if (!user || !user.is_active) {
        return res.status(401).json({
          success: false,
          message: 'Invalid user',
        });
      }

      const accessToken = TokenService.generateAccessToken(user.id, user.email, user.role);

      res.json({
        success: true,
        data: { accessToken },
      });
    } catch (error) {
      res.status(401).json({
        success: false,
        message: 'Invalid or expired refresh token',
      });
    }
  }

  static async logout(req, res) {
    try {
      const { refreshToken } = req.body;
      if (refreshToken) {
        await TokenService.revokeRefreshToken(refreshToken);
      }
      res.json({
        success: true,
        message: 'Logged out successfully',
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: 'Logout failed',
      });
    }
  }

  static async requestPasswordReset(req, res) {
    try {
      const { email } = req.body;
      const user = await User.findByEmail(email);
      
      if (!user) {
        return res.json({
          success: true,
          message: 'If that email exists, a password reset link has been sent',
        });
      }

      const resetToken = await TokenService.generatePasswordResetToken(user.id);
      await emailService.sendPasswordResetEmail(email, resetToken, user.first_name);

      res.json({
        success: true,
        message: 'If that email exists, a password reset link has been sent',
      });
    } catch (error) {
      console.error('Password reset request error:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to process password reset request',
      });
    }
  }

  static async resetPassword(req, res) {
    try {
      const { token, newPassword } = req.body;
      const resetToken = await TokenService.verifyPasswordResetToken(token);
      await User.updatePassword(resetToken.user_id, newPassword);
      await TokenService.markPasswordResetTokenAsUsed(token);
      await TokenService.revokeAllUserTokens(resetToken.user_id);

      res.json({
        success: true,
        message: 'Password reset successful',
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: 'Invalid or expired reset token',
      });
    }
  }

  static async getProfile(req, res) {
    try {
      const user = await User.findById(req.user.id);
      if (!user) {
        return res.status(404).json({
          success: false,
          message: 'User not found',
        });
      }

      res.json({
        success: true,
        data: {
          user: {
            id: user.id,
            email: user.email,
            firstName: user.first_name,
            lastName: user.last_name,
            role: user.role,
            isVerified: user.is_verified,
            createdAt: user.created_at,
          },
        },
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: 'Failed to get profile',
      });
    }
  }

  static async updateProfile(req, res) {
    try {
      const { firstName, lastName } = req.body;
      const updatedUser = await User.updateProfile(req.user.id, { firstName, lastName });

      res.json({
        success: true,
        message: 'Profile updated successfully',
        data: { user: updatedUser },
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: 'Failed to update profile',
      });
    }
  }
}

module.exports = AuthController;
