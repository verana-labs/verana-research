#!/usr/bin/env python3
"""Render landscape-paper.md into the Verana Research paper template (Journal design).

Markdown subset: #/##/### headings, paragraphs, ordered lists, one table, ---,
**bold**, *italic*, [text](url), bare URLs, [n]-prefixed references. The three
webinar diagrams are extracted from the built v4 deck and injected as Figures
1-3, retinted to the journal palette via CSS variables. Fonts for the figures
(Space Grotesk / InterD / PlexMono) are inlined from the deck; body type is
Source Serif 4 from Google Fonts.
"""
import os, re, html as htmlmod

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(HERE, "landscape-paper.md")
OUT = os.path.join(HERE, "landscape-paper.html")
DECK = os.path.join(HERE, "..", "..", "webinars", "2026-09-17-eclipse-models-for-privacy",
                    "verana-verifiable-trust-eclipse-webinar-v4.html")

deck_html = open(DECK).read()
fonts = "\n".join(re.findall(r"@font-face \{[^}]*\}", deck_html))
assert fonts.count("@font-face") == 4

def deck_svg(label_start):
    i = deck_html.find(label_start)
    assert i != -1, label_start
    a = deck_html.rfind("<svg", 0, i)
    b = deck_html.find("</svg>", i) + 6
    svg = deck_html[a:b]
    svg = re.sub(r'<svg[^>]*?(viewBox="[^"]+")[^>]*?(role="img")[^>]*?(aria-label="[^"]*")[^>]*>',
                 r'<svg \1 \2 \3 class="figsvg">', svg, count=1)
    return svg

def figure(svg, cls, caption):
    return ('<figure class="fig ' + cls + '"><div class="figwrap">' + svg + "</div>"
            "<figcaption><strong>" + caption[0] + "</strong> " + caption[1] + "</figcaption></figure>")

FIG1 = figure(deck_svg('aria-label="Left: a central agent registry'), "fig--wide",
    ("Figure 1.", "A central agent registry observes every connection (left); mutual, peer-to-peer Proof-of-Trust leaves no observer (right)."))
FIG2 = figure(deck_svg('aria-label="Participant tree of a credential schema'), "fig--mid",
    ("Figure 2.", "The participant tree of a credential schema: the ecosystem root accredits grantors, grantors accredit issuers and verifiers; issuers issue to, and verifiers verify, holders."))
FIG3 = figure(deck_svg('aria-label="Mutual trust resolution between two peers'), "fig--wide",
    ("Figure 3.", "Mutual trust resolution: both peers resolve each other, verify locally, check accreditations against public replicated state, then connect; optional private credentials flow only over the established channel."))

LOGO = ('<div class="logo"><svg width="42" height="40" viewBox="0 0 54 52" fill="none" role="img" aria-label="Verana">'
        '<path d="M26.9932 51.6972L5.805 11.0977L2.91263 16.2161L0 10.6048L5.98725 0L26.9932 40.2483L47.9993 0L54 10.6217L51.0773 16.2161L48.1849 11.0977L26.9932 51.6972Z" fill="currentColor"/>'
        '<path d="M13.696 0L26.9935 25.4637L39.9367 0H13.696Z" fill="currentColor"/></svg></div>')

# ------------------------- markdown parsing -------------------------
def inline(s):
    s = htmlmod.escape(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"(?<![\"'>=\w])(https?://[^\s<·]+[^\s<·.,;)])", r'<a href="\1">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    return s

src = open(MD).read()
blocks = re.split(r"\n\s*\n", src.strip())
body, in_refs, title, subtitle = [], False, "", ""
for b in blocks:
    lines = [l.rstrip() for l in b.strip().split("\n")]
    first = lines[0]
    if first.startswith("# "):
        title = first[2:].strip(); continue
    if first.startswith("*A comparative") and not subtitle:
        subtitle = inline(first.strip("*")); continue
    if first.startswith("**Fabrice"):
        body.append('<p class="authors">' + "<br>".join(inline(l) for l in lines) + "</p>"); continue
    if first.startswith("*Version") or first.startswith("*Companion"):
        body.append('<p class="meta">' + "<br>".join(inline(l.strip("*")) for l in lines) + "</p>"); continue
    if first == "---":
        body.append("<hr>"); continue
    if first.startswith("## "):
        h = first[3:].strip()
        if h == "References": in_refs = True
        body.append("<h2>" + inline(h) + "</h2>"); continue
    if first.startswith("### "):
        body.append("<h3>" + inline(first[4:].strip()) + "</h3>"); continue
    if first.startswith("|"):
        rows = [l for l in lines if l.startswith("|")]
        head = [c.strip() for c in rows[0].strip("|").split("|")]
        out = ['<div class="tablewrap"><table><thead><tr>']
        out += ["<th>" + inline(c) + "</th>" for c in head]
        out.append("</tr></thead><tbody>")
        for r in rows[2:]:
            cells = [c.strip() for c in r.strip("|").split("|")]
            out.append("<tr>" + "".join(('<td class="k">' if i == 0 else "<td>") + inline(c) + "</td>"
                                        for i, c in enumerate(cells)) + "</tr>")
        out.append("</tbody></table></div>")
        body.append("".join(out)); continue
    if re.match(r"^\d+\.\s", first):
        out = ["<ol>"]
        for l in lines:
            m = re.match(r"^\d+\.\s+(.*)$", l)
            out.append("<li>" + inline(m.group(1)) + "</li>")
        out.append("</ol>")
        body.append("".join(out)); continue
    if in_refs and re.match(r"^\[\d+\]\s", first):
        m = re.match(r"^\[(\d+)\]\s+(.*)$", " ".join(lines))
        body.append('<p class="ref"><span class="refno">[' + m.group(1) + "]</span> " + inline(m.group(2)) + "</p>"); continue
    if first.startswith("*©"):
        body.append('<p class="colophon">' + inline(" ".join(lines).strip("*")) + "</p>"); continue
    text = inline(" ".join(lines))
    if body and body[-1] == "<h2>Abstract</h2>":
        body.append('<div class="abstract"><p>' + text + "</p></div>")
    else:
        body.append("<p>" + text + "</p>")

def insert_after(needle, fig):
    for i, blk in enumerate(body):
        if needle in blk:
            body.insert(i + 1, fig); return
    raise AssertionError(needle)
def insert_before(needle, fig):
    for i, blk in enumerate(body):
        if needle in blk:
            body.insert(i, fig); return
    raise AssertionError(needle)

insert_after("relocated one layer up.", FIG1)
insert_before("Against the framework:", FIG3)
insert_before("Against the framework:", FIG2)  # ends up before FIG3

article = "\n".join(body)
assert "—" not in article, "em-dash in paper"

# ------------------------- template (Journal) -------------------------
FIGVARS_LIGHT = "--bg:#FBFAF6;--surface:#F4F1E9;--card:#FFFFFF;--line:#DAD5C8;--line-soft:#E7E3D8;--ink:#211F1A;--muted:#5A554A;--faint:#8B857A;--purple:#1F4E79;--purple-deep:#163B5C;--purple-soft:#E8EEF5;--green:#2E6B4F;--green-soft:#EAF2ED;--green-line:#BFD6CB;--ember:#A34A1F;"
FIGVARS_DARK = "--bg:#151410;--surface:#1B1A15;--card:#201F19;--line:#38362E;--line-soft:#2C2A23;--ink:#EAE7DC;--muted:#B0AB9D;--faint:#7E796C;--purple:#7FA8CC;--purple-deep:#5F8CB4;--purple-soft:#20303E;--green:#7FB79A;--green-soft:#1C2A23;--green-line:#3A5A4A;--ember:#D98B57;"

css = """
  :root { --bg:#FBFAF6; --ink:#211F1A; --muted:#5A554A; --faint:#8B857A; --accent:#1F4E79; --line:#DAD5C8; --soft:#F4F1E9;
          --fline:#DAD5C8; --fcard-bg:#FFFFFF; --fcap:#5A554A; """ + FIGVARS_LIGHT + """ }
  html.dark { --bg:#151410; --ink:#EAE7DC; --muted:#B0AB9D; --faint:#7E796C; --accent:#7FA8CC; --line:#38362E; --soft:#1B1A15;
          --fline:#38362E; --fcard-bg:#1B1A15; --fcap:#B0AB9D; """ + FIGVARS_DARK + """ }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:var(--bg); color:var(--ink); font-family:"Source Serif 4", Georgia, serif; font-size:16.5px; line-height:1.72; -webkit-font-smoothing:antialiased; }
  main { max-width:980px; margin:0 auto; padding:64px 30px 100px; }
  .logo { text-align:center; color:var(--accent); margin-bottom:16px; }
  .logo svg { display:inline-block; }
  .kicker-line { text-align:center; font-size:13px; letter-spacing:.28em; text-transform:uppercase; color:var(--faint); margin-bottom:26px; }
  h1 { font-weight:700; font-size:clamp(28px,4.6vw,37px); line-height:1.2; text-align:center; text-wrap:balance; margin-bottom:12px; }
  .subtitle { text-align:center; font-style:italic; font-size:18px; color:var(--muted); margin-bottom:28px; }
  .authors { text-align:center; font-size:15.5px; margin-bottom:8px; }
  .authors strong { font-weight:600; font-variant:small-caps; letter-spacing:.04em; font-size:17px; }
  .meta { text-align:center; font-size:13px; color:var(--faint); font-style:italic; line-height:1.8; margin-bottom:6px; }
  hr { border:0; border-top:1px solid var(--line); margin:36px auto; width:120px; }
  h2 { font-weight:700; font-size:22.5px; margin:46px 0 14px; }
  h3 { font-weight:600; font-size:18px; font-style:italic; margin:30px 0 10px; }
  p { margin:0 0 15px; }
  a { color:var(--accent); text-decoration:none; border-bottom:1px solid color-mix(in srgb, var(--accent) 35%, transparent); }
  a:hover { border-bottom-color:var(--accent); }
  ol { margin:0 0 15px 24px; } ol li { margin-bottom:8px; }
  .abstract { border-top:2px solid var(--ink); border-bottom:1px solid var(--line); padding:18px 6px 12px; margin:8px 0 14px; }
  .abstract p { font-size:15px; line-height:1.66; margin:0; }
  .abstract p::before { content:"Abstract. "; font-variant:small-caps; font-weight:600; letter-spacing:.05em; }
  .tablewrap { overflow-x:auto; margin:20px 0 24px; }
  table { border-collapse:collapse; width:100%; min-width:640px; border-top:2px solid var(--ink); border-bottom:2px solid var(--ink); }
  th { font-size:12.5px; letter-spacing:.06em; text-transform:uppercase; font-weight:600; text-align:left; padding:10px 12px; border-bottom:1px solid var(--ink); }
  td { font-size:14.5px; color:var(--muted); padding:9px 12px; border-bottom:1px solid var(--line); vertical-align:top; }
  tr:last-child td { border-bottom:none; }
  td.k { color:var(--ink); font-weight:600; white-space:nowrap; }
  .ref { font-size:14px; color:var(--muted); padding-left:34px; text-indent:-34px; margin-bottom:9px; }
  .refno { color:var(--accent); }
  .ref a { word-break:break-all; }
  .colophon { margin-top:30px; font-size:13.5px; color:var(--faint); font-style:italic; text-align:center; }
  .fig { margin:26px 0 30px; }
  .fig--wide { width:100%; }
  .fig--mid { max-width:640px; margin-left:auto; margin-right:auto; }
  .figwrap { border:1px solid var(--fline); border-radius:12px; background:var(--fcard-bg); padding:18px 14px 10px; }
  .figsvg { width:100%; height:auto; display:block; }
  figcaption { font-size:13px; color:var(--fcap); margin-top:10px; line-height:1.5; text-align:center; }
  #themebtn { position:fixed; top:18px; right:18px; width:38px; height:38px; border-radius:50%; border:1px solid var(--line); background:var(--soft); color:var(--muted); cursor:pointer; z-index:5; }
  #themebtn:hover { color:var(--ink); border-color:var(--accent); }
  .ic-sun { display:none; } html.dark .ic-sun { display:inline; } html.dark .ic-moon { display:none; }
  @media print { #themebtn { display:none; } body { background:#fff; color:#000; } }
"""

page = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400;1,8..60,600&display=swap">
<style>
__FONTS__
__CSS__
</style>
</head>
<body>
<button id="themebtn" aria-label="Toggle light / dark mode"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><g class="ic-moon"><path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8z"/></g><g class="ic-sun"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></g></svg></button>
<main>
__LOGO__
<div class="kicker-line">Verana Research</div>
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
  document.getElementById("themebtn").addEventListener("click", function () { setTheme(!root.classList.contains("dark")); });
</script>
</body>
</html>
"""

page = (page.replace("__FONTS__", fonts).replace("__CSS__", css)
            .replace("__TITLE__", htmlmod.escape(title)).replace("__SUBTITLE__", subtitle)
            .replace("__LOGO__", LOGO).replace("__ARTICLE__", article))
open(OUT, "w").write(page)
print(f"wrote {OUT} ({len(page)} bytes)")
