import os
import warnings
from pathlib import Path

import gradio as gr
from deoldify import device
from deoldify.device_id import DeviceId
from deoldify.visualize import get_image_colorizer
from huggingface_hub import snapshot_download

# Print the installed Python packages (mainly useful for debugging the environment).
os.system("pip freeze")

# Silence a specific noisy UserWarning coming from DeOldify / dependencies.
warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")

# ---- Model setup ----
# Start on CPU so DeOldify can safely initialize before switching to GPU.
device.set(device=DeviceId.CPU)

# ID of the DeOldify model repository hosted on Hugging Face Hub.
REPO_ID = "allinaseri/deoldify"

# Download the full model snapshot (weights + config) to a local folder cache.
snapshot_folder = snapshot_download(repo_id=REPO_ID)

# Switch computation to the first GPU (GPU0) to speed up colorization.
device.set(device=DeviceId.GPU0)

# Create an image colorizer using the downloaded model files.
# 'artistic=True' uses the more vivid / stylized DeOldify model.
colorizer = get_image_colorizer(root_folder=Path(snapshot_folder), artistic=True)


def predict(image_path, render_factor):
    """
    Take a grayscale image path and a render factor, and return a colorized image.
    The render factor controls how much detail the model tries to add.
    """
    return colorizer.get_transformed_image(
        image_path,
        render_factor=int(render_factor),
        watermarked=False,  # Do not add DeOldify watermark on the output image.
    )


# ---- UI text content ----
TITLE = "Colorize Me🎨"

# Short description shown at the top of the app to explain what it does.
DESCRIPTION_MD = """
Colorize grayscale(black/white) images using DeOldify.

- Upload a grayscale image
- Tune the render factor
- Download the colorized output
"""

# Footer with contact email and reference paper link.
FOOTER_MD = """
Questions / comments: `ali.naseri3179@gmail.com`

Base Article: [https://www.ipol.im/pub/art/2022/403/article_lr.pdf](https://www.ipol.im/pub/art/2022/403/article_lr.pdf)  
If you like this Space, consider giving a ⭐.
"""

# Extra tips to help users pick a good render factor.
TIPS_MD = """
- Try 25–35 for most images.
- If faces look odd, lower the render factor a bit.
- Very small images may produce weaker results.
"""

# ---- Gradio theme and custom CSS ----
# Use Gradio's built‑in Glass theme with some custom color / spacing tweaks.
THEME = gr.themes.Glass(
    primary_hue="blue",
    neutral_hue="slate",
    radius_size="lg",
    spacing_size="md",
)

# Custom CSS to give the app a polished, responsive “glassmorphism” look.
CSS = """
/* ---------- Fluid typography scale ---------- */
/* Make font size adapt slightly to screen size, but keep it within a comfortable range */
.gradio-container{
  font-size: clamp(15px, 0.35vw + 16px, 20px);
  line-height: 1.55;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
}

/* Keep text readable everywhere */
p, li, ol { color: #f5f5f5; font-size: 1rem; line-height: 1.6; }
small { font-size: 0.875rem; }
a { color: f8f8f8}
/* Headings: fluid + consistent spacing */
h1 { color:#f5f5f5; font-size: clamp(1.55rem, 1.1rem + 2.2vw, 2.4rem); line-height: 1.15; margin: 0.2em 0 0.35em; }
h2 { color:#f5f5f5; font-size: clamp(1.25rem, 1.0rem + 1.5vw, 1.75rem); line-height: 1.2;  margin: 0.25em 0 0.35em; }
h3 { color:#f5f5f5; font-size: clamp(1.10rem, 0.95rem + 0.9vw, 1.35rem); line-height: 1.25; margin: 0.25em 0 0.35em; }
h4,h5,h6 { color:#f5f5f5; font-size: clamp(1.0rem, 0.95rem + 0.4vw, 1.15rem); line-height: 1.3; }

/* Align markdown titles inside the custom header container */
#app_title h1, #app_title h2, #app_title h3 { margin-bottom: 6px; }

/* ---------- Responsive app shell ---------- */
/* Center the app, set a max width, and give it a dark glass background */
.gradio-container {
  width: min(1040px, calc(100% - 24px)) !important;
  max-width: 100% !important;
  margin: 5px auto !important;
  border-radius: 22px;
  padding: clamp(10px, 2vw, 18px);
  background:
    radial-gradient(900px 500px at 15% 0%, rgba(59,130,246,0.18), rgba(0,0,0,0)),
    radial-gradient(700px 420px at 110% 10%, rgba(37,99,235,0.14), rgba(0,0,0,0)),
    #0b1220 !important;
  border: 1px solid rgba(148,163,184,0.12);
  box-shadow: 0 18px 60px rgba(0,0,0,0.45);
}

/* ---------- Glass / blur cards ---------- */
/* Reusable card style for the main app sections, with blur and subtle border. */
#app_card, #io_card {
  background: rgba(2, 6, 23, 0.38);
  border: 1px solid rgba(148, 163, 184, 0.16);
  border-radius: 18px;
  -webkit-backdrop-filter: blur(18px) saturate(140%);
  backdrop-filter: blur(18px) saturate(140%);
  box-shadow:
    0 10px 30px rgba(0,0,0,0.38),
    0 0 0 1px rgba(148, 163, 184, 0.08) inset;
  will-change: backdrop-filter;
}

/* Inner padding of the main sections. */
#app_card { padding: 12px; }
#io_card  { padding: 8px; }

/* Header layout tweaks: spacing around title and description. */
#app_header { padding: 18px 18px 6px 18px; }
#app_desc p { margin: 0.4rem 0; }

/* ---------- Buttons ---------- */
/* Give the Colorize button a clear size and rounded corners. */
#colorize_btn { min-height: 2.75rem; border-radius: 14px; font-weight: 650; }

/* Your existing button styles (keep) */
#colorize_btn button {
  font-size: 1rem;
  padding: 0.65rem 1rem;
  background: linear-gradient(180deg, rgba(59,130,246,0.95), rgba(37,99,235,0.95)) !important;
  border: 1px solid rgba(147,197,253,0.25) !important;
  box-shadow: 0 10px 20px rgba(37,99,235,0.25) !important;

  /* Needed for the animated border layer */
  position: relative;
  border-radius: 12px; /* adjust if you want pill style */
  isolation: isolate;  /* keeps pseudo elements behind content cleanly */
}

#colorize_btn button:hover { filter: brightness(1.05); }

/* Turn on the “AI working” ring only while loading */
#colorize_btn button.is-loading::before {
  content: "";
  position: absolute;
  inset: -3px;          /* ring sits slightly outside */
  padding: 2px;         /* ring thickness */
  border-radius: inherit;
  pointer-events: none;
  z-index: -1;

  /* Rotating ring */
  background: conic-gradient(
    from 0deg,
    rgba(147,197,253,0.15),
    rgba(147,197,253,0.95),
    rgba(59,130,246,0.25),
    rgba(147,197,253,0.15)
  );

  /* Mask out the middle so only the border area is visible */
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
          mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
          mask-composite: exclude;

  animation: aiRingSpin 1.1s linear infinite;
}

/


/* ---------- Embedded Space responsiveness ---------- */
/* Style for when this app is embedded in another page via iframe. */
.hf-embed {
  width: 100%;
  border: 0;
  border-radius: 12px;
  display: block;
  height: 780px;
}

/* Mobile */
@media (max-width: 640px) {
    li{
    color:#808080 ;
    }
  /* Slightly different layout and font size for small screens. */
  .gradio-container {
    width: calc(100% - 12px) !important;
    margin: 4px auto !important;
    padding: 6px;
    font-size: clamp(15px, 0.7vw + 13px, 17px); /* slightly larger on small screens */
  }
  #app_header { padding: 14px 12px 4px 12px; }
  #app_card, #io_card { border-radius: 16px; }
  .hf-embed { height: 560px; }
}

/* Very small devices: reduce the iframe height to fit better. */
@media (max-width: 420px) {
  .hf-embed { height: 520px; }
}

/* Touch devices: slightly reduce blur for better performance. */
@media (max-width: 768px) and (hover: none) {
  #app_card, #io_card {
    -webkit-backdrop-filter: blur(12px) saturate(135%);
    backdrop-filter: blur(12px) saturate(135%);
  }
}
"""


# ---- Gradio interface layout ----
with gr.Blocks(title=TITLE, theme=THEME, css=CSS) as demo:
    # Top section: title + short explanation.
    with gr.Column(elem_id="app_header"):
        gr.Markdown(f"## {TITLE}", elem_id="app_title")
        gr.Markdown(DESCRIPTION_MD, elem_id="app_desc")

    # Main card that holds inputs, outputs, tips, and footer.
    with gr.Column(elem_id="app_card"):
        # Two-column layout: left = inputs, right = output.
        with gr.Row(equal_height=True):
            # Left column: image upload, render slider, buttons.
            with gr.Column(scale=1, elem_id="io_card"):
                # Input image component; Gradio passes the file path to the function.
                inp = gr.Image(
                    type="filepath",
                    label="Input (grayscale)",
                    sources=["upload"],
                )

                # Slider to control the render factor parameter for the model.
                render = gr.Slider(
                    minimum=1,
                    maximum=45,
                    value=35,
                    step=1,
                    label="Render factor",
                    info="Higher can add detail but may introduce artifacts.",
                )

                # Buttons row: run colorization or clear everything.
                with gr.Row():
                    btn = gr.Button("Colorize", variant="primary", elem_id="colorize_btn")
                    clear = gr.Button("Clear")

            # Right column: shows the colorized image returned by the model.
            with gr.Column(scale=1, elem_id="io_card"):
                out = gr.Image(type="pil", label="Output (colorized)")

        # Collapsible panel with usage tips.
        with gr.Accordion("Tips", open=False):
            gr.Markdown(TIPS_MD)

        # Footer with contact info and reference.
        gr.Markdown(FOOTER_MD)

    # Wire the Colorize button to the predict() function.
    # Inputs: uploaded image + render factor slider; Output: colorized image.
    btn.click(fn=predict, inputs=[inp, render], outputs=out)

    # Clear button resets image, slider value, and output preview.
    clear.click(fn=lambda: (None, 35, None), inputs=None, outputs=[inp, render, out])

# Enable request queuing (better for multiple users) and launch the app.
demo.queue().launch()
