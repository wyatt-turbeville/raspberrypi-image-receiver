#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "Please run with sudo: sudo ./install.sh"
  exit 1
fi

TARGET_USER="${SUDO_USER:-$USER}"
TARGET_HOME=$(eval echo ~$TARGET_USER)
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing service for user: $TARGET_USER"
echo "Installation directory: $INSTALL_DIR"

# Replace placeholders and write to systemd directory
sed -e "s|__USER__|$TARGET_USER|g" \
    -e "s|__INSTALL_DIR__|$INSTALL_DIR|g" \
    image-receiver.service.template > /etc/systemd/system/image-receiver.service

systemctl daemon-reload
systemctl enable image-receiver.service
systemctl restart image-receiver.service

echo "Service installed and started successfully!"
