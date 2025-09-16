"""
data.py - Contains all our constants and fake data
Think of this as our "database" of information
"""

# AWS Pricing (simplified but realistic)
PRICING = {
    'rds_multi_az': {
        'name': 'RDS Multi-AZ',
        'base_cost': 450,  # Base monthly cost in USD
        'cost_per_gb': 0.115,  # Per GB storage cost
        'cost_per_million_requests': 0.20,
        'description': 'High availability database with automatic failover'
    },
    'dynamodb': {
        'name': 'DynamoDB On-Demand',
        'base_cost': 0,  # No base cost - pay per use
        'cost_per_gb': 0.25,
        'cost_per_million_requests': 1.25,
        'description': 'Serverless NoSQL database with automatic scaling'
    },
    'aurora_serverless': {
        'name': 'Aurora Serverless v2',
        'base_cost': 150,
        'cost_per_gb': 0.10,
        'cost_per_million_requests': 0.35,
        'description': 'MySQL-compatible serverless database'
    }
}

# Carbon Footprint (kg CO2 per month)
# Based on AWS region us-east-1 (Virginia)
CARBON_FOOTPRINT = {
    'rds_multi_az': {
        'base_carbon': 45,  # kg CO2/month for running instances
        'carbon_per_gb': 0.002,
        'carbon_per_million_requests': 0.008
    },
    'dynamodb': {
        'base_carbon': 5,  # Much lower - serverless
        'carbon_per_gb': 0.001,
        'carbon_per_million_requests': 0.003
    },
    'aurora_serverless': {
        'base_carbon': 20,
        'carbon_per_gb': 0.0015,
        'carbon_per_million_requests': 0.005
    }
}

# Security & Compliance Scores (out of 100)
SECURITY_SCORES = {
    'rds_multi_az': {
        'encryption': 100,
        'backup': 100,
        'access_control': 95,
        'monitoring': 90,
        'compliance': 95,  # HIPAA, SOC2, ISO ready
        'total': 96
    },
    'dynamodb': {
        'encryption': 95,
        'backup': 85,
        'access_control': 90,
        'monitoring': 85,
        'compliance': 80,  # Different consistency model
        'total': 87
    },
    'aurora_serverless': {
        'encryption': 100,
        'backup': 95,
        'access_control': 95,
        'monitoring': 95,
        'compliance': 90,
        'total': 95
    }
}

# Availability SLA (Service Level Agreement)
AVAILABILITY = {
    'rds_multi_az': 99.95,  # ~22 minutes downtime/month
    'dynamodb': 99.99,      # ~4 minutes downtime/month  
    'aurora_serverless': 99.95
}
