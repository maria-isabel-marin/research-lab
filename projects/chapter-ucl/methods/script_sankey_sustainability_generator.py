# -*- coding: utf-8 -*-
"""
Metáforas que contienen 'paz': dominios fuente y formulaciones
Autor: [Tu nombre]

Entrada esperada: CSV con columnas
  id, volumen, expresión, dominio_fuente, dominio_meta, metáfora

Salidas (en outputs_paz_contenido/):
  - paz_all.csv  (todas las filas que contienen 'paz' según KEYWORDS/REGEX)
  - fig_A_top_dom_fuente_paz.png
  - fig_B_sankey_fuente_a_metafora.html / .png (si kaleido)
  - fig_C_treemap_paz_domMeta_fuente.html / .png (si kaleido)
  - paz_all_ejemplos.csv (ejemplos por dominio)
"""

from pathlib import Path
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Plotly para Sankey y Treemap
import plotly.graph_objects as go
import plotly.express as px

# ===================== CONFIG =====================
INPUT_FILE = Path("corpus_metaforas.csv")   # <-- Cambia a tu ruta real si es necesario
OUTDIR = Path("outputs_sustainability_contenido")
OUTDIR.mkdir(exist_ok=True, parents=True)

# Palabras clave para "contiene paz"
# Puedes ampliar con 'pacificación', 'pacífica', etc. o usar REGEX si te conviene.
KEYWORDS = ["planta", "agua", "explotación", "agrícola", "agricultura", "campesino", 
        "narcotráfico", "coca", "cocaína", "semilla", "río", "territorio","tierra","étnia",
        "cultivo","campo","amazonía","ambiente","indígena"]     # se buscan en expresión, metáfora y dominio_meta
USE_REGEX = False       # si True, usa KEYWORDS como patrones regex exactos

# Sankey: top-N dominios_meta a mostrar y mínimo conteo por par (fuente→meta)
TOP_N_METAFORAS = 12
MIN_PAIR_COUNT = 1

# >>> Listas de dominios a omitir <<<
# Edita estas listas con coincidencias EXACTAS tal como aparecen en tu CSV:
EXCLUDE_SRC = [
    "UN SUJETO",
    "UN CICLO",
    "UNA BASE",
    "LA RECONSTRUCCIÓN DE LAS RELACIONES ROTAS POR LA GUERRA",
    "RECONSTRUCTORES DE EDIFICIOS EN RUINAS"
]
EXCLUDE_TGT = [
     "EL TRABAJO DE OBRA",
     "EL TOMO DE MI CUERPO ES LA VERDAD"
]

# Limitar cuántos dominios fuente se conectan a CADA dominio_meta en el Sankey
MAX_SOURCES_PER_TARGET = 8   # 0 o None = sin límite
TIEBREAK = "random"            # "alpha" (alfabético) | "random"
RANDOM_SEED = 42              # para desempate reproducible si TIEBREAK="random"

# Pares fuente→meta a excluir (coincidencia exacta, respetando acentos)
EXCLUDE_PAIRS = [
    # ("UNA CONSTRUCCIÓN", "EL TRABAJO DE OBRA"),
     ("UNA PERSONA", "LA COMISIÓN DE LA VERDAD")
]
# (Opcional) Exclusión por regex (case-insensitive): compila patrones fuente y meta
EXCLUDE_PAIRS_REGEX = [
    # (r"^una constru.*", r".*trabajo de obra$"),
]

# ==================================================

def limit_sources_per_target(pairs_df: pd.DataFrame,
                             max_sources: int = None,
                             tiebreak: str = "random",
                             seed: int = 42) -> pd.DataFrame:
    """
    Limita el número máximo de dominios_fuente por cada dominio_meta.
    Espera un DataFrame con columnas: ['dominio_fuente','dominio_meta','weight'].
    Ordena por weight DESC y aplica tiebreak para empates.
    """
    if not max_sources or max_sources <= 0:
        return pairs_df.copy()

    rng = np.random.RandomState(seed)
    out = []

    # Orden primario por peso desc; luego desempate
    for tgt, grp in pairs_df.groupby("dominio_meta", sort=False):
        # Ordenado por peso desc
        grp = grp.sort_values("weight", ascending=False).copy()

        # Desempate: dentro de cada bloque de igual peso
        if tiebreak == "alpha":
            # orden alfabético estable
            grp = grp.sort_values(["weight", "dominio_fuente"],
                                  ascending=[False, True])
        elif tiebreak == "random":
            # mismo peso -> barajar
            # aplicamos un índice aleatorio por cada fila para desempatar
            grp["_rand"] = rng.rand(len(grp))
            grp = grp.sort_values(["weight", "_rand"], ascending=[False, True]).drop(columns="_rand")
        else:
            # por defecto, alfabético
            grp = grp.sort_values(["weight", "dominio_fuente"],
                                  ascending=[False, True])

        out.append(grp.head(max_sources))

    return pd.concat(out, axis=0).reset_index(drop=True)

def read_csv_safely(path: Path) -> pd.DataFrame:
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return pd.read_csv(path, encoding=enc)
        except Exception:
            continue
    raise RuntimeError(f"No pude leer el CSV: {path}")

# ---------- CARGA ----------
df = read_csv_safely(INPUT_FILE)

required = ["id", "volumen", "expresión", "dominio_fuente", "dominio_meta", "metáfora"]
missing = [c for c in required if c not in df.columns]
if missing:
    raise ValueError(f"Faltan columnas requeridas: {missing}. Columnas disponibles: {list(df.columns)}")

# Normalización básica
for c in required:
    df[c] = df[c].astype(str).fillna("").str.strip()

# === Filtro global por dominios a omitir (se aplica a todo el pipeline) ===
if EXCLUDE_SRC:
    df = df[~df["dominio_fuente"].isin(EXCLUDE_SRC)]
if EXCLUDE_TGT:
    df = df[~df["dominio_meta"].isin(EXCLUDE_TGT)]

def contains_keywords(text: str, keywords, use_regex=False) -> bool:
    t = text.lower()
    if use_regex:
        for kw in keywords:
            if re.search(kw, t):
                return True
    else:
        for kw in keywords:
            if kw.lower() in t:
                return True
    return False

# ---------- FILTRO: “metáforas que contienen paz” ----------
mask_paz = (
    # df["expresión"].apply(lambda x: contains_keywords(x, KEYWORDS, USE_REGEX)) |
    df["metáfora"].apply(lambda x: contains_keywords(x, KEYWORDS, USE_REGEX)) |
    df["dominio_meta"].apply(lambda x: contains_keywords(x, KEYWORDS, USE_REGEX))
)

df_paz_any = df[mask_paz].copy()
df_paz_any.to_csv(OUTDIR / "paz_all.csv", index=False)
print(f"✅ Filas con 'paz' (o KEYWORDS): {len(df_paz_any)}  →  {OUTDIR/'paz_all.csv'}")

# ---------- FIGURA A: Top dominios fuente ----------
vc_fuente = df_paz_any["dominio_fuente"].value_counts().reset_index()
vc_fuente.columns = ["dominio_fuente", "frecuencia"]

plt.figure(figsize=(10, 7))
plt.barh(vc_fuente["dominio_fuente"].head(20), vc_fuente["frecuencia"].head(20))
plt.gca().invert_yaxis()
plt.xlabel("Frecuencia")
plt.title("Figura A. Top dominios fuente en metáforas que contienen 'paz'")
plt.tight_layout()
plt.savefig(OUTDIR / "fig_A_top_dom_fuente_paz.png", dpi=300, bbox_inches="tight")
plt.close()
print(f"✅ Figura A guardada: {OUTDIR/'fig_A_top_dom_fuente_paz.png'}")

# ---------- FIGURA B: Sankey (dominio_fuente → dominio_meta con 'paz') ----------

def filter_pairs_exact(df_pairs, exclude_pairs):
    """Excluye pares exactos (fuente, meta)."""
    if not exclude_pairs:
        return df_pairs
    excl = {(s.strip(), t.strip()) for (s, t) in exclude_pairs}
    mask = df_pairs.apply(
        lambda r: (str(r["dominio_fuente"]).strip(), str(r["dominio_meta"]).strip()) in excl,
        axis=1
    )
    return df_pairs[~mask].copy()

def filter_pairs_regex(df_pairs, exclude_pairs_regex):
    """Excluye pares que cumplan patrones regex (case-insensitive)."""
    if not exclude_pairs_regex:
        return df_pairs
    comp = [(re.compile(s, re.I), re.compile(t, re.I)) for (s, t) in exclude_pairs_regex]
    def match_any(s, t):
        s = str(s); t = str(t)
        return any(s_pat.search(s) and t_pat.search(t) for (s_pat, t_pat) in comp)
    mask = df_pairs.apply(lambda r: match_any(r["dominio_fuente"], r["dominio_meta"]), axis=1)
    return df_pairs[~mask].copy()

# Agrupamos por (dominio_fuente, dominio_meta) restringiendo a filas que contienen KEYWORDS
df_paz_meta = df_paz_any.copy()

pairs = (df_paz_meta.groupby(["dominio_fuente","dominio_meta"])
         .size().reset_index(name="weight")
         .sort_values("weight", ascending=False))

# Filtrar por mínimo conteo
if MIN_PAIR_COUNT > 1:
    pairs = pairs[pairs["weight"] >= MIN_PAIR_COUNT]

# Tomar top-N dominios_meta (para legibilidad); retenemos todas las fuentes que conectan con esas metas
top_metas = pairs["dominio_meta"].value_counts().head(TOP_N_METAFORAS).index.tolist()
pairs_top = pairs[pairs["dominio_meta"].isin(top_metas)].copy()

# Excluir pares fuente→meta no deseados
pairs_top = filter_pairs_exact(pairs_top, EXCLUDE_PAIRS)
pairs_top = filter_pairs_regex(pairs_top, EXCLUDE_PAIRS_REGEX)

# Limitar el número de dominios_fuente por cada dominio_meta (N máx. por target)
pairs_top = limit_sources_per_target(
    pairs_top,
    max_sources=MAX_SOURCES_PER_TARGET,
    tiebreak=TIEBREAK,
    seed=RANDOM_SEED
)

# Construcción sankey
sources = pairs_top["dominio_fuente"].unique().tolist()
targets = pairs_top["dominio_meta"].unique().tolist()
node_labels = sources + targets

# Indices
idx_src = {s: i for i, s in enumerate(sources)}
offset = len(sources)
idx_tgt = {t: i + offset for i, t in enumerate(targets)}

sankey_src = [idx_src[s] for s in pairs_top["dominio_fuente"]]
sankey_tgt = [idx_tgt[t] for t in pairs_top["dominio_meta"]]
sankey_val = pairs_top["weight"].tolist()

fig_sankey = go.Figure(data=[
    go.Sankey(
        arrangement="snap",
        node=dict(
            pad=100,              # ↑ espacio vertical entre nodos
            thickness=5,        # ↓ grosor del nodo (más “aire”)
            line=dict(color="rgba(0,0,0,0.25)", width=0.6),
            label=node_labels,
            hovertemplate="%{label}<extra></extra>",
        ),
        link=dict(
            source=sankey_tgt, # Cambio el orden
            target=sankey_src,# Cambio el orden
            value=sankey_val,
            hovertemplate="%{target.label} → %{source.label}<br>freq: %{value}<extra></extra>",
            # hovertemplate="%{source.label} → %{target.label}<br>freq: %{value}<extra></extra>",
        ),
    )
])
fig_sankey.update_layout(
    title=dict(text="Sankey — Metáforas de 'sustentabilidad'", x=0.5),
    font=dict(size=10),
    margin=dict(l=10, r=10, t=60, b=10),
    height=1000,         # ↑ altura total para más aire vertical
)
html_sankey = OUTDIR / "fig_B_sankey_fuente_a_metafora.html"
fig_sankey.write_html(str(html_sankey), include_plotlyjs="cdn")
print(f"✅ Sankey HTML: {html_sankey}")

try:
    fig_sankey.write_image(str(OUTDIR / "fig_B_sankey_fuente_a_metafora.png"), scale=3)
    print(f"✅ Sankey PNG: {OUTDIR/'fig_B_sankey_fuente_a_metafora.png'}")
except Exception as e:
    print("ℹ️ Para exportar PNG instala 'kaleido':  pip install -U kaleido")

# ---------- FIGURA C: Treemap (PAZ → dominio_meta (con KEYWORDS) → dominio_fuente) ----------
df_paz_dommeta = df_paz_any[df_paz_any["dominio_meta"].apply(lambda x: contains_keywords(x, KEYWORDS, USE_REGEX))].copy()

if len(df_paz_dommeta) > 0:
    # Construimos tamaño por (dominio_meta, dominio_fuente)
    agg = (df_paz_dommeta.groupby(["dominio_meta","dominio_fuente"])
           .size().reset_index(name="weight")
           .sort_values("weight", ascending=False))
    
    # Función para cortar etiquetas largas con saltos de línea cada 20 caracteres
    def wrap_label(s, width=20):
        s = str(s)
        return "<br>".join([s[i:i+width] for i in range(0, len(s), width)])
    
    agg["dominio_meta_wrapped"] = agg["dominio_meta"].apply(wrap_label)
    agg["dominio_fuente_wrapped"] = agg["dominio_fuente"].apply(wrap_label)

    # Treemap jerárquico con etiquetas envueltas
    fig_tree = px.treemap(
        agg,
        path=["dominio_meta_wrapped", "dominio_fuente_wrapped"],  # jerarquía
        values="weight",
        title="Figura C. Treemap — dominios meta (con KEYWORDS) → dominios fuente",
    )
    fig_tree.update_traces(root_color="lightgrey")
    fig_tree.update_layout(
        margin=dict(l=10, r=10, t=60, b=10),
        uniformtext=dict(minsize=10, mode="show")
    )

    html_tree = OUTDIR / "fig_C_treemap_paz_domMeta_fuente.html"
    fig_tree.write_html(str(html_tree), include_plotlyjs="cdn")
    print(f"✅ Treemap HTML: {html_tree}")
    try:
        fig_tree.write_image(str(OUTDIR / "fig_C_treemap_paz_domMeta_fuente.png"), scale=3)
        print(f"✅ Treemap PNG: {OUTDIR/'fig_C_treemap_paz_domMeta_fuente.png'}")
    except Exception:
        print("ℹ️ Para exportar PNG instala 'kaleido':  pip install -U kaleido")
else:
    print("ℹ️ No hay filas donde 'dominio_meta' contenga KEYWORDS; se omite treemap.")

# ---------- Tabla de ejemplos por dominio ----------
# Para cada dominio_fuente (top 10), extraemos 1-2 ejemplos con KEYWORDS en metáfora/expresión/meta
ejemplos = []
top_sources = vc_fuente["dominio_fuente"].head(10).tolist()
for src in top_sources:
    sample = df_paz_any[df_paz_any["dominio_fuente"] == src].head(2)
    for _, r in sample.iterrows():
        ejemplos.append({
            "volumen": r["volumen"],
            "dominio_fuente": r["dominio_fuente"],
            "dominio_meta": r["dominio_meta"],
            "metáfora": r["metáfora"],
            "expresión": r["expresión"],
        })

ej_df = pd.DataFrame(ejemplos)
ej_out = OUTDIR / "paz_all_ejemplos.csv"
ej_df.to_csv(ej_out, index=False)
print(f"✅ Ejemplos guardados: {ej_out}")

print("\nListo. Salidas en:", OUTDIR.resolve())