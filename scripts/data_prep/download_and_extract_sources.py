#!/usr/bin/env python3
"""Download available source PDFs/HTML pages and extract text.

Outputs:
- docs/research/papers/S###-slug.{pdf,html}
- docs/research/paper-text/S###-slug.md
- docs/research/papers/manifest.md
"""
from __future__ import annotations

import html
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

import fitz  # PyMuPDF
import requests

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs/research/source-ledger.md"
PAPERS = ROOT / "docs/research/papers"
TEXTS = ROOT / "docs/research/paper-text"
MANIFEST = PAPERS / "manifest.md"
PAPERS.mkdir(parents=True, exist_ok=True)
TEXTS.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/125 Safari/537.36 hibah-riset-research-bot"
}
TIMEOUT = 35

EXPLICIT_PDFS = {
    "S001": ["https://arxiv.org/pdf/2601.12882"],
    "S003": ["https://arxiv.org/pdf/2405.14458"],
    "S004": ["https://openaccess.thecvf.com/content/CVPR2024/papers/Zhao_DETRs_Beat_YOLOs_on_Real-time_Object_Detection_CVPR_2024_paper.pdf", "https://arxiv.org/pdf/2304.08069"],
    "S005": ["https://arxiv.org/pdf/2410.13842", "https://openreview.net/pdf?id=MFZjrTFE7h"],
    "S007": ["https://arxiv.org/pdf/2511.09554", "https://openreview.net/pdf?id=qHm5GePxTh"],
    "S009": ["https://www.mdpi.com/2076-3417/15/13/7533/pdf?download=1"],
    "S010": ["https://www.mdpi.com/2073-431X/14/11/476/pdf?download=1"],
    "S011": ["https://www.mdpi.com/2313-433X/12/1/27/pdf?download=1"],
    "S013": ["https://www.nature.com/articles/s41598-026-43938-2.pdf"],
    "S014": ["https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0342246&type=printable"],
    "S015": ["https://openaccess.thecvf.com/content/CVPR2025/papers/Shim_Focusing_on_Tracks_for_Online_Multi-Object_Tracking_CVPR_2025_paper.pdf"],
    "S016": ["https://openaccess.thecvf.com/content/CVPR2025/papers/Gao_Multiple_Object_Tracking_as_ID_Prediction_CVPR_2025_paper.pdf"],
    "S017": ["https://openaccess.thecvf.com/content/WACV2025/papers/Galoaa_DragonTrack_Transformer-Enhanced_Graphical_Multi-Person_Tracking_in_Complex_Scenarios_WACV_2025_paper.pdf"],
    "S018": ["https://www.mdpi.com/2076-3417/15/24/13030/pdf?download=1"],
    "S021": ["https://openaccess.thecvf.com/content/CVPR2024/papers/Lv_DiffMOT_A_Real-time_Diffusion-based_Multiple_Object_Tracker_with_Non-linear_Prediction_CVPR_2024_paper.pdf", "https://arxiv.org/pdf/2403.02075"],
    "S024": ["https://openaccess.thecvf.com/content/CVPR2023/papers/Cao_Observation-Centric_SORT_Rethinking_SORT_for_Robust_Multi-Object_Tracking_CVPR_2023_paper.pdf", "https://arxiv.org/pdf/2203.14360"],
    "S028": ["https://www.nature.com/articles/s41598-025-90750-5.pdf"],
    "S033": ["https://openaccess.thecvf.com/content/CVPR2024/papers/Ranasinghe_CrowdDiff_Multi-Hypothesis_Crowd_Density_Estimation_Using_Diffusion_Models_CVPR_2024_paper.pdf", "https://arxiv.org/pdf/2303.12790"],
    "S036": ["https://arxiv.org/pdf/2003.09003"],
    "S037": ["https://arxiv.org/pdf/2111.14690"],
    "S038": ["https://arxiv.org/pdf/1805.00123"],
}


def slugify(text: str, maxlen: int = 70) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return text[:maxlen].strip("-") or "source"


def parse_ledger():
    rows = []
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| S"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 11:
            continue
        sid, use, status, topic, source_note, year, title, urls, evidence, risk, mapped = cells[:11]
        rows.append({
            "id": sid,
            "use": use,
            "status": status,
            "topic": topic,
            "source_note": source_note,
            "year": year,
            "title": title,
            "urls": [u.strip() for u in re.split(r"\s*;\s*", urls) if u.strip().startswith("http")],
            "evidence": evidence,
            "risk": risk,
            "mapped": mapped,
        })
    return rows


def is_pdf_response(resp: requests.Response) -> bool:
    ctype = resp.headers.get("content-type", "").lower()
    return "pdf" in ctype or resp.content[:4] == b"%PDF"


def get(url: str) -> requests.Response:
    return requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)


def extract_pdf_links(html_text: str, base_url: str) -> list[str]:
    links = []
    for href in re.findall(r'href=["\']([^"\']+)["\']', html_text, flags=re.I):
        low = href.lower()
        if any(x in low for x in [".pdf", "/pdf", "download"]):
            links.append(urljoin(base_url, html.unescape(href)))
    # preserve order / unique
    out = []
    for l in links:
        if l not in out:
            out.append(l)
    return out


def html_to_text(html_text: str) -> str:
    text = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", html_text)
    text = re.sub(r"(?is)<br\s*/?>", "\n", text)
    text = re.sub(r"(?is)</(p|div|h[1-6]|li|tr|section|article)>", "\n", text)
    text = re.sub(r"(?is)<.*?>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    return text.strip()


def extract_pdf_text(pdf_path: Path) -> str:
    doc = fitz.open(pdf_path)
    parts = []
    meta = doc.metadata or {}
    parts.append(f"# Extracted text: {pdf_path.name}\n")
    if meta:
        parts.append("## PDF metadata\n" + "\n".join(f"- {k}: {v}" for k, v in meta.items() if v) + "\n")
    for i, page in enumerate(doc, start=1):
        txt = page.get_text("text")
        parts.append(f"\n\n## Page {i}\n\n{txt}")
    return "".join(parts)


def try_download_pdf(sid: str, slug: str, candidates: list[str]) -> tuple[Path | None, str | None]:
    seen = []
    for url in candidates:
        if url in seen:
            continue
        seen.append(url)
        try:
            resp = get(url)
            if resp.status_code >= 400:
                continue
            if is_pdf_response(resp):
                out = PAPERS / f"{sid}-{slug}.pdf"
                out.write_bytes(resp.content)
                return out, url
            # If candidate page has PDF links, chase first few.
            ctype = resp.headers.get("content-type", "").lower()
            if "html" in ctype or resp.text[:100].lstrip().startswith("<"):
                for link in extract_pdf_links(resp.text, resp.url)[:8]:
                    try:
                        r2 = get(link)
                        if r2.status_code < 400 and is_pdf_response(r2):
                            out = PAPERS / f"{sid}-{slug}.pdf"
                            out.write_bytes(r2.content)
                            return out, link
                    except Exception:
                        continue
        except Exception:
            continue
    return None, None


def save_html_source(row: dict, slug: str) -> tuple[Path | None, str | None]:
    for url in row["urls"]:
        try:
            resp = get(url)
            if resp.status_code >= 400:
                continue
            out = PAPERS / f"{row['id']}-{slug}.html"
            out.write_text(resp.text, encoding="utf-8", errors="ignore")
            return out, resp.url
        except Exception:
            continue
    return None, None


def main() -> int:
    rows = parse_ledger()
    manifest_rows = []
    for row in rows:
        sid = row["id"]
        slug = slugify(row["title"])
        print(f"[{sid}] {row['title']}")
        candidates = []
        candidates.extend(EXPLICIT_PDFS.get(sid, []))
        candidates.extend(row["urls"])
        if any("arxiv.org/abs/" in u for u in row["urls"]):
            for u in row["urls"]:
                m = re.search(r"arxiv\.org/abs/([0-9.]+)", u)
                if m:
                    candidates.insert(0, f"https://arxiv.org/pdf/{m.group(1)}")
        file_path, source_url = try_download_pdf(sid, slug, candidates)
        kind = "pdf"
        note = "downloaded PDF"
        if file_path is None:
            file_path, source_url = save_html_source(row, slug)
            kind = "html"
            note = "saved source page HTML; PDF not openly downloadable by script"
        if file_path is None:
            manifest_rows.append([sid, row["title"], "failed", "", "Could not download PDF/HTML"])
            print("  -> failed")
            continue
        text_path = TEXTS / f"{sid}-{slug}.md"
        try:
            if kind == "pdf":
                text = extract_pdf_text(file_path)
            else:
                text = f"# Extracted text: {file_path.name}\n\nSource URL: {source_url}\n\n" + html_to_text(file_path.read_text(encoding="utf-8", errors="ignore"))
            header = (
                f"---\nsource_id: {sid}\ntitle: {row['title']}\nsource_url: {source_url}\n"
                f"source_file: {file_path.relative_to(ROOT)}\nsource_kind: {kind}\nextraction_note: {note}\n---\n\n"
            )
            text_path.write_text(header + text[:400000], encoding="utf-8")
            manifest_rows.append([sid, row["title"], kind, str(file_path.relative_to(ROOT)), note])
            print(f"  -> {kind} {file_path.name}")
        except Exception as e:
            manifest_rows.append([sid, row["title"], kind, str(file_path.relative_to(ROOT)), f"extract failed: {e}"])
            print(f"  -> extract failed {e}")
        time.sleep(0.4)

    lines = [
        "# Downloaded Source Manifest\n",
        "> Generated by `scripts/download_and_extract_sources.py`. PDFs are saved when openly downloadable; otherwise source HTML pages are saved for traceability.\n",
        "| ID | Title/source | Saved kind | Path | Note |",
        "|---|---|---|---|---|",
    ]
    for sid, title, kind, path, note in manifest_rows:
        lines.append(f"| {sid} | {title.replace('|','/')} | {kind} | `{path}` | {note.replace('|','/')} |")
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
