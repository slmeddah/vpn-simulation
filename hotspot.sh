#!/bin/bash
sudo ifconfig wlan0 192.168.20.18
sudo systemctl restart dnsmasq
sudo sysctl net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo hostapd /etc/hostapd/hostapd.conf
