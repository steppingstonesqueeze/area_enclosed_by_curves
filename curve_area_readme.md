# Piecewise Linear Curve Area Calculator 📐

A comprehensive Python implementation for approximating the area enclosed by piecewise linear curves using two powerful numerical methods: **Intelligent Grid Sampling** and **Monte Carlo Simulation**. Perfect for exploring fractal-like boundaries and understanding computational geometry!

## 🌟 Features

### Core Algorithms
- **Intelligent Grid Method**: Configurable resolution with partial cell coverage estimation
- **Monte Carlo Simulation**: Random point sampling with statistical convergence
- **Ray Casting**: Robust point-in-polygon testing for any closed curve
- **Analytical Verification**: Shoelace formula for exact area comparison

### Visual Analytics
- **Polygon Visualization**: Clean plotting of the piecewise linear curve
- **Grid Method Visualization**: Color-coded squares showing contribution levels
- **Monte Carlo Visualization**: "Dartboard" view of random sampling points
- **Fractal Analysis**: Multi-resolution grid analysis for complex curves

### Performance Features
- Comprehensive error analysis and timing benchmarks
- Configurable sampling parameters for accuracy vs. speed trade-offs
- Multiple test cases from simple triangles to complex star shapes

## 🚀 Quick Start

### Prerequisites
```bash
pip install numpy matplotlib
```

### Basic Usage
```python
from curve_area_calculator import CurveAreaCalculator

# Define your polygon vertices (automatically closed)
triangle = [(0, 0), (4, 0), (2, 3)]
calc = CurveAreaCalculator(triangle)

# Get area estimates using both methods
calc.compare_methods()

# Create beautiful visualizations
calc.visualize_all_methods()
```

## 📊 Method Details

### 1. Intelligent Grid Method

The grid method divides the bounding box into a configurable grid and intelligently estimates partial cell coverage:

```python
result = calc.grid_method(
    grid_resolution=100,     # 100×100 grid cells
    samples_per_cell=16      # 16 sample points per cell
)
```

**How it works:**
- Creates a uniform grid over the curve's bounding box
- For each cell, samples multiple points to estimate coverage fraction
- Accounts for partial coverage where the boundary cuts through cells
- Sums fractional contributions: `total_area = Σ(cell_fraction × cell_area)`

**Perfect for:** Complex, fractal-like curves where boundary detail matters

### 2. Monte Carlo Simulation

Random sampling approach that converges statistically to the true area:

```python
result = calc.monte_carlo_method(n_samples=100000)
```

**How it works:**
- Generates random points within the curve's bounding box
- Uses ray casting to test if each point is inside the polygon
- Estimates area: `area = (points_inside / total_points) × bounding_box_area`

**Perfect for:** Quick estimates and understanding probabilistic methods

### 3. Ray Casting Algorithm

Core point-in-polygon test used by both methods:

```python
is_inside = calc.point_in_polygon_ray_casting(x, y)
```

**Algorithm:** Casts a ray from the test point to infinity and counts edge intersections. Odd count = inside, even count = outside.

## 🎨 Visualizations

### Basic Polygon Plot
```python
calc.plot_curve()
```
Shows the piecewise linear curve with vertices highlighted and area filled.

### Grid Method Visualization
```python
calc.plot_grid_method(grid_resolution=80, samples_per_cell=16)
```
**Color coding:**
- **No color**: Cells completely outside
- **Light green**: Partial coverage (boundary cuts through cell)
- **Dark green**: Full coverage (cell completely inside)

Perfect for understanding how grid resolution affects fractal boundaries!

### Monte Carlo Visualization  
```python
calc.plot_monte_carlo_method(n_samples=5000, point_size=2.0)
```
**Point colors:**
- **🔴 Red points**: Random samples outside the polygon
- **🟢 Green points**: Random samples inside the polygon

Watch the "dartboard" pattern emerge as samples accumulate!

### All Methods Combined
```python
calc.visualize_all_methods(
    grid_resolution=50,
    mc_samples=3000,
    mc_point_size=2.0
)
```

## 🔬 Advanced Usage

### Fractal Resolution Analysis

Explore how grid resolution reveals detail in complex curves:

```python
star_shape = [(4*cos(2πi/10), 4*sin(2πi/10)) if i%2==0 
              else (2*cos(2πi/10), 2*sin(2πi/10)) 
              for i in range(10)]

calc = CurveAreaCalculator(star_shape)

# Test multiple resolutions
for resolution in [50, 100, 200, 400]:
    result = calc.grid_method(grid_resolution=resolution)
    print(f"Resolution {resolution}×{resolution}: Area = {result['area']:.4f}")
```

### Performance Benchmarking

Compare method efficiency:

```python
# Quick but less accurate
quick_result = calc.monte_carlo_method(n_samples=10000)

# Slower but more accurate  
precise_result = calc.grid_method(grid_resolution=200, samples_per_cell=25)

# Analytical truth
true_area = calc.analytical_area()
```

### Custom Polygons

```python
# Regular pentagon
import math
pentagon = [(3*math.cos(2*math.pi*i/5), 3*math.sin(2*math.pi*i/5)) 
            for i in range(5)]

# Complex star shape
star = []
for i in range(10):
    radius = 4 if i % 2 == 0 else 2
    angle = 2 * math.pi * i / 10
    star.append((radius * math.cos(angle), radius * math.sin(angle)))

# Irregular polygon
irregular = [(0,0), (3,1), (4,4), (1,5), (-1,3), (-2,1)]
```

## 📈 Understanding Results

### Method Comparison Output
```
Analytical area (Shoelace formula): 15.500000

Grid Method Results:
  Estimated area: 15.485600
  Error: 0.093%
  Grid resolution: 100×100
  Computation time: 0.0234 seconds

Monte Carlo Method Results:
  Estimated area: 15.478400
  Error: 0.139%
  Sample points: 100,000
  Computation time: 0.1876 seconds
```

### Key Metrics
- **Area**: The estimated enclosed area
- **Error**: Percentage difference from analytical solution
- **Resolution/Samples**: Algorithm parameters used
- **Computation time**: Performance measurement

## 🧮 Mathematical Background

### Shoelace Formula (Analytical)
For a polygon with vertices (x₀,y₀), (x₁,y₁), ..., (xₙ₋₁,yₙ₋₁):

```
Area = ½|Σᵢ(xᵢyᵢ₊₁ - xᵢ₊₁yᵢ)|
```

### Grid Method Convergence
As grid resolution increases: `Error ∝ 1/√(resolution)`

### Monte Carlo Convergence  
Standard error decreases as: `Error ∝ 1/√(n_samples)`

## 🎯 Use Cases

### Educational
- **Computational Geometry**: Demonstrate numerical integration
- **Probability Theory**: Visualize Monte Carlo convergence
- **Fractal Mathematics**: Explore resolution-dependent measurements

### Research Applications
- **Geographic Information Systems**: Area calculation for complex regions
- **Computer Graphics**: Polygon area computation
- **Numerical Analysis**: Method comparison and validation

### Fun Projects
- **Coastline Paradox**: Measure fractal coastlines at different scales
- **Art and Design**: Generate interesting visual patterns
- **Game Development**: Collision detection and area calculations

## 🛠️ Code Structure

```
CurveAreaCalculator/
├── __init__(coordinates)           # Initialize with polygon vertices
├── point_in_polygon_ray_casting()  # Core geometric test
├── grid_method()                   # Intelligent grid sampling
├── monte_carlo_method()            # Random point sampling  
├── analytical_area()               # Exact Shoelace calculation
├── compare_methods()               # Comprehensive comparison
├── plot_curve()                    # Basic visualization
├── plot_grid_method()              # Grid color visualization
├── plot_monte_carlo_method()       # Dartboard visualization
└── visualize_all_methods()         # Complete visual suite
```

## 🎨 Customization Options

### Grid Method Parameters
```python
result = calc.grid_method(
    grid_resolution=200,        # Finer grid = more accuracy
    samples_per_cell=25         # More samples = better partial estimation
)
```

### Monte Carlo Parameters
```python
result = calc.monte_carlo_method(
    n_samples=1000000          # More samples = better convergence
)
```

### Visualization Parameters
```python
# Grid visualization
calc.plot_grid_method(
    grid_resolution=100,        # Grid fineness
    samples_per_cell=16         # Accuracy of partial coverage
)

# Monte Carlo visualization  
calc.plot_monte_carlo_method(
    n_samples=10000,           # Number of "darts"
    point_size=1.5             # Visual point size
)
```

## 🔍 Tips for Best Results

### For Grid Method
- **Simple polygons**: Lower resolution (50×50) is sufficient
- **Complex/fractal curves**: Higher resolution (200×200+) reveals detail
- **Partial coverage**: Use 16+ samples per cell for accuracy

### For Monte Carlo
- **Quick estimates**: 10,000-50,000 samples
- **High accuracy**: 100,000+ samples  
- **Statistical significance**: Run multiple times and average

### For Visualization
- **Presentations**: Use moderate sample sizes (3,000-5,000 points)
- **Analysis**: Higher resolutions show method behavior clearly
- **Performance**: Lower settings for interactive exploration

## 🚀 Running the Examples

The code includes three built-in examples that automatically run:

1. **Simple Triangle**: Validates basic functionality
2. **Regular Pentagon**: Tests with curved boundaries
3. **Star Shape**: Demonstrates fractal-like behavior

Simply run the script to see all examples with full analysis and visualizations!

## 🎓 Learning Objectives

After using this code, you'll understand:
- How numerical integration approximates continuous problems
- The trade-offs between deterministic and probabilistic methods
- How resolution affects accuracy in computational geometry
- The fascinating relationship between fractals and measurement
- Practical implementation of fundamental geometric algorithms

---

**Happy polygon area calculating!** 🎉

*Feel free to experiment with your own curves and discover the beautiful patterns that emerge at different scales!*