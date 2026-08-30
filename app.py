import os
import io
import numpy as np
import streamlit as st
from PIL import Image

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

POKEFIRERED = os.path.join(
    os.path.dirname(__file__), "graphics_pokemon"
)
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Gen 1 Pokémon list  (display name, folder name)
# ---------------------------------------------------------------------------

GEN1 = [
    ("Bulbasaur", "bulbasaur"), ("Ivysaur", "ivysaur"), ("Venusaur", "venusaur"),
    ("Charmander", "charmander"), ("Charmeleon", "charmeleon"), ("Charizard", "charizard"),
    ("Squirtle", "squirtle"), ("Wartortle", "wartortle"), ("Blastoise", "blastoise"),
    ("Caterpie", "caterpie"), ("Metapod", "metapod"), ("Butterfree", "butterfree"),
    ("Weedle", "weedle"), ("Kakuna", "kakuna"), ("Beedrill", "beedrill"),
    ("Pidgey", "pidgey"), ("Pidgeotto", "pidgeotto"), ("Pidgeot", "pidgeot"),
    ("Rattata", "rattata"), ("Raticate", "raticate"),
    ("Spearow", "spearow"), ("Fearow", "fearow"),
    ("Ekans", "ekans"), ("Arbok", "arbok"),
    ("Pikachu", "pikachu"), ("Raichu", "raichu"),
    ("Sandshrew", "sandshrew"), ("Sandslash", "sandslash"),
    ("Nidoran♀", "nidoran_f"), ("Nidorina", "nidorina"), ("Nidoqueen", "nidoqueen"),
    ("Nidoran♂", "nidoran_m"), ("Nidorino", "nidorino"), ("Nidoking", "nidoking"),
    ("Clefairy", "clefairy"), ("Clefable", "clefable"),
    ("Vulpix", "vulpix"), ("Ninetales", "ninetales"),
    ("Jigglypuff", "jigglypuff"), ("Wigglytuff", "wigglytuff"),
    ("Zubat", "zubat"), ("Golbat", "golbat"),
    ("Oddish", "oddish"), ("Gloom", "gloom"), ("Vileplume", "vileplume"),
    ("Paras", "paras"), ("Parasect", "parasect"),
    ("Venonat", "venonat"), ("Venomoth", "venomoth"),
    ("Diglett", "diglett"), ("Dugtrio", "dugtrio"),
    ("Meowth", "meowth"), ("Persian", "persian"),
    ("Psyduck", "psyduck"), ("Golduck", "golduck"),
    ("Mankey", "mankey"), ("Primeape", "primeape"),
    ("Growlithe", "growlithe"), ("Arcanine", "arcanine"),
    ("Poliwag", "poliwag"), ("Poliwhirl", "poliwhirl"), ("Poliwrath", "poliwrath"),
    ("Abra", "abra"), ("Kadabra", "kadabra"), ("Alakazam", "alakazam"),
    ("Machop", "machop"), ("Machoke", "machoke"), ("Machamp", "machamp"),
    ("Bellsprout", "bellsprout"), ("Weepinbell", "weepinbell"), ("Victreebel", "victreebel"),
    ("Tentacool", "tentacool"), ("Tentacruel", "tentacruel"),
    ("Geodude", "geodude"), ("Graveler", "graveler"), ("Golem", "golem"),
    ("Ponyta", "ponyta"), ("Rapidash", "rapidash"),
    ("Slowpoke", "slowpoke"), ("Slowbro", "slowbro"),
    ("Magnemite", "magnemite"), ("Magneton", "magneton"),
    ("Farfetch'd", "farfetchd"),
    ("Doduo", "doduo"), ("Dodrio", "dodrio"),
    ("Seel", "seel"), ("Dewgong", "dewgong"),
    ("Grimer", "grimer"), ("Muk", "muk"),
    ("Shellder", "shellder"), ("Cloyster", "cloyster"),
    ("Gastly", "gastly"), ("Haunter", "haunter"), ("Gengar", "gengar"),
    ("Onix", "onix"),
    ("Drowzee", "drowzee"), ("Hypno", "hypno"),
    ("Krabby", "krabby"), ("Kingler", "kingler"),
    ("Voltorb", "voltorb"), ("Electrode", "electrode"),
    ("Exeggcute", "exeggcute"), ("Exeggutor", "exeggutor"),
    ("Cubone", "cubone"), ("Marowak", "marowak"),
    ("Hitmonlee", "hitmonlee"), ("Hitmonchan", "hitmonchan"),
    ("Lickitung", "lickitung"),
    ("Koffing", "koffing"), ("Weezing", "weezing"),
    ("Rhyhorn", "rhyhorn"), ("Rhydon", "rhydon"),
    ("Chansey", "chansey"),
    ("Tangela", "tangela"),
    ("Kangaskhan", "kangaskhan"),
    ("Horsea", "horsea"), ("Seadra", "seadra"),
    ("Goldeen", "goldeen"), ("Seaking", "seaking"),
    ("Staryu", "staryu"), ("Starmie", "starmie"),
    ("Mr. Mime", "mr_mime"),
    ("Scyther", "scyther"),
    ("Jynx", "jynx"),
    ("Electabuzz", "electabuzz"),
    ("Magmar", "magmar"),
    ("Pinsir", "pinsir"),
    ("Tauros", "tauros"),
    ("Magikarp", "magikarp"), ("Gyarados", "gyarados"),
    ("Lapras", "lapras"),
    ("Ditto", "ditto"),
    ("Eevee", "eevee"), ("Vaporeon", "vaporeon"), ("Jolteon", "jolteon"), ("Flareon", "flareon"),
    ("Porygon", "porygon"),
    ("Omanyte", "omanyte"), ("Omastar", "omastar"),
    ("Kabuto", "kabuto"), ("Kabutops", "kabutops"),
    ("Aerodactyl", "aerodactyl"),
    ("Snorlax", "snorlax"),
    ("Articuno", "articuno"), ("Zapdos", "zapdos"), ("Moltres", "moltres"),
    ("Dratini", "dratini"), ("Dragonair", "dragonair"), ("Dragonite", "dragonite"),
    ("Mewtwo", "mewtwo"), ("Mew", "mew"),
]

DISPLAY_NAMES = [d for d, _ in GEN1]
FOLDER_NAMES = {d: f for d, f in GEN1}

# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def get_pokemon_paths(folder_name: str):
    base = os.path.join(POKEFIRERED, folder_name)
    return os.path.join(base, "front.png"), os.path.join(base, "normal.pal")


def pixel_usage(png_path: str) -> list:
    """Return a list of 16 pixel counts, one per palette slot index."""
    img = Image.open(png_path).convert("P")
    indices = np.array(img).flatten()
    counts = [0] * 16
    for i in range(16):
        counts[i] = int(np.sum(indices == i))
    return counts


def load_pal(path: str) -> list:
    colors = []
    with open(path, "r") as f:
        lines = f.read().splitlines()
    # Skip header: JASC-PAL, 0100, count
    for line in lines[3:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) >= 3:
            colors.append((int(parts[0]), int(parts[1]), int(parts[2])))
    return colors[:16]


def save_pal(path: str, colors: list):
    lines = ["JASC-PAL", "0100", str(len(colors))]
    for r, g, b in colors:
        lines.append(f"{r} {g} {b}")
    with open(path, "w", newline="\r\n") as f:
        f.write("\r\n".join(lines) + "\r\n")


def render(png_path: str, palette_16: list) -> Image.Image:
    img = Image.open(png_path).convert("P")
    flat = []
    for r, g, b in palette_16:
        flat += [r, g, b]
    flat += [0, 0, 0] * (256 - 16)
    img.putpalette(flat)
    rgba = img.convert("RGBA")
    data = np.array(rgba)
    mask = (data[:, :, 0] == 255) & (data[:, :, 1] == 0) & (data[:, :, 2] == 255)
    data[mask] = [255, 255, 255, 255]  # white background instead of transparent
    return Image.fromarray(data, "RGBA").convert("RGB")


def zoom(img: Image.Image, scale: int = 4) -> Image.Image:
    return img.resize((img.width * scale, img.height * scale), Image.NEAREST)


def swatch_html(r: int, g: int, b: int) -> str:
    return (
        f'<span style="display:inline-block;width:20px;height:20px;'
        f'background:rgb({r},{g},{b});border:1px solid #555;'
        f'vertical-align:middle;margin-right:4px;"></span>'
    )


def to_png_bytes(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Palette matching helpers
# ---------------------------------------------------------------------------

MAGENTA = (255, 0, 255)

def brightness(rgb):
    r, g, b = rgb
    return 0.299 * r + 0.587 * g + 0.114 * b

def rgb_to_lab(rgb):
    def linearize(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = [linearize(x) for x in rgb]
    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505
    x, y, z = x / 0.95047, y / 1.00000, z / 1.08883
    def f(t):
        return t ** (1/3) if t > 0.008856 else 7.787 * t + 16/116
    return (116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z)))

def lab_distance(a, b):
    return sum((x - y) ** 2 for x, y in zip(rgb_to_lab(a), rgb_to_lab(b))) ** 0.5

def color_distance(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5

def active_slots(pal):
    return [(i, c) for i, c in enumerate(pal) if i != 0 and c != MAGENTA]

def sort_match(src_pal, donor_pal, key_fn):
    src_sorted = [i for i, _ in sorted(active_slots(src_pal), key=lambda x: key_fn(x[1]))]
    donor_sorted = [i for i, _ in sorted(active_slots(donor_pal), key=lambda x: key_fn(x[1]))]
    mapping = list(range(16))
    for rank, src_i in enumerate(src_sorted):
        mapping[src_i] = donor_sorted[min(rank, len(donor_sorted) - 1)]
    return mapping

def nearest_match(src_pal, donor_pal, dist_fn, allow_reuse=False):
    donor_active = active_slots(donor_pal)
    mapping = list(range(16))
    used = set()
    for src_i, src_c in active_slots(src_pal):
        candidates = donor_active if allow_reuse else [(i, c) for i, c in donor_active if i not in used]
        if not candidates:
            candidates = donor_active
        best_i = min(candidates, key=lambda x: dist_fn(src_c, x[1]))[0]
        mapping[src_i] = best_i
        used.add(best_i)
    return mapping


def usage_match(src_pal, donor_pal, src_usage, donor_usage):
    """Map slots by pixel frequency rank: most-used src slot → most-used donor slot.
    Counts are normalised by each sprite's total body pixels so size doesn't matter."""
    def body_total(pal, usage):
        return sum(usage[i] for i, c in active_slots(pal)) or 1

    src_total = body_total(src_pal, src_usage)
    donor_total = body_total(donor_pal, donor_usage)

    src_ranked = sorted(
        [i for i, c in active_slots(src_pal)],
        key=lambda i: src_usage[i] / src_total, reverse=True
    )
    donor_ranked = sorted(
        [i for i, c in active_slots(donor_pal)],
        key=lambda i: donor_usage[i] / donor_total, reverse=True
    )
    mapping = list(range(16))
    for rank, src_i in enumerate(src_ranked):
        mapping[src_i] = donor_ranked[min(rank, len(donor_ranked) - 1)]
    return mapping


def show_image(img: Image.Image, caption: str):
    st.caption(caption)
    st.image(img)


# ---------------------------------------------------------------------------
# Streamlit app
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Pokémon Repainter", layout="wide")
st.title("Pokémon Repainter")

st.markdown(
    "<style>button[title='View fullscreen']{display:none}</style>",
    unsafe_allow_html=True,
)

# --- Pokémon selectors ---
if "donor_index" not in st.session_state:
    st.session_state.donor_index = DISPLAY_NAMES.index("Ivysaur")

col_src, col_donor = st.columns(2)
with col_src:
    st.markdown("**Source Pokémon**")
    src_display = st.selectbox("Source Pokémon", DISPLAY_NAMES, index=0, label_visibility="collapsed")
with col_donor:
    st.markdown("**Donor Pokémon (palette)**")
    # Pre-set selectbox value if arrows changed donor_index
    if st.session_state.get("_donor_arrow_fired"):
        st.session_state["donor_selectbox"] = DISPLAY_NAMES[st.session_state.donor_index]
        st.session_state["_donor_arrow_fired"] = False
    donor_display = st.selectbox(
        "Donor Pokémon (palette)",
        DISPLAY_NAMES,
        index=st.session_state.donor_index,
        label_visibility="collapsed",
        key="donor_selectbox",
    )
    st.session_state.donor_index = DISPLAY_NAMES.index(donor_display)
    _, btn_prev, btn_next, _ = st.columns([2, 1, 1, 2])
    with btn_prev:
        if st.button("◀", key="donor_prev", use_container_width=True):
            st.session_state.donor_index = (st.session_state.donor_index - 1) % len(DISPLAY_NAMES)
            st.session_state["_donor_arrow_fired"] = True
            st.rerun()
    with btn_next:
        if st.button("▶", key="donor_next", use_container_width=True):
            st.session_state.donor_index = (st.session_state.donor_index + 1) % len(DISPLAY_NAMES)
            st.session_state["_donor_arrow_fired"] = True
            st.rerun()

src_folder = FOLDER_NAMES[src_display]
donor_folder = FOLDER_NAMES[donor_display]

src_png, src_pal_path = get_pokemon_paths(src_folder)
donor_png, donor_pal_path = get_pokemon_paths(donor_folder)

src_pal = load_pal(src_pal_path)
donor_pal = load_pal(donor_pal_path)
src_usage = pixel_usage(src_png)
donor_usage = pixel_usage(donor_png)

# --- Initialize slot mapping in session state ---
mapping_key = f"mapping_{src_folder}_{donor_folder}"
version_key = f"version_{src_folder}_{donor_folder}"
if mapping_key not in st.session_state:
    st.session_state[mapping_key] = sort_match(src_pal, donor_pal, brightness)
    st.session_state[version_key] = 0

mapping: list = st.session_state[mapping_key]
slot_version = st.session_state[version_key]

# --- Build remapped palette from last run's mapping ---
remapped_pal = [donor_pal[mapping[i]] for i in range(16)]

# --- Sprite previews ---
st.subheader("Preview")
img_col1, img_col2, img_col3 = st.columns(3)
with img_col1:
    show_image(zoom(render(src_png, src_pal)), f"Original — {src_display}")
with img_col2:
    show_image(zoom(render(src_png, remapped_pal)), f"Recolored with {donor_display}'s palette")
with img_col3:
    show_image(zoom(render(donor_png, donor_pal)), f"Donor — {donor_display}")

# --- Controls ---
st.subheader("Palette Slot Mapper")

METHODS = {
    "Brightness":           lambda s, d: sort_match(s, d, brightness),
    "Nearest (RGB)":        lambda s, d: nearest_match(s, d, color_distance),
    "Nearest (Lab)":        lambda s, d: nearest_match(s, d, lab_distance),
    "Nearest (reuse ok)":   lambda s, d: nearest_match(s, d, lab_distance, allow_reuse=True),
    "Reverse brightness":   lambda s, d: sort_match(s, d, lambda c: -brightness(c)),
    "Pixel frequency":      lambda s, d: usage_match(s, d, src_usage, donor_usage),
}

btn_cols = st.columns(len(METHODS) + 1)
for col, (label, fn) in zip(btn_cols, METHODS.items()):
    with col:
        if st.button(label, use_container_width=True):
            st.session_state[mapping_key] = fn(src_pal, donor_pal)
            st.session_state[version_key] += 1
            st.rerun()
with btn_cols[-1]:
    if st.button("Reset 1:1", use_container_width=True):
        st.session_state[mapping_key] = list(range(16))
        st.session_state[version_key] += 1
        st.rerun()

st.caption("For each source slot, choose which donor slot provides its color.")

slot_options = list(range(16))

header_cols = st.columns([1, 3, 2, 3])
header_cols[0].markdown("**Slot**")
header_cols[1].markdown("**Source color**")
header_cols[2].markdown("**→ Donor slot**")
header_cols[3].markdown("**Donor color**")

for i in range(16):
    sr, sg, sb = src_pal[i]
    cols = st.columns([1, 3, 2, 3])
    cols[0].markdown(f"`{i:2d}`")
    cols[1].markdown(swatch_html(sr, sg, sb) + f" ({sr}, {sg}, {sb})", unsafe_allow_html=True)

    sel = cols[2].selectbox(
        label=f"slot_{i}",
        options=slot_options,
        index=mapping[i],
        label_visibility="collapsed",
        key=f"slot_sel_{mapping_key}_v{slot_version}_{i}",
    )
    mapping[i] = sel

    dr, dg, db = donor_pal[sel]
    cols[3].markdown(swatch_html(dr, dg, db) + f" ({dr}, {dg}, {db})", unsafe_allow_html=True)

st.session_state[mapping_key] = mapping

# --- Export ---
st.subheader("Export")
out_filename = f"{src_folder}_repainted.pal"
out_path = os.path.join(OUTPUT_DIR, out_filename)
if st.button(f"Save  {out_filename}"):
    save_pal(out_path, remapped_pal)
    st.success(f"Saved to output/{out_filename}")
