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
    return (
        os.path.join(base, "front.png"),
        os.path.join(base, "back.png"),
        os.path.join(base, "normal.pal"),
    )


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

def active_slots(pal, usage=None):
    return [
        (i, c) for i, c in enumerate(pal)
        if i != 0 and c != MAGENTA and (usage is None or usage[i] > 0)
    ]

def sort_match(src_pal, donor_pal, key_fn, src_usage=None, donor_usage=None):
    src_sorted = [i for i, _ in sorted(active_slots(src_pal, src_usage), key=lambda x: key_fn(x[1]))]
    donor_sorted = [i for i, _ in sorted(active_slots(donor_pal, donor_usage), key=lambda x: key_fn(x[1]))]
    mapping = list(range(16))
    for rank, src_i in enumerate(src_sorted):
        # Use donor slot at same rank; if donor has fewer slots, cycle back through
        mapping[src_i] = donor_sorted[rank % len(donor_sorted)]
    return mapping

def nearest_match(src_pal, donor_pal, dist_fn, allow_reuse=False, src_usage=None, donor_usage=None):
    donor_active = active_slots(donor_pal, donor_usage)
    mapping = list(range(16))
    used = set()
    for src_i, src_c in active_slots(src_pal, src_usage):
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
        return sum(usage[i] for i, c in active_slots(pal, usage)) or 1

    src_total = body_total(src_pal, src_usage)
    donor_total = body_total(donor_pal, donor_usage)

    src_ranked = sorted(
        [i for i, c in active_slots(src_pal, src_usage)],
        key=lambda i: src_usage[i] / src_total, reverse=True
    )
    donor_ranked = sorted(
        [i for i, c in active_slots(donor_pal, donor_usage)],
        key=lambda i: donor_usage[i] / donor_total, reverse=True
    )
    mapping = list(range(16))
    for rank, src_i in enumerate(src_ranked):
        mapping[src_i] = donor_ranked[rank % len(donor_ranked)]
    return mapping


def usage_match_preserve_outline(src_pal, donor_pal, src_usage, donor_usage):
    """Frequency match, then enforce that the darkest source slots map to the
    darkest donor slots so outlines stay dark."""
    mapping = usage_match(src_pal, donor_pal, src_usage, donor_usage)

    active = [i for i, c in active_slots(src_pal, src_usage)]
    donor_active = [i for i, c in active_slots(donor_pal, donor_usage)]

    src_by_dark = sorted(active, key=lambda i: brightness(src_pal[i]))
    donor_by_dark = sorted(donor_active, key=lambda i: brightness(donor_pal[i]))

    outline_src = [i for i in src_by_dark if brightness(src_pal[i]) < 50]
    outline_donor = donor_by_dark[:len(outline_src)]

    for src_i, want_donor_i in zip(outline_src, outline_donor):
        have_donor_i = mapping[src_i]
        if have_donor_i == want_donor_i:
            continue
        for other_src_i in active:
            if mapping[other_src_i] == want_donor_i:
                mapping[other_src_i] = have_donor_i
                break
        mapping[src_i] = want_donor_i

    return mapping


def usage_match_hue_groups(src_pal, donor_pal, src_usage, donor_usage):
    """Frequency match that groups shades of the same hue together before ranking.
    Groups are ranked by total pixel count; within each group slots are ordered by brightness."""

    def hue(rgb):
        r, g, b = [x / 255.0 for x in rgb]
        mx, mn = max(r, g, b), min(r, g, b)
        diff = mx - mn
        if diff == 0:
            return None  # achromatic
        if mx == r:
            h = (g - b) / diff % 6
        elif mx == g:
            h = (b - r) / diff + 2
        else:
            h = (r - g) / diff + 4
        return h / 6.0

    def saturation(rgb):
        r, g, b = [x / 255.0 for x in rgb]
        mx, mn = max(r, g, b), min(r, g, b)
        return (mx - mn) / mx if mx != 0 else 0.0

    HUE_THRESHOLD = 0.08
    SAT_THRESHOLD = 0.15

    def cluster(pal, usage):
        slots = active_slots(pal, usage)
        achromatic = []
        chromatic = []
        for i, c in slots:
            if saturation(c) < SAT_THRESHOLD:
                achromatic.append(i)
            else:
                chromatic.append(i)

        # Greedy hue clustering
        groups = []
        for i in chromatic:
            h = hue(pal[i])
            placed = False
            for g in groups:
                gh = sum(hue(pal[j]) for j in g) / len(g)
                diff = min(abs(h - gh), 1 - abs(h - gh))  # circular hue distance
                if diff < HUE_THRESHOLD:
                    g.append(i)
                    placed = True
                    break
            if not placed:
                groups.append([i])

        # Add achromatic slots as one group each (outline/white/grey should stay separate)
        for i in achromatic:
            groups.append([i])

        # Sort slots within each group by brightness
        for g in groups:
            g.sort(key=lambda i: brightness(pal[i]))

        # Sort groups by total pixel count descending
        groups.sort(key=lambda g: sum(usage[i] for i in g), reverse=True)
        return groups

    src_groups = cluster(src_pal, src_usage)
    donor_groups = cluster(donor_pal, donor_usage)

    mapping = list(range(16))
    for g_rank, src_group in enumerate(src_groups):
        donor_group = donor_groups[g_rank % len(donor_groups)]
        for s_rank, src_i in enumerate(src_group):
            mapping[src_i] = donor_group[s_rank % len(donor_group)]

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
if "src_index" not in st.session_state:
    st.session_state.src_index = 0

col_src, col_donor = st.columns(2)
with col_src:
    st.markdown("**Source Pokémon**")
    if st.session_state.get("_src_arrow_fired"):
        st.session_state["src_selectbox"] = DISPLAY_NAMES[st.session_state.src_index]
        st.session_state["_src_arrow_fired"] = False
    src_display = st.selectbox("Source Pokémon", DISPLAY_NAMES, index=st.session_state.src_index, label_visibility="collapsed", key="src_selectbox")
    st.session_state.src_index = DISPLAY_NAMES.index(src_display)
    _, btn_prev_src, btn_next_src, _ = st.columns([2, 1, 1, 2])
    with btn_prev_src:
        if st.button("◀", key="src_prev", use_container_width=True):
            st.session_state.src_index = (st.session_state.src_index - 1) % len(DISPLAY_NAMES)
            st.session_state["_src_arrow_fired"] = True
            st.rerun()
    with btn_next_src:
        if st.button("▶", key="src_next", use_container_width=True):
            st.session_state.src_index = (st.session_state.src_index + 1) % len(DISPLAY_NAMES)
            st.session_state["_src_arrow_fired"] = True
            st.rerun()
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

src_png, src_back_png, src_pal_path = get_pokemon_paths(src_folder)
donor_png, donor_back_png, donor_pal_path = get_pokemon_paths(donor_folder)

src_pal = load_pal(src_pal_path)
donor_pal = load_pal(donor_pal_path)
src_usage = pixel_usage(src_png)
donor_usage = pixel_usage(donor_png)

# --- Initialize slot mapping in session state ---
mapping_key = f"mapping_{src_folder}_{donor_folder}"
version_key = f"version_{src_folder}_{donor_folder}"
if mapping_key not in st.session_state:
    st.session_state[mapping_key] = sort_match(src_pal, donor_pal, brightness, src_usage, donor_usage)
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

show_back = st.toggle("Show back sprites", value=False)
if show_back:
    back_col1, back_col2, back_col3 = st.columns(3)
    with back_col1:
        st.image(zoom(render(src_back_png, src_pal)))
    with back_col2:
        st.image(zoom(render(src_back_png, remapped_pal)))
    with back_col3:
        st.image(zoom(render(donor_back_png, donor_pal)))

# --- Controls ---
st.subheader("Palette Slot Mapper")

METHODS = {
    "Brightness":              lambda s, d: sort_match(s, d, brightness, src_usage, donor_usage),
    "Nearest (RGB)":           lambda s, d: nearest_match(s, d, color_distance, src_usage=src_usage, donor_usage=donor_usage),
    "Nearest (Lab)":           lambda s, d: nearest_match(s, d, lab_distance, src_usage=src_usage, donor_usage=donor_usage),
    "Nearest (reuse ok)":      lambda s, d: nearest_match(s, d, lab_distance, allow_reuse=True, src_usage=src_usage, donor_usage=donor_usage),
    "Reverse brightness":      lambda s, d: sort_match(s, d, lambda c: -brightness(c), src_usage, donor_usage),
    "Pixel frequency":         lambda s, d: usage_match(s, d, src_usage, donor_usage),
    "Pixel freq + outline":    lambda s, d: usage_match_preserve_outline(s, d, src_usage, donor_usage),
    "Pixel freq + groups":     lambda s, d: usage_match_hue_groups(s, d, src_usage, donor_usage),
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
base = f"{src_folder}_x_{donor_folder}"
def next_available_path():
    p = os.path.join(OUTPUT_DIR, f"{base}.pal")
    if not os.path.exists(p):
        return p, f"{base}.pal"
    counter = 2
    while os.path.exists(os.path.join(OUTPUT_DIR, f"{base}_{counter}.pal")):
        counter += 1
    return os.path.join(OUTPUT_DIR, f"{base}_{counter}.pal"), f"{base}_{counter}.pal"

out_path, out_filename = next_available_path()
if st.button(f"Save  {out_filename}"):
    save_pal(out_path, remapped_pal)
    st.success(f"Saved to output/{out_filename}")
    st.rerun()
