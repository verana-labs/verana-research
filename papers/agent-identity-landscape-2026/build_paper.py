#!/usr/bin/env python3
"""Render landscape-paper.md into the Verana Research paper template.

Handles the markdown subset the paper uses: #/##/### headings, paragraphs,
ordered lists, one table, ---, **bold**, *italic*, [text](url), bare URLs,
and [n]-prefixed reference paragraphs. Fonts are inlined from the built
webinar deck so the page is fully self-contained.
"""
import os, re, html as htmlmod

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(HERE, "landscape-paper.md")
OUT = os.path.join(HERE, "landscape-paper.html")
DECK = os.path.join(HERE, "..", "..", "webinars", "2026-09-17-eclipse-models-for-privacy",
                    "verana-verifiable-trust-eclipse-webinar-v4.html")

fonts = "\n".join(re.findall(r"@font-face \{[^}]*\}", open(DECK).read()))
assert fonts.count("@font-face") == 4

def inline(s):
    s = htmlmod.escape(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"(?<![\"'>=\w])(https?://[^\s<·]+[^\s<·.,;)])", r'<a href="\1">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    return s

src = open(MD).read()
blocks = re.split(r"\n\s*\n", src.strip())

body = []
in_refs = False
title = subtitle = ""
meta_done = 0

for b in blocks:
    lines = [l.rstrip() for l in b.strip().split("\n")]
    first = lines[0]

    if first.startswith("# "):
        title = first[2:].strip()
        continue
    if first.startswith("*A comparative") and not subtitle:
        subtitle = inline(first.strip("*"))
        continue
    if first.startswith("**Fabrice"):
        body.append('<p class="authors">' + "<br>".join(inline(l) for l in lines) + "</p>")
        continue
    if first.startswith("*Version") or first.startswith("*Companion"):
        body.append('<p class="meta">' + "<br>".join(inline(l.strip("*")) for l in lines) + "</p>")
        continue
    if first == "---":
        body.append("<hr>")
        continue
    if first.startswith("## "):
        h = first[3:].strip()
        if h == "References":
            in_refs = True
        body.append("<h2>" + inline(h) + "</h2>")
        continue
    if first.startswith("### "):
        body.append("<h3>" + inline(first[4:].strip()) + "</h3>")
        continue
    if first.startswith("|"):
        rows = [l for l in lines if l.startswith("|")]
        head = [c.strip() for c in rows[0].strip("|").split("|")]
        out = ['<div class="tablewrap"><table><thead><tr>']
        out += ["<th>" + inline(c) + "</th>" for c in head]
        out.append("</tr></thead><tbody>")
        for r in rows[2:]:
            cells = [c.strip() for c in r.strip("|").split("|")]
            out.append("<tr>" + "".join(
                ('<td class="k">' if i == 0 else "<td>") + inline(c) + "</td>"
                for i, c in enumerate(cells)) + "</tr>")
        out.append("</tbody></table></div>")
        body.append("".join(out))
        continue
    if re.match(r"^\d+\.\s", first):
        out = ["<ol>"]
        for l in lines:
            m = re.match(r"^\d+\.\s+(.*)$", l)
            out.append("<li>" + inline(m.group(1)) + "</li>")
        out.append("</ol>")
        body.append("".join(out))
        continue
    if in_refs and re.match(r"^\[\d+\]\s", first):
        m = re.match(r"^\[(\d+)\]\s+(.*)$", " ".join(lines))
        body.append('<p class="ref"><span class="refno">[' + m.group(1) + "]</span> "
                    + inline(m.group(2)) + "</p>")
        continue
    if first.startswith("*©"):
        body.append('<p class="colophon">' + inline(" ".join(lines).strip("*")) + "</p>")
        continue
    # abstract paragraph gets its own card: detect by previous h2
    text = inline(" ".join(lines))
    if body and body[-1] == "<h2>Abstract</h2>":
        body.append('<div class="abstract"><p>' + text + "</p></div>")
    else:
        body.append("<p>" + text + "</p>")

article = "\n".join(body)

page = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
__FONTS__
  :root {
    --bg: #FAF9FD; --surface: #FFFFFF; --ink: #17131F; --muted: #5B5470;
    --faint: #8A84A0; --purple: #6B2FD9; --green: #0E8A6D;
    --line: #E2DEEE; --line-soft: #ECE9F4; --soft: #F1EBFD;
  }
  html.dark {
    --bg: #0A0910; --surface: #131019; --ink: #F0EDF8; --muted: #A39CB8;
    --faint: #6E6885; --purple: #9F7AEA; --green: #3FBF9A;
    --line: #272236; --line-soft: #1E1A2B; --soft: #1E1631;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: var(--bg); color: var(--ink);
    font-family: "InterD", system-ui, sans-serif;
    font-size: 16px; line-height: 1.65;
    -webkit-font-smoothing: antialiased;
  }
  main { max-width: 780px; margin: 0 auto; padding: 64px 28px 90px; }
  .eyebrow {
    font-family: "PlexMono", monospace; font-size: 12px; font-weight: 500;
    letter-spacing: .24em; text-transform: uppercase; color: var(--purple);
    margin-bottom: 22px;
  }
  h1 {
    font-family: "Space Grotesk", sans-serif; font-weight: 700;
    font-size: clamp(30px, 5vw, 42px); line-height: 1.12;
    letter-spacing: -0.015em; text-wrap: balance; margin-bottom: 12px;
  }
  .subtitle { font-size: 18px; color: var(--muted); font-style: italic; margin-bottom: 26px; }
  .authors { font-size: 15px; margin-bottom: 10px; }
  .authors strong { font-weight: 600; }
  .meta { font-family: "PlexMono", monospace; font-size: 12px; color: var(--faint); line-height: 1.8; margin-bottom: 8px; }
  hr { border: 0; border-top: 1px solid var(--line); margin: 34px 0; }
  h2 {
    font-family: "Space Grotesk", sans-serif; font-weight: 700; font-size: 24px;
    letter-spacing: -0.01em; margin: 44px 0 14px; text-wrap: balance;
  }
  h3 {
    font-family: "Space Grotesk", sans-serif; font-weight: 600; font-size: 18px;
    margin: 30px 0 10px;
  }
  p { margin: 0 0 14px; color: var(--ink); }
  p strong { font-weight: 600; }
  a { color: var(--purple); text-decoration: none; }
  a:hover { text-decoration: underline; }
  ol { margin: 0 0 14px 22px; }
  ol li { margin-bottom: 8px; }
  .abstract {
    background: var(--surface); border: 1px solid var(--line); border-left: 3px solid var(--purple);
    border-radius: 12px; padding: 20px 24px; margin: 6px 0 10px;
  }
  .abstract p { margin: 0; font-size: 15.5px; }
  .tablewrap { overflow-x: auto; margin: 18px 0 22px; border: 1px solid var(--line); border-radius: 12px; background: var(--surface); }
  table { border-collapse: collapse; width: 100%; min-width: 640px; }
  th {
    font-family: "PlexMono", monospace; font-size: 11px; letter-spacing: .12em;
    text-transform: uppercase; color: var(--faint); font-weight: 500;
    text-align: left; padding: 10px 14px; border-bottom: 1px solid var(--line);
  }
  td { font-size: 14px; color: var(--muted); padding: 10px 14px; border-bottom: 1px solid var(--line-soft); vertical-align: top; }
  tr:last-child td { border-bottom: none; }
  td.k { color: var(--ink); font-weight: 600; white-space: nowrap; }
  .ref { font-size: 14px; color: var(--muted); padding-left: 34px; text-indent: -34px; margin-bottom: 10px; }
  .ref a { word-break: break-all; }
  .refno { font-family: "PlexMono", monospace; font-size: 12.5px; color: var(--purple); }
  .colophon { margin-top: 26px; font-size: 13px; color: var(--faint); font-style: italic; }
  #themebtn {
    position: fixed; top: 18px; right: 18px; width: 38px; height: 38px;
    border-radius: 10px; border: 1px solid var(--line); background: var(--surface);
    color: var(--muted); cursor: pointer; z-index: 5;
  }
  #themebtn:hover { color: var(--ink); border-color: var(--purple); }
  .ic-sun { display: none; }
  html.dark .ic-sun { display: inline; }
  html.dark .ic-moon { display: none; }
  @media print {
    #themebtn { display: none; }
    body { background: #fff; color: #000; font-size: 12.5px; }
    main { padding: 0; max-width: none; }
    a { color: inherit; }
  }
</style>
</head>
<body>
<button id="themebtn" aria-label="Toggle light / dark mode"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><g class="ic-moon"><path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8z"/></g><g class="ic-sun"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></g></svg></button>
<main>
<div class="eyebrow">Verana Research · Paper</div>
<h1>__TITLE__</h1>
<p class="subtitle">__SUBTITLE__</p>
__ARTICLE__
</main>
<script>
  var root = document.documentElement;
  function setTheme(dark, save) {
    root.classList.toggle("dark", dark);
    if (save !== false) { try { localStorage.setItem("vrpaper-theme", dark ? "dark" : "light"); } catch (e) {} }
  }
  var stored = null;
  try { stored = localStorage.getItem("vrpaper-theme"); } catch (e) {}
  if (stored) setTheme(stored === "dark", false);
  else if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) setTheme(true, false);
  document.getElementById("themebtn").addEventListener("click", function () {
    setTheme(!root.classList.contains("dark"));
  });
</script>
</body>
</html>
"""

page = page.replace("__FONTS__", fonts).replace("__TITLE__", htmlmod.escape(title)) \
           .replace("__SUBTITLE__", subtitle).replace("__ARTICLE__", article)
assert "—" not in article, "em-dash in paper"
open(OUT, "w").write(page)
print(f"wrote {OUT} ({len(page)} bytes)")
