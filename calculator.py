"""
calculator.py - Performs all calculations
This is where we compute costs, carbon, and scores
"""

from data import PRICING, CARBON_FOOTPRINT, SECURITY_SCORES, AVAILABILITY

class ArchitectureCalculator:
    """
    This class calculates metrics for each architecture option.
    Think of it as a calculator specifically designed for cloud architectures.
    """
    
    def __init__(self, storage_gb, requests_millions, 
                 cost_weight, carbon_weight, security_weight):
        """
        Initialize with user inputs
        
        Parameters:
        - storage_gb: How much data to store (in gigabytes)
        - requests_millions: How many millions of requests per month
        - cost_weight: How important is cost? (0-10)
        - carbon_weight: How important is environment? (0-10)
        - security_weight: How important is security? (0-10)
        """
        self.storage_gb = storage_gb
        self.requests_millions = requests_millions
        
        # Normalize weights to sum to 1 (like percentages)
        total_weight = cost_weight + carbon_weight + security_weight
        self.cost_weight = cost_weight / total_weight
        self.carbon_weight = carbon_weight / total_weight
        self.security_weight = security_weight / total_weight
    
    def calculate_monthly_cost(self, architecture):
        """Calculate monthly cost in USD"""
        pricing = PRICING[architecture]
        
        monthly_cost = (
            pricing['base_cost'] +
            (pricing['cost_per_gb'] * self.storage_gb) +
            (pricing['cost_per_million_requests'] * self.requests_millions)
        )
        
        return round(monthly_cost, 2)
    
    def calculate_annual_cost(self, architecture):
        """Calculate annual cost (monthly * 12)"""
        return round(self.calculate_monthly_cost(architecture) * 12, 2)
    
    def calculate_carbon_footprint(self, architecture):
        """Calculate monthly carbon footprint in kg CO2"""
        carbon = CARBON_FOOTPRINT[architecture]
        
        monthly_carbon = (
            carbon['base_carbon'] +
            (carbon['carbon_per_gb'] * self.storage_gb) +
            (carbon['carbon_per_million_requests'] * self.requests_millions)
        )
        
        return round(monthly_carbon, 2)
    
    def calculate_annual_carbon(self, architecture):
        """Calculate annual carbon footprint"""
        return round(self.calculate_carbon_footprint(architecture) * 12, 2)
    
    def get_security_score(self, architecture):
        """Get security score (already calculated in our data)"""
        return SECURITY_SCORES[architecture]['total']
    
    def get_availability(self, architecture):
        """Get availability percentage"""
        return AVAILABILITY[architecture]
    
    def calculate_overall_score(self, architecture):
        """
        Calculate weighted overall score.
        This is the key decision metric!
        """
        
        # Get raw values
        cost = self.calculate_monthly_cost(architecture)
        carbon = self.calculate_carbon_footprint(architecture)
        security = self.get_security_score(architecture)
        
        # Normalize scores (inverse for cost and carbon - lower is better)
        # We use 1000 as max cost and 100 as max carbon for normalization
        cost_score = max(0, 100 - (cost / 1000) * 100)
        carbon_score = max(0, 100 - (carbon / 100) * 100)
        security_score = security  # Already 0-100
        
        # Calculate weighted score
        overall = (
            self.cost_weight * cost_score +
            self.carbon_weight * carbon_score +
            self.security_weight * security_score
        )
        
        return round(overall, 2)
    
    def get_recommendation(self):
        """
        Determine which architecture is best based on weighted scores
        """
        architectures = ['rds_multi_az', 'dynamodb', 'aurora_serverless']
        scores = {}
        
        for arch in architectures:
            scores[arch] = self.calculate_overall_score(arch)
        
        # Find the best option
        best_arch = max(scores, key=scores.get)
        
        return {
            'recommended': PRICING[best_arch]['name'],
            'architecture_key': best_arch,
            'score': scores[best_arch],
            'all_scores': scores,
            'reason': self._get_recommendation_reason(best_arch, scores)
        }
    
    def _get_recommendation_reason(self, best_arch, scores):
        """Generate human-readable recommendation reason"""
        if self.security_weight > 0.5:
            return "Based on your high security priority, this option provides the best protection while managing costs."
        elif self.carbon_weight > 0.5:
            return "This option minimizes environmental impact while maintaining security standards."
        elif self.cost_weight > 0.5:
            return "This option provides the best value for money with acceptable security and sustainability."
        else:
            return "This option provides the best balanced solution across all your priorities."
    
    def get_all_metrics(self):
        """
        Get all metrics for all architectures.
        This will be used to create our comparison tables.
        """
        architectures = ['rds_multi_az', 'dynamodb', 'aurora_serverless']
        metrics = {}
        
        for arch in architectures:
            metrics[arch] = {
                'name': PRICING[arch]['name'],
                'description': PRICING[arch]['description'],
                'monthly_cost': self.calculate_monthly_cost(arch),
                'annual_cost': self.calculate_annual_cost(arch),
                'monthly_carbon': self.calculate_carbon_footprint(arch),
                'annual_carbon': self.calculate_annual_carbon(arch),
                'security_score': self.get_security_score(arch),
                'availability': self.get_availability(arch),
                'overall_score': self.calculate_overall_score(arch)
            }
        
        return metrics