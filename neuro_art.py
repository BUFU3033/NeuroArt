import argparse
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


def lerp_color(start_color, end_color, t):
    return tuple(int(start + (end - start) * t) for start, end in zip(start_color, end_color))


def make_background(width, height, seed):
    random.seed(seed)
    # Dark backdrop with subtle vertical gradient.
    base_top = (14, 10, 20)
    base_bottom = (5, 3, 10)

    img = Image.new("RGB", (width, height), base_bottom)
    pixels = img.load()
    for y in range(height):
        t = y / max(height - 1, 1)
        color = lerp_color(base_top, base_bottom, t)
        for x in range(width):
            pixels[x, y] = color

    # Add soft vignette to draw focus toward the center.
    vignette = Image.new("L", (width, height), 0)
    vdraw = ImageDraw.Draw(vignette)
    max_radius = math.sqrt((width / 2) ** 2 + (height / 2) ** 2)
    for r in range(int(max_radius), 0, -8):
        intensity = int(255 * (1 - (r / max_radius)))
        bbox = [width / 2 - r, height / 2 - r, width / 2 + r, height / 2 + r]
        vdraw.ellipse(bbox, fill=intensity)
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=80))
    img = Image.composite(img, Image.new("RGB", (width, height), (0, 0, 0)), vignette)
    return img


def tapered_line(draw, start, end, thickness, color):
    # Draws a tapered stroke by creating overlapping ellipses.
    steps = int(max(4, thickness * 3))
    for i in range(steps + 1):
        t = i / steps
        x = start[0] + (end[0] - start[0]) * t
        y = start[1] + (end[1] - start[1]) * t
        radius = max(0.2, thickness * (1 - 0.8 * t))
        bbox = [x - radius, y - radius, x + radius, y + radius]
        draw.ellipse(bbox, fill=color)


def draw_branch(draw, start, length, angle, depth, color, thickness, randomness, branch_prob, taper):
    if depth <= 0 or length <= 2:
        return

    rad_angle = math.radians(angle + random.uniform(-randomness, randomness))
    end = (
        start[0] + length * math.cos(rad_angle),
        start[1] + length * math.sin(rad_angle),
    )

    stroke_thickness = max(0.5, thickness * (taper ** 0.8))
    tapered_line(draw, start, end, stroke_thickness, color)

    # Draw subtle glow using blurred duplicate strokes.
    glow_color = tuple(min(255, int(c * 1.3)) for c in color)
    for blur_radius in (2, 4):
        glow_img = Image.new("RGBA", draw.im.size, (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_img)
        tapered_line(glow_draw, start, end, stroke_thickness + 1, glow_color + (70,))
        blur = glow_img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        draw.im.paste(blur, (0, 0), blur)

    next_length = length * random.uniform(0.65, 0.85)
    next_thickness = thickness * 0.8
    next_depth = depth - 1

    if random.random() < branch_prob:
        branch_angle = angle + random.uniform(18, 55)
        draw_branch(
            draw,
            end,
            next_length,
            branch_angle,
            next_depth,
            color,
            next_thickness,
            randomness,
            branch_prob * 0.95,
            taper * 0.92,
        )

    if random.random() < branch_prob:
        branch_angle = angle - random.uniform(18, 55)
        draw_branch(
            draw,
            end,
            next_length,
            branch_angle,
            next_depth,
            color,
            next_thickness,
            randomness,
            branch_prob * 0.95,
            taper * 0.92,
        )

    # Continue forward growth to create long arborizations.
    draw_branch(
        draw,
        end,
        next_length,
        angle + random.uniform(-randomness, randomness),
        next_depth,
        color,
        next_thickness,
        randomness,
        branch_prob,
        taper * 0.96,
    )


def generate_neuron_layer(base_image, seed, count, palette):
    random.seed(seed)
    canvas = base_image.convert("RGBA")
    draw = ImageDraw.Draw(canvas, "RGBA")
    width, height = base_image.size

    for i in range(count):
        # Position neurons in a loose grid for balanced coverage.
        x = random.gauss(width * 0.5, width * 0.2)
        y = random.gauss(height * 0.5, height * 0.25)
        start = (x, y)

        color = random.choice(palette)
        angle = random.uniform(-80, 80)
        length = random.uniform(height * 0.09, height * 0.17)
        thickness = random.uniform(3, 6)
        depth = random.randint(5, 8)

        draw_branch(
            draw,
            start,
            length,
            angle,
            depth,
            color,
            thickness,
            randomness=10,
            branch_prob=0.65,
            taper=0.9,
        )

    # Add slight blur and noise to soften strokes.
    softened = canvas.filter(ImageFilter.GaussianBlur(radius=0.6))
    return Image.alpha_composite(base_image.convert("RGBA"), softened)


def add_specular_highlights(image, accent_color=(255, 220, 120)):
    width, height = image.size
    highlight_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(highlight_img)
    for _ in range(60):
        x = random.uniform(0, width)
        y = random.uniform(0, height)
        radius = random.uniform(1.5, 3.5)
        intensity = random.randint(160, 255)
        color = (*accent_color, intensity)
        bbox = [x - radius, y - radius, x + radius, y + radius]
        draw.ellipse(bbox, fill=color)
    blurred = highlight_img.filter(ImageFilter.GaussianBlur(radius=1.4))
    return Image.alpha_composite(image.convert("RGBA"), blurred)


def generate_neuro_art(width, height, seed, output_path):
    base = make_background(width, height, seed)
    palette = [
        (217, 174, 52),  # gold
        (180, 140, 90),
        (255, 232, 180),
        (200, 210, 220),
    ]

    neuron_layer = generate_neuron_layer(base, seed + 1, count=14, palette=palette)
    neuron_layer = generate_neuron_layer(neuron_layer, seed + 5, count=8, palette=palette)
    with_highlights = add_specular_highlights(neuron_layer)
    final = with_highlights.convert("RGB")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    final.save(output_path)
    return output_path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate digital neuro art inspired by Greg Dunn's style.",
    )
    parser.add_argument("--width", type=int, default=1920, help="Output width in pixels.")
    parser.add_argument("--height", type=int, default=1080, help="Output height in pixels.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility.")
    parser.add_argument(
        "--output",
        type=str,
        default="output/neuro_art.png",
        help="Path to save the generated artwork.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    output_path = generate_neuro_art(args.width, args.height, args.seed, args.output)
    print(f"Artwork saved to {output_path}")


if __name__ == "__main__":
    main()
