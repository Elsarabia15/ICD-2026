"""Arma presentacion.html (figuras SVG incrustadas) y la exporta a PDF con Chrome sin ventana.

Uso (desde la carpeta Proyecto):
    py Presentacion/figuras/generar_figuras_presentacion.py
    py Presentacion/construir.py
"""
import re
import subprocess
from pathlib import Path

AQUI = Path(__file__).resolve().parent
CHROME = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
          r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"]


def figura(m):
    nombre, escala = m.group(1), float(m.group(2))
    svg = (AQUI / "figuras" / f"{nombre}.svg").read_text(encoding="utf-8")
    svg = svg[svg.index("<svg"):]
    ancho_pt = float(re.search(r'width="([\d.]+)pt"', svg).group(1))
    svg = re.sub(r'\s(width|height)="[\d.]+pt"', "", svg, count=2)
    ancho_px = ancho_pt * 4 / 3 * escala
    return f'<div class="fig" style="width:{ancho_px:.0f}px; max-width:100%">{svg}</div>'


html = (AQUI / "plantilla.html").read_text(encoding="utf-8")
html = re.sub(r"\{\{fig:(\w+):([\d.]+)\}\}", figura, html)
(AQUI / "presentacion.html").write_text(html, encoding="utf-8")

exe = next(c for c in CHROME if Path(c).exists())
pdf = AQUI / "Presentacion-Proyecto-CMAPSS.pdf"
subprocess.run([exe, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                "--allow-file-access-from-files", f"--print-to-pdf={pdf}",
                (AQUI / "presentacion.html").as_uri()], check=True, timeout=120)
print("PDF:", pdf)
