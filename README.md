AI Smart EV Charging Orchestrator  
Secure AI-Controlled Renewable Infrastructure using WSO2 MCP Gateway Architecture

---------------------------------------------------------------------

Project Overview

This project demonstrates a production-style AI-controlled EV charging orchestration system built using:

- AI Decision Engine (FastAPI)
- WSO2 API Manager (OAuth2 + Gateway Control Plane)
- Renewable Energy Microservices (Solar, Battery, Grid)
- API Throttling & Governance
- Structured Logging & Observability

The system simulates a smart renewable EV charging infrastructure where an AI agent dynamically optimizes charging decisions while being securely governed by an API Gateway.

---------------------------------------------------------------------

Real-World Problem

EV charging stations face:

- Solar variability
- Battery instability
- Grid overload
- Lack of intelligent orchestration
- No secure AI governance layer

Most AI systems directly call backend services without proper governance.

This project solves that using a secure MCP-style Gateway architecture.

---------------------------------------------------------------------

System Architecture

Client
   ↓
AI Decision Engine (FastAPI)
   ↓ (OAuth2 Token)
WSO2 API Gateway (Control Plane)
   ↓ (Throttling + RBAC)
Energy Microservices
   - Solar Service
   - Battery Service
   - Grid Service

---------------------------------------------------------------------

Development Timeline

Day 1 – Architecture & Project Setup

- Designed system architecture
- Created project structure
- Defined problem statement
- Initialized GitHub repository
- Structured backend, gateway, docs, diagrams folders

Day 2 – Energy Microservices

Built three independent FastAPI services:

Solar Service  
- Simulates solar generation based on time of day

Battery Service  
- Simulates battery charge percentage

Grid Service  
- Simulates grid load percentage

Each runs independently as a microservice.

Day 3 – AI Charging Optimization Engine

Implemented AI decision logic.

Decision Rules:

- Grid > 85% → Pause Charging
- High Solar + High Battery → Fast Charging (22kW)
- Medium Solar → Normal Charging (11kW)
- Low Solar → Slow Charging (5kW)

Created endpoint:

/optimize-charging

This endpoint orchestrates renewable energy intelligently.

Day 4 – WSO2 Gateway Integration

Integrated WSO2 API Manager as a secure control plane between AI and microservices.

Implemented:

- Published SolarAPI, BatteryAPI, GridAPI
- OAuth2 token-based authentication
- Application subscription (EVApp)
- Gateway routing
- Backend connectivity debugging

System upgraded from:

AI → Services  
to  
AI → Gateway → Services

Day 5 – Production Hardening

Upgraded system to enterprise-level:

- Removed hardcoded access tokens
- Implemented secure environment variable handling
- Added API throttling (10 requests per minute)
- Enforced OAuth2 authentication
- Added structured logging
- Implemented gateway error handling

Now protected against:

- Token leakage
- Overuse attacks
- Unauthorized access

Day 6 – Enterprise Enhancements

Implemented:

Automatic OAuth2 Token Generation  
AI Agent dynamically requests tokens using Client Credentials flow.

Structured Logging  
Added timestamp-based logs for observability.

Health Check Endpoint  
/health  
Used for monitoring and production readiness.

Architecture Documentation  
Added system documentation inside docs folder.

---------------------------------------------------------------------

Security Model

- OAuth2 Client Credentials Flow
- Token-based authentication
- API-level throttling
- Gateway-enforced routing
- No secrets committed to GitHub

---------------------------------------------------------------------

Technologies Used

- Python (FastAPI)
- WSO2 API Manager 4.6.x
- OAuth2
- REST APIs
- Microservices Architecture
- Logging & Observability
- Git & GitHub

---------------------------------------------------------------------

Available Endpoints

AI Service  
GET /health  
GET /optimize-charging  

Microservices  
GET /solar-status  
GET /battery-status  
GET /grid-load  

---------------------------------------------------------------------

How To Run

1. Start Microservices

uvicorn main:app --reload --port 8001  
uvicorn main:app --reload --port 8002  
uvicorn main:app --reload --port 8003  

2. Start WSO2 API Manager

api-manager.bat  

3. Set Environment Variables

Git Bash:

export WSO2_CLIENT_ID="your_client_id"  
export WSO2_CLIENT_SECRET="your_client_secret"  

Windows CMD:

set WSO2_CLIENT_ID=your_client_id  
set WSO2_CLIENT_SECRET=your_client_secret  

4. Run AI Agent

uvicorn main:app --reload --port 8004  

---------------------------------------------------------------------

Future Improvements

- Real-time IoT sensor integration
- Grid prediction model using ML
- Token caching system
- Docker containerization
- Kubernetes deployment
- Centralized monitoring dashboard

---------------------------------------------------------------------

Author

Vinod Perera  
Computer Science & Electrical Engineering Undergraduate  
Focused on AI, Cybersecurity, Renewable Energy and API Integration
