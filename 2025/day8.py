from typing import Any
import math


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x

        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        return True

    def get_component_sizes(self):
        components = {}
        for i in range(len(self.parent)):
            root = self.find(i)
            if root not in components:
                components[root] = 0
            components[root] += 1
        return list(components.values())


def solve_part_1(input_data: str) -> Any:
    """Solve part 1 of the challenge."""
    lines = input_data.strip().split('\n')

    boxes = []
    for line in lines:
        x, y, z = map(int, line.split(','))
        boxes.append((x, y, z))

    n = len(boxes)

    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1, z1 = boxes[i]
            x2, y2, z2 = boxes[j]
            dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
            distances.append((dist, i, j))

    distances.sort()

    uf = UnionFind(n)

    for idx, (dist, i, j) in enumerate(distances):
        if idx >= 1000:
            break
        uf.union(i, j)

    circuit_sizes = uf.get_component_sizes()
    circuit_sizes.sort(reverse=True)

    result = circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]
    return result


def solve_part_2(input_data: str) -> Any:
    """Solve part 2 of the challenge."""
    lines = input_data.strip().split('\n')

    boxes = []
    for line in lines:
        x, y, z = map(int, line.split(','))
        boxes.append((x, y, z))

    n = len(boxes)

    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1, z1 = boxes[i]
            x2, y2, z2 = boxes[j]
            dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
            distances.append((dist, i, j))

    distances.sort()

    uf = UnionFind(n)

    for dist, i, j in distances:
        if uf.union(i, j):
            num_circuits = len(set(uf.find(k) for k in range(n)))
            if num_circuits == 1:
                x1, y1, z1 = boxes[i]
                x2, y2, z2 = boxes[j]
                return x1 * x2

    return None


def create_animation(input_data: str):
    """Create a 3D matplotlib animation visualizing the Union-Find algorithm."""
    try:
        import matplotlib.pyplot as plt
        import matplotlib.animation as animation
        from mpl_toolkits.mplot3d import Axes3D
        import numpy as np
        from collections import defaultdict
    except ImportError as e:
        print(f"❌ Required library not available for animation: {e}")
        print("📋 Please install required packages:")
        print("   pip install matplotlib numpy")
        return None

    lines = input_data.strip().split('\n')
    boxes = []
    for line in lines:
        x, y, z = map(int, line.split(','))
        boxes.append((x, y, z))

    n = len(boxes)

    # Limit to reasonable number for visualization
    max_boxes = 50 if len(boxes) > 50 else len(boxes)
    if n > max_boxes:
        boxes = boxes[:max_boxes]
        n = max_boxes
        print(f"📊 Showing first {max_boxes} boxes for visualization clarity")

    # Normalize coordinates for better visualization
    if boxes:
        xs, ys, zs = zip(*boxes)
        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)
        z_min, z_max = min(zs), max(zs)

        # Normalize to 0-100 range
        normalized_boxes = []
        for x, y, z in boxes:
            norm_x = (x - x_min) / (x_max - x_min) * 100 if x_max != x_min else 50
            norm_y = (y - y_min) / (y_max - y_min) * 100 if y_max != y_min else 50
            norm_z = (z - z_min) / (z_max - z_min) * 100 if z_max != z_min else 50
            normalized_boxes.append((norm_x, norm_y, norm_z))
        boxes = normalized_boxes

    # Calculate distances
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1, z1 = boxes[i]
            x2, y2, z2 = boxes[j]
            dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
            distances.append((dist, i, j))

    distances.sort()

    # Limit connections for part 1 visualization
    max_connections = min(1000, len(distances))
    distances = distances[:max_connections]

    # Set up the figure and 3D axis
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Extract coordinates
    xs, ys, zs = zip(*boxes)

    # Initialize Union-Find
    uf = UnionFind(n)

    # Animation data
    connection_frames = []
    current_connections = []
    component_color_map = {}  # Stable color mapping for components
    next_color_index = 0

    # Store original distances length for progress calculation
    total_distances = len(distances)

    # Create frames for animation
    step_size = max(1, len(distances) // 50)  # Create ~50 frames

    for i in range(0, len(distances), step_size):
        # Process batch of connections
        batch_end = min(i + step_size, len(distances))
        new_connections_in_batch = []

        for j in range(i, batch_end):
            dist, box_i, box_j = distances[j]

            # Check if this creates a new connection
            root_i = uf.find(box_i)
            root_j = uf.find(box_j)

            if root_i != root_j:
                uf.union(box_i, box_j)
                current_connections.append((box_i, box_j))
                new_connections_in_batch.append((box_i, box_j))

        # Get current component information with stable coloring
        components = defaultdict(list)
        for k in range(n):
            root = uf.find(k)
            components[root].append(k)

        # Assign stable colors to new components
        for root in components:
            if root not in component_color_map:
                component_color_map[root] = next_color_index
                next_color_index += 1

        # Store frame data
        frame_data = {
            'connections': current_connections.copy(),
            'new_connections': new_connections_in_batch,
            'components': dict(components),
            'component_colors': component_color_map.copy(),
            'step': i // step_size + 1,
            'total_steps': (len(distances) + step_size - 1) // step_size,
            'progress': batch_end / total_distances  # Use original total for correct progress
        }
        connection_frames.append(frame_data)

        # Check if all connected (early termination for part 2)
        if len(components) == 1:
            # Add final frame with 100% progress
            frame_data['progress'] = 1.0
            break

    # Animation function
    def animate_frame(frame_num):
        ax.clear()

        if frame_num >= len(connection_frames):
            frame_num = len(connection_frames) - 1

        frame_data = connection_frames[frame_num]
        connections = frame_data['connections']
        new_connections = frame_data['new_connections']
        components = frame_data['components']
        component_colors = frame_data['component_colors']

        # Color palette for components - use a stable colormap
        max_colors = max(component_colors.values()) + 1 if component_colors else 1
        colors = plt.cm.Set3(np.linspace(0, 1, max_colors))

        # Plot boxes colored by component using stable color mapping
        for root, members in components.items():
            color_idx = component_colors[root]
            color = colors[color_idx % len(colors)]
            comp_xs = [xs[i] for i in members]
            comp_ys = [ys[i] for i in members]
            comp_zs = [zs[i] for i in members]

            ax.scatter(comp_xs, comp_ys, comp_zs,
                      c=[color], s=100, alpha=0.8,
                      label=f'Component {color_idx + 1} ({len(members)} boxes)')

        # Draw all connections in light gray
        for box_i, box_j in connections:
            if (box_i, box_j) not in new_connections:  # Don't draw new ones twice
                ax.plot([xs[box_i], xs[box_j]],
                       [ys[box_i], ys[box_j]],
                       [zs[box_i], zs[box_j]],
                       'lightgray', alpha=0.3, linewidth=1)

        # Highlight new connections in red
        for box_i, box_j in new_connections:
            ax.plot([xs[box_i], xs[box_j]],
                   [ys[box_i], ys[box_j]],
                   [zs[box_i], zs[box_j]],
                   'red', alpha=0.8, linewidth=3)

        # Set labels and title
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_zlabel('Z Coordinate')

        step = frame_data['step']
        total_steps = frame_data['total_steps']
        progress = frame_data['progress']

        title = f"🔗 Union-Find Circuit Connection (Step {step}/{total_steps})\n"
        title += f"Progress: {progress*100:.1f}% | Components: {len(components)} | "
        title += f"Connections: {len(connections)}"

        # Check for part results
        if len(components) == 1:
            title += " | 🎉 ALL CONNECTED!"
        elif len(connections) >= 1000:
            component_sizes = sorted([len(members) for members in components.values()], reverse=True)
            if len(component_sizes) >= 3:
                result = component_sizes[0] * component_sizes[1] * component_sizes[2]
                title += f" | Part 1: {result}"

        ax.set_title(title, fontsize=10)

        # Set consistent axis limits
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.set_zlim(0, 100)

        # Add legend if not too many components
        if len(components) <= 8:
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

        return ax.artists

    # Create animation
    print("🎬 Creating 3D animation...")
    print(f"📊 Visualizing {n} boxes with {len(distances)} connections")
    print(f"🎞️  Animation will have {len(connection_frames)} frames")

    anim = animation.FuncAnimation(fig, animate_frame, frames=len(connection_frames),
                                  interval=500, blit=False, repeat=True)

    # Create a custom Animation object to integrate with our system
    from core.animation import Animation as CustomAnimation

    class MatplotlibAnimation(CustomAnimation):
        def __init__(self, title, matplotlib_anim, figure):
            super().__init__(title, 1.0)
            self.matplotlib_anim = matplotlib_anim
            self.figure = figure

        def play(self, loop=False, export_gif=None):
            """Play the matplotlib animation."""
            print("🎮 Controls:")
            print("   - Close window to stop animation")
            print("   - Animation will loop automatically")

            if export_gif:
                print(f"💾 Exporting GIF to {export_gif}...")
                try:
                    # Save as GIF
                    writer = animation.PillowWriter(fps=2)
                    self.matplotlib_anim.save(export_gif, writer=writer)
                    print(f"✅ 3D animation exported to {export_gif}")
                except Exception as e:
                    print(f"❌ Failed to export GIF: {e}")
                    print("   Make sure Pillow is installed: pip install Pillow")

            # Show the plot
            try:
                plt.tight_layout()
                plt.show()
            except KeyboardInterrupt:
                print("\n🛑 Animation stopped by user")
            except Exception as e:
                print(f"\n❌ Animation error: {e}")

    return MatplotlibAnimation("🔗 3D Union-Find Circuit Visualization", anim, fig)


