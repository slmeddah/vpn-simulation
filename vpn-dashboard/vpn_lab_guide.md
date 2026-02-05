# OpenVPN Deployment and PKI Lab Guide

## Laboratory Objective
The purpose of this lab is to deploy a secure OpenVPN server using certificate-based authentication via PKI. This lab demonstrates:
- Secure server-client communication
- Certificate generation and management
- Tunnel interface creation
- Network traffic verification

## Laboratory Architecture
We use **3 virtual machines**:
1. **OpenVPN Server** – central authority for authentication and tunnel.
2. **OpenVPN Client** – connects securely to the server using certificates.
3. **Observer Machine** – monitors VPN traffic and verifies encrypted communication.

## Environment Requirements
- Linux-based system (Ubuntu recommended)
- Administrative privileges
- Internet access

## Installing OpenVPN and Easy-RSA
**Purpose:** OpenVPN provides the VPN service; Easy-RSA handles PKI certificates.

**Command:**
```bash
sudo apt update
sudo apt install openvpn easy-rsa


Explanation: After installation, OpenVPN binaries and certificate management tools are available.

PKI Initialization

Purpose: PKI allows secure authentication between server and client.

Commands:

make-cadir ~/openvpn-ca
cd ~/openvpn-ca


Directory Structure:

openvpn-ca/
├── pki/
│   ├── private/
│   ├── issued/
│   └── reqs/
├── vars
└── openssl-easyrsa.cnf


Explanation:

private/ stores private keys

issued/ stores signed certificates

reqs/ stores certificate requests

vars defines certificate parameters

Creating Certificate Authority

Purpose: The CA signs all server and client certificates to guarantee trust.

Commands:
./easyrsa init-pki
./easyrsa build-ca

Generated Files:

ca.crt – public certificate

ca.key – private key

Server Certificate Generation

Purpose: Allows clients to verify server identity.

Commands:
./easyrsa gen-req server nopass
./easyrsa sign-req server server

Generated Files:

server.crt

server.key

Client Certificate Generation

Purpose: Each client needs its own certificate.

Commands:
./easyrsa gen-req client nopass
./easyrsa sign-req client client

OpenVPN Server Configuration

Server Configuration File:

port 1194
proto udp
dev tun
ca ca.crt
cert server.crt
key server.key
server 10.8.0.0 255.255.255.0
keepalive 10 120
persist-key
persist-tun


Explanation:

port 1194 – VPN port

proto udp – faster UDP transport

dev tun – routed tunnel

server – VPN subnet

persist-* – maintain keys and tunnel if interrupted

Starting OpenVPN Server

Command:
sudo systemctl start openvpn-server@server
Check tunnel interface:
Network Interfaces
├── eth0
├── lo
└── tun0 (VPN server interface)

Client Configuration

Client Configuration File:
client
dev tun
proto udp
remote SERVER_IP 1194
ca ca.crt
cert client.crt
key client.key

Starting VPN Client:
sudo openvpn --config client.ovpn

Expected Result:

TLS handshake success

Tunnel interface created (tun1)

VPN IP assigned

Observer Machine Role

Monitors VPN traffic between server and client. Verifies:

Encrypted packet flow

Source and destination addresses

Protocol types

Connectivity Verification

Ping Test:
ping 10.8.0.1

Expected Result:

ICMP replies received

Stable latency

No packet loss

Tunnel Interface Verification

Each VPN connection generates a virtual interface:
Virtual Interfaces
├── tun0 (Server)
├── tun1 (Client)

Conclusion

This lab validates:

PKI-based authentication

VPN tunnel creation

Encrypted communication

Proper network isolation
