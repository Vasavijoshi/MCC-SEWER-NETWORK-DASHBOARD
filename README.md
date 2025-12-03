# 🏙️ MCC Sewer Network Dashboard

<div align="center">

![Version](https://img.shields.io/badge/version-3.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

**Real-time Infrastructure Intelligence for Mangalore City Corporation**

A comprehensive, professional-grade interactive dashboard for monitoring, analyzing, and managing municipal sewer network infrastructure with advanced geospatial visualization and risk analytics.

[Features](#-key-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation) • [Screenshots](#-screenshots)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Data Requirements](#-data-requirements)
- [Usage](#-usage)
- [Dashboard Views](#-dashboard-views)
- [Analytics Capabilities](#-analytics-capabilities)
- [Screenshots](#-screenshots)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

The **MCC Sewer Network Dashboard** is an enterprise-level web application designed to provide municipal engineers, urban planners, and infrastructure managers with powerful tools to monitor, analyze, and maintain sewer network infrastructure. Built with modern data science and geospatial technologies, this dashboard transforms raw infrastructure data into actionable insights.

### Purpose

- **Real-time Monitoring**: Track the health and status of manholes and pipe networks
- **Risk Assessment**: Identify critical assets requiring immediate attention
- **Strategic Planning**: Make data-driven decisions for maintenance and upgrades
- **Resource Optimization**: Prioritize maintenance activities based on condition analytics
- **Geospatial Intelligence**: Visualize infrastructure in 2D/3D interactive maps

---

## ✨ Key Features

### 🎨 Professional UI/UX
- **Sleek Dark Theme**: Modern, eye-friendly interface with gradient backgrounds
- **Responsive Design**: Optimized for desktop, tablet, and mobile viewing
- **Intuitive Navigation**: Sidebar-based module selection with global filters
- **Real-time Updates**: Dynamic data refresh capabilities

### 📊 Executive Dashboard
- **KPI Metrics**: Total manholes, pipes, connections, and critical assets
- **Visual Analytics**: Bar charts, pie charts, and histograms
- **Condition Distribution**: Real-time asset health monitoring
- **Material Composition**: Infrastructure material breakdown
- **Quick Map Preview**: Snapshot of network geography

### 🔍 Manhole Condition & Risk Analysis
- **Advanced Filtering**: Multi-dimensional filters (condition, material, ward, connections)
- **Risk Scoring System**: Automated risk assessment based on condition and connectivity
- **Risk Categorization**: Low, Medium, High, and Critical risk levels
- **Detailed Inventory**: Comprehensive manhole database with export functionality
- **Critical Asset Alerts**: Prioritized list of assets needing immediate attention

### 🏗️ Material & Cover Analysis
- **Material Performance**: Comparative analysis of different materials
- **Cover Type Distribution**: Analysis of manhole cover types
- **Performance Metrics**: Good condition percentages by material
- **Maintenance Recommendations**: Data-driven suggestions for material upgrades
- **Quality Standards**: Benchmarking and quality monitoring

### 🔗 Pipe Network & Connections
- **Network Statistics**: Total length, material types, diameter distribution
- **Connectivity Analysis**: Manhole connection mapping
- **Critical Node Identification**: High-connectivity critical assets
- **Material vs Diameter Matrix**: Cross-dimensional analysis
- **Length Distribution**: Statistical analysis of pipe segments

### 🗺️ Geospatial & Mapping Integration
- **Interactive Network Map**: Folium-based 2D visualization with layer controls
- **3D Underground View**: PyDeck-powered 3D visualization of network depth
- **Network Topology**: Graph-based network visualization
- **Condition Heatmap**: Density mapping of network issues
- **Fullscreen Mode**: Enhanced viewing experience
- **Measure Tools**: Distance and area measurement capabilities

---

## 🛠️ Technology Stack

### Core Framework
- **Streamlit** (1.28+): Web application framework
- **Python** (3.8+): Programming language

### Data Processing
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing

### Visualization
- **Plotly Express & Graph Objects**: Interactive charts
- **Folium**: Interactive 2D maps
- **PyDeck**: 3D geospatial visualization
- **Streamlit-Folium**: Folium integration for Streamlit

### Geospatial
- **Geopy**: Geographic calculations
- **Folium Plugins**: MarkerCluster, HeatMap, MeasureControl

---

## 📦 Installation

### Prerequisites

```bash
# Python 3.8 or higher
python --version

# pip package manager
pip --version
```

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/mcc-sewer-dashboard.git
cd mcc-sewer-dashboard
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.23.0
plotly>=5.14.0
folium>=0.14.0
streamlit-folium>=0.13.0
pydeck>=0.8.0
geopy>=2.3.0
```

### Step 4: Prepare Data Directory

```bash
mkdir -p data
# Place your CSV files in the data directory
```

---

## 📊 Data Requirements

### Required Data Files

The dashboard expects the following CSV files in the `data/` directory:

#### 1. Manhole Data (`data/AddedFields.csv`)

| Column | Description | Type | Example |
|--------|-------------|------|---------|
| ID | Unique manhole identifier | String | MH0001 |
| Material | Construction material | String | Concrete, PVC, Brick |
| Condition | Current condition | String | Good, Fair, Poor, Broken |
| Cover type | Type of manhole cover | String | Circular, Rectangular |
| no of connnections | Number of pipe connections | Integer | 5 |
| Road | Road name/location | String | Main Street |
| Ward | Administrative ward | String | Ward 1 |
| Zone | Geographic zone | String | Zone A |

#### 2. Pipe Data (`data/Layer1Pipe.csv`)

| Column | Description | Type | Example |
|--------|-------------|------|---------|
| ID | Unique pipe identifier | String | PIPE0001 |
| Length | Pipe length in meters | Float | 125.5 |
| Material | Pipe material | String | PVC, Concrete, Clay |
| Diameter | Pipe diameter | String | 300mm |
| Layer | Network layer | String | Layer 1 |

### Sample Data Generation

If data files are not available, the dashboard automatically generates comprehensive sample data with:
- **200 manholes** with realistic distributions
- **150 pipes** connecting manholes
- **GPS coordinates** centered around Mangalore (12.9141° N, 74.8560° E)
- **Synthetic attributes** for testing and demonstration

---

## 🚀 Usage

### Starting the Dashboard

```bash
streamlit run app.py
```

The dashboard will automatically open in your default web browser at `http://localhost:8501`

### Alternative Ports

```bash
# Use custom port
streamlit run app.py --server.port 8080

# Run on network
streamlit run app.py --server.address 0.0.0.0
```

### Command Line Options

```bash
# Disable theme
streamlit run app.py --theme.base "light"

# Increase memory
streamlit run app.py --server.maxUploadSize 500

# Enable development mode
streamlit run app.py --server.runOnSave true
```

---

## 📱 Dashboard Views

### 1. 🏠 Executive Dashboard

**Purpose**: High-level overview for decision-makers

**Features**:
- Real-time KPI metrics (total manholes, pipes, connections)
- Condition distribution charts
- Material composition analysis
- Connection histogram
- Cover type distribution
- Critical assets table
- Quick map preview

**Best For**: Daily monitoring, executive reports, quick status checks

---

### 2. 🔍 Manhole Condition & Risk

**Purpose**: Detailed risk assessment and filtering

**Features**:
- Multi-dimensional filters (condition, material, ward, connections)
- Risk scoring algorithm
- Risk categorization (Low/Medium/High/Critical)
- Condition by material analysis
- Condition by ward visualization
- Risk assessment matrix
- Detailed inventory table
- CSV export functionality

**Best For**: Maintenance planning, risk mitigation, asset prioritization

---

### 3. 🏗️ Material & Cover Analysis

**Purpose**: Infrastructure quality and material performance

**Features**:
- Material type distribution
- Cover type analysis
- Material performance metrics
- Condition by material crosstab
- Cover type vs material matrix
- Performance percentage calculations
- Maintenance recommendations
- Quality standards display

**Best For**: Material selection, quality assurance, upgrade planning

---

### 4. 🔗 Pipe Network & Connections

**Purpose**: Pipeline infrastructure analysis

**Features**:
- Total pipe length calculations
- Material and diameter filters
- Length distribution analysis
- Material vs diameter matrix
- Network connectivity analysis
- Top connected manholes
- High-connectivity critical assets identification
- Pipe inventory table

**Best For**: Network planning, connectivity analysis, expansion projects

---

### 5. 🗺️ Geospatial & Mapping

**Purpose**: Geographic visualization and spatial analysis

**Features**:

#### Interactive Network Map
- Color-coded manhole markers
- Pipe network overlay
- Click for detailed information
- Layer controls (manholes, pipes, heatmap)
- Fullscreen mode
- Measure tools

#### 3D Underground View
- Depth-based visualization
- Rotating camera controls
- Color-coded by condition
- Interactive tooltips

#### Network Topology
- Graph-based network visualization
- Node-edge representation
- Connection patterns

#### Condition Heatmap
- Density-based visualization
- Hot spot identification
- Zoom controls

**Best For**: Spatial planning, field operations, geographic analysis

---

## 📈 Analytics Capabilities

### Risk Assessment Algorithm

The dashboard uses a sophisticated risk scoring system:

```python
Risk Score = Condition Score + Connection Score

Condition Scores:
- Good: 1 point
- Fair: 2 points
- Poor: 3 points
- Broken: 4 points

Connection Score:
- Scaled based on number of connections (0-3 points)

Risk Categories:
- Low: 0-2 points
- Medium: 2-4 points
- High: 4-6 points
- Critical: 6-8 points
```

### Performance Metrics

- **Good Condition %**: Percentage of assets in good condition by material
- **Network Health**: Overall infrastructure health score
- **Connectivity Index**: Average connections per manhole
- **Material Performance**: Comparative material durability analysis

### Geospatial Analysis

- **Cluster Detection**: Identifies geographic concentrations of issues
- **Distance Calculations**: Uses geodesic formulas for accurate measurements
- **Elevation Analysis**: Incorporates topographic data
- **Zone-based Aggregation**: Ward and zone-level statistics

---

## 🖼️ Screenshots

### Executive Dashboard
![Executive Dashboard]<img width="1657" height="876" alt="image" src="https://github.com/user-attachments/assets/869be10a-4269-4db6-a1e4-b2765eac47bc" />
<img width="1634" height="873" alt="image" src="https://github.com/user-attachments/assets/db1202e6-7286-42ae-97bb-8338bd647d3b" />

*Real-time KPI metrics and condition analytics*

### Geospatial View
![Map View](screenshots/map_view.png)
*Interactive network visualization with layer controls*

### Risk Assessment
![Risk Analysis](screenshots/risk_analysis.png)
*Comprehensive risk scoring and categorization*

---

## ⚙️ Configuration

### Custom Styling

Edit the CSS in the `st.markdown()` section of `app.py`:

```python
# Background color
background: linear-gradient(180deg, #0b0b0b 0%, #141414 50%, #0d0d0d 100%);

# Accent colors
primary: #1a5490
secondary: #2e7ab5
```

### Default Coordinates

Change the center point for maps:

```python
# Mangalore coordinates (default)
center_lat, center_lon = 12.9141, 74.8560

# Change to your city
center_lat, center_lon = YOUR_LAT, YOUR_LON
```

### Data Paths

Modify file paths in the code:

```python
# Default paths
manhole_data = "data/AddedFields.csv"
pipe_data = "data/Layer1Pipe.csv"

# Custom paths
manhole_data = "path/to/your/manholes.csv"
pipe_data = "path/to/your/pipes.csv"
```

---

## 🐛 Troubleshooting

### Common Issues

#### Map Not Displaying

**Problem**: Map appears blank or throws errors

**Solution**:
```bash
# Reinstall folium
pip uninstall folium streamlit-folium
pip install folium==0.14.0 streamlit-folium==0.13.0
```

#### Data Loading Errors

**Problem**: CSV files not found

**Solution**:
- Ensure `data/` directory exists
- Check file names match exactly
- Verify CSV formatting (UTF-8 encoding)

#### Performance Issues

**Problem**: Dashboard runs slowly

**Solutions**:
- Reduce dataset size for testing
- Use data sampling: `df.sample(n=1000)`
- Clear Streamlit cache: `st.cache_data.clear()`
- Increase memory: `streamlit run app.py --server.maxUploadSize 500`

#### Package Conflicts

**Problem**: Import errors or version conflicts

**Solution**:
```bash
# Create fresh virtual environment
python -m venv fresh_venv
source fresh_venv/bin/activate  # or fresh_venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---
