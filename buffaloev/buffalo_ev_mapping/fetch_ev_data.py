#!/usr/bin/env python3
"""
Buffalo EV Charging Infrastructure Analysis
Fetches real charging station data from OpenChargeMap API
"""

import requests
import json
import pandas as pd
from datetime import datetime

# Buffalo, NY bounding box (approximate)
BUFFALO_LAT = 42.8864
BUFFALO_LON = -78.8784
RADIUS_KM = 15  # ~15km radius covers Buffalo metro

def fetch_ev_stations():
    """Fetch EV charging stations near Buffalo from OpenChargeMap"""
    
    # OpenChargeMap API endpoint (free, no key required)
    url = "https://api.openchargemap.io/v3/poi"
    
    params = {
        "latitude": BUFFALO_LAT,
        "longitude": BUFFALO_LON,
        "distance": RADIUS_KM,
        "distanceunit": "km",
        "maxresults": 1000,
        "compact": True,
        "verbose": False,
        "output": "json"
    }
    
    print(f"Fetching EV charging stations within {RADIUS_KM}km of Buffalo...")
    print(f"API URL: {url}")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print(f"✓ Retrieved {len(data)} charging locations")
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching data: {e}")
        return []

def parse_stations(raw_data):
    """Parse raw API response into structured dataframe"""
    
    stations = []
    
    for poi in raw_data:
        try:
            # Extract key fields
            station = {
                'id': poi.get('ID'),
                'name': poi.get('AddressInfo', {}).get('Title', 'Unknown'),
                'latitude': poi.get('AddressInfo', {}).get('Latitude'),
                'longitude': poi.get('AddressInfo', {}).get('Longitude'),
                'address': poi.get('AddressInfo', {}).get('AddressLine1', ''),
                'city': poi.get('AddressInfo', {}).get('Town', 'Buffalo'),
                'postcode': poi.get('AddressInfo', {}).get('Postcode', ''),
                'country': poi.get('AddressInfo', {}).get('Country', {}).get('Title', 'USA'),
                'connector_count': len(poi.get('Connections', [])) if poi.get('Connections') else 0,
                'power_kw': max([c.get('PowerKW', 0) for c in poi.get('Connections', [])]) if poi.get('Connections') else 0,
                'is_operational': poi.get('StatusType', {}).get('IsOperational', True) if poi.get('StatusType') else True,
                'access_restricted': poi.get('AccessRestrictionTypeID') is not None,
                'usage_cost': poi.get('UsageCost') if poi.get('UsageCost') else 'Unknown',
            }
            stations.append(station)
        except Exception as e:
            print(f"Warning: Could not parse station {poi.get('ID')}: {e}")
            continue
    
    return pd.DataFrame(stations)

def calculate_neighborhood_coverage(df):
    """Calculate basic coverage stats by area"""
    
    print("\n=== EV CHARGING COVERAGE SUMMARY ===")
    print(f"Total stations: {len(df)}")
    print(f"Operational: {df['is_operational'].sum()}")
    print(f"Restricted access: {df['access_restricted'].sum()}")
    print(f"Average connectors per station: {df['connector_count'].mean():.1f}")
    print(f"Average power (kW): {df['power_kw'].mean():.1f}")
    print(f"\nStations by city/town:")
    print(df['city'].value_counts().head(10))

def save_to_csv(df, filename='buffalo_ev_stations.csv'):
    """Save stations to CSV for QGIS import"""
    df.to_csv(filename, index=False)
    print(f"\n✓ Saved {len(df)} stations to {filename}")
    return filename

def save_to_geojson(df, filename='buffalo_ev_stations.geojson'):
    """Save as GeoJSON for web mapping and QGIS"""
    
    features = []
    
    for idx, row in df.iterrows():
        if pd.notna(row['latitude']) and pd.notna(row['longitude']):
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [row['longitude'], row['latitude']]
                },
                "properties": {
                    'id': row['id'],
                    'name': row['name'],
                    'address': row['address'],
                    'city': row['city'],
                    'postcode': row['postcode'],
                    'connectors': int(row['connector_count']),
                    'power_kw': float(row['power_kw']),
                    'operational': bool(row['is_operational']),
                    'restricted': bool(row['access_restricted']),
                    'cost': str(row['usage_cost'])
                }
            }
            features.append(feature)
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    with open(filename, 'w') as f:
        json.dump(geojson, f, indent=2)
    
    print(f"✓ Saved {len(features)} stations to {filename}")
    return filename

def main():
    print("=" * 50)
    print("Buffalo EV Charging Infrastructure Analysis")
    print("=" * 50)
    
    # Fetch data
    raw_data = fetch_ev_stations()
    
    if not raw_data:
        print("No data retrieved. Check your internet connection.")
        return
    
    # Parse into dataframe
    df = parse_stations(raw_data)
    
    if df.empty:
        print("No valid stations found.")
        return
    
    # Display summary stats
    calculate_neighborhood_coverage(df)
    
    # Save outputs
    csv_file = save_to_csv(df)
    geojson_file = save_to_geojson(df)
    
    print(f"\n✓ Project files ready:")
    print(f"  - {csv_file} (for QGIS)")
    print(f"  - {geojson_file} (for web maps + QGIS)")
    print(f"\nNext steps:")
    print(f"  1. Open QGIS")
    print(f"  2. Layer → Add Layer → Add Delimited Text Layer")
    print(f"  3. Select {csv_file}")
    print(f"  4. Set X=longitude, Y=latitude, CRS=EPSG:4326")
    print(f"  5. Add Buffalo boundary shapefile for context")
    print(f"  6. Create heatmaps, density analysis, proximity buffers")

if __name__ == "__main__":
    main()
