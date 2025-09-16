# Green Tech Cloud Architecture Decision Tool

> Interactive dashboard helping green technology companies optimize cloud architecture decisions across cost, sustainability, and security.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://green-tech-cloud-architecture-decision-tool.streamlit.app/)

## Overview

A data-driven decision support tool that addresses the unique challenge facing green tech companies: balancing robust cloud infrastructure needs with environmental sustainability goals and cost efficiency.

**Problem**: Traditional cloud architecture decisions optimize for single dimensions, leading to suboptimal outcomes for mission-driven companies.

**Solution**: Multi-criteria analysis across three AWS architecture patterns with weighted recommendations based on organizational priorities.

## Features

 **Intelligent Recommendations**
- Multi-criteria decision analysis algorithm
- Customizable priority weighting (cost/carbon/security)
- Clear rationale for each recommendation

 **Comprehensive Analysis**
- Real-time cost calculations with 5-year projections
- Carbon footprint assessment with environmental equivalents
- Security scoring based on NIST, ISO 27001, SOC 2 frameworks

 **Interactive Visualizations**
- Multi-dimensional radar charts
- Comparative cost analysis
- Executive-friendly dashboards

## Architecture Options

### RDS Multi-AZ
**Best for**: Mission-critical healthcare applications
- 99.95% availability SLA
- HIPAA compliance ready
- Automatic failover capabilities

### DynamoDB Serverless
**Best for**: Variable IoT workloads with sustainability focus
- Scales to zero for cost efficiency
- Lowest carbon footprint option
- Pay-per-request pricing model

### Aurora Serverless
**Best for**: Balanced enterprise requirements
- Auto-scaling compute capacity
- MySQL compatibility
- Strong security with flexibility

## Technology Stack

- **Framework**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy
- **Deployment**: Streamlit Community Cloud

## Quick Start

1. **Try the live demo**: [Launch Dashboard](https://green-tech-cloud-architecture-decision-tool.streamlit.app/)

2. **Run locally**:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```

## Use Cases

- **Healthcare IoT**: Patient monitoring systems requiring HIPAA compliance
- **Smart Cities**: Sensor networks with sustainability mandates  
- **Renewable Energy**: Grid monitoring with environmental reporting requirements
- **Green Tech Startups**: Cost-conscious infrastructure decisions

## Skills Demonstrated

- **Cloud Architecture**: AWS service patterns and trade-off analysis
- **Security Frameworks**: NIST, ISO 27001, SOC 2 implementation
- **Data Visualization**: Interactive dashboard development
- **Business Analysis**: Multi-criteria decision support systems
- **Sustainable Technology**: Environmental impact assessment

## Project Impact

- **Cost Optimization**: Potential annual savings of $2,000-5,000 per workload
- **Risk Mitigation**: Framework-aligned security assessment
- **Sustainability**: 20-40% carbon reduction through optimized choices
- **Decision Transparency**: Clear documentation of architectural trade-offs

---

**Author**: Amarlin | **Focus**: Cloud Security & Solutions Architecture  
**Certifications**: CompTIA Security+ | **Currently**: AWS Solutions Architect Associate
