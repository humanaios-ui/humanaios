#!/bin/bash

# HumanAIOS - GitHub Setup Script
# Run this from the humainos/ directory

echo "🚀 Initializing HumanAIOS Git Repository..."
echo ""

# Initialize git
git init

# Add all files
echo "📦 Adding all files..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: HumanAIOS authentication system

✅ Complete authentication system with JWT
✅ User registration and login endpoints
✅ PostgreSQL + TimescaleDB database schema
✅ Redis integration
✅ Docker development environment
✅ Multi-tenant organization support
✅ Production-ready security

Ready for Day 2: Agent monitoring endpoints"

# Rename to main branch
echo "🌿 Setting main branch..."
git branch -M main

# Add GitHub remote
echo "🔗 Adding GitHub remote..."
git remote add origin git@github.com:humainos/humainos.git

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Success! Repository pushed to GitHub"
echo "🌐 View at: https://github.com/humainos/humainos"
echo ""
echo "Next steps:"
echo "1. Visit GitHub to verify the push"
echo "2. Set repository to private (Settings → Danger Zone)"
echo "3. Add collaborators if needed"
echo ""
