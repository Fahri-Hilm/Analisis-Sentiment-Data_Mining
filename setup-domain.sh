#!/bin/bash

DOMAIN=$1

if [ -z "$DOMAIN" ]; then
    echo "Usage: ./setup-domain.sh your-domain.com"
    exit 1
fi

echo "🌐 Setting up domain: $DOMAIN"

# Update nginx config with domain
sed -i "s/your-domain.com/$DOMAIN/g" nginx.conf

# Restart nginx
sudo docker-compose restart nginx

echo "✅ Domain setup complete!"
echo "🌐 Access: http://$DOMAIN"

# Optional: Setup SSL with Let's Encrypt
read -p "Setup SSL certificate? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📜 Installing Certbot..."
    sudo apt update
    sudo apt install -y certbot python3-certbot-nginx
    
    echo "🔒 Getting SSL certificate..."
    sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN
    
    echo "✅ SSL setup complete!"
    echo "🔒 Access: https://$DOMAIN"
fi
