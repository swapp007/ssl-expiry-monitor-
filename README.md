# Auto SSL Certificate Expiry Monitor

Checks SSL expiry for configured domains and sends alert email when certificates are near expiration.

## Features
- Fetches SSL certificate expiry date
- Configurable alert threshold
- Email notifications
- Cron schedulable

## Tech Stack
- Python
- SMTP
- SSL socket
- YAML config

## Usage
1. Edit config.yaml
2. Install requirements
3. Run python ssl_check.py
4. Schedule via cron
