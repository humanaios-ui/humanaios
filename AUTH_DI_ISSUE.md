# Auth Dependency Injection Issue - Technical Documentation

**Created:** February 9, 2026, 11:35 AM  
**Status:** Blocked - needs systematic fix  
**Priority:** High (blocking API testing)  
**Estimated Fix Time:** 1-2 hours with fresh approach

## 🔴 PROBLEM: AuthService undefined in AuthController

**Error:** `Cannot read properties of undefined (reading 'register')`

## 🔧 RECOMMENDED FIX (Day 5)

**Approach 1: Express-Style Auth** (90% confidence, 45-60 min)
- Remove NestJS DI complexity
- Use passport-jwt directly
- Manual bcrypt in UsersService
- Simple middleware pattern

**Approach 2: Systematic Debug** (2-4 hours)
- Deep NestJS DI investigation
- Module dependency graph analysis
- Rebuild from official examples

**Approach 3: Standalone Service** (30-45 min)
- Manual service instantiation
- Bypass module DI timing
- Direct wiring in main.ts

## ⏰ TIME INVESTED: 2.5 hours across Day 3-4

## 🎯 CURRENT WORKAROUND: Auth bypassed for development

See full debugging history in git commit messages.

**Next session: Try Approach 1 first (highest confidence)**
