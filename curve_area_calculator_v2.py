import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
import random
import time

class CurveAreaCalculator:
    def __init__(self, coordinates: List[Tuple[float, float]]):
        """
        Initialize with a list of (x, y) coordinates defining a piecewise linear curve.
        The curve is automatically closed (last point connects to first).
        """
        self.coordinates = coordinates
        self.n_points = len(coordinates)
        
        # Get bounding box
        x_coords = [p[0] for p in coordinates]
        y_coords = [p[1] for p in coordinates]
        
        self.min_x = min(x_coords)
        self.max_x = max(x_coords)
        self.min_y = min(y_coords)
        self.max_y = max(y_coords)
        
        self.bbox_width = self.max_x - self.min_x
        self.bbox_height = self.max_y - self.min_y
        self.bbox_area = self.bbox_width * self.bbox_height
    
    def point_in_polygon_ray_casting(self, x: float, y: float) -> bool:
        """
        Determine if point (x, y) is inside the polygon using ray casting algorithm.
        Casts a ray from the point to the right and counts intersections.
        """
        inside = False
        j = self.n_points - 1
        
        for i in range(self.n_points):
            xi, yi = self.coordinates[i]
            xj, yj = self.coordinates[j]
            
            if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
                inside = not inside
            j = i
            
        return inside
    
    def grid_method(self, grid_resolution: int = 100, samples_per_cell: int = 16) -> dict:
        """
        Approximate area using intelligent grid sampling.
        
        Args:
            grid_resolution: Number of grid cells along each axis
            samples_per_cell: Number of sample points within each cell for partial coverage estimation
            
        Returns:
            dict with area estimate and method details
        """
        start_time = time.time()
        
        cell_width = self.bbox_width / grid_resolution
        cell_height = self.bbox_height / grid_resolution
        cell_area = cell_width * cell_height
        
        total_area = 0.0
        cells_processed = 0
        
        # Create sample points within a unit cell (0,0) to (1,1)
        samples_per_side = int(np.sqrt(samples_per_cell))
        sample_coords = []
        for i in range(samples_per_side):
            for j in range(samples_per_side):
                # Add small random offset to avoid systematic bias
                offset_x = random.uniform(-0.1, 0.1) / samples_per_side
                offset_y = random.uniform(-0.1, 0.1) / samples_per_side
                sample_x = (i + 0.5) / samples_per_side + offset_x
                sample_y = (j + 0.5) / samples_per_side + offset_y
                sample_coords.append((sample_x, sample_y))
        
        for i in range(grid_resolution):
            for j in range(grid_resolution):
                # Cell boundaries
                cell_left = self.min_x + i * cell_width
                cell_bottom = self.min_y + j * cell_height
                
                # Sample points within this cell
                inside_count = 0
                for sx, sy in sample_coords:
                    test_x = cell_left + sx * cell_width
                    test_y = cell_bottom + sy * cell_height
                    
                    if self.point_in_polygon_ray_casting(test_x, test_y):
                        inside_count += 1
                
                # Estimate fraction of cell that's inside the curve
                cell_fraction = inside_count / len(sample_coords)
                total_area += cell_fraction * cell_area
                cells_processed += 1
        
        computation_time = time.time() - start_time
        
        return {
            'area': total_area,
            'method': 'Intelligent Grid Sampling',
            'grid_resolution': grid_resolution,
            'samples_per_cell': len(sample_coords),
            'total_cells': cells_processed,
            'computation_time': computation_time
        }
    
    def monte_carlo_method(self, n_samples: int = 100000) -> dict:
        """
        Approximate area using Monte Carlo simulation.
        
        Args:
            n_samples: Number of random sample points to generate
            
        Returns:
            dict with area estimate and method details
        """
        start_time = time.time()
        
        inside_count = 0
        
        for _ in range(n_samples):
            # Generate random point in bounding box
            x = random.uniform(self.min_x, self.max_x)
            y = random.uniform(self.min_y, self.max_y)
            
            if self.point_in_polygon_ray_casting(x, y):
                inside_count += 1
        
        # Area = (fraction inside) * (bounding box area)
        fraction_inside = inside_count / n_samples
        estimated_area = fraction_inside * self.bbox_area
        
        computation_time = time.time() - start_time
        
        return {
            'area': estimated_area,
            'method': 'Monte Carlo Simulation',
            'n_samples': n_samples,
            'inside_count': inside_count,
            'fraction_inside': fraction_inside,
            'bounding_box_area': self.bbox_area,
            'computation_time': computation_time
        }
    
    def analytical_area(self) -> float:
        """
        Calculate exact area using the Shoelace formula (for comparison).
        """
        area = 0.0
        j = self.n_points - 1
        
        for i in range(self.n_points):
            area += (self.coordinates[j][0] + self.coordinates[i][0]) * (self.coordinates[j][1] - self.coordinates[i][1])
            j = i
        
        return abs(area) / 2.0
    
    def compare_methods(self, grid_resolution: int = 100, samples_per_cell: int = 16, 
                       monte_carlo_samples: int = 100000) -> None:
        """
        Compare both methods and print results.
        """
        print(f"Curve with {self.n_points} vertices")
        print(f"Bounding box: [{self.min_x:.2f}, {self.max_x:.2f}] × [{self.min_y:.2f}, {self.max_y:.2f}]")
        print(f"Bounding box area: {self.bbox_area:.4f}")
        print("-" * 60)
        
        # Analytical solution
        true_area = self.analytical_area()
        print(f"Analytical area (Shoelace formula): {true_area:.6f}")
        print("-" * 60)
        
        # Grid method
        grid_result = self.grid_method(grid_resolution, samples_per_cell)
        grid_error = abs(grid_result['area'] - true_area) / true_area * 100
        
        print(f"Grid Method Results:")
        print(f"  Estimated area: {grid_result['area']:.6f}")
        print(f"  Error: {grid_error:.3f}%")
        print(f"  Grid resolution: {grid_result['grid_resolution']}×{grid_result['grid_resolution']}")
        print(f"  Samples per cell: {grid_result['samples_per_cell']}")
        print(f"  Total cells: {grid_result['total_cells']:,}")
        print(f"  Computation time: {grid_result['computation_time']:.4f} seconds")
        print("-" * 60)
        
        # Monte Carlo method
        mc_result = self.monte_carlo_method(monte_carlo_samples)
        mc_error = abs(mc_result['area'] - true_area) / true_area * 100
        
        print(f"Monte Carlo Method Results:")
        print(f"  Estimated area: {mc_result['area']:.6f}")
        print(f"  Error: {mc_error:.3f}%")
        print(f"  Sample points: {mc_result['n_samples']:,}")
        print(f"  Points inside: {mc_result['inside_count']:,}")
        print(f"  Fraction inside: {mc_result['fraction_inside']:.6f}")
        print(f"  Computation time: {mc_result['computation_time']:.4f} seconds")
        print("-" * 60)
    
    def plot_curve(self, show_grid: bool = False, grid_resolution: int = 50):
        """
        Visualize the curve and optionally overlay a grid.
        """
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        
        # Plot the curve
        x_coords = [p[0] for p in self.coordinates] + [self.coordinates[0][0]]
        y_coords = [p[1] for p in self.coordinates] + [self.coordinates[0][1]]
        
        ax.plot(x_coords, y_coords, 'b-', linewidth=2, label='Piecewise Linear Curve')
        ax.fill(x_coords, y_coords, alpha=0.3, color='lightblue', label='Enclosed Area')
        ax.scatter([p[0] for p in self.coordinates], [p[1] for p in self.coordinates], 
                  color='red', s=50, zorder=5, label='Vertices')
        
        # Optionally show grid
        if show_grid:
            cell_width = self.bbox_width / grid_resolution
            cell_height = self.bbox_height / grid_resolution
            
            # Vertical lines
            for i in range(grid_resolution + 1):
                x = self.min_x + i * cell_width
                ax.axvline(x, color='gray', alpha=0.3, linewidth=0.5)
            
            # Horizontal lines
            for j in range(grid_resolution + 1):
                y = self.min_y + j * cell_height
                ax.axhline(y, color='gray', alpha=0.3, linewidth=0.5)
        
        ax.set_xlim(self.min_x - 0.1 * self.bbox_width, self.max_x + 0.1 * self.bbox_width)
        ax.set_ylim(self.min_y - 0.1 * self.bbox_height, self.max_y + 0.1 * self.bbox_height)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Piecewise Linear Curve Area Approximation')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
        
        plt.tight_layout()
        plt.show()
    
    def plot_grid_method(self, grid_resolution: int = 50, samples_per_cell: int = 16):
        """
        Visualize the grid method showing colored squares based on their contribution.
        """
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        
        cell_width = self.bbox_width / grid_resolution
        cell_height = self.bbox_height / grid_resolution
        
        # Create sample points within a unit cell
        samples_per_side = int(np.sqrt(samples_per_cell))
        sample_coords = []
        for i in range(samples_per_side):
            for j in range(samples_per_side):
                sample_x = (i + 0.5) / samples_per_side
                sample_y = (j + 0.5) / samples_per_side
                sample_coords.append((sample_x, sample_y))
        
        # Color each cell based on coverage
        for i in range(grid_resolution):
            for j in range(grid_resolution):
                cell_left = self.min_x + i * cell_width
                cell_bottom = self.min_y + j * cell_height
                cell_right = cell_left + cell_width
                cell_top = cell_bottom + cell_height
                
                # Test sample points within this cell
                inside_count = 0
                for sx, sy in sample_coords:
                    test_x = cell_left + sx * cell_width
                    test_y = cell_bottom + sy * cell_height
                    
                    if self.point_in_polygon_ray_casting(test_x, test_y):
                        inside_count += 1
                
                # Calculate coverage fraction
                coverage = inside_count / len(sample_coords)
                
                # Color the cell based on coverage
                if coverage > 0:
                    # Color from light green (partial) to dark green (full coverage)
                    color = plt.cm.Greens(0.3 + 0.7 * coverage)
                    rect = plt.Rectangle((cell_left, cell_bottom), cell_width, cell_height,
                                       facecolor=color, edgecolor='black', linewidth=0.1, alpha=0.8)
                    ax.add_patch(rect)
        
        # Plot the original curve on top
        x_coords = [p[0] for p in self.coordinates] + [self.coordinates[0][0]]
        y_coords = [p[1] for p in self.coordinates] + [self.coordinates[0][1]]
        
        ax.plot(x_coords, y_coords, 'red', linewidth=3, label='Polygon Boundary', zorder=10)
        ax.scatter([p[0] for p in self.coordinates], [p[1] for p in self.coordinates], 
                  color='darkred', s=60, zorder=11, label='Vertices', edgecolor='white')
        
        # Create custom legend for grid colors
        from matplotlib.patches import Patch
        legend_elements = [
            ax.lines[0],  # Polygon boundary
            ax.collections[0] if ax.collections else Patch(color='darkred', label='Vertices'),  # Vertices
            Patch(facecolor=plt.cm.Greens(0.4), label='Partial Coverage'),
            Patch(facecolor=plt.cm.Greens(1.0), label='Full Coverage')
        ]
        
        ax.set_xlim(self.min_x, self.max_x)
        ax.set_ylim(self.min_y, self.max_y)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(f'Grid Method Visualization ({grid_resolution}×{grid_resolution} cells)')
        ax.legend(handles=legend_elements)
        ax.set_aspect('equal')
        
        plt.tight_layout()
        plt.show()
    
    def plot_monte_carlo_method(self, n_samples: int = 5000, point_size: float = 1.0):
        """
        Visualize Monte Carlo method showing 'darts thrown' - points inside vs outside.
        """
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        
        # Generate random points and classify them
        inside_points = []
        outside_points = []
        
        for _ in range(n_samples):
            x = random.uniform(self.min_x, self.max_x)
            y = random.uniform(self.min_y, self.max_y)
            
            if self.point_in_polygon_ray_casting(x, y):
                inside_points.append((x, y))
            else:
                outside_points.append((x, y))
        
        # Plot the outside points first (so inside points are on top)
        if outside_points:
            outside_x, outside_y = zip(*outside_points)
            ax.scatter(outside_x, outside_y, c='red', s=point_size, alpha=0.6, 
                      label=f'Outside ({len(outside_points)} points)')
        
        # Plot the inside points
        if inside_points:
            inside_x, inside_y = zip(*inside_points)
            ax.scatter(inside_x, inside_y, c='green', s=point_size, alpha=0.7, 
                      label=f'Inside ({len(inside_points)} points)')
        
        # Plot the polygon boundary
        x_coords = [p[0] for p in self.coordinates] + [self.coordinates[0][0]]
        y_coords = [p[1] for p in self.coordinates] + [self.coordinates[0][1]]
        
        ax.fill(x_coords, y_coords, alpha=0.2, color='lightblue', zorder=5)
        ax.plot(x_coords, y_coords, 'blue', linewidth=3, label='Polygon Boundary', zorder=10)
        ax.scatter([p[0] for p in self.coordinates], [p[1] for p in self.coordinates], 
                  color='darkblue', s=80, zorder=11, label='Vertices', edgecolor='white')
        
        # Draw bounding box
        bbox_rect = plt.Rectangle((self.min_x, self.min_y), self.bbox_width, self.bbox_height,
                                 fill=False, edgecolor='black', linewidth=2, linestyle='--', 
                                 label='Bounding Box')
        ax.add_patch(bbox_rect)
        
        # Calculate and display statistics
        fraction_inside = len(inside_points) / n_samples if n_samples > 0 else 0
        estimated_area = fraction_inside * self.bbox_area
        
        ax.set_xlim(self.min_x - 0.05 * self.bbox_width, self.max_x + 0.05 * self.bbox_width)
        ax.set_ylim(self.min_y - 0.05 * self.bbox_height, self.max_y + 0.05 * self.bbox_height)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(f'Monte Carlo Method: {n_samples} Random Points\n'
                    f'Estimated Area: {estimated_area:.4f} ({fraction_inside:.3%} inside)')
        ax.legend()
        ax.set_aspect('equal')
        
        plt.tight_layout()
        plt.show()
    
    def visualize_all_methods(self, grid_resolution: int = 50, samples_per_cell: int = 16, 
                             mc_samples: int = 3000, mc_point_size: float = 2.0):
        """
        Create all three visualizations in sequence.
        """
        print("Generating visualizations...")
        
        print("1. Basic polygon plot")
        self.plot_curve()
        
        print("2. Grid method visualization")
        self.plot_grid_method(grid_resolution, samples_per_cell)
        
        print("3. Monte Carlo method visualization") 
        self.plot_monte_carlo_method(mc_samples, mc_point_size)


# Example usage and test cases
if __name__ == "__main__":
    
    # Example 1: Simple triangle
    print("=" * 80)
    print("EXAMPLE 1: Simple Triangle")
    print("=" * 80)
    triangle = [(0, 0), (4, 0), (2, 3)]
    calc1 = CurveAreaCalculator(triangle)
    calc1.compare_methods(grid_resolution=50, monte_carlo_samples=50000)
    
    # Example 2: More complex polygon (pentagon)
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Regular Pentagon")
    print("=" * 80)
    
    # Generate regular pentagon
    import math
    pentagon = []
    for i in range(5):
        angle = 2 * math.pi * i / 5
        x = 3 * math.cos(angle)
        y = 3 * math.sin(angle)
        pentagon.append((x, y))
    
    calc2 = CurveAreaCalculator(pentagon)
    calc2.compare_methods(grid_resolution=100, samples_per_cell=25, monte_carlo_samples=100000)
    
    # Example 3: Star shape (more fractal-like)
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Star Shape (Fractal-like)")
    print("=" * 80)
    
    star = []
    for i in range(10):  # 5-pointed star with 10 vertices
        angle = 2 * math.pi * i / 10
        if i % 2 == 0:
            radius = 4  # Outer points
        else:
            radius = 2  # Inner points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        star.append((x, y))
    
    calc3 = CurveAreaCalculator(star)
    calc3.compare_methods(grid_resolution=150, samples_per_cell=25, monte_carlo_samples=150000)
    
    print("\n" + "=" * 80)
    print("FRACTAL RESOLUTION ANALYSIS")
    print("=" * 80)
    print("Testing star shape with different grid resolutions:")
    
    
    print("\n" + "=" * 80)
    print("VISUALIZATION EXAMPLES")
    print("=" * 80)
    
    # Show visualizations for the star shape (most interesting)
    print("Creating visualizations for the star shape...")
    calc3.visualize_all_methods(grid_resolution=80, mc_samples=5000, mc_point_size=3.0)
    
    print("\nTo see more visualizations, you can call:")
    print("calc1.plot_curve()                    # Basic polygon plot") 
    print("calc1.plot_grid_method(50, 16)        # Grid visualization")
    print("calc1.plot_monte_carlo_method(3000)   # Monte Carlo darts")
    print("calc1.visualize_all_methods()         # All three plots")
