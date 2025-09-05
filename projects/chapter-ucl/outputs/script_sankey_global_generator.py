# -*- coding: utf-8 -*-
"""
Sankey de dominios: dominio_fuente → dominio_meta (con exclusión de dominios)
"""

from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

# ======== CONFIG =========
INPUT_FILE = Path("corpus_metaforas.csv")
OUTPUT_HTML = Path("figura_5_0E_sankey_fuente_meta.html")
OUTPUT_PNG  = Path("figura_5_0E_sankey_fuente_meta.png")

TOP_N_LINKS   = 60
MIN_COUNT     = None

TRUNCATE_LABELS = 30
SHOW_PERCENT    = True
FONT_SIZE       = 12

# >>> Listas de dominios a omitir <<<
OMIT_SRC = ["UNA CONSTRUCCIÓN"]   # dominios fuente a excluir
OMIT_TGT = ["EL TRABAJO DE OBRA"] # dominios meta a excluir

# ======== CARGA Y PREP =========
def safe_read_csv(path: Path) -> pd.DataFrame:
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return pd.read_csv(path, encoding=enc)
        except Exception:
            continue
    raise RuntimeError(f"No pude leer el CSV: {path}")

df = safe_read_csv(INPUT_FILE)

required = {"dominio_fuente", "dominio_meta"}
missing = required.difference(df.columns)
if missing:
    raise ValueError(f"Faltan columnas: {missing}. Columnas: {list(df.columns)}")

df["dominio_fuente"] = df["dominio_fuente"].astype(str).str.strip()
df["dominio_meta"]   = df["dominio_meta"].astype(str).str.strip()

# === Filtrar dominios omitidos ===
df = df[~df["dominio_fuente"].isin(OMIT_SRC)]
df = df[~df["dominio_meta"].isin(OMIT_TGT)]

# Agregar flujos
flows = (df.groupby(["dominio_fuente","dominio_meta"])
           .size().reset_index(name="weight")
           .sort_values("weight", ascending=False))

total_weight = flows["weight"].sum()

if MIN_COUNT is not None:
    flows = flows[flows["weight"] >= MIN_COUNT]
if TOP_N_LINKS is not None:
    flows = flows.head(TOP_N_LINKS)

flows = flows.reset_index(drop=True)

# ======== NODOS =========
sources_unique = flows["dominio_fuente"].unique().tolist()
targets_unique = flows["dominio_meta"].unique().tolist()

node_labels_raw = sources_unique + targets_unique

def trunc(s, n=TRUNCATE_LABELS):
    s = str(s)
    if n is None or len(s) <= n:
        return s
    return s[:n-1] + "…"

node_labels = [trunc(s) for s in node_labels_raw]

idx_src = {lab: i for i, lab in enumerate(sources_unique)}
offset  = len(sources_unique)
idx_tgt = {lab: i + offset for i, lab in enumerate(targets_unique)}

# ======== ENLACES =========
sankey_src, sankey_tgt, sankey_val, custom_pct = [], [], [], []

for _, row in flows.iterrows():
    s, t, w = row["dominio_fuente"], row["dominio_meta"], int(row["weight"])
    sankey_src.append(idx_src[s])
    sankey_tgt.append(idx_tgt[t])
    sankey_val.append(w)
    custom_pct.append(100.0 * w / total_weight if SHOW_PERCENT and total_weight > 0 else None)

# ======== FIGURA =========
fig = go.Figure(data=[
    go.Sankey(
        arrangement="snap",
        node=dict(
            pad=18,
            thickness=16,
            line=dict(color="rgba(0,0,0,0.25)", width=0.6),
            label=node_labels,
            hovertemplate="%{label}<extra></extra>",
        ),
        link=dict(
            source=sankey_tgt, # Inversión columnas fuente y meta
            target=sankey_src, # Inversión columnas fuente y meta
            value=sankey_val,
            customdata=custom_pct,
            hovertemplate="%{target.label} → %{source.label}<br>" + # Inversión columnas fuente y meta
                          "freq: %{value}" +
                          (" — %{customdata:.1f}%" if SHOW_PERCENT else "") +
                          "<extra></extra>"
        )
    )
])

fig.update_layout(
    title=dict(
        text="Sankey — Metáforas del informe de la Comisión de la Verdad",
        x=0.5, xanchor="center"
    ),
    font=dict(size=FONT_SIZE),
    margin=dict(l=10, r=10, t=60, b=10),
    height=700,
)

# ======== EXPORTAR =========
fig.write_html(str(OUTPUT_HTML), include_plotlyjs="cdn")
print("✅ HTML:", OUTPUT_HTML.resolve())

try:
    fig.write_image(str(OUTPUT_PNG), scale=3)  # requiere kaleido
    print("✅ PNG :", OUTPUT_PNG.resolve())
except Exception as e:
    print("ℹ️ Para exportar PNG instala 'kaleido':  pip install -U kaleido")
    print("   Error:", e)