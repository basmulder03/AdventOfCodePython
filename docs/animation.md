# Animation System Documentation

## Overview

The Advent of Code CLI now supports animated visualizations for solutions that implement them. This allows you to see algorithms in action and export them as GIF files for sharing or documentation.

## Usage

### Running Animations

There are two ways to run animations:

1. **Using the regular run command with --animation flag:**
   ```bash
   python main.py 2025 8 --animation
   python main.py 2025 8 --sample --animation
   python main.py 2025 8 --animation --export-gif my_animation.gif
   ```

2. **Using the dedicated animation subcommand:**
   ```bash
   python main.py animation 2025 8
   python main.py animation 2025 8 --sample
   python main.py animation 2025 8 --export-gif my_animation.gif --speed 2.0
   ```

### Command Line Options

#### For regular run command:
- `--animation`: Enable animation if available for the solution
- `--export-gif FILENAME`: Export animation as GIF (requires --animation)

#### For animation subcommand:
- `--sample`, `-s`: Use sample input instead of actual input
- `--sample-input TEXT`: Provide sample input directly as a string
- `--export-gif FILENAME`: Export animation as GIF file
- `--speed MULTIPLIER`: Animation speed multiplier (default: 1.0)
- `--no-tracking`: Disable run tracking

### Speed Control

You can control animation speed with the `--speed` parameter:
- `--speed 0.5`: Half speed (slower)
- `--speed 1.0`: Normal speed (default)  
- `--speed 2.0`: Double speed (faster)

### GIF Export

Animations can be exported as GIF files using the `--export-gif` option:

```bash
# Export with default settings
python main.py animation 2025 8 --sample --export-gif sample.gif

# Export with custom speed
python main.py animation 2025 8 --sample --export-gif fast.gif --speed 3.0
```

**Requirements:**
- **For 3D visualizations:** matplotlib library (automatically installed with `pip install -r requirements.txt`)
- **For GIF export:** Pillow library (automatically installed with `pip install -r requirements.txt`)
- **System requirements:** Display capability for matplotlib windows
- Sufficient disk space for the generated images

**Fallback behavior:**
- If Pillow is not available, frames are exported as numbered text files
- If GIF export fails, frames are saved as text files with naming pattern: `filename_frame_XXXX.txt`

## Available Animations

Currently implemented animations:

### 2025 Day 8: Union-Find Circuit Connection (3D Visualization)
- **Visualizes:** The Union-Find algorithm connecting boxes in 3D space using matplotlib
- **Shows:** 3D scatter plot with animated connections forming between boxes
- **Features:** 
  - Interactive 3D plot with rotation and zoom capabilities
  - Color-coded components that update as connections form
  - Real-time connection animation with highlighted new connections
  - Progress tracking in plot title
  - Automatic normalization of coordinates for optimal viewing
  - GIF export of the 3D animation

#### Example Usage:
```bash
# Interactive 3D animation with sample data
python main.py animation 2025 8 --sample

# Export 3D animation as GIF
python main.py animation 2025 8 --sample --export-gif 3d_union_find.gif

# Full dataset visualization (automatically limits to 50 boxes for performance)
python main.py animation 2025 8 --export-gif full_visualization.gif
```

**3D Animation Features:**
- **Interactive Controls**: Mouse to rotate, scroll to zoom, right-click to pan
- **Real-time Updates**: Components change colors as connections form
- **Connection Highlighting**: New connections appear in red before becoming permanent
- **Automatic Scaling**: Coordinates normalized to 0-100 range for optimal viewing
- **Performance Optimization**: Limited to 50 boxes maximum for smooth animation

## Implementing Animations for Solutions

To add animation support to a solution, add a `create_animation(input_data: str)` function to your solution file:

```python
def create_animation(input_data: str):
    \"\"\"Create an animation for this solution.\"\"\"
    from core.animation import Animation
    
    # Create animation object
    animation = Animation("My Algorithm Visualization", 1.0)
    
    # Add frames
    animation.add_frame("Initial state...", 1.0)
    animation.add_frame("Processing step 1...", 0.5)
    animation.add_frame("Final result!", 2.0)
    
    return animation
```

### Animation Framework API

#### Animation Class
```python
class Animation:
    def __init__(self, title: str = "", speed_multiplier: float = 1.0)
    def add_frame(self, content: str, duration: float = 0.1)
    def play(self, loop: bool = False, export_gif: Optional[str] = None)
```

#### AnimationFrame Class
```python
class AnimationFrame:
    def __init__(self, content: str, duration: float = 0.1)
```

#### Utility Functions
```python
def has_animation(module) -> bool  # Check if module supports animation
def run_animation(module, input_data: str, speed: float = 1.0, 
                 export_gif: Optional[str] = None) -> Optional[Animation]
```

### Animation Design Guidelines

#### General Guidelines:
1. **Keep it visual:** Use Unicode symbols, colors (emojis), and clear formatting
2. **Limit complexity:** For large datasets, show only the first N items for clarity
3. **Progressive disclosure:** Show algorithm steps incrementally
4. **Meaningful duration:** Adjust frame duration based on content complexity
5. **Include statistics:** Show progress, counts, and results
6. **Handle edge cases:** Consider empty inputs, single items, etc.

#### Matplotlib 3D Animation Guidelines:
1. **Performance optimization:** Limit datasets to reasonable sizes (≤50 items)
2. **Coordinate normalization:** Scale coordinates to consistent ranges for better viewing
3. **Color coding:** Use distinct colors for different components/groups
4. **Interactive controls:** Leverage matplotlib's built-in zoom, pan, and rotate
5. **Frame rate:** Use appropriate intervals (200-1000ms) for smooth animation
6. **GIF compatibility:** Ensure animations work with PillowWriter for GIF export

### Example Animation Patterns

#### Algorithm Visualization:
```python
# Show initial state
animation.add_frame("🎯 Initial state: " + str(initial_data), 2.0)

# Show steps
for step, state in enumerate(algorithm_steps):
    content = f"Step {step + 1}: {describe_state(state)}"
    animation.add_frame(content, 0.5)

# Show final result
animation.add_frame("🎉 Final result: " + str(result), 3.0)
```

#### Progress Tracking:
```python
for i, item in enumerate(items):
    progress = f"Progress: {i + 1}/{len(items)} ({100 * (i + 1) // len(items)}%)"
    content = f"{progress}\n{current_state}"
    animation.add_frame(content, 0.3)
```

## Error Handling

The animation system provides graceful error handling:

- **No animation available:** Clear message explaining what's needed
- **Animation fails:** Error details with fallback options  
- **GIF export fails:** Automatic fallback to text file export
- **Missing dependencies:** Clear instructions for installation

## Performance Considerations

- Animations are limited to reasonable dataset sizes for visualization
- GIF export can be memory-intensive for many frames
- Large animations may take time to export
- Use appropriate frame durations to balance viewing experience and file size

## Troubleshooting

### Common Issues:

1. **"No animation available" message:**
   - The solution file needs a `create_animation` function
   - Check the function signature matches the expected format

2. **GIF export fails:**
   - Ensure Pillow is installed: `pip install Pillow`
   - Check available disk space
   - Try reducing animation length or frame size

3. **Animation runs too fast/slow:**
   - Use `--speed` parameter to adjust playback speed
   - Modify frame durations in the animation code

4. **Memory issues with large animations:**
   - Reduce the number of frames
   - Limit dataset size for visualization
   - Use shorter text content per frame

### Getting Help:

```bash
# Show animation subcommand help
python main.py animation --help

# Show general help with animation options
python main.py --help

# Test with sample data first
python main.py animation YEAR DAY --sample
```

## Future Enhancements

Potential future improvements:
- Interactive animations with user controls
- Multiple animation formats (MP4, WebM)
- Custom themes and color schemes
- Animation templates for common algorithm patterns
- Web-based animation viewer
- Animation comparison between different solutions
