# Known Issues - HumanAIOS

## Day 3: Auth Module Dependency Injection Issue

**Status:** In Progress  
**Priority:** High  
**Discovered:** February 8, 2026  
**Target Fix:** Day 4

### Issue Description

AuthService is not being properly injected into AuthController. The NestJS dependency injection container is creating AuthService but with undefined dependencies (JwtService, initially UsersService).

### Symptoms

- API returns 500 errors on `/api/v1/auth/register` and `/api/v1/auth/login`
- Error: `Cannot read properties of undefined (reading 'register')`
- Debug logs show: `AuthController constructor - authService: false`
- AuthService constructor shows: `jwtService: false`

### Root Cause Analysis

Multiple issues discovered:
1. **Module initialization order** - AuthService created before JwtModule fully initialized
2. **Circular dependency** - Potential circular reference between AuthModule and UsersModule
3. **Duplicate imports** - UsersModule was imported in both AppModule and AuthModule (fixed)
4. **Constructor injection timing** - Services being constructed before their dependencies are ready

### Attempted Fixes

- ✅ Added DatabaseModule to AuthModule imports
- ✅ Removed duplicate UsersModule import from AppModule
- ✅ Added forwardRef() for UsersService injection
- ✅ Tried ModuleRef dynamic injection
- ❌ JwtService still not injecting properly

### Workaround for Day 3

For testing purposes, auth endpoints can be temporarily bypassed or we can create a minimal auth implementation that doesn't rely on complex DI.

### Proper Fix (Day 4)

**Option 1: Restructure Modules**
- Move auth logic to a simpler structure
- Use direct JwtModule.registerAsync() with proper factory
- Ensure all dependencies are available before AuthService instantiation

**Option 2: Custom Providers**
- Create custom provider factories for AuthService
- Manually handle dependency injection order
- Use @Inject() tokens with proper module configuration

**Option 3: Separate Auth into Microservice**
- Create standalone auth service
- Communicate via HTTP/gRPC
- Eliminates circular dependency issues

### Next Steps

1. Review NestJS docs on circular dependencies
2. Test with clean module structure
3. Consider using @nestjs/jwt in async mode
4. Add integration tests to catch DI issues early

### Impact

- **Blocking:** API testing, end-to-end workflows
- **Not Blocking:** Database setup, agent endpoints (once JWT is bypassed), MCP SDK development
- **Timeline:** Should be fixable in 1-2 hours with fresh eyes

### Debug Logs

Last successful initialization showed:
cd ~/Desktop/humanaios
cat > KNOWN_ISSUES.md << 'EOF'
# Known Issues - HumanAIOS

## Day 3: Auth Module Dependency Injection Issue

**Status:** In Progress  
**Priority:** High  
**Discovered:** February 8, 2026  
**Target Fix:** Day 4

### Issue Description

AuthService is not being properly injected into AuthController. The NestJS dependency injection container is creating AuthService but with undefined dependencies (JwtService, initially UsersService).

### Symptoms

- API returns 500 errors on `/api/v1/auth/register` and `/api/v1/auth/login`
- Error: `Cannot read properties of undefined (reading 'register')`
- Debug logs show: `AuthController constructor - authService: false`
- AuthService constructor shows: `jwtService: false`

### Root Cause Analysis

Multiple issues discovered:
1. **Module initialization order** - AuthService created before JwtModule fully initialized
2. **Circular dependency** - Potential circular reference between AuthModule and UsersModule
3. **Duplicate imports** - UsersModule was imported in both AppModule and AuthModule (fixed)
4. **Constructor injection timing** - Services being constructed before their dependencies are ready

### Attempted Fixes

- ✅ Added DatabaseModule to AuthModule imports
- ✅ Removed duplicate UsersModule import from AppModule
- ✅ Added forwardRef() for UsersService injection
- ✅ Tried ModuleRef dynamic injection
- ❌ JwtService still not injecting properly

### Workaround for Day 3

For testing purposes, auth endpoints can be temporarily bypassed or we can create a minimal auth implementation that doesn't rely on complex DI.

### Proper Fix (Day 4)

**Option 1: Restructure Modules**
- Move auth logic to a simpler structure
- Use direct JwtModule.registerAsync() with proper factory
- Ensure all dependencies are available before AuthService instantiation

**Option 2: Custom Providers**
- Create custom provider factories for AuthService
- Manually handle dependency injection order
- Use @Inject() tokens with proper module configuration

**Option 3: Separate Auth into Microservice**
- Create standalone auth service
- Communicate via HTTP/gRPC
- Eliminates circular dependency issues

### Next Steps

1. Review NestJS docs on circular dependencies
2. Test with clean module structure
3. Consider using @nestjs/jwt in async mode
4. Add integration tests to catch DI issues early

### Impact

- **Blocking:** API testing, end-to-end workflows
- **Not Blocking:** Database setup, agent endpoints (once JWT is bypassed), MCP SDK development
- **Timeline:** Should be fixable in 1-2 hours with fresh eyes

### Debug Logs

Last successful initialization showed:
```
AuthService constructor called!
  - usersService: true
  - jwtService: false  ← PROBLEM HERE
```

Auth module loads but AuthService doesn't get injected into AuthController:
```
AuthController constructor - authService: false
```

---

**Created:** February 8, 2026, 9:10 PM  
**Last Updated:** February 8, 2026, 9:10 PM
