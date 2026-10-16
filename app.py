import html
import streamlit as st

st.set_page_config(
    page_title="Hello World Motion Lab",
    page_icon="🌦️",
    layout="wide",
)

st.title("🌦️ Hello World Motion Lab")
st.write("Type your name, pick a style, and bring your Hello World screen to life.")

# Controls
with st.sidebar:
    st.header("Customize your app")
    name = st.text_input("Your name", value="World", max_chars=40)

    font_options = {
        "Arial": "Arial, Helvetica, sans-serif",
        "Georgia": "Georgia, serif",
        "Courier New": "'Courier New', monospace",
        "Trebuchet MS": "'Trebuchet MS', sans-serif",
        "Verdana": "Verdana, sans-serif",
        "Times New Roman": "'Times New Roman', serif",
        "Impact": "Impact, Haettenschweiler, sans-serif",
        "Comic Sans MS": "'Comic Sans MS', cursive, sans-serif",
    }
    font_name = st.selectbox("Font", list(font_options.keys()))
    font_size = st.slider("Text size", min_value=24, max_value=100, value=56, step=2)

    backgrounds = {
        "Midnight": ("#10152f", "#252f65", "#f7f8ff"),
        "Ocean": ("#063b52", "#0b7890", "#effcff"),
        "Sunset": ("#451a50", "#e76f51", "#fff8ed"),
        "Forest": ("#102f27", "#34765a", "#f1fff5"),
        "Rose": ("#521d37", "#c04f75", "#fff4f8"),
        "Cloud": ("#dce8f4", "#f7fbff", "#182b43"),
        "Candy": ("#5a2a83", "#d65db1", "#fff8ff"),
        "Plain white": ("#ffffff", "#f0f3f7", "#172033"),
    }
    background_name = st.selectbox("Background", list(backgrounds.keys()))

    effects = {
        "None": "none",
        "Rain": "rain",
        "Snow": "snow",
        "Hail": "hail",
        "Wind gust": "wind",
        "Confetti": "confetti",
        "Tornado": "tornado",
    }
    effect_name = st.selectbox("Animated effect", list(effects.keys()))
    st.caption("Animations run continuously and are decorative.")

bg_top, bg_bottom, text_color = backgrounds[background_name]
safe_name = html.escape(name.strip() or "World")
safe_font = font_options[font_name]
effect = effects[effect_name]

# Each effect uses CSS-only loops, so there is no JavaScript dependency.
effect_css = {
    "none": "",
    "rain": """
      .particle { position:absolute; top:-15%; width:2px; height:22px; background:rgba(170,220,255,.85);
        border-radius:3px; animation: rain-fall linear infinite; }
      @keyframes rain-fall { to { transform:translate3d(-35px, 125vh, 0); } }
    """,
    "snow": """
      .particle { position:absolute; top:-10%; color:#fff; text-shadow:0 0 7px #b9e9ff;
        animation:snow-fall linear infinite; }
      @keyframes snow-fall { 50% { transform:translate3d(35px, 55vh, 0); }
        to { transform:translate3d(-20px, 115vh, 0) rotate(360deg); } }
    """,
    "hail": """
      .particle { position:absolute; top:-10%; width:7px; height:7px; border-radius:50%;
        background:#e8f7ff; box-shadow:0 0 8px #b8e5ff; animation:hail-fall .9s linear infinite; }
      @keyframes hail-fall { to { transform:translate3d(-25px, 120vh, 0); } }
    """,
    "wind": """
      .particle { position:absolute; left:-45%; height:2px; width:90px; border-radius:5px;
        background:rgba(255,255,255,.65); animation:wind-sweep 2.4s ease-in-out infinite; }
      @keyframes wind-sweep { 0% { transform:translateX(0) scaleX(.4); opacity:0; }
        25% { opacity:.9; } 100% { transform:translateX(170vw) scaleX(1.4); opacity:0; } }
    """,
    "confetti": """
      .particle { position:absolute; top:-12%; width:9px; height:15px; border-radius:2px;
        background:var(--confetti-color); animation:confetti-fall linear infinite; }
      @keyframes confetti-fall { to { transform:translate3d(55px, 120vh, 0) rotate(900deg); } }
    """,
    "tornado": """
      .particle { position:absolute; left:50%; top:50%; width:var(--trail-width); height:4px;
        border-radius:50%; background:rgba(255,255,255,.72); transform-origin:left center;
        animation:tornado-spin var(--duration) linear infinite; }
      @keyframes tornado-spin { from { transform:rotate(0deg) translateX(var(--radius)) scaleX(.7); opacity:.15; }
        50% { opacity:.9; } to { transform:rotate(360deg) translateX(var(--radius)) scaleX(.7); opacity:.15; } }
    """,
}

# Create repeatable particles with distinct delays and positions.
particles = []
if effect in ("rain", "snow", "hail", "confetti"):
    count = 75 if effect in ("rain", "snow", "confetti") else 38
    for i in range(count):
        left = (i * 37.7) % 100
        delay = -((i * 0.37) % 8)
        duration = 1.0 + ((i * 0.23) % (5.5 if effect != "hail" else 0.7))
        if effect == "snow":
            symbol = "❄" if i % 3 == 0 else "•"
            style = f"left:{left}%; animation-delay:{delay:.2f}s; animation-duration:{duration + 2:.2f}s; font-size:{10 + i % 16}px;"
            particles.append(f'<span class="particle" style="{style}">{symbol}</span>')
        elif effect == "confetti":
            colors = ["#ff4d6d", "#ffd166", "#06d6a0", "#4cc9f0", "#c77dff", "#ffffff"]
            style = f"left:{left}%; --confetti-color:{colors[i % len(colors)]}; animation-delay:{delay:.2f}s; animation-duration:{duration + 1:.2f}s;"
            particles.append(f'<span class="particle" style="{style}"></span>')
        else:
            style = f"left:{left}%; animation-delay:{delay:.2f}s; animation-duration:{duration:.2f}s;"
            particles.append(f'<span class="particle" style="{style}"></span>')
elif effect == "wind":
    for i in range(22):
        top = (i * 19.3) % 100
        delay = -((i * 0.29) % 3)
        style = f"top:{top}%; animation-delay:{delay:.2f}s; width:{45 + (i % 6) * 24}px;"
        particles.append(f'<span class="particle" style="{style}"></span>')
elif effect == "tornado":
    for i in range(42):
        style = (
            f"--radius:{18 + (i % 12) * 5}px; "
            f"--trail-width:{28 + (i % 7) * 5}px; "
            f"--duration:{1.4 + (i % 10) * .12:.2f}s; "
            f"animation-delay:{-i * .09:.2f}s; "
            f"top:{34 + (i % 30) * 1.1}%;"
        )
        particles.append(f'<span class="particle" style="{style}"></span>')

particles_html = "".join(particles)
escaped_effect = html.escape(effect_name)

st.markdown(
    f"""
    <style>
      .motion-stage {{
        position: relative; isolation: isolate; overflow: hidden;
        min-height: 420px; border-radius: 24px; padding: 24px;
        display: flex; align-items: center; justify-content: center;
        background: linear-gradient(135deg, {bg_top}, {bg_bottom});
        color: {text_color}; box-shadow: 0 12px 32px rgba(0,0,0,.16);
      }}
      .motion-stage .particle-layer {{ position:absolute; inset:0; overflow:hidden; z-index:0; pointer-events:none; }}
      .motion-stage .particle {{ pointer-events:none; }}
      .hello-content {{ position:relative; z-index:2; text-align:center; max-width:100%; overflow-wrap:anywhere; }}
      .hello-kicker {{ font: 600 13px/1.4 Arial, sans-serif; letter-spacing:.22em; text-transform:uppercase; opacity:.78; }}
      .hello-name {{ font-family:{safe_font}; font-size:clamp(24px, {font_size}px, 100px);
        line-height:1.15; font-weight:800; margin:18px 0; text-shadow:0 4px 18px rgba(0,0,0,.18); }}
      .hello-subtitle {{ font: 500 15px/1.5 Arial, sans-serif; opacity:.82; }}
      {effect_css.get(effect, "")}
      .motion-stage .particle-layer {{ z-index:1; }}
      .effect-pill {{ display:inline-block; margin-top:18px; padding:7px 12px; border:1px solid currentColor;
        border-radius:999px; font:600 12px Arial,sans-serif; opacity:.8; }}
      @media (prefers-reduced-motion: reduce) {{
        .motion-stage .particle {{ animation-duration: 20s !important; }}
      }}
    </style>
    <div class="motion-stage">
      <div class="particle-layer">{particles_html}</div>
      <div class="hello-content">
        <div class="hello-kicker">Welcome to the Motion Lab</div>
        <div class="hello-name">Hello, {safe_name}!</div>
        <div class="hello-subtitle">Your name. Your style. Your little corner of the web.</div>
        <div class="effect-pill">Effect: {escaped_effect}</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption("Tip: Change the controls in the sidebar to explore how a few settings can transform an app.")
