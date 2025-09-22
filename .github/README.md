# CI/CD Pipeline Documentation

This directory contains GitHub Actions workflows for the Greek Derby RAG Chatbot project.

## 🚀 Workflows Overview

### 1. Continuous Integration (`ci.yml`)
**Triggers:** Push to `main`/`develop` branches, Pull Requests

**Jobs:**
- **Backend Tests**: Python linting, formatting, and unit tests
- **Frontend Tests**: TypeScript checking, linting, and build verification
- **Security Scan**: Vulnerability scanning with Trivy
- **Docker Build Test**: Multi-stage Docker image building

**Features:**
- Code quality checks (flake8, black, isort)
- Test coverage reporting
- Security vulnerability scanning
- Docker image validation

### 2. Continuous Deployment (`cd.yml`)
**Triggers:** Push to `main` branch, Manual dispatch

**Environments:**
- **Staging**: Automatic deployment on main branch pushes
- **Production**: Manual deployment with approval

**Features:**
- Multi-environment deployment
- Docker image building and pushing to GitHub Container Registry
- Automated cleanup of old images
- Smoke tests and health checks

### 3. Dependency Updates (`dependency-update.yml`)
**Triggers:** Weekly schedule (Mondays 2 AM UTC), Manual dispatch

**Features:**
- Automatic Python and Node.js dependency updates
- Pull request creation for dependency changes
- Security audit fixes

### 4. Security Scanning (`security.yml`)
**Triggers:** Push to `main`/`develop`, Pull Requests, Weekly schedule

**Features:**
- Trivy vulnerability scanning
- CodeQL analysis
- Safety checks for Python dependencies
- npm audit for Node.js dependencies

## 🔧 Configuration

### Required Secrets
Set these in your GitHub repository settings:

```bash
# Required for deployment
GITHUB_TOKEN  # Automatically provided by GitHub

# Optional for external services
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_GREEK_DERBY_INDEX_NAME=your_index_name
```

### Environment Variables
The workflows use these environment variables:

```yaml
env:
  PYTHON_VERSION: '3.11'
  NODE_VERSION: '18'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}
```

## 📊 Monitoring and Notifications

### Code Quality Metrics
- **Coverage**: Backend test coverage reported to Codecov
- **Security**: Vulnerability reports uploaded to GitHub Security tab
- **Performance**: Docker build times and cache efficiency

### Deployment Status
- **Staging**: Automatic deployment with health checks
- **Production**: Manual approval required
- **Rollback**: Automatic cleanup of old images

## 🛠️ Local Development

### Running Tests Locally

**Backend:**
```bash
cd backend
pip install -r requirements-dev.txt
pytest --cov=. --cov-report=html
```

**Frontend:**
```bash
cd front-end/react-chatbot
npm install
npm run test
npm run test:coverage
```

### Docker Development

**Build for development:**
```bash
# Backend
docker build --target development -t greek-derby-backend:dev ./backend

# Frontend
docker build --target development -t greek-derby-frontend:dev ./front-end/react-chatbot
```

**Build for production:**
```bash
# Backend
docker build --target production -t greek-derby-backend:prod ./backend

# Frontend
docker build --target production -t greek-derby-frontend:prod ./front-end/react-chatbot
```

## 🔍 Troubleshooting

### Common Issues

1. **Test Failures**
   - Check environment variables are set
   - Ensure all dependencies are installed
   - Verify API keys are valid

2. **Docker Build Failures**
   - Check Dockerfile syntax
   - Verify all required files are present
   - Ensure proper multi-stage build configuration

3. **Deployment Issues**
   - Verify GitHub Container Registry permissions
   - Check environment-specific configurations
   - Review deployment logs

### Debug Commands

```bash
# Check workflow status
gh run list --workflow=ci.yml

# View workflow logs
gh run view <run-id> --log

# Test Docker builds locally
docker-compose -f docker-compose.yml config
```

## 📈 Performance Optimization

### Docker Layer Caching
- Dependencies installed before copying source code
- Multi-stage builds for smaller production images
- GitHub Actions cache for faster builds

### Test Optimization
- Parallel test execution
- Selective test running based on changed files
- Coverage reporting only for relevant code

### Security Best Practices
- Non-root users in containers
- Minimal base images
- Regular dependency updates
- Vulnerability scanning

## 🚀 Future Enhancements

### Planned Features
- [ ] E2E testing with Playwright
- [ ] Performance testing with k6
- [ ] Database migration testing
- [ ] Blue-green deployments
- [ ] Canary releases
- [ ] Monitoring and alerting integration

### Integration Options
- **Kubernetes**: For container orchestration
- **Terraform**: For infrastructure as code
- **ArgoCD**: For GitOps deployment
- **Prometheus/Grafana**: For monitoring
- **Slack/Discord**: For notifications
