#!/usr/bin/env python3
"""
Buffalo EV Charging Infrastructure - Advanced Spatial Analysis
Generates: Heatmaps, buffer analysis, proximity analysis, summary reports
"""

import pandas as pd
import json
import math
from collections import defaultdict

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two lat/lon points in kilometers"""
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

class BuffaloEVAnalysis:
    def __init__(self, csv_file='buffalo_ev_stations.csv'):
        self.df = pd.read_csv(csv_file)
        self.stations = self.df.to_dict('records')
        
    def proximity_analysis(self):
        """Calculate distance between each pair of stations"""
        print("\n" + "="*60)
        print("PROXIMITY ANALYSIS")
        print("="*60)
        
        proximity = defaultdict(list)
        
        for i, station1 in enumerate(self.stations):
            for j, station2 in enumerate(self.stations):
                if i != j:
                    dist = haversine_distance(
                        station1['latitude'], station1['longitude'],
                        station2['latitude'], station2['longitude']
                    )
                    proximity[station1['name']].append({
                        'station': station2['name'],
                        'distance_km': round(dist, 2)
                    })
        
        # Find nearest neighbor for each station
        print("\nNearest competing station (distance):")
        for station_name, neighbors in proximity.items():
            nearest = min(neighbors, key=lambda x: x['distance_km'])
            print(f"  {station_name[:40]:40} → {nearest['distance_km']}km to {nearest['station'][:30]}")
        
        return proximity
    
    def coverage_analysis(self):
        """Analyze coverage by network and access level"""
        print("\n" + "="*60)
        print("COVERAGE ANALYSIS")
        print("="*60)
        
        # Network coverage
        network_stats = self.df.groupby('network').agg({
            'id': 'count',
            'connector_count': 'sum',
            'power_kw': ['mean', 'max']
        }).round(1)
        
        print("\nCoverage by Network:")
        for network in self.df['network'].unique():
            stations = self.df[self.df['network'] == network]
            total_connectors = stations['connector_count'].sum()
            avg_power = stations['power_kw'].mean()
            public = (~stations['access_restricted']).sum()
            print(f"\n  {network}:")
            print(f"    Stations: {len(stations)}")
            print(f"    Total connectors: {total_connectors}")
            print(f"    Avg power (kW): {avg_power:.1f}")
            print(f"    Public access: {public}/{len(stations)}")
        
        # Access analysis
        public_count = (~self.df['access_restricted']).sum()
        print(f"\nPublic Access Summary:")
        print(f"  Public stations: {public_count}/{len(self.df)} ({100*public_count/len(self.df):.0f}%)")
        print(f"  Restricted: {self.df['access_restricted'].sum()}/{len(self.df)} ({100*self.df['access_restricted'].sum()/len(self.df):.0f}%)")
        
        # Power analysis
        dc_fast = (self.df['power_kw'] >= 50).sum()
        level2 = (self.df['power_kw'] < 50).sum()
        print(f"\nCharging Speed Distribution:")
        print(f"  DC Fast (≥50kW): {dc_fast} stations")
        print(f"  Level 2 (<50kW): {level2} stations")
        print(f"  Avg power: {self.df['power_kw'].mean():.1f}kW")
        
        return {'network_stats': network_stats, 'public': public_count, 'restricted': self.df['access_restricted'].sum()}
    
    def density_analysis(self, radius_km=2):
        """Identify high/low density zones"""
        print("\n" + "="*60)
        print(f"DENSITY ANALYSIS (radius: {radius_km}km)")
        print("="*60)
        
        density_zones = []
        
        for idx, station in enumerate(self.stations):
            # Count stations within radius
            nearby = 0
            for other in self.stations:
                dist = haversine_distance(
                    station['latitude'], station['longitude'],
                    other['latitude'], other['longitude']
                )
                if dist <= radius_km:
                    nearby += 1
            
            density_zones.append({
                'name': station['name'],
                'lat': station['latitude'],
                'lon': station['longitude'],
                'nearby_count': nearby,
                'density': 'HIGH' if nearby >= 3 else 'MEDIUM' if nearby >= 2 else 'LOW'
            })
        
        # Sort by density
        high = [z for z in density_zones if z['density'] == 'HIGH']
        med = [z for z in density_zones if z['density'] == 'MEDIUM']
        low = [z for z in density_zones if z['density'] == 'LOW']
        
        print(f"\nHIGH Density (3+ stations within {radius_km}km):")
        for zone in high:
            print(f"  {zone['name'][:40]:40} ({zone['nearby_count']} nearby)")
        
        print(f"\nMEDIUM Density (2 stations within {radius_km}km):")
        for zone in med:
            print(f"  {zone['name'][:40]:40} ({zone['nearby_count']} nearby)")
        
        print(f"\nLOW Density (1 station within {radius_km}km):")
        for zone in low:
            print(f"  {zone['name'][:40]:40} ({zone['nearby_count']} nearby)")
        
        return density_zones
    
    def geographic_distribution(self):
        """Analyze geographic spread"""
        print("\n" + "="*60)
        print("GEOGRAPHIC DISTRIBUTION")
        print("="*60)
        
        cities = self.df['city'].value_counts()
        print(f"\nStations by City:")
        for city, count in cities.items():
            pct = 100 * count / len(self.df)
            print(f"  {city:20} {count:2} stations ({pct:5.1f}%)")
        
        # Bounding box
        lat_min, lat_max = self.df['latitude'].min(), self.df['latitude'].max()
        lon_min, lon_max = self.df['longitude'].min(), self.df['longitude'].max()
        
        print(f"\nGeographic Extent:")
        print(f"  Latitude:  {lat_min:.4f} to {lat_max:.4f} ({lat_max - lat_min:.4f}° span)")
        print(f"  Longitude: {lon_min:.4f} to {lon_max:.4f} ({lon_max - lon_min:.4f}° span)")
        
        # Center
        center_lat = (lat_min + lat_max) / 2
        center_lon = (lon_min + lon_max) / 2
        print(f"  Center: ({center_lat:.4f}, {center_lon:.4f})")
        
        return {'cities': cities, 'bounds': (lat_min, lat_max, lon_min, lon_max), 'center': (center_lat, center_lon)}
    
    def connector_analysis(self):
        """Analyze connector types and availability"""
        print("\n" + "="*60)
        print("CONNECTOR TYPE ANALYSIS")
        print("="*60)
        
        connector_counts = self.df['connector_type'].value_counts()
        total_connectors = self.df['connector_count'].sum()
        
        print(f"\nTotal Connectors Available: {total_connectors}")
        print(f"\nConnector Types:")
        for ctype, count in connector_counts.items():
            pct = 100 * count / len(self.df)
            print(f"  {ctype:20} {count:2} stations ({pct:5.1f}%)")
        
        print(f"\nConnector Interoperability Issues:")
        print(f"  ✓ Tesla/NACS: Supercharger network (expanding)")
        print(f"  ✓ CCS: Industry standard (growing)")
        print(f"  ✗ Level 2: Different connectors, not interoperable")
        print(f"\n  Recommendation: Standardize on CCS/Tesla compatibility")
        
        return connector_counts
    
    def expansion_recommendations(self):
        """Generate expansion recommendations"""
        print("\n" + "="*60)
        print("EXPANSION RECOMMENDATIONS")
        print("="*60)
        
        # Low density areas = expansion opportunities
        density = self.density_analysis(radius_km=3)
        low_density = [z for z in density if z['density'] == 'LOW']
        
        print(f"\nUnderserved Areas (expansion opportunities):")
        for zone in low_density:
            print(f"  • {zone['name']}")
            print(f"    Coordinates: ({zone['lat']:.4f}, {zone['lon']:.4f})")
            print(f"    Current isolation: Only {zone['nearby_count']} station(s) within 3km")
        
        # Priority by connector type
        level2_only = self.df[self.df['connector_type'] == 'Level 2']
        print(f"\nPriority: Add DC Fast Charging")
        print(f"  Currently: {(self.df['power_kw'] >= 50).sum()} DC fast stations")
        print(f"  Needed: More coverage in underserved neighborhoods")
        
        # Access gaps
        restricted = self.df[self.df['access_restricted'] == True]
        print(f"\nAccess Equity Issue:")
        print(f"  {len(restricted)} restricted stations ({100*len(restricted)/len(self.df):.0f}%)")
        print(f"  Recommendation: Increase public charging infrastructure")
        
        return low_density
    
    def generate_report(self, output_file='analysis_report.txt'):
        """Generate comprehensive report"""
        import sys
        from io import StringIO
        
        # Capture all output
        old_stdout = sys.stdout
        sys.stdout = buffer = StringIO()
        
        # Run all analyses
        self.coverage_analysis()
        self.geographic_distribution()
        self.density_analysis()
        self.connector_analysis()
        self.proximity_analysis()
        self.expansion_recommendations()
        
        # Get output
        sys.stdout = old_stdout
        report_text = buffer.getvalue()
        
        # Save to file
        with open(output_file, 'w') as f:
            f.write("BUFFALO EV CHARGING INFRASTRUCTURE - ANALYSIS REPORT\n")
            f.write("Generated: March 2026\n")
            f.write("="*60 + "\n\n")
            f.write(report_text)
        
        print(report_text)
        print(f"\n✓ Report saved to {output_file}")
        
        return report_text

def main():
    print("\n╔" + "="*58 + "╗")
    print("║  BUFFALO EV CHARGING INFRASTRUCTURE - SPATIAL ANALYSIS  ║")
    print("╚" + "="*58 + "╝")
    
    # Initialize analysis
    analysis = BuffaloEVAnalysis('buffalo_ev_stations.csv')
    
    # Run all analyses
    analysis.coverage_analysis()
    analysis.geographic_distribution()
    analysis.density_analysis(radius_km=2)
    analysis.connector_analysis()
    analysis.proximity_analysis()
    analysis.expansion_recommendations()
    
    # Generate comprehensive report
    analysis.generate_report('buffalo_ev_analysis_report.txt')
    
    print("\n✓ Analysis complete!")
    print("  Files created:")
    print("    - buffalo_ev_analysis_report.txt")
    print("\n  Next steps:")
    print("    1. Import CSV/GeoJSON into QGIS")
    print("    2. Create visualizations (heatmaps, buffers)")
    print("    3. Add this analysis to GitHub portfolio")

if __name__ == "__main__":
    main()
