# Deployment Guide

## Prerequisites

### System Requirements
- **OS**: Ubuntu 20.04+ / CentOS 8+ / Windows Server 2019+
- **Python**: 3.9 or higher
- **Database**: MySQL 8.0+ / PostgreSQL 14+
- **RAM**: Minimum 2GB (4GB recommended)
- **Disk**: 10GB minimum
- **Network**: HTTPS/443, HTTP/80

### Software Requirements
```bash
- Python 3.9+
- pip 21+
- virtualenv
- MySQL/PostgreSQL
- Nginx (production)
- Gunicorn (production)
```

---

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/your-org/testing-platform.git
cd testing-platform
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
cp .env.example .env
nano .env  # Edit with your values
```

**Required Variables**:
```bash
SECRET_KEY=your-secret-key-here-min-32-characters
ENCRYPTION_KEY=your-encryption-key-32-bytes-base64
DATABASE_URL=mysql://user:pass@localhost/testing_platform
FLASK_ENV=production
```

**Generate Keys**:
```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Generate ENCRYPTION_KEY
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 5. Setup Database
```bash
# Create database
mysql -u root -p
CREATE DATABASE testing_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'testuser'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON testing_platform.* TO 'testuser'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Create Admin User
```bash
python scripts/create_admin.py
```

### 7. Test Application
```bash
# Development server
python run.py

# Access at http://localhost:5000
```

---

## Production Deployment

### Method 1: Gunicorn + Nginx (Recommended)

#### 1. Install Gunicorn
```bash
pip install gunicorn
```

#### 2. Create Gunicorn Config
```bash
# gunicorn_config.py
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
timeout = 120
accesslog = "/var/log/testing-platform/access.log"
errorlog = "/var/log/testing-platform/error.log"
loglevel = "info"
```

#### 3. Create Systemd Service
```bash
sudo nano /etc/systemd/system/testing-platform.service
```

```ini
[Unit]
Description=Testing Platform
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/testing-platform
Environment="PATH=/var/www/testing-platform/venv/bin"
ExecStart=/var/www/testing-platform/venv/bin/gunicorn -c gunicorn_config.py wsgi:app

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable testing-platform
sudo systemctl start testing-platform
sudo systemctl status testing-platform
```

#### 4. Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/testing-platform
```

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/ssl/certs/your_cert.crt;
    ssl_certificate_key /etc/ssl/private/your_key.key;
    ssl_protocols TLSv1.2 TLSv1.3;

    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/testing-platform/app/static;
        expires 30d;
    }

    location /storage {
        internal;
        alias /var/www/testing-platform/storage;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/testing-platform /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

### Method 2: Docker (Alternative)

#### 1. Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-c", "gunicorn_config.py", "wsgi:app"]
```

#### 2. Create docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - ENCRYPTION_KEY=${ENCRYPTION_KEY}
      - DATABASE_URL=${DATABASE_URL}
    volumes:
      - ./storage:/app/storage
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: testing_platform
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

#### 3. Deploy
```bash
docker-compose up -d
```

---

## SSL/TLS Certificate

### Using Let's Encrypt (Free)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

## Database Backup

### Automated Daily Backup
```bash
# Create backup script
sudo nano /usr/local/bin/backup-db.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/testing-platform"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

mysqldump -u testuser -p'password' testing_platform | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Keep only last 7 days
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete
```

```bash
# Make executable
sudo chmod +x /usr/local/bin/backup-db.sh

# Add to crontab
crontab -e
0 2 * * * /usr/local/bin/backup-db.sh
```

---

## Monitoring

### Application Logs
```bash
# View application logs
sudo journalctl -u testing-platform -f

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Health Check Endpoint
```bash
# Add to app
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

# Monitor
curl http://localhost:8000/health
```

---

## Performance Tuning

### Database Optimization
```sql
-- Add indexes
CREATE INDEX idx_test_created_by ON tests(created_by);
CREATE INDEX idx_question_test_id ON questions(test_id);
CREATE INDEX idx_result_student ON results(student_id);
CREATE INDEX idx_assignment_student ON assignments(student_id);
```

### Gunicorn Workers
```python
# Calculate workers
workers = (2 × CPU_CORES) + 1

# For 2 CPU cores
workers = 5
```

---

## Troubleshooting

### Common Issues

**1. Database Connection Error**
```bash
# Check MySQL is running
sudo systemctl status mysql

# Test connection
mysql -u testuser -p testing_platform
```

**2. Permission Denied**
```bash
# Fix file permissions
sudo chown -R www-data:www-data /var/www/testing-platform
sudo chmod -R 755 /var/www/testing-platform
```

**3. Gunicorn Won't Start**
```bash
# Check logs
sudo journalctl -u testing-platform -n 50

# Test manually
gunicorn -c gunicorn_config.py wsgi:app
```

**4. Static Files Not Loading**
```bash
# Check Nginx config
sudo nginx -t

# Verify static path
ls -la /var/www/testing-platform/app/static
```

---

## Security Hardening

### Firewall
```bash
# UFW
sudo ufw allow 22/tcp  # SSH
sudo ufw allow 80/tcp  # HTTP
sudo ufw allow 443/tcp # HTTPS
sudo ufw enable
```

### Fail2Ban
```bash
# Install
sudo apt install fail2ban

# Configure
sudo nano /etc/fail2ban/jail.local
```

```ini
[nginx-limit-req]
enabled = true
port = http,https
filter = nginx-limit-req
logpath = /var/log/nginx/error.log
```

---

## Maintenance

### Update Application
```bash
cd /var/www/testing-platform
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
sudo systemctl restart testing-platform
```

### Clear Old Logs
```bash
# Add to crontab
0 0 * * 0 find /var/log/testing-platform -name "*.log" -mtime +30 -delete
```

---

## Scaling

### Horizontal Scaling
1. Load balancer (HAProxy/Nginx)
2. Multiple application servers
3. Shared session storage (Redis)
4. Centralized file storage (NFS/S3)

### Vertical Scaling
1. Increase RAM
2. More CPU cores
3. SSD storage
4. Database optimization

---

## Deployment Checklist

### Pre-Deployment
- [ ] Environment variables configured
- [ ] Database created and migrated
- [ ] Admin user created
- [ ] SSL certificate obtained
- [ ] Backups configured
- [ ] Firewall rules set

### Post-Deployment
- [ ] Application accessible
- [ ] HTTPS working
- [ ] Login functional
- [ ] File uploads working
- [ ] Database writes successful
- [ ] Logs being written
- [ ] Backups running

---

**Deployment Version**: 1.0  
**Last Updated**: 2024  
**Support**: support@example.com
