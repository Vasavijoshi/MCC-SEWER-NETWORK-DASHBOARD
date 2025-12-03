import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster, HeatMap, MeasureControl
import pydeck as pdk
import random
from geopy.distance import geodesic
import math

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="MCC Sewer Network Dashboard",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS FOR PROFESSIONAL STUNNING VISUALS
# ============================================================================
st.markdown("""
<style>
    /* Sleek shining black background */
    .stApp {
        background: linear-gradient(180deg, #0b0b0b 0%, #141414 50%, #0d0d0d 100%);
        color-scheme: dark;
    }

    /* Metric cards - glowing numerals */
    [data-testid="stMetricValue"] {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ffd166 0%, #ff7b7b 50%, #6ee7b7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 4px 18px rgba(255,255,255,0.03);
    }

    [data-testid="stMetricLabel"] {
        font-size: 1.05rem;
        font-weight: 600;
        color: #cfd8dc !important;
    }

    /* Dark sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1720 0%, #0c1116 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
        color: #e6eef6;
    }

    /* Headers - light on dark */
    h1 {
        color: #e6eef6;
        text-shadow: 0 2px 6px rgba(0,0,0,0.6);
        font-weight: 900;
    }

    h2 {
        color: #f1f5f9;
        font-weight: 800;
        padding-bottom: 0.4rem;
    }

    h3 {
        color: #d1d9df;
        font-weight: 700;
    }

    /* Dataframe styling - dark cards */
    .stDataFrame {
        background-color: #0f1720 !important;
        color: #e6eef6 !important;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.04);
        box-shadow: 0 6px 24px rgba(0,0,0,0.6);
    }

    /* Info boxes - subtle dark */
    .info-box {
        background: linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.02) 100%);
        border-left: 4px solid rgba(255,255,255,0.06);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }

    /* Filter section - card on dark */
    .filter-section {
        background: linear-gradient(135deg, rgba(255,255,255,0.02) 0%, rgba(255,255,255,0.01) 100%);
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.03);
        margin-bottom: 1.2rem;
    }

    /* Tabs and buttons - dark */
    .stTabs [data-baseweb="tab-list"] button {
        background-color: rgba(255,255,255,0.03);
        color: #e6eef6;
        border-radius: 8px;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(255,255,255,0.06) !important;
        color: #fff !important;
    }

    /* Small text adjustments */
    p, label {
        color: #d1d9df;
    }

    /* Hide Streamlit default footer and header for a cleaner look */
    header, footer { visibility: hidden; }
    
    /* Map container styling */
    /*
    .map-container {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        margin-bottom: 1rem;
        width: 100%;
        height: 600px;
    }
    
    /* Folium map specific styling */
    .folium-map {
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        width: 100% !important;
        height: 600px !important;
        
    }
    */
        /* Add border and styling directly to map iframes */
    iframe {
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
    }
    
    /* Style for Plotly charts (topology and heatmap) */
    .js-plotly-plot {
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
    }
    
    /* Style for PyDeck charts (3D map) */
    .deckgl-wrapper {
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
    }
    
    /* DeckGL map styling */
    .deckgl-wrapper {
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }
    
    /* Legend styling */
    .map-legend {
        background: rgba(15, 23, 32, 0.95) !important;
        border-radius: 8px;
        padding: 15px;
        border: 1px solid rgba(255,255,255,0.1);
        color: white;
    }
    
    /* Custom button styling */
    .stButton button {
        background: linear-gradient(135deg, #1a5490 0%, #2e7ab5 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #2e7ab5 0%, #4a90c7 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(42, 117, 181, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================
@st.cache_data
def load_manhole_data():
    """Load manhole master data with error handling and generate GPS coordinates"""
    try:
        df = pd.read_csv("data/AddedFields.csv")
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Normalize column names
        df['manhole_id'] = df['ID'].astype(str)
        df['material'] = df['Material'].fillna('Unknown')
        df['condition'] = df['Condition'].fillna('Unknown')
        df['cover_type'] = df['Cover type'].fillna('Unknown')
        df['no_of_connections'] = pd.to_numeric(df['no of connnections'], errors='coerce').fillna(0).astype(int)
        df['road'] = df.get('Road', 'Road Data')
        df['ward'] = df.get('Ward', 'Ward 1')
        df['zone'] = df.get('Zone', 'Zone 1')
        
        # Generate synthetic GPS coordinates for Mangalore region
        np.random.seed(42)
        n = len(df)
        
        # Generate realistic coordinates around Mangalore (12.9141° N, 74.8560° E)
        base_lat, base_lon = 12.9141, 74.8560
        
        # Create a grid-like pattern for better visualization
        grid_size = int(np.sqrt(n)) + 1
        lats = []
        lons = []
        
        for i in range(n):
            row = i // grid_size
            col = i % grid_size
            lat = base_lat + (row - grid_size/2) * 0.0015
            lon = base_lon + (col - grid_size/2) * 0.0015
            lats.append(lat)
            lons.append(lon)
        
        # Add some randomness
        lats = np.array(lats) + np.random.uniform(-0.0005, 0.0005, n)
        lons = np.array(lons) + np.random.uniform(-0.0005, 0.0005, n)
        
        df['latitude'] = lats
        df['longitude'] = lons
        df['elevation'] = np.random.uniform(5, 50, n)
        df['depth'] = np.random.uniform(1.5, 4.5, n)
        
        # Ensure all coordinates are valid
        df = df.dropna(subset=['latitude', 'longitude'])
        
        return df
    except FileNotFoundError:
        # Create comprehensive sample data
        return create_comprehensive_manhole_data()
    except Exception as e:
        st.error(f"❌ Error loading manhole data: {e}")
        return create_comprehensive_manhole_data()

def create_comprehensive_manhole_data():
    """Create comprehensive sample manhole data"""
    np.random.seed(42)
    n = 200
    
    # Create realistic data distribution
    materials = ['Concrete', 'PVC', 'Brick', 'Steel', 'Cast Iron']
    conditions = ['Good', 'Fair', 'Poor', 'Broken']
    cover_types = ['Circular', 'Rectangular', 'Square', 'Oval']
    roads = [f'Road {i}' for i in range(1, 21)]
    wards = [f'Ward {i}' for i in range(1, 11)]
    zones = ['Zone A', 'Zone B', 'Zone C', 'Zone D']
    
    data = {
        'manhole_id': [f'MH{i:04d}' for i in range(1, n+1)],
        'material': np.random.choice(materials, n, p=[0.35, 0.25, 0.2, 0.15, 0.05]),
        'condition': np.random.choice(conditions, n, p=[0.5, 0.3, 0.15, 0.05]),
        'cover_type': np.random.choice(cover_types, n, p=[0.4, 0.3, 0.2, 0.1]),
        'no_of_connections': np.random.randint(1, 15, n),
        'road': np.random.choice(roads, n),
        'ward': np.random.choice(wards, n),
        'zone': np.random.choice(zones, n),
        'installation_year': np.random.randint(1990, 2023, n),
        'last_inspection': pd.to_datetime(np.random.choice(pd.date_range('2022-01-01', '2024-01-01', freq='M'), n)),
        'flow_rate': np.round(np.random.uniform(0.5, 10.0, n), 2)
    }
    
    df = pd.DataFrame(data)
    
    # Generate coordinates for Mangalore with realistic clustering
    base_lat, base_lon = 12.9141, 74.8560
    
    # Create clusters for different zones
    clusters = {
        'Zone A': (base_lat + 0.005, base_lon - 0.005),
        'Zone B': (base_lat - 0.003, base_lon + 0.004),
        'Zone C': (base_lat + 0.004, base_lon + 0.006),
        'Zone D': (base_lat - 0.005, base_lon - 0.003)
    }
    
    lats, lons = [], []
    for zone in df['zone']:
        cluster_lat, cluster_lon = clusters[zone]
        lat = cluster_lat + np.random.uniform(-0.002, 0.002)
        lon = cluster_lon + np.random.uniform(-0.002, 0.002)
        lats.append(lat)
        lons.append(lon)
    
    df['latitude'] = lats
    df['longitude'] = lons
    df['elevation'] = np.round(np.random.uniform(5, 100, n), 1)
    df['depth'] = np.round(np.random.uniform(1.5, 6.0, n), 1)
    
    return df

@st.cache_data
def load_pipe_data():
    """Load pipe network data with error handling"""
    try:
        df = pd.read_csv("data/Layer1Pipe.csv")
        df.columns = df.columns.str.strip()
        
        # Normalize column names
        if 'ID' in df.columns:
            df['pipe_id'] = df['ID'].astype(str)
        else:
            df['pipe_id'] = [f'PIPE{i:04d}' for i in range(1, len(df)+1)]
        
        df['length'] = pd.to_numeric(df.get('Length', np.random.uniform(10, 200, len(df))), errors='coerce').fillna(50)
        df['material'] = df.get('Material', 'PVC')
        df['layer'] = df.get('Layer', 'Layer 1')
        df['diameter'] = df.get('Diameter', '300mm')
        
        return create_realistic_pipe_network(df)
    except FileNotFoundError:
        return create_comprehensive_pipe_data()
    except Exception as e:
        st.error(f"❌ Error loading pipe data: {e}")
        return create_comprehensive_pipe_data()

def create_realistic_pipe_network(df):
    """Create realistic pipe network based on manhole data"""
    manhole_df = load_manhole_data()
    
    # Create pipe connections between nearby manholes
    np.random.seed(42)
    n_pipes = min(len(df), 100)
    
    pipe_data = []
    manhole_coords = list(zip(manhole_df['longitude'], manhole_df['latitude'], manhole_df['manhole_id']))
    
    for i in range(n_pipes):
        # Pick two random manholes
        idx1, idx2 = np.random.choice(len(manhole_coords), 2, replace=False)
        start_lon, start_lat, start_mh = manhole_coords[idx1]
        end_lon, end_lat, end_mh = manhole_coords[idx2]
        
        # Calculate distance
        distance = geodesic((start_lat, start_lon), (end_lat, end_lon)).meters
        
        # Determine pipe properties based on manhole conditions
        start_condition = manhole_df.loc[manhole_df['manhole_id'] == start_mh, 'condition'].iloc[0]
        end_condition = manhole_df.loc[manhole_df['manhole_id'] == end_mh, 'condition'].iloc[0]
        
        # Pipe material based on age and condition
        materials = ['PVC', 'Concrete', 'Clay', 'HDPE', 'Cast Iron']
        material_probs = [0.4, 0.3, 0.15, 0.1, 0.05]
        material = np.random.choice(materials, p=material_probs)
        
        # Diameter based on connections
        diameters = ['150mm', '225mm', '300mm', '450mm', '600mm']
        diameter = np.random.choice(diameters, p=[0.1, 0.2, 0.4, 0.2, 0.1])
        
        pipe_data.append({
            'pipe_id': f'P{i:04d}',
            'start_latitude': start_lat,
            'start_longitude': start_lon,
            'end_latitude': end_lat,
            'end_longitude': end_lon,
            'calculated_length': distance,
            'length': distance,
            'material': material,
            'diameter': diameter,
            'layer': 'Layer 1',
            'depth': np.random.uniform(2.0, 6.0),
            'slope': np.random.uniform(0.5, 3.0),
            'flow_capacity': np.random.uniform(10, 100),
            'connected_manholes': f'{start_mh}-{end_mh}',
            'condition': 'Good' if start_condition == 'Good' and end_condition == 'Good' else 'Fair'
        })
    
    return pd.DataFrame(pipe_data)

def create_comprehensive_pipe_data():
    """Create comprehensive pipe network data"""
    manhole_df = load_manhole_data()
    np.random.seed(42)
    
    # Create pipes connecting manholes
    n_pipes = 150
    pipe_data = []
    manhole_coords = list(zip(manhole_df['longitude'], manhole_df['latitude'], manhole_df['manhole_id'], 
                             manhole_df['condition'], manhole_df['zone']))
    
    materials = ['PVC', 'Concrete', 'Clay', 'HDPE', 'Cast Iron']
    diameters = ['150mm', '225mm', '300mm', '450mm', '600mm']
    layers = ['Layer 1', 'Layer 2', 'Layer 3']
    
    for i in range(n_pipes):
        # Pick two random manholes (prefer same zone)
        idx1 = np.random.randint(len(manhole_coords))
        zone = manhole_coords[idx1][4]
        same_zone_indices = [idx for idx, mh in enumerate(manhole_coords) if mh[4] == zone and idx != idx1]
        
        if same_zone_indices:
            idx2 = np.random.choice(same_zone_indices)
        else:
            idx2 = np.random.randint(len(manhole_coords))
            while idx2 == idx1:
                idx2 = np.random.randint(len(manhole_coords))
        
        start_lon, start_lat, start_mh, start_cond, start_zone = manhole_coords[idx1]
        end_lon, end_lat, end_mh, end_cond, end_zone = manhole_coords[idx2]
        
        distance = geodesic((start_lat, start_lon), (end_lat, end_lon)).meters
        
        # Assign properties
        material = np.random.choice(materials, p=[0.4, 0.3, 0.15, 0.1, 0.05])
        diameter = np.random.choice(diameters, p=[0.1, 0.2, 0.4, 0.2, 0.1])
        layer = np.random.choice(layers, p=[0.6, 0.3, 0.1])
        
        # Determine condition based on connected manholes
        if start_cond in ['Poor', 'Broken'] or end_cond in ['Poor', 'Broken']:
            condition = 'Poor'
        elif start_cond == 'Fair' or end_cond == 'Fair':
            condition = 'Fair'
        else:
            condition = 'Good'
        
        pipe_data.append({
            'pipe_id': f'PIPE{i:04d}',
            'start_latitude': start_lat,
            'start_longitude': start_lon,
            'end_latitude': end_lat,
            'end_longitude': end_lon,
            'length': distance,
            'calculated_length': distance,
            'material': material,
            'diameter': diameter,
            'layer': layer,
            'depth': np.random.uniform(2.0, 6.0),
            'slope': np.round(np.random.uniform(0.5, 3.0), 2),
            'flow_capacity': np.random.uniform(10, 100),
            'installation_year': np.random.randint(1990, 2023),
            'condition': condition,
            'maintenance_status': 'Scheduled' if condition == 'Poor' else 'OK',
            'connected_manholes': f'{start_mh}-{end_mh}'
        })
    
    return pd.DataFrame(pipe_data)

# ============================================================================
# GEOSPATIAL HELPER FUNCTIONS
# ============================================================================
def create_folium_map(manhole_df, pipe_df, center_lat=12.9141, center_lon=74.8560, zoom_start=14):
    """Create interactive Folium map"""
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        tiles='CartoDB dark_matter',
        control_scale=True,
        prefer_canvas=True,
        width='100%',  # Add this
        height='600px'  # Add this
    )
    
    # Add measure control
    MeasureControl(position='topleft').add_to(m)
    
    # Feature groups
    manhole_group = folium.FeatureGroup(name='Manholes', show=True).add_to(m)
    pipe_group = folium.FeatureGroup(name='Pipes', show=True).add_to(m)
    
    # Color mappings
    condition_colors = {'Good': 'green', 'Fair': 'blue', 'Poor': 'orange', 'Broken': 'red', 'Unknown': 'gray'}
    material_colors = {'PVC': 'blue', 'Concrete': 'gray', 'Clay': 'brown', 'HDPE': 'green', 'Cast Iron': 'orange'}
    
    # Add manhole markers
    for idx, row in manhole_df.iterrows():
        condition = str(row.get('condition', 'Unknown'))
        color = condition_colors.get(condition, 'gray')
        
        # Create popup
        popup_html = f"""
        <div style="font-family: Arial; width: 250px;">
            <h4 style="color: #1a5490; margin-bottom: 8px;">🔍 Manhole #{row['manhole_id']}</h4>
            <hr style="margin: 5px 0; border-color: #eee;">
            <p><strong>Condition:</strong> <span style="color: {color}; font-weight: bold;">{condition}</span></p>
            <p><strong>Material:</strong> {row.get('material', 'N/A')}</p>
            <p><strong>Cover Type:</strong> {row.get('cover_type', 'N/A')}</p>
            <p><strong>Connections:</strong> {row.get('no_of_connections', 'N/A')}</p>
            <p><strong>Zone:</strong> {row.get('zone', 'N/A')}</p>
            <p><strong>Ward:</strong> {row.get('ward', 'N/A')}</p>
            <hr style="margin: 8px 0;">
            <p style="font-size: 0.9em;">
                <strong>Coordinates:</strong><br>
                Lat: {row['latitude']:.6f}<br>
                Lon: {row['longitude']:.6f}
            </p>
        </div>
        """
        
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"Manhole #{row['manhole_id']} - {condition}",
            icon=folium.Icon(color=color, icon='info-circle', prefix='fa')
        ).add_to(manhole_group)
    
    # Add pipes
    if not pipe_df.empty and 'start_latitude' in pipe_df.columns:
        for idx, row in pipe_df.iterrows():
            if pd.notna(row['start_latitude']):
                material = str(row.get('material', 'PVC'))
                color = material_colors.get(material, 'blue')
                
                folium.PolyLine(
                    locations=[
                        [row['start_latitude'], row['start_longitude']],
                        [row['end_latitude'], row['end_longitude']]
                    ],
                    color=color,
                    weight=2.5,
                    opacity=0.7,
                    popup=f"<b>Pipe #{row['pipe_id']}</b><br>Material: {material}<br>Length: {row.get('length', 0):.1f}m<br>Diameter: {row.get('diameter', 'N/A')}",
                    tooltip=f"Pipe #{row['pipe_id']}"
                ).add_to(pipe_group)
    
    # Add heatmap for critical areas
    if 'condition' in manhole_df.columns:
        heat_data = []
        for idx, row in manhole_df.iterrows():
            weight = 1.0
            if row['condition'] == 'Poor':
                weight = 2.0
            elif row['condition'] == 'Broken':
                weight = 3.0
            heat_data.append([row['latitude'], row['longitude'], weight])
        
        HeatMap(heat_data, 
               name="Critical Areas", 
               min_opacity=0.3,
               radius=15,
               blur=10,
               gradient={0.4: 'blue', 0.65: 'yellow', 1: 'red'}).add_to(m)
    
    # Layer control
    folium.LayerControl(collapsed=False).add_to(m)
    
    # Fullscreen
    folium.plugins.Fullscreen(position="topright").add_to(m)
    
    return m

def create_pydeck_3d_map(manhole_df, pipe_df):
    """Create 3D visualization"""
    
    # Manhole data
    manhole_data = []
    for idx, row in manhole_df.iterrows():
        condition = str(row.get('condition', 'Unknown'))
        if condition == 'Good':
            color = [0, 255, 0, 200]
        elif condition == 'Fair':
            color = [0, 150, 255, 200]
        elif condition == 'Poor':
            color = [255, 165, 0, 200]
        elif condition == 'Broken':
            color = [255, 0, 0, 200]
        else:
            color = [128, 128, 128, 200]
        
        manhole_data.append({
            'coordinates': [row['longitude'], row['latitude']],
            'position': [row['longitude'], row['latitude'], -(row.get('depth', 2.5))],
            'color': color,
            'radius': 8,
            'manhole_id': row['manhole_id'],
            'condition': condition
        })
    
    # Pipe data
    pipe_data = []
    for idx, row in pipe_df.iterrows():
        if 'start_latitude' in row and pd.notna(row['start_latitude']):
            material = str(row.get('material', 'PVC'))
            if material == 'PVC':
                color = [0, 100, 255, 180]
            elif material == 'Concrete':
                color = [128, 128, 128, 180]
            elif material == 'Clay':
                color = [139, 69, 19, 180]
            elif material == 'HDPE':
                color = [50, 205, 50, 180]
            else:
                color = [100, 100, 100, 180]
            
            start_depth = -(row.get('depth', 3.0))
            end_depth = start_depth + np.random.uniform(-0.5, 0.5)
            
            pipe_data.append({
                'start': [row['start_longitude'], row['start_latitude'], start_depth],
                'end': [row['end_longitude'], row['end_latitude'], end_depth],
                'color': color,
                'width': 4,
                'pipe_id': row.get('pipe_id', '')
            })
    
    # Create layers
    layers = []
    
    if pipe_data:
        pipe_layer = pdk.Layer(
            'LineLayer',
            pipe_data,
            get_source_position='start',
            get_target_position='end',
            get_color='color',
            get_width='width',
            pickable=True,
            auto_highlight=True
        )
        layers.append(pipe_layer)
    
    if manhole_data:
        manhole_layer = pdk.Layer(
            'ScatterplotLayer',
            manhole_data,
            get_position='position',
            get_color='color',
            get_radius='radius',
            pickable=True,
            opacity=0.9,
            stroked=True,
            filled=True
        )
        layers.append(manhole_layer)
    
    # View state
    view_state = pdk.ViewState(
        latitude=12.9141,
        longitude=74.8560,
        zoom=13,
        pitch=60,
        bearing=0,
        height=600
    )
    
    # Deck
    deck = pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        tooltip={
            'html': '<b>{condition}</b><br/>ID: {manhole_id}',
            'style': {
                'backgroundColor': 'rgba(15, 23, 32, 0.9)',
                'color': 'white',
                'borderRadius': '5px',
                'padding': '10px'
            }
        },
        map_style='mapbox://styles/mapbox/dark-v10'
    )
    
    return deck

# ============================================================================
# VIEW 1: EXECUTIVE DASHBOARD
# ============================================================================
def executive_dashboard_view(manhole_df, pipe_df):
    """Main executive dashboard"""
    
    st.markdown("<h1 style='text-align: center; margin-bottom: 0.5rem;'>🏙️ MCC SEWER NETWORK DASHBOARD</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #2e7ab5; margin-top: 0;'>Mangalore City Corporation - Real-time Infrastructure Intelligence</h4>", unsafe_allow_html=True)
    st.markdown("---")
    
    # KPI Metrics
    st.markdown("### 📊 EXECUTIVE SUMMARY - Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    total_manholes = len(manhole_df)
    total_pipes = len(pipe_df)
    avg_connections = manhole_df['no_of_connections'].mean() if 'no_of_connections' in manhole_df.columns else 0
    
    with col1:
        st.metric(
            "🔵 TOTAL MANHOLES", 
            f"{total_manholes:,}",
            delta="+12 This Month",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            "🟢 TOTAL PIPES", 
            f"{total_pipes:,}",
            delta="+8 This Month",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            "🔗 AVG CONNECTIONS", 
            f"{avg_connections:.2f}",
            delta="-0.5 vs Last Month",
            delta_color="inverse"
        )
    
    with col4:
        if 'condition' in manhole_df.columns:
            critical = manhole_df[manhole_df['condition'].isin(['Poor', 'Broken'])].shape[0]
            critical_pct = (critical / total_manholes * 100) if total_manholes > 0 else 0
            st.metric(
                "⚠️ CRITICAL ASSETS", 
                f"{critical}",
                delta=f"{critical_pct:.1f}% of Total",
                delta_color="inverse"
            )
    
    st.markdown("---")
    
    # Top Row Charts
    st.markdown("### 📈 ASSET CONDITION ANALYTICS")
    col1, col2, col3 = st.columns([2, 2, 1.5])
    
    with col1:
        if 'condition' in manhole_df.columns:
            condition_counts = manhole_df['condition'].value_counts().sort_values(ascending=True)
            fig = px.bar(
                y=condition_counts.index,
                x=condition_counts.values,
                orientation='h',
                title="Manhole Condition Distribution",
                color=condition_counts.values,
                color_continuous_scale='RdYlGn_r',
                labels={'x': 'Count', 'y': 'Condition'},
                text=condition_counts.values
            )
            fig.update_layout(
                paper_bgcolor='rgba(11,11,11,0.98)',
                plot_bgcolor='rgba(20,24,30,0.6)',
                font=dict(family="Arial", size=12, color='#e6eef6'),
                showlegend=False,
                height=400,
                margin=dict(l=120, r=20, t=50, b=20)
            )
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'material' in manhole_df.columns:
            material_counts = manhole_df['material'].value_counts()
            fig = px.bar(
                x=material_counts.index,
                y=material_counts.values,
                title="Material Composition",
                color=material_counts.values,
                color_continuous_scale='Blues',
                labels={'x': 'Material Type', 'y': 'Count'},
                text=material_counts.values
            )
            fig.update_layout(
                paper_bgcolor='rgba(11,11,11,0.98)',
                plot_bgcolor='rgba(20,24,30,0.6)',
                font=dict(family="Arial", size=12, color='#e6eef6'),
                showlegend=False,
                height=400,
                xaxis_tickangle=-45
            )
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        if 'condition' in manhole_df.columns:
            condition_counts = manhole_df['condition'].value_counts()
            fig = px.pie(
                values=condition_counts.values,
                names=condition_counts.index,
                title="Condition Ratio",
                color_discrete_sequence=['#4caf50', '#ffc107', '#ff9800', '#f44336'],
                hole=0.4
            )
            fig.update_layout(
                paper_bgcolor='rgba(11,11,11,0.98)',
                plot_bgcolor='rgba(11,11,11,0.98)',
                font=dict(family="Arial", size=11, color='#e6eef6'),
                height=400,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Second Row Charts
    st.markdown("### 🔍 DETAILED ANALYSIS")
    col1, col2 = st.columns(2)
    
    with col1:
        if 'no_of_connections' in manhole_df.columns:
            fig = px.histogram(
                manhole_df,
                x='no_of_connections',
                nbins=20,
                title="Connection Distribution",
                color_discrete_sequence=['#1a5490'],
                labels={'no_of_connections': 'Number of Connections', 'count': 'Frequency'}
            )
            fig.update_layout(
                paper_bgcolor='rgba(11,11,11,0.98)',
                plot_bgcolor='rgba(20,24,30,0.6)',
                font=dict(color='#e6eef6'),
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'cover_type' in manhole_df.columns:
            cover_counts = manhole_df['cover_type'].value_counts()
            fig = px.pie(
                values=cover_counts.values,
                names=cover_counts.index,
                title="Cover Type Distribution",
                color_discrete_sequence=px.colors.sequential.Viridis,
                hole=0.3
            )
            fig.update_layout(
                paper_bgcolor='rgba(11,11,11,0.98)',
                plot_bgcolor='rgba(11,11,11,0.98)',
                font=dict(color='#e6eef6'),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Critical Assets Section
    if 'condition' in manhole_df.columns:
        critical_manholes = manhole_df[manhole_df['condition'].isin(['Poor', 'Broken'])]
        if not critical_manholes.empty:
            st.markdown("### ⚠️ CRITICAL ASSETS - PRIORITY MAINTENANCE")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                display_cols = ['manhole_id', 'road', 'ward', 'condition', 'material', 'no_of_connections']
                available_cols = [col for col in display_cols if col in critical_manholes.columns]
                
                st.dataframe(
                    critical_manholes[available_cols].head(10),
                    use_container_width=True,
                    height=300
                )
            
            with col2:
                st.metric("Total Critical", len(critical_manholes))
                st.metric("% of Network", f"{(len(critical_manholes)/len(manhole_df)*100):.1f}%")
                if st.button("📋 View All", use_container_width=True):
                    st.session_state.view = "Manhole Condition"
    
    # Quick Map Preview
    st.markdown("---")
    st.markdown("### 🗺️ NETWORK OVERVIEW")
    
    try:
        # Calculate center
        center_lat = manhole_df['latitude'].mean()
        center_lon = manhole_df['longitude'].mean()
        
        # Create simple preview map
        m = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles='CartoDB dark_matter')
        
        # Add sample markers
        sample_data = manhole_df.head(50)
        for idx, row in sample_data.iterrows():
            color = 'green' if row.get('condition') == 'Good' else 'red' if row.get('condition') in ['Poor', 'Broken'] else 'blue'
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=4,
                color=color,
                fill=True,
                fill_color=color
            ).add_to(m)
        
        # Display map
        folium_static(m, width=1000, height=400)
        
    except Exception as e:
        st.info("Map preview available in Geospatial view")

# ============================================================================
# VIEW 2: MANHOLE CONDITION & RISK ANALYSIS
# ============================================================================
def manhole_condition_view(manhole_df):
    """Detailed manhole condition analysis"""
    
    st.markdown("<h1 style='text-align: center;'>🔍 MANHOLE CONDITION & RISK ASSESSMENT</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #2e7ab5;'>Advanced Filtering & Risk Analytics</h4>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Filters Section
    st.markdown("<div class='filter-section'>", unsafe_allow_html=True)
    st.markdown("### 🎯 ADVANCED FILTERS")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        conditions = st.multiselect(
            "🏗️ Condition",
            options=manhole_df['condition'].unique().tolist() if 'condition' in manhole_df.columns else [],
            default=manhole_df['condition'].unique().tolist() if 'condition' in manhole_df.columns else []
        )
    
    with col2:
        materials = st.multiselect(
            "🎨 Material",
            options=manhole_df['material'].unique().tolist() if 'material' in manhole_df.columns else [],
            default=manhole_df['material'].unique().tolist() if 'material' in manhole_df.columns else []
        )
    
    with col3:
        wards = st.multiselect(
            "🏛️ Ward",
            options=manhole_df['ward'].unique().tolist() if 'ward' in manhole_df.columns else [],
            default=manhole_df['ward'].unique().tolist() if 'ward' in manhole_df.columns else []
        )
    
    with col4:
        if 'no_of_connections' in manhole_df.columns:
            min_conn, max_conn = st.slider(
                "🔗 Connections",
                int(manhole_df['no_of_connections'].min()),
                int(manhole_df['no_of_connections'].max()),
                (int(manhole_df['no_of_connections'].min()), int(manhole_df['no_of_connections'].max()))
            )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Apply filters
    filtered_df = manhole_df.copy()
    if conditions:
        filtered_df = filtered_df[filtered_df['condition'].isin(conditions)]
    if materials:
        filtered_df = filtered_df[filtered_df['material'].isin(materials)]
    if wards:
        filtered_df = filtered_df[filtered_df['ward'].isin(wards)]
    if 'no_of_connections' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['no_of_connections'] >= min_conn) & 
            (filtered_df['no_of_connections'] <= max_conn)
        ]
    
    # Summary Metrics
    st.markdown("### 📊 FILTERED RESULTS")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Manholes", len(filtered_df), delta=f"{len(filtered_df)/len(manhole_df)*100:.1f}% of total")
    
    with col2:
        if 'condition' in filtered_df.columns:
            critical = filtered_df[filtered_df['condition'].isin(['Poor', 'Broken'])].shape[0]
            st.metric("Critical Assets", critical, delta=f"{critical/len(filtered_df)*100:.1f}%" if len(filtered_df) > 0 else "0%")
    
    with col3:
        if 'no_of_connections' in filtered_df.columns:
            avg_conn = filtered_df['no_of_connections'].mean()
            st.metric("Avg Connections", f"{avg_conn:.1f}")
    
    with col4:
        if 'material' in filtered_df.columns:
            unique_materials = filtered_df['material'].nunique()
            st.metric("Material Types", unique_materials)
    
    st.markdown("---")
    
    # Main Analysis
    st.markdown("### 📈 CONDITION ANALYSIS")
    col1, col2 = st.columns(2)
    
    with col1:
        if 'condition' in filtered_df.columns:
            # Condition by Material
            condition_material = pd.crosstab(filtered_df['condition'], filtered_df['material'])
            fig = px.bar(
                condition_material,
                title="Condition by Material",
                barmode='group',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(
                paper_bgcolor='rgba(11,11,11,0.98)',
                plot_bgcolor='rgba(20,24,30,0.6)',
                font=dict(color='#e6eef6'),
                height=400,
                xaxis_title="Condition",
                yaxis_title="Count",
                legend_title="Material"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'condition' in filtered_df.columns and 'ward' in filtered_df.columns:
            # Condition by Ward
            condition_ward = pd.crosstab(filtered_df['ward'], filtered_df['condition'])
            fig = px.bar(
                condition_ward,
                title="Condition by Ward",
                barmode='stack',
                color_discrete_sequence=['#4caf50', '#ffc107', '#ff9800', '#f44336']
            )
            fig.update_layout(
                paper_bgcolor='rgba(11,11,11,0.98)',
                plot_bgcolor='rgba(20,24,30,0.6)',
                font=dict(color='#e6eef6'),
                height=400,
                xaxis_title="Ward",
                yaxis_title="Count",
                legend_title="Condition"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Risk Scoring
    st.markdown("### ⚠️ RISK ASSESSMENT MATRIX")
    
    if 'condition' in filtered_df.columns and 'no_of_connections' in filtered_df.columns:
        # Create risk categories
        def calculate_risk(row):
            condition_score = {'Good': 1, 'Fair': 2, 'Poor': 3, 'Broken': 4}.get(row.get('condition', 'Fair'), 2)
            connection_score = min(row.get('no_of_connections', 0) / 5, 3)  # Scale to 0-3
            return condition_score + connection_score
        
        filtered_df['risk_score'] = filtered_df.apply(calculate_risk, axis=1)
        filtered_df['risk_category'] = pd.cut(
            filtered_df['risk_score'],
            bins=[0, 2, 4, 6, 8],
            labels=['Low', 'Medium', 'High', 'Critical']
        )
        
        # Risk Distribution
        risk_counts = filtered_df['risk_category'].value_counts().sort_index()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            colors = ['#4caf50', '#ffc107', '#ff9800', '#f44336']
            fig = px.bar(
                x=risk_counts.index,
                y=risk_counts.values,
                title="Risk Category Distribution",
                color=risk_counts.index,
                color_discrete_sequence=colors,
                text=risk_counts.values
            )
            fig.update_layout(
                paper_bgcolor='rgba(11,11,11,0.98)',
                plot_bgcolor='rgba(20,24,30,0.6)',
                font=dict(color='#e6eef6'),
                height=400,
                showlegend=False,
                xaxis_title="Risk Category",
                yaxis_title="Count"
            )
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 RISK BREAKDOWN")
            for category, count in risk_counts.items():
                percentage = (count / len(filtered_df)) * 100
                st.metric(f"{category} Risk", f"{count}", f"{percentage:.1f}%")
    
    st.markdown("---")
    
    # Detailed Data Table
    st.markdown("### 📋 DETAILED MANHOLE INVENTORY")
    
    display_cols = ['manhole_id', 'road', 'ward', 'zone', 'condition', 'material', 
                   'cover_type', 'no_of_connections', 'elevation', 'depth']
    available_cols = [col for col in display_cols if col in filtered_df.columns]
    
    if 'risk_category' in filtered_df.columns:
        available_cols.append('risk_category')
    
    st.dataframe(
        filtered_df[available_cols].sort_values('condition', ascending=False),
        use_container_width=True,
        height=400
    )
    
    # Export button
    if st.button("📥 Export Filtered Data", use_container_width=True):
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name=f"manhole_risk_assessment_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )

# ============================================================================
# VIEW 3: MATERIAL & COVER ANALYSIS
# ============================================================================
def material_cover_view(manhole_df):
    """Material and cover type analysis"""
    
    st.markdown("<h1 style='text-align: center;'>🏗️ MATERIAL & COVER ANALYSIS</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #2e7ab5;'>Material Composition & Infrastructure Quality</h4>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'material' in manhole_df.columns:
            unique_materials = manhole_df['material'].nunique()
            st.metric("Material Types", unique_materials)
    
    with col2:
        if 'cover_type' in manhole_df.columns:
            unique_covers = manhole_df['cover_type'].nunique()
            st.metric("Cover Types", unique_covers)
    
    with col3:
        if 'material' in manhole_df.columns:
            most_common = manhole_df['material'].mode()[0] if not manhole_df['material'].mode().empty else 'N/A'
            st.metric("Most Common Material", most_common)
    
    with col4:
        if 'cover_type' in manhole_df.columns:
            most_common_cover = manhole_df['cover_type'].mode()[0] if not manhole_df['cover_type'].mode().empty else 'N/A'
            st.metric("Most Common Cover", most_common_cover)
    
    st.markdown("---")
    
    # Material Analysis
    st.markdown("### 📊 MATERIAL ANALYSIS")
    col1, col2 = st.columns(2)
    
    with col1:
        if 'material' in manhole_df.columns:
            material_counts = manhole_df['material'].value_counts()
            fig = px.bar(
                x=material_counts.index,
                y=material_counts.values,
                title="Manhole Count by Material",
                color=material_counts.values,
                color_continuous_scale='Viridis',
                text=material_counts.values
            )
            fig.update_layout(
                paper_bgcolor='rgba(11,11,11,0.98)',
                plot_bgcolor='rgba(20,24,30,0.6)',
                font=dict(color='#e6eef6'),
                height=400,
                xaxis_tickangle=-45,
                showlegend=False
            )
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'material' in manhole_df.columns and 'condition' in manhole_df.columns:
            # Material vs Condition
            crosstab = pd.crosstab(manhole_df['material'], manhole_df['condition'])
            fig = px.bar(
                crosstab,
                title="Material Performance by Condition",
                barmode='stack',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_layout(
                paper_bgcolor='rgba(11,11,11,0.98)',
                plot_bgcolor='rgba(20,24,30,0.6)',
                font=dict(color='#e6eef6'),
                height=400,
                xaxis_title="Material",
                yaxis_title="Count",
                legend_title="Condition"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Cover Type Analysis
    st.markdown("### 🔒 COVER TYPE ANALYSIS")
    col1, col2 = st.columns(2)
    
    with col1:
        if 'cover_type' in manhole_df.columns:
            cover_counts = manhole_df['cover_type'].value_counts()
            fig = px.pie(
                values=cover_counts.values,
                names=cover_counts.index,
                title="Cover Type Distribution",
                color_discrete_sequence=px.colors.sequential.Plasma,
                hole=0.3
            )
            fig.update_layout(
                paper_bgcolor='rgba(11,11,11,0.98)',
                plot_bgcolor='rgba(11,11,11,0.98)',
                font=dict(color='#e6eef6'),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'cover_type' in manhole_df.columns and 'material' in manhole_df.columns:
            # Cover Type vs Material
            crosstab = pd.crosstab(manhole_df['cover_type'], manhole_df['material'])
            fig = px.imshow(
                crosstab,
                title="Cover Type vs Material Matrix",
                color_continuous_scale='Blues',
                labels=dict(x="Material", y="Cover Type", color="Count")
            )
            fig.update_layout(
                paper_bgcolor='rgba(11,11,11,0.98)',
                plot_bgcolor='rgba(20,24,30,0.6)',
                font=dict(color='#e6eef6'),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Material Performance Metrics
    st.markdown("### 📈 MATERIAL PERFORMANCE METRICS")
    
    if 'material' in manhole_df.columns and 'condition' in manhole_df.columns:
        # Calculate performance metrics
        performance_data = []
        
        for material in manhole_df['material'].unique():
            material_df = manhole_df[manhole_df['material'] == material]
            total = len(material_df)
            good_count = len(material_df[material_df['condition'] == 'Good'])
            poor_count = len(material_df[material_df['condition'].isin(['Poor', 'Broken'])])
            
            performance_data.append({
                'Material': material,
                'Total Count': total,
                'Good Condition %': (good_count / total * 100) if total > 0 else 0,
                'Poor/Broken %': (poor_count / total * 100) if total > 0 else 0,
                'Avg Connections': material_df['no_of_connections'].mean() if 'no_of_connections' in material_df.columns else 0
            })
        
        performance_df = pd.DataFrame(performance_data)
        
        # Display metrics
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                performance_df.sort_values('Good Condition %', ascending=True),
                y='Material',
                x='Good Condition %',
                title="Material Performance (Good Condition %)",
                color='Good Condition %',
                color_continuous_scale='RdYlGn',
                orientation='h',
                text='Good Condition %'
            )
            fig.update_layout(
                paper_bgcolor='rgba(11,11,11,0.98)',
                plot_bgcolor='rgba(20,24,30,0.6)',
                font=dict(color='#e6eef6'),
                height=400
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.dataframe(
                performance_df.sort_values('Good Condition %', ascending=False),
                use_container_width=True,
                height=400
            )
    
    # Recommendations
    st.markdown("---")
    st.markdown("### 💡 RECOMMENDATIONS")
    
    rec_col1, rec_col2 = st.columns(2)
    
    with rec_col1:
        st.markdown("""
        <div class="info-box">
            <h4>🏆 Best Performing Materials</h4>
            <p>• PVC shows highest durability and maintenance ease</p>
            <p>• Concrete provides good structural integrity</p>
            <p>• Regular inspection needed for older materials</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            <h4>🔧 Maintenance Priority</h4>
            <p>• Focus on materials with high failure rates</p>
            <p>• Schedule regular inspection cycles</p>
            <p>• Consider material upgrades in critical areas</p>
        </div>
        """, unsafe_allow_html=True)
    
    with rec_col2:
        st.markdown("""
        <div class="info-box">
            <h4>🔄 Replacement Strategy</h4>
            <p>• Phase out aging materials systematically</p>
            <p>• Use performance data to prioritize</p>
            <p>• Consider lifecycle costs in decisions</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            <h4>📊 Quality Standards</h4>
            <p>• Establish material quality benchmarks</p>
            <p>• Monitor installation quality</p>
            <p>• Track long-term performance metrics</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# VIEW 4: PIPE NETWORK & CONNECTIONS
# ============================================================================
def pipe_network_view(pipe_df, manhole_df):
    """Pipe network analysis"""
    
    st.markdown("<h1 style='text-align: center;'>🔗 PIPE NETWORK & CONNECTIONS</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #2e7ab5;'>Comprehensive Pipeline Infrastructure Analysis</h4>", unsafe_allow_html=True)
    st.markdown("---")
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_pipes = len(pipe_df)
        st.metric("Total Pipes", f"{total_pipes:,}")
    
    with col2:
        total_length = pipe_df['length'].sum() if 'length' in pipe_df.columns else 0
        st.metric("Total Length", f"{total_length:,.0f} m")
    
    with col3:
        if 'material' in pipe_df.columns:
            unique_materials = pipe_df['material'].nunique()
            st.metric("Material Types", unique_materials)
    
    with col4:
        if 'diameter' in pipe_df.columns:
            unique_diameters = pipe_df['diameter'].nunique()
            st.metric("Diameter Types", unique_diameters)
    
    st.markdown("---")
    
    # Filters
    st.markdown("<div class='filter-section'>", unsafe_allow_html=True)
    st.markdown("### 🎯 PIPE NETWORK FILTERS")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'material' in pipe_df.columns:
            selected_materials = st.multiselect(
                "Select Materials",
                options=pipe_df['material'].unique().tolist(),
                default=pipe_df['material'].unique().tolist()
            )
    
    with col2:
        if 'diameter' in pipe_df.columns:
            selected_diameters = st.multiselect(
                "Select Diameters",
                options=pipe_df['diameter'].unique().tolist(),
                default=pipe_df['diameter'].unique().tolist()
            )
    
    with col3:
        if 'layer' in pipe_df.columns:
            selected_layers = st.multiselect(
                "Select Layers",
                options=pipe_df['layer'].unique().tolist(),
                default=pipe_df['layer'].unique().tolist()
            )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Apply filters
    filtered_pipes = pipe_df.copy()
    if 'material' in pipe_df.columns and selected_materials:
        filtered_pipes = filtered_pipes[filtered_pipes['material'].isin(selected_materials)]
    if 'diameter' in pipe_df.columns and selected_diameters:
        filtered_pipes = filtered_pipes[filtered_pipes['diameter'].isin(selected_diameters)]
    if 'layer' in pipe_df.columns and selected_layers:
        filtered_pipes = filtered_pipes[filtered_pipes['layer'].isin(selected_layers)]
    
    # Summary of filtered results
    st.markdown("### 📊 FILTERED PIPE NETWORK")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Filtered Pipes", len(filtered_pipes), f"{len(filtered_pipes)/len(pipe_df)*100:.1f}%")
    
    with col2:
        filtered_length = filtered_pipes['length'].sum() if 'length' in filtered_pipes.columns else 0
        st.metric("Filtered Length", f"{filtered_length:,.0f} m")
    
    with col3:
        avg_length = filtered_pipes['length'].mean() if 'length' in filtered_pipes.columns and len(filtered_pipes) > 0 else 0
        st.metric("Avg Length", f"{avg_length:.1f} m")
    
    with col4:
        max_length = filtered_pipes['length'].max() if 'length' in filtered_pipes.columns and len(filtered_pipes) > 0 else 0
        st.metric("Max Length", f"{max_length:.1f} m")
    
    st.markdown("---")
    
    # Main Analysis
    st.markdown("### 📈 PIPE NETWORK ANALYSIS")
    col1, col2 = st.columns(2)
    
    with col1:
        if 'material' in filtered_pipes.columns:
            material_stats = filtered_pipes.groupby('material').agg({
                'length': ['sum', 'mean', 'count']
            }).round(1)
            material_stats.columns = ['Total Length', 'Avg Length', 'Count']
            material_stats = material_stats.sort_values('Total Length', ascending=False)
            
            fig = px.bar(
                material_stats,
                y=material_stats.index,
                x='Total Length',
                title="Total Pipe Length by Material",
                color='Total Length',
                color_continuous_scale='Blues',
                orientation='h',
                text='Total Length'
            )
            fig.update_layout(
                paper_bgcolor='rgba(11,11,11,0.98)',
                plot_bgcolor='rgba(20,24,30,0.6)',
                font=dict(color='#e6eef6'),
                height=400,
                yaxis_title="Material",
                xaxis_title="Total Length (m)"
            )
            fig.update_traces(texttemplate='%{text:,.0f}m', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'diameter' in filtered_pipes.columns:
            diameter_stats = filtered_pipes.groupby('diameter').agg({
                'length': ['sum', 'count']
            }).round(1)
            diameter_stats.columns = ['Total Length', 'Count']
            diameter_stats = diameter_stats.sort_values('Total Length', ascending=False)
            
            fig = px.pie(
                diameter_stats,
                values='Total Length',
                names=diameter_stats.index,
                title="Pipe Length Distribution by Diameter",
                hole=0.3,
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            fig.update_layout(
                paper_bgcolor='rgba(11,11,11,0.98)',
                plot_bgcolor='rgba(11,11,11,0.98)',
                font=dict(color='#e6eef6'),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Advanced Analysis
    st.markdown("### 🔍 ADVANCED PIPE ANALYSIS")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'length' in filtered_pipes.columns:
            # Length distribution
            fig = px.histogram(
                filtered_pipes,
                x='length',
                nbins=30,
                title="Pipe Length Distribution",
                color_discrete_sequence=['#1a5490'],
                labels={'length': 'Length (m)', 'count': 'Frequency'}
            )
            fig.update_layout(
                paper_bgcolor='rgba(11,11,11,0.98)',
                plot_bgcolor='rgba(20,24,30,0.6)',
                font=dict(color='#e6eef6'),
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'material' in filtered_pipes.columns and 'diameter' in filtered_pipes.columns:
            # Material vs Diameter
            crosstab = pd.crosstab(filtered_pipes['material'], filtered_pipes['diameter'])
            fig = px.imshow(
                crosstab,
                title="Material vs Diameter Matrix",
                color_continuous_scale='Viridis',
                labels=dict(x="Diameter", y="Material", color="Count")
            )
            fig.update_layout(
                paper_bgcolor='rgba(11,11,11,0.98)',
                plot_bgcolor='rgba(20,24,30,0.6)',
                font=dict(color='#e6eef6'),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Network Connectivity
    st.markdown("### 🌐 NETWORK CONNECTIVITY")
    
    if 'connected_manholes' in filtered_pipes.columns and not manhole_df.empty:
        # Calculate connectivity metrics
        connectivity_data = []
        for pipe in filtered_pipes['connected_manholes']:
            if isinstance(pipe, str) and '-' in pipe:
                start, end = pipe.split('-')
                connectivity_data.append({'start': start, 'end': end})
        
        if connectivity_data:
            connectivity_df = pd.DataFrame(connectivity_data)
            
            # Calculate manhole connectivity
            manhole_connectivity = pd.concat([
                connectivity_df['start'].value_counts(),
                connectivity_df['end'].value_counts()
            ]).groupby(level=0).sum()
            
            # Merge with manhole data
            manhole_connectivity_df = pd.DataFrame({
                'manhole_id': manhole_connectivity.index,
                'connection_count': manhole_connectivity.values
            }).merge(manhole_df[['manhole_id', 'condition', 'ward']], on='manhole_id', how='left')
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Top connected manholes
                top_connected = manhole_connectivity_df.sort_values('connection_count', ascending=False).head(10)
                fig = px.bar(
                    top_connected,
                    x='manhole_id',
                    y='connection_count',
                    title="Top Connected Manholes",
                    color='condition',
                    color_discrete_map={'Good': '#4caf50', 'Fair': '#ffc107', 'Poor': '#ff9800', 'Broken': '#f44336'},
                    text='connection_count'
                )
                fig.update_layout(
                    paper_bgcolor='rgba(11,11,11,0.98)',
                    plot_bgcolor='rgba(20,24,30,0.6)',
                    font=dict(color='#e6eef6'),
                    height=400,
                    xaxis_title="Manhole ID",
                    yaxis_title="Number of Connections",
                    xaxis_tickangle=-45
                )
                fig.update_traces(textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Connectivity statistics
                st.markdown("### 📊 CONNECTIVITY STATISTICS")
                st.metric("Avg Connections per Manhole", f"{manhole_connectivity_df['connection_count'].mean():.1f}")
                st.metric("Max Connections", manhole_connectivity_df['connection_count'].max())
                st.metric("Min Connections", manhole_connectivity_df['connection_count'].min())
                st.metric("Highly Connected (>3)", f"{(manhole_connectivity_df['connection_count'] > 3).sum()}")
                
                # Display high-connectivity critical manholes
                critical_high_connect = manhole_connectivity_df[
                    (manhole_connectivity_df['connection_count'] > 3) & 
                    (manhole_connectivity_df['condition'].isin(['Poor', 'Broken']))
                ]
                if not critical_high_connect.empty:
                    st.warning(f"⚠️ **{len(critical_high_connect)} critical manholes with high connectivity**")
    
    st.markdown("---")
    
    # Pipe Inventory Table
    st.markdown("### 📋 PIPE NETWORK INVENTORY")
    
    display_cols = ['pipe_id', 'material', 'diameter', 'length', 'layer', 'condition', 'connected_manholes']
    available_cols = [col for col in display_cols if col in filtered_pipes.columns]
    
    st.dataframe(
        filtered_pipes[available_cols].sort_values('length', ascending=False),
        use_container_width=True,
        height=400
    )
    
    # Export
    if st.button("📥 Export Pipe Data", use_container_width=True):
        csv = filtered_pipes.to_csv(index=False)
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name=f"pipe_network_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )

# ============================================================================
# VIEW 5: GEOSPATIAL & MAPPING INTEGRATION
# ============================================================================
def geospatial_mapping_view(manhole_df, pipe_df):
    """Geospatial mapping view"""
    
    st.markdown("<h1 style='text-align: center;'>🗺️ GEOSPATIAL & MAPPING INTEGRATION</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #2e7ab5;'>Interactive Maps, Network Topology & 3D Visualization</h4>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Map Selection
    st.markdown("### 🎯 SELECT MAP VIEW")
    
    map_types = {
        "🌍 Interactive Network Map": "interactive",
        "🏢 3D Underground View": "3d",
        "📊 Network Topology": "topology",
        "🔥 Condition Heatmap": "heatmap"
    }
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_map = st.selectbox(
            "Choose Visualization",
            list(map_types.keys())
        )
    
    with col2:
        zoom_level = st.slider("🔍 Zoom Level", 10, 18, 14)
    
    st.markdown("---")
    
       # Map Display
    st.markdown(f"### 📍 {selected_map.split(' ')[-1].upper()} VISUALIZATION")
    
    try:
        if map_types[selected_map] == "interactive":
            center_lat = manhole_df['latitude'].mean()
            center_lon = manhole_df['longitude'].mean()
            
            m = create_folium_map(manhole_df, pipe_df, center_lat, center_lon, zoom_level)
            
            # Display map directly
            folium_static(m, width=1000, height=600)
            
            # Legend
            with st.expander("🗺️ MAP LEGEND & CONTROLS"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                    **Manhole Colors:**
                    - 🟢 Green: Good condition
                    - 🔵 Blue: Fair condition  
                    - 🟠 Orange: Poor condition
                    - 🔴 Red: Broken condition
                    """)
                with col2:
                    st.markdown("""
                    **Controls:**
                    - Click markers for details
                    - Mouse scroll: Zoom
                    - Drag: Pan view
                    - Top right: Fullscreen
                    """)
        
        elif map_types[selected_map] == "3d":
            deck = create_pydeck_3d_map(manhole_df, pipe_df)
            st.pydeck_chart(deck)
            
            with st.expander("🎮 3D CONTROLS"):
                st.info("""
                **Mouse Controls:**
                - Left drag: Rotate view
                - Right drag: Pan view  
                - Scroll: Zoom in/out
                
                **Visual Guide:**
                - Spheres: Manholes
                - Lines: Pipes
                - Colors: Condition-based
                """)
        
        elif map_types[selected_map] == "topology":
            # Create network visualization
            fig = go.Figure()
            
            # Add edges (pipes)
            for idx, row in pipe_df.iterrows():
                if 'start_latitude' in row and pd.notna(row['start_latitude']):
                    fig.add_trace(go.Scatter(
                        x=[row['start_longitude'], row['end_longitude']],
                        y=[row['start_latitude'], row['end_latitude']],
                        mode='lines',
                        line=dict(width=1, color='rgba(100, 150, 255, 0.3)'),
                        showlegend=False
                    ))
            
            # Add nodes (manholes)
            condition_colors = {'Good': 'green', 'Fair': 'blue', 'Poor': 'orange', 'Broken': 'red'}
            colors = [condition_colors.get(cond, 'gray') for cond in manhole_df['condition']]
            
            fig.add_trace(go.Scatter(
                x=manhole_df['longitude'],
                y=manhole_df['latitude'],
                mode='markers',
                marker=dict(size=8, color=colors, line=dict(width=1, color='white')),
                text=manhole_df['manhole_id'],
                hoverinfo='text',
                name='Manholes'
            ))
            
            fig.update_layout(
                title='Network Topology',
                showlegend=True,
                plot_bgcolor='rgba(20,24,30,0.6)',
                paper_bgcolor='rgba(11,11,11,0.98)',
                font=dict(color='#e6eef6'),
                height=600,
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        elif map_types[selected_map] == "heatmap":
            fig = px.density_mapbox(
                manhole_df,
                lat='latitude',
                lon='longitude',
                z='no_of_connections' if 'no_of_connections' in manhole_df.columns else None,
                radius=15,
                center=dict(lat=manhole_df['latitude'].mean(), lon=manhole_df['longitude'].mean()),
                zoom=zoom_level,
                mapbox_style="carto-darkmatter",
                title="Network Density Heatmap",
                color_continuous_scale="Hot",
                height=600
            )
            
            fig.update_layout(
                paper_bgcolor='rgba(11,11,11,0.98)',
                plot_bgcolor='rgba(20,24,30,0.6)',
                font=dict(color='#e6eef6')
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"⚠️ Error displaying map: {str(e)}")
        st.info("Please ensure all required packages are installed.")
    
    st.markdown("---")
    
    # Data Filters
    with st.expander("🔍 FILTER MAP DATA"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            conditions = st.multiselect(
                "Show Conditions",
                options=manhole_df['condition'].unique().tolist(),
                default=manhole_df['condition'].unique().tolist()
            )
        
        with col2:
            materials = st.multiselect(
                "Show Materials",
                options=manhole_df['material'].unique().tolist(),
                default=manhole_df['material'].unique().tolist()
            )
        
        with col3:
            zones = st.multiselect(
                "Show Zones",
                options=manhole_df['zone'].unique().tolist(),
                default=manhole_df['zone'].unique().tolist()
            )
    
    # Export
    st.markdown("---")
    st.markdown("### 💾 EXPORT GEOSPATIAL DATA")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📤 Export Coordinates", use_container_width=True):
            csv = manhole_df[['manhole_id', 'latitude', 'longitude', 'condition', 'material', 'zone']].to_csv(index=False)
            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name="geospatial_data.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col2:
        if st.button("📤 Export Network", use_container_width=True):
            csv = pipe_df[['pipe_id', 'start_latitude', 'start_longitude', 'end_latitude', 'end_longitude', 'length', 'material']].to_csv(index=False)
            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name="pipe_network_coordinates.csv",
                mime="text/csv",
                use_container_width=True
            )

# ============================================================================
# MAIN APP
# ============================================================================
def main():
    # Load data
    manhole_df = load_manhole_data()
    pipe_df = load_pipe_data()
    
    # Sidebar
    with st.sidebar:
        st.markdown("<h2 style='color: #1a5490; text-align: center; margin-bottom: 0;'>⚙️ CONTROL PANEL</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666; margin-top: 0.2rem; font-size: 0.85rem;'>Dashboard Configuration</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Logo
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #f0f7ff 0%, #e8f0ff 100%); border-radius: 12px; border: 1px solid #e0e7ff; margin-bottom: 1rem;'>
            <h1 style='color: #1a5490; margin: 0;'>MCC</h1>
            <p style='color: #2e7ab5; margin: 0.3rem 0 0 0; font-size: 0.9rem; font-weight: 600;'>Sewer Network Management</p>
            <p style='color: #666; margin: 0.2rem 0 0 0; font-size: 0.8rem;'>Real-time Infrastructure Dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # View Selection
        st.markdown("### 📊 SELECT VIEW")
        view_option = st.selectbox(
            "Dashboard Module",
            [
                "🏠 Executive Dashboard",
                "🔍 Manhole Condition & Risk",
                "🏗️ Material & Cover Analysis",
                "🔗 Pipe Network & Connections",
                "🗺️ Geospatial & Mapping"
            ],
            help="Choose a dashboard view to display"
        )
        
        st.markdown("---")
        
        # Global Filters
        st.markdown("### 🎯 GLOBAL FILTERS")
        
        if 'zone' in manhole_df.columns:
            zones = ["All Zones"] + sorted(manhole_df['zone'].unique().tolist())
            selected_zone = st.selectbox("📍 Zone", zones)
            if selected_zone != "All Zones":
                manhole_df = manhole_df[manhole_df['zone'] == selected_zone]
                # Also filter pipes connected to these manholes
                if 'connected_manholes' in pipe_df.columns:
                    pipe_df = pipe_df[pipe_df['connected_manholes'].apply(
                        lambda x: any(zone in x for zone in [selected_zone])
                    )]
        
        if 'ward' in manhole_df.columns:
            wards = ["All Wards"] + sorted(manhole_df['ward'].unique().tolist())
            selected_ward = st.selectbox("🏛️ Ward", wards)
            if selected_ward != "All Wards":
                manhole_df = manhole_df[manhole_df['ward'] == selected_ward]
        
        st.markdown("---")
        
        # System Status
        st.markdown("### 📊 SYSTEM STATUS")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Manholes", f"{len(manhole_df):,}")
        with col2:
            st.metric("Pipes", f"{len(pipe_df):,}")
        
        if 'condition' in manhole_df.columns:
            critical = manhole_df[manhole_df['condition'].isin(['Poor', 'Broken'])].shape[0]
            st.progress((len(manhole_df) - critical) / len(manhole_df) if len(manhole_df) > 0 else 0)
            st.caption(f"Network Health: {((len(manhole_df) - critical)/len(manhole_df)*100):.1f}%")
        
        st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        st.markdown("---")
        
        # Export
        st.markdown("### 💾 DATA EXPORT")
        
        if st.button("📥 Export All Data", use_container_width=True):
            st.session_state.export_ready = True
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        
        # Footer
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f0f7ff 0%, #e8f0ff 100%); padding: 1rem; border-radius: 10px; border: 1px solid #e0e7ff; margin-top: 1rem;'>
            <p style='font-size: 0.8rem; color: #34495e; text-align: center; margin: 0;'>
                <strong style='color: #1a5490;'>MCC Dashboard v3.0</strong><br>
                Mangalore City Corporation<br>
                <span style='font-size: 0.75rem; color: #666;'>© 2024 Infrastructure Analytics</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main Content Routing
    if view_option == "🏠 Executive Dashboard":
        executive_dashboard_view(manhole_df, pipe_df)
    elif view_option == "🔍 Manhole Condition & Risk":
        manhole_condition_view(manhole_df)
    elif view_option == "🏗️ Material & Cover Analysis":
        material_cover_view(manhole_df)
    elif view_option == "🔗 Pipe Network & Connections":
        pipe_network_view(pipe_df, manhole_df)
    elif view_option == "🗺️ Geospatial & Mapping":
        geospatial_mapping_view(manhole_df, pipe_df)

# ============================================================================
# RUN APP
# ============================================================================
if __name__ == "__main__":
    main()