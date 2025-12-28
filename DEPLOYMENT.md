# Deployment Guide

## Production Deployment Checklist

### Pre-Deployment

- [ ] Generate secure JWT secret: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- [ ] Create `.env` file with production values
- [ ] Set `ENVIRONMENT=production`
- [ ] Configure HTTPS/SSL certificates
- [ ] Set up production database (or keep SQLite with proper backups)
- [ ] Review and configure CORS settings for your domain

### Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite://./blog.db
JWT_SECRET=<generate-secure-random-key>
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
BCRYPT_ROUNDS=12
ENVIRONMENT=production
```

### Deployment Options

#### Option 1: Systemd Service (Linux)

1. Create systemd service file `/etc/systemd/system/blog-app.service`:

```ini
[Unit]
Description=Blog Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/blog_app
Environment="PATH=/var/www/blog_app/.venv/bin"
ExecStart=/var/www/blog_app/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

2. Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable blog-app
sudo systemctl start blog-app
sudo systemctl status blog-app
```

#### Option 2: Docker

1. Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

# Copy application
COPY . .

# Run migrations and start server
CMD alembic upgrade head && \
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

EXPOSE 8000
```

2. Build and run:

```bash
docker build -t blog-app .
docker run -d -p 8000:8000 --name blog-app \
  -e JWT_SECRET=<your-secret> \
  -v $(pwd)/blog.db:/app/blog.db \
  blog-app
```

#### Option 3: Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite://./blog.db
      - JWT_SECRET=${JWT_SECRET}
      - ENVIRONMENT=production
    volumes:
      - ./blog.db:/app/blog.db
      - ./static:/app/static
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

### Nginx Reverse Proxy

Create `/etc/nginx/sites-available/blog-app`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    # SSL configuration
    ssl_certificate /path/to/fullchain.pem;
    ssl_certificate_key /path/to/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Static files
    location /static {
        alias /var/www/blog_app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Proxy to FastAPI app
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/blog-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Database Backup

Create backup script `/usr/local/bin/backup-blog-db.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/blog-app"
DB_PATH="/var/www/blog_app/blog.db"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
cp $DB_PATH "$BACKUP_DIR/blog-$DATE.db"

# Keep only last 30 days of backups
find $BACKUP_DIR -name "blog-*.db" -mtime +30 -delete
```

Add to crontab:
```bash
0 2 * * * /usr/local/bin/backup-blog-db.sh
```

### Monitoring & Logging

1. **Application Logs**: Configure in `app/main.py`

```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/blog-app/app.log'),
        logging.StreamHandler()
    ]
)
```

2. **Log Rotation**: Create `/etc/logrotate.d/blog-app`

```
/var/log/blog-app/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload blog-app > /dev/null 2>&1 || true
    endscript
}
```

### Security Hardening

1. **Firewall Rules** (ufw):
```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

2. **Fail2Ban** (protect SSH):
```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

3. **Update System Regularly**:
```bash
sudo apt update && sudo apt upgrade -y
```

### Performance Tuning

1. **Uvicorn Workers**: Set workers = CPU cores
2. **SQLite Optimization**: WAL mode is already enabled
3. **Static File Caching**: Configured in Nginx
4. **Gzip Compression**: Already enabled in FastAPI

### Health Checks

Add health check endpoint in `app/main.py`:

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": await check_db_connection()
    }
```

Monitor with:
```bash
curl http://localhost:8000/health
```

### Rollback Procedure

If deployment fails:

1. Stop the application:
```bash
sudo systemctl stop blog-app
```

2. Restore previous version:
```bash
cd /var/www/blog_app
git checkout <previous-commit>
```

3. Restore database backup:
```bash
cp /var/backups/blog-app/blog-YYYYMMDD_HHMMSS.db ./blog.db
```

4. Rollback migrations:
```bash
alembic downgrade -1
```

5. Restart application:
```bash
sudo systemctl start blog-app
```

### Post-Deployment Verification

- [ ] Application starts without errors
- [ ] Homepage loads successfully
- [ ] User registration works
- [ ] Login works and JWT cookie is set
- [ ] Create post works
- [ ] Add comment works
- [ ] Static files load (CSS, JS)
- [ ] HTTPS redirects working
- [ ] Database backups running

### Maintenance

#### Daily
- Monitor error logs
- Check disk space
- Verify backups are running

#### Weekly
- Review application performance
- Update dependencies if security patches available
- Test backup restoration procedure

#### Monthly
- Security audit
- Performance optimization review
- Update SSL certificates (if needed)

## Support

For issues or questions, refer to:
- Application logs: `/var/log/blog-app/app.log`
- API documentation: `https://yourdomain.com/docs`
- Design specs: `specs/001-blog-app/`

---

**Deployment Status**: Ready for production deployment

