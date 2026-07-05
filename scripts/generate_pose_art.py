#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate all pose reference illustrations with Gemini image models."""

import os
import sys
import time
import argparse
from pathlib import Path

def load_env():
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    if key not in os.environ:
                        os.environ[key] = value.strip('"\'')

load_env()

from google import genai
from google.genai import types

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = "gemini-3-pro-image-preview"

STYLE_PREFIX = (
    "Elegant black-and-white line art illustration, fashion-illustration figure sketch style, "
    "like a professional wedding photography posing-guide reference. Single clean fine black "
    "outline on a plain white background, no color fill, no shading, no cross-hatching, no "
    "greyscale gradients. Realistic, elegant human proportions and anatomy, gentle simple facial "
    "features (eyes, nose, subtle smile) clearly visible on the face, natural-looking hands. "
    "Fine linework, tasteful clothing fold details. Full body visible from head to feet, "
    "centered composition, generous margin around the figures. Absolutely no text, no "
    "captions, no labels, no watermarks anywhere in the image. "
)

def generate(prompt_text, output_path, aspect_ratio="3:4"):
    client = genai.Client(api_key=GEMINI_API_KEY)
    full_prompt = STYLE_PREFIX + prompt_text

    response = client.models.generate_content(
        model=MODEL,
        contents=full_prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
            image_config=types.ImageConfig(aspect_ratio=aspect_ratio),
            safety_settings=[
                types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_LOW_AND_ABOVE"),
                types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_LOW_AND_ABOVE"),
                types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_LOW_AND_ABOVE"),
                types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_LOW_AND_ABOVE"),
            ],
        ),
    )

    image_data = None
    for part in response.candidates[0].content.parts:
        if getattr(part, "inline_data", None) and part.inline_data.mime_type.startswith("image/"):
            image_data = part.inline_data.data
            break

    if not image_data:
        print(f"  No image returned for: {output_path.name}")
        return None

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(image_data)
    print(f"  Saved: {output_path.name}")
    return output_path


POSES = [
    # id, aspect_ratio, prompt
    ("c01", "3:4", "A bride in a wedding dress and a groom in a suit stand facing each other close together, one hand of the groom resting on the bride's waist, both looking into each other's eyes, weight shifted onto the back leg, elegant three-quarter body angle."),
    ("c02", "3:4", "A bride and groom standing at a slight angle to each other, front foot pointing toward the viewer, looking toward each other, elegant three-quarter body pose."),
    ("c03", "3:4", "A bride in a flowing wedding dress with a veil and flower crown, and a groom in a suit, standing facing each other with their foreheads gently touching, eyes closed, holding both hands together between them. Romantic, tender mood."),
    ("c04", "3:4", "A groom stands with his back gently leaning against the bride's back, both looking past each other into the distance, calm romantic mood."),
    ("c05", "3:4", "A groom dips the bride slightly backward in a dance pose, supporting her waist and hand, as if finishing a dance, both smiling."),
    ("c06", "3:4", "A bride and groom walking hand in hand along a path, viewed from a three-quarter front angle, mid-stride, natural movement."),
    ("c07", "3:4", "A bride and groom walking hand in hand directly toward the viewer, laughing, mid-stride, dynamic candid movement."),
    ("c08", "3:4", "A bride and groom seen from behind walking a few steps away, both turning back over their shoulders to look toward the viewer, wedding dress and suit jacket flowing."),
    ("c09", "3:4", "A groom holding the bride's hand up as she twirls under his arm, her wedding dress swirling around her, dynamic joyful movement."),
    ("c10", "3:4", "A bride laughing and walking ahead while the groom follows behind reaching for her hand, playful chase, candid joyful movement."),
    ("c11", "3:4", "A groom embracing the bride from behind, his chin resting on her shoulder, both looking in the same direction, tender mood."),
    ("c12", "3:4", "A groom whispering something into the bride's ear, both smiling, close and intimate."),
    ("c13", "3:4", "A groom kissing the bride gently on the forehead, her eyes closed with a soft smile, tender romantic mood."),
    ("c14", "3:4", "A groom gently holding the bride's face with one hand, both looking into each other's eyes, close and tender."),
    ("c15", "3:4", "A bride and groom sharing a gentle kiss, one head tilted slightly, one hand resting on the other's cheek, romantic close embrace."),
    ("c16", "3:4", "A bride and groom laughing together at a shared joke, natural candid joyful expressions, standing close."),
    ("c17", "3:4", "A groom playfully tickling or teasing the bride, both laughing, playful candid movement."),
    ("c18", "3:4", "A bride and groom standing close together both looking off to the side at something outside the frame, natural relaxed expressions."),
    ("c19", "3:4", "A bride and groom standing close in a gentle embrace, foreheads close together, softly backlit romantic pose, simple outline composition."),
    ("c20", "3:4", "A bride and groom standing together near a reflective surface such as a puddle, both visible along with their mirrored reflection below them."),
    ("c21", "4:3", "A small bride and groom figure standing together in the center of a large open landscape or grand architectural setting, wide environmental composition."),
    ("c22", "3:4", "A bride and groom standing close together, the groom holding an open vintage umbrella over both of them, romantic prop styling."),
    ("c23", "3:4", "A bride and groom standing side by side, arms around each other, both smiling directly at the camera."),
    ("c24", "3:4", "A bride and groom playfully touching noses together, eyes half-closed, both smiling."),
    ("c25", "3:4", "A groom gently placing his hand over the bride's heart on her chest, tender eye contact between them."),
    ("c26", "3:4", "A bride and groom walking arm in arm at a relaxed strolling pace, elegant posture, looking ahead or at each other."),
    ("c27", "3:4", "A bride and groom running together side by side holding hands, joyfully laughing, dynamic movement."),
    ("c28", "3:4", "A bride and groom with foreheads and noses gently touching, eyes closed, dreamy soft smiles."),
    ("c29", "3:4", "The bride resting her head against the groom's chest, eyes closed, being gently held by him."),
    ("c30", "3:4", "The bride with both arms wrapped around the groom's neck, close warm embrace."),
    ("c31", "3:4", "A bride looking at the groom admiringly from the side while he looks toward the camera, romantic mood."),
    ("c32", "3:4", "A bride and groom laughing heartily together in a moment of relief and joy, candid genuine expressions."),
    ("c33", "3:4", "A bride and groom doing a silly improvised dance move together, both laughing."),
    ("c34", "3:4", "A bride and groom close together with the wedding veil pulled over both of their heads, intimate framed moment underneath."),
    ("c35", "3:4", "A bride and groom walking together into golden backlight, romantic silhouette with soft light rays around them."),
    ("c36", "1:1", "ONLY a tight close-up crop of two hands with wedding rings resting next to an elegant bridal bouquet, filling the entire frame. No faces, no full body, no additional figures, no inset circles, no collage, just one single close-up detail image."),
    ("c37", "3:4", "A bride and groom sitting side by side on steps, one resting their head on the other's shoulder, relaxed intimate pose."),
    ("c38", "3:4", "A bride and groom sitting relaxed together on a blanket on the grass, facing each other, casual picnic mood."),
    ("c39", "3:4", "A bride and groom sitting close together on a staircase step, relaxed cozy body language."),
    ("c40", "1:1", "ONLY a tight close-up crop of a hand sliding a wedding ring onto another hand's finger during the ceremony, filling the entire frame. No faces, no full body, no additional figures, no inset circles, no collage, just one single close-up ring-exchange detail image."),
    ("c41", "3:4", "A bride and groom sharing their first kiss as a married couple, with a soft blurred suggestion of wedding guests in the background."),
    ("c42", "4:3", "A bride and groom walking arm in arm through a cheering crowd of wedding guests throwing confetti, joyful festive movement."),

    ("f01", "4:3", "A large wedding group of about ten people arranged in two rows, taller people standing in the back row and shorter people in the front row, all facing the camera, formal group portrait."),
    ("f02", "4:3", "A bride and groom stand at the center, surrounded by a semicircle of family members standing close together, all facing the camera, warm celebratory group portrait."),
    ("f03", "4:3", "A bride and groom standing close together with both sets of parents around them, arms around each other, an intimate close family group portrait."),
    ("f04", "4:3", "A bride and groom standing with the bride's side of the family gathered closely around them, a warm family group portrait."),
    ("f05", "4:3", "A large wedding party of about fifteen guests standing together on wide steps, arranged so everyone is visible, festive group portrait."),
    ("f06", "1:1", "A group of wedding guests lying down in a circle on the ground, viewed from directly above, faces pointing inward, a creative overhead group composition."),
    ("f07", "4:3", "A group of wedding guests joyfully throwing confetti into the air together, caught in mid-air motion, festive celebratory scene."),
    ("f08", "4:3", "A group of wedding guests laughing together naturally, candid joyful expressions, standing close in a loose cluster."),
    ("f09", "4:3", "A small group of wedding guests standing in a circle, talking naturally to each other, candid relaxed body language."),
    ("f10", "3:4", "Two wedding guests sharing a warm spontaneous hug, caught mid-embrace, candid emotional moment."),
    ("f11", "3:4", "A parent carrying a small child on their shoulders, both laughing joyfully, warm family moment."),
    ("f12", "4:3", "Two small children running happily toward the camera across a lawn, joyful candid movement."),
    ("f13", "4:3", "Grandparents sitting together on a bench with grandchildren cuddled beside them and on their lap, warm tender family portrait."),
    ("f14", "4:3", "A small relaxed group portrait of the bride and groom together with their siblings, standing casually close together."),
    ("f15", "4:3", "A bride and groom standing with their best man and maid of honor close beside them, a warm close-knit group portrait."),
    ("f16", "4:3", "A large family group portrait where some family members sit on chairs in the front row and the rest stand behind them."),
    ("f17", "4:3", "A group of wedding guests raising champagne glasses together in a toast, joyful celebratory group portrait."),
    ("f18", "4:3", "A group of wedding guests forming a heart shape with their raised hands above the bride and groom standing in the center."),
    ("f19", "3:4", "A warm emotional embrace between the bride and one of her parents, tender candid moment."),
    ("f20", "3:4", "A wedding guest wiping away a happy tear, candid emotional portrait."),
    ("f21", "3:4", "Two wedding guests laughing and clinking their glasses together in a toast, candid joyful moment."),
    ("f22", "3:4", "Small flower children scattering flower petals, captured mid-motion, joyful candid movement."),
    ("f23", "3:4", "A small ring bearer child proudly holding up the ring pillow toward the camera."),
    ("f24", "3:4", "A group of children dancing freely and joyfully on the dance floor."),
    ("f25", "3:4", "The parents of the bride and groom dancing romantically together."),
    ("f26", "3:4", "Grandparents standing arm in arm, warm content smiles."),
    ("f27", "3:4", "A pair of siblings goofing around together, candid playful moment."),
    ("f28", "3:4", "The maid of honor and the bride with their heads together, laughing warmly."),
    ("f29", "4:3", "The bride and groom having their first dance together, wedding guests watching in the background."),
    ("f30", "3:4", "The bride and groom cutting the wedding cake together, hands overlapping on the knife."),
    ("f31", "4:3", "The bride throwing the bridal bouquet over her shoulder, a group of guests reaching up to catch it."),
    ("f32", "4:3", "A row of wedding guests clapping and cheering, forming an aisle for the bride and groom to walk through."),
    ("f33", "4:3", "A large joyful group of wedding guests cheering and jumping together at the end of the celebration."),

    ("s01", "3:4", "A single bride in a flowing wedding dress with a veil, standing in a relaxed three-quarter pose, weight on her back leg, looking gently toward the camera."),
    ("s02", "3:4", "A groom standing relaxed with one hand in his trouser pocket, body angled slightly to the side, confident casual portrait pose."),
    ("s03", "3:4", "A bride standing with her back to the camera, turning her head and upper body back over her shoulder toward the viewer, showing both the back of her dress and her face."),
    ("s04", "3:4", "A groom leaning casually with his shoulder against a wall, one leg slightly bent, relaxed confident portrait pose."),
    ("s05", "3:4", "A bride sitting on stone steps, elbows resting on her knees, hands loosely clasped, relaxed elegant portrait pose."),
    ("s06", "3:4", "A groom sitting sideways on a bench, one arm resting along the backrest, relaxed confident portrait pose looking to the side."),
    ("s07", "3:4", "A bride sitting gently on the ground with her wedding dress elegantly draped and spread around her in a wide circle, graceful portrait pose."),
    ("s08", "3:4", "A bride walking casually toward the camera, arms swinging naturally, relaxed candid movement, mid-stride."),
    ("s09", "3:4", "A bride spinning around in her wedding dress, the fabric swirling outward with the motion, joyful dynamic movement."),
    ("s10", "3:4", "A bride with her hair and veil flowing dramatically in the wind, captured mid-motion, romantic dynamic portrait."),
    ("s11", "1:1", "ONLY a tight close-up crop of two hands gently clasped together showing wedding rings, filling the entire frame. No other body parts, no faces, no additional figures, no inset circles, no collage, just one single close-up image of the hands."),
    ("s12", "1:1", "ONLY a tight extreme close-up crop of delicate lace fabric texture and buttons on a wedding dress, filling the entire frame. No faces, no full body, no additional figures, no inset circles, no collage, just one single close-up fabric detail image."),
    ("s13", "1:1", "A close-up of elegant wedding shoes on a woman's feet, styled on a staircase, fashion detail illustration."),
]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", default=str(Path(__file__).parent.parent / "illustrations"))
    parser.add_argument("--only", nargs="*", help="Only generate these pose ids")
    parser.add_argument("--retries", type=int, default=2)
    args = parser.parse_args()

    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not set")
        sys.exit(1)

    out_dir = Path(args.out_dir)
    todo = POSES if not args.only else [p for p in POSES if p[0] in args.only]

    ok, failed = [], []
    for pose_id, ratio, desc in todo:
        print(f"[{pose_id}] generating...")
        result = None
        for attempt in range(args.retries + 1):
            try:
                result = generate(desc, out_dir / f"{pose_id}.png", aspect_ratio=ratio)
            except Exception as e:
                print(f"  Error ({attempt+1}/{args.retries+1}): {e}")
            if result:
                break
            time.sleep(3)
        (ok if result else failed).append(pose_id)
        time.sleep(2)

    print(f"\nDone. {len(ok)} succeeded, {len(failed)} failed.")
    if failed:
        print("Failed:", ", ".join(failed))
