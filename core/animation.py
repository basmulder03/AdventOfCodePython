"""
Animation system for visualizing Advent of Code solutions.
"""
import time
import os
from typing import Any, List, Optional
from pathlib import Path


class AnimationFrame:
    """Represents a single frame in an animation."""

    def __init__(self, content: str, duration: float = 0.1):
        """
        Initialize an animation frame.

        Args:
            content: The text content to display for this frame
            duration: How long to display this frame in seconds
        """
        self.content = content
        self.duration = duration


class Animation:
    """Handles the display and export of animations."""

    def __init__(self, title: str = "", speed_multiplier: float = 1.0):
        """
        Initialize animation system.

        Args:
            title: Title to display above the animation
            speed_multiplier: Multiplier for animation speed (1.0 = normal)
        """
        self.title = title
        self.speed_multiplier = speed_multiplier
        self.frames: List[AnimationFrame] = []
        self.is_playing = False
        self.export_frames: List[str] = []

    def add_frame(self, content: str, duration: float = 0.1):
        """Add a frame to the animation."""
        self.frames.append(AnimationFrame(content, duration))

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def play(self, loop: bool = False, export_gif: Optional[str] = None):
        """
        Play the animation.

        Args:
            loop: Whether to loop the animation
            export_gif: Path to export GIF file (if specified)
        """
        if not self.frames:
            print("No frames to animate")
            return

        self.is_playing = True

        try:
            while self.is_playing:
                for frame in self.frames:
                    if not self.is_playing:
                        break

                    self.clear_screen()

                    # Display title if provided
                    if self.title:
                        print(f"{self.title}")
                        print("=" * len(self.title))
                        print()

                    # Display frame content
                    print(frame.content)

                    # Store frame for GIF export if requested
                    if export_gif:
                        self.export_frames.append(frame.content)

                    # Wait for frame duration
                    time.sleep(frame.duration / self.speed_multiplier)

                if not loop:
                    break

        except KeyboardInterrupt:
            print("\nAnimation stopped by user")
        finally:
            self.is_playing = False

        # Export GIF if requested
        if export_gif and self.export_frames:
            self.export_to_gif(export_gif)

    def stop(self):
        """Stop the animation."""
        self.is_playing = False

    def export_to_gif(self, filename: str):
        """
        Export animation frames to a GIF file.

        Args:
            filename: Output filename for the GIF
        """
        print(f"🎬 Exporting animation to {filename}...")

        try:
            # Try to use pillow for GIF creation
            from PIL import Image, ImageDraw, ImageFont

            images = []

            # Create images from text frames
            for frame_content in self.export_frames:
                # Create a simple text image
                img = self._text_to_image(frame_content)
                images.append(img)

            if images:
                # Save as animated GIF
                duration_ms = int(self.frames[0].duration * 1000) if self.frames else 100
                images[0].save(
                    filename,
                    save_all=True,
                    append_images=images[1:],
                    duration=duration_ms,
                    loop=0
                )
                print(f"✅ Animation exported to {filename}")
            else:
                print("❌ No frames to export")

        except ImportError:
            print("⚠️  PIL (Pillow) not available for GIF export")
            print("   Install with: pip install pillow")
            # Fallback: save as text files
            self._export_as_text_files(filename)

        except Exception as e:
            print(f"❌ Failed to export GIF: {e}")
            # Fallback: save as text files
            self._export_as_text_files(filename)

    def _text_to_image(self, text: str, width: int = 800, height: int = 600) -> Any:
        """Convert text to an image."""
        from PIL import Image, ImageDraw, ImageFont

        # Create image with black background
        img = Image.new('RGB', (width, height), color='black')
        draw = ImageDraw.Draw(img)

        try:
            # Try to use a monospace font
            font = ImageFont.truetype("consola.ttf", 12)  # Consolas on Windows
        except (OSError, IOError):
            try:
                font = ImageFont.truetype("DejaVuSansMono.ttf", 12)  # Linux
            except (OSError, IOError):
                font = ImageFont.load_default()

        # Draw text (white on black), limit text length to prevent overflow
        draw.text((10, 10), text[:2000], fill='white', font=font)

        return img

    def _export_as_text_files(self, base_filename: str):
        """Export frames as numbered text files."""
        base_path = Path(base_filename).with_suffix('')

        for i, frame_content in enumerate(self.export_frames):
            frame_file = f"{base_path}_frame_{i:04d}.txt"
            with open(frame_file, 'w', encoding='utf-8') as f:
                f.write(frame_content)

        print(f"✅ Animation frames exported as text files: {base_path}_frame_XXXX.txt")


def has_animation(module: Any) -> bool:
    """Check if a solution module has animation support."""
    return hasattr(module, 'create_animation')


def run_animation(module: Any, input_data: str, speed: float = 1.0,
                 export_gif: Optional[str] = None) -> Optional[Animation]:
    """
    Run animation from a solution module.

    Args:
        module: The solution module
        input_data: Input data for the solution
        speed: Animation speed multiplier
        export_gif: Optional filename to export GIF

    Returns:
        Animation object if successful, None otherwise
    """
    if not has_animation(module):
        print("❌ This solution does not have animation support")
        return None

    try:
        animation = module.create_animation(input_data)
        if animation is None:
            return None
        animation.speed_multiplier = speed
        animation.play(export_gif=export_gif)
        return animation
    except ImportError as e:
        if 'matplotlib' in str(e):
            print(f"❌ Animation failed: matplotlib not available")
            print("📋 To enable 3D animations, install matplotlib:")
            print("   pip install matplotlib")
        else:
            print(f"❌ Animation failed: Missing dependency - {e}")
        return None
    except Exception as e:
        print(f"❌ Animation failed: {e}")
        return None
