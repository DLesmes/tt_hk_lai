# ETA Agent System - Deployment Guide

## 🚀 Production Deployment

This guide covers deploying the ETA Agent System to production environments with proper security, monitoring, and scalability considerations.

## 📋 Prerequisites

### System Requirements

- **OS**: Linux (Ubuntu 20.04+ recommended)
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Memory**: 2GB+ RAM
- **Storage**: 10GB+ free space
- **Network**: Stable internet connection

### Required Accounts & Keys

- **OpenAI API Key**: For AI functionality
- **OpenRouteService API Key**: For traffic data (optional)
- **Domain Name**: For production access (recommended)
- **SSL Certificate**: For HTTPS (recommended)

## 🔧 Environment Setup

### 1. Production Environment Variables

Create a production `.env` file:

```bash
# Core Configuration
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=WARNING
SECRET_KEY=your-super-secret-production-key-here

# API Keys
OPENAI_API_KEY=sk-your-openai-api-key
OPENROUTESERVICE_API_KEY=your-openrouteservice-key
WEATHER_API_KEY=your-weather-api-key

# Database
DATABASE_URL=sqlite:///./data/lesmes.db

# Security
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CORS_ORIGINS=https://your-domain.com,https://www.your-domain.com

# Performance
WORKERS=4
MAX_CONNECTIONS=100
```

### 2. Security Configuration

#### Generate Secure Secret Key

```bash
# Generate a secure secret key
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Set File Permissions

```bash
# Set proper permissions
chmod 600 .env
chmod 755 backend/data
chmod 755 frontend
```

## 🐳 Docker Production Setup

### 1. Build Production Images

```bash
# Build optimized production images
docker-compose -f docker-compose.prod.yml build --no-cache

# Verify images
docker images | grep lesmes
```

### 2. Start Production Services

```bash
# Start services in detached mode
docker-compose -f docker-compose.prod.yml up -d

# Check service status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### 3. Health Checks

```bash
# Check backend health
curl http://localhost:8000/health

# Check frontend health
curl http://localhost:8501/_stcore/health

# Run comprehensive tests
python3 run_tests.py
```

## 🌐 Reverse Proxy Setup (Nginx)

### 1. Create Nginx Configuration

Create `nginx/nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:8501;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=chat:10m rate=5r/s;

    server {
        listen 80;
        server_name your-domain.com www.your-domain.com;
        
        # Redirect HTTP to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com www.your-domain.com;

        # SSL Configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
        ssl_prefer_server_ciphers off;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_cache_bypass $http_upgrade;
        }

        # Backend API
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Chat endpoint with stricter rate limiting
        location /chat {
            limit_req zone=chat burst=10 nodelay;
            proxy_pass http://backend/chat;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health checks
        location /health {
            proxy_pass http://backend/health;
            access_log off;
        }
    }
}
```

### 2. SSL Certificate Setup

```bash
# Create SSL directory
mkdir -p nginx/ssl

# For Let's Encrypt (recommended)
sudo certbot certonly --standalone -d your-domain.com -d www.your-domain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/key.pem

# Set permissions
chmod 644 nginx/ssl/cert.pem
chmod 600 nginx/ssl/key.pem
```

### 3. Start with Nginx

```bash
# Start with Nginx reverse proxy
docker-compose -f docker-compose.prod.yml --profile production up -d
```

## 📊 Monitoring & Logging

### 1. Log Management

```bash
# View real-time logs
docker-compose -f docker-compose.prod.yml logs -f

# View specific service logs
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend

# Export logs
docker-compose -f docker-compose.prod.yml logs > production_logs.txt
```

### 2. Health Monitoring

Create a monitoring script `monitor.sh`:

```bash
#!/bin/bash

# Health check endpoints
BACKEND_URL="https://your-domain.com/health"
FRONTEND_URL="https://your-domain.com/_stcore/health"

# Check backend
if curl -f -s $BACKEND_URL > /dev/null; then
    echo "$(date): ✅ Backend healthy"
else
    echo "$(date): ❌ Backend unhealthy"
    # Send alert (email, Slack, etc.)
fi

# Check frontend
if curl -f -s $FRONTEND_URL > /dev/null; then
    echo "$(date): ✅ Frontend healthy"
else
    echo "$(date): ❌ Frontend unhealthy"
    # Send alert
fi
```

### 3. Performance Monitoring

```bash
# Monitor resource usage
docker stats

# Check disk usage
df -h

# Monitor API response times
curl -w "@curl-format.txt" -o /dev/null -s "https://your-domain.com/health"
```

## 🔄 Backup & Recovery

### 1. Database Backup

```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups/lesmes"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
docker-compose -f docker-compose.prod.yml exec backend cp /app/data/lesmes.db /app/data/lesmes_$DATE.db
docker cp lesmes-backend-1:/app/data/lesmes_$DATE.db $BACKUP_DIR/

# Backup configuration
cp .env $BACKUP_DIR/.env_$DATE

echo "Backup completed: $BACKUP_DIR/lesmes_$DATE.db"
EOF

chmod +x backup.sh
```

### 2. Automated Backups

```bash
# Add to crontab for daily backups
crontab -e

# Add this line for daily backups at 2 AM
0 2 * * * /path/to/lesmes/backup.sh
```

## 🔒 Security Hardening

### 1. Firewall Configuration

```bash
# Configure UFW firewall
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### 2. Container Security

```bash
# Run containers as non-root user
# Add to docker-compose.prod.yml
services:
  backend:
    user: "1000:1000"
  frontend:
    user: "1000:1000"
```

### 3. API Key Rotation

```bash
# Rotate API keys regularly
# Update .env file with new keys
# Restart services
docker-compose -f docker-compose.prod.yml restart
```

## 📈 Scaling Considerations

### 1. Horizontal Scaling

```bash
# Scale backend services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3

# Use load balancer for multiple instances
```

### 2. Database Scaling

For high-traffic scenarios, consider:
- PostgreSQL instead of SQLite
- Database clustering
- Read replicas

### 3. Caching

```bash
# Add Redis for caching
# Update docker-compose.prod.yml
services:
  redis:
    image: redis:alpine
    networks:
      - lesmes-network
```

## 🚨 Troubleshooting

### Common Production Issues

1. **High Memory Usage**
   ```bash
   # Check memory usage
   docker stats
   
   # Restart services
   docker-compose -f docker-compose.prod.yml restart
   ```

2. **API Rate Limiting**
   ```bash
   # Check OpenAI rate limits
   # Monitor API usage
   # Implement caching
   ```

3. **SSL Certificate Expiry**
   ```bash
   # Renew Let's Encrypt certificate
   sudo certbot renew
   
   # Restart Nginx
   docker-compose -f docker-compose.prod.yml restart nginx
   ```

### Emergency Procedures

```bash
# Emergency restart
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d

# Rollback to previous version
git checkout <previous-tag>
docker-compose -f docker-compose.prod.yml up -d --build
```

## 📞 Support & Maintenance

### Regular Maintenance Tasks

1. **Weekly**
   - Check logs for errors
   - Monitor resource usage
   - Run health checks

2. **Monthly**
   - Update dependencies
   - Review security patches
   - Performance optimization

3. **Quarterly**
   - Full system backup
   - Security audit
   - Capacity planning

### Contact Information

- **System Administrator**: [Your Contact]
- **Emergency Contact**: [Emergency Contact]
- **Documentation**: [Documentation URL]

---

**Production Deployment Guide v1.0** - ETA Agent System 