# HumanAIOS API Documentation

Auto-generated API documentation from OpenAPI/Swagger specifications.

## Quick Start

```bash
npm install
npm run build
npm run serve
```

Then open http://localhost:8080

## Features

- ✅ OpenAPI 3.0 specification
- ✅ Interactive Swagger UI explorer
- ✅ RedOC static documentation
- ✅ Automatic changelog generation
- ✅ Try-it-out request testing
- ✅ Specification validation
- ✅ CI/CD integration ready

## Project Structure

```
api-docs/
├── openapi/
│   └── api-spec.yml          # OpenAPI 3.0 specification
├── templates/
│   ├── swagger-ui.html       # Interactive explorer
│   ├── CHANGELOG.md.hbs      # Changelog template
│   └── README.md.hbs         # README template
├── scripts/
│   └── changelog-generator.js # Auto-generate changelog
├── dist/                      # Generated documentation (build output)
├── docs-config.json          # Documentation configuration
└── package.json              # Dependencies
```

## Commands

- `npm run build` - Generate all documentation formats
- `npm run validate` - Validate OpenAPI specification
- `npm run generate` - Generate HTML documentation
- `npm run watch` - Auto-rebuild on spec changes
- `npm run serve` - Serve docs locally
- `npm run changelog:generate` - Generate changelog from spec
- `npm run test:spec` - Test spec against JSON Schema
- `npm run lint:spec` - Lint OpenAPI specification

## Adding New Endpoints

1. Add endpoint definition to `openapi/api-spec.yml`
2. Run `npm run validate` to check for errors
3. Run `npm run build` to regenerate docs
4. Commit changes

## CI/CD Integration

```yaml
- name: Generate API Docs
  run: |
    cd api-docs
    npm ci
    npm run build
    npm run changelog:generate

- name: Deploy Docs
  run: |
    # Deploy dist/ to docs.humanaios.com
```

## Versioning

The API documentation supports multiple versions through:
- URL path versioning: `/api-docs/v1/`, `/api-docs/v2/`
- Version-specific OpenAPI specs: `openapi/api-spec-v1.yml`, etc.
- Automatic changelog per version

## Security

- API keys shown as Bearer tokens in docs
- Try-it-out requests use actual endpoints
- Authentication tested with JWT tokens
- Request/response examples don't include secrets

## Support

For API documentation issues, contact: api-docs@humanaios.com
