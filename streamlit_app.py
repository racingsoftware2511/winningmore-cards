import json
import glob
import os
import textwrap
from datetime import datetime

import streamlit as st


def html(markup: str):
    """Render dedented HTML/CSS — st.markdown treats indented text as a code block."""
    st.markdown(textwrap.dedent(markup), unsafe_allow_html=True)

st.set_page_config(
    page_title="WinningMore — Daily Card",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAVY = "#0A1F44"
INK = "#1B1F27"
PARCHMENT = "#F6F2E7"
PARCHMENT_DARK = "#EDE6D3"
GOLD = "#A67C1E"
GOLD_SOFT = "#F1E6C8"
RED = "#9C3B36"
RED_SOFT = "#F3E1DF"
GREEN = "#2F6B4F"
GREY = "#6B6B63"
HAIRLINE = "#D9D2BC"

STATUS_STYLE = {
    "primary": {"color": GREEN, "label": "Backed"},
    "danger": {"color": RED, "label": "Avoid"},
    "skip": {"color": GREY, "label": "No bet"},
    "pending": {"color": GOLD, "label": "Pending"},
}

STARTING_BANKROLL = 500.0

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


@st.cache_data(ttl=300)
def load_cards():
    cards = {}
    for path in glob.glob(os.path.join(DATA_DIR, "*.json")):
        with open(path, "r", encoding="utf-8") as f:
            card = json.load(f)
            cards[card["date"]] = card
    return dict(sorted(cards.items(), reverse=True))


def money(n):
    return f"${n:,.0f}"


_CSS = "".join([
    f"html, body, [class*='css'] {{ font-family: 'Inter', sans-serif; color: {INK}; }}",
    f".stApp {{ background-color: {PARCHMENT}; }}",
    f"section[data-testid='stSidebar'] {{ background-color: {NAVY}; }}",
    f"section[data-testid='stSidebar'] * {{ color: {PARCHMENT} !important; }}",
    "section[data-testid='stSidebar'] .stSelectbox label, "
    "section[data-testid='stSidebar'] .stMultiSelect label { "
    f"color: {GOLD_SOFT} !important; font-weight: 600; font-size: 0.85rem; }}",
    "#MainMenu, footer, header { visibility: hidden; }",
    ".block-container { padding-top: 1.5rem; max-width: 980px; }",
    f".wm-wordmark {{ font-family: 'Inter', sans-serif; font-weight: 700; "
    f"font-size: 0.95rem; color: {GOLD}; letter-spacing: 0.02em; margin-bottom: 0.15rem; }}",
    f".wm-date {{ font-family: 'Fraunces', serif; font-weight: 700; font-size: 2.6rem; "
    f"color: {NAVY}; line-height: 1.05; margin: 0; }}",
    f".wm-sub {{ font-family: 'Inter', sans-serif; font-size: 0.95rem; color: {GREY}; "
    f"margin-top: 0.3rem; border-top: 1px solid {HAIRLINE}; padding-top: 0.6rem; }}",
    f".wm-lesson {{ border-left: 3px solid {GOLD}; background: {GOLD_SOFT}; padding: 0.7rem 1rem; "
    f"font-size: 0.92rem; color: {INK}; margin: 1.1rem 0; }}",
    f".wm-lesson b {{ color: {NAVY}; }}",
    f".wm-match {{ display: flex; gap: 1.4rem; padding: 1.1rem 0; border-bottom: 1px solid {HAIRLINE}; }}",
    f".wm-match.featured {{ border-left: 3px solid {GOLD}; padding-left: 1rem; "
    "background: rgba(166,124,30,0.05); }",
    f".wm-match.danger {{ border-left: 3px solid {RED}; padding-left: 1rem; }}",
    f".wm-mnum {{ font-family: 'Fraunces', serif; font-weight: 600; font-size: 1.3rem; "
    f"color: {GREY}; width: 1.6rem; flex-shrink: 0; }}",
    ".wm-minfo { flex: 1.3; min-width: 0; }",
    f".wm-league {{ font-size: 0.72rem; font-weight: 600; color: {GOLD}; margin-bottom: 0.15rem; }}",
    f".wm-teams {{ font-family: 'Fraunces', serif; font-weight: 600; font-size: 1.15rem; color: {NAVY}; }}",
    f".wm-time {{ font-size: 0.8rem; color: {GREY}; margin-top: 0.15rem; }}",
    f".wm-analysis {{ flex: 2; font-size: 0.88rem; color: {INK}; line-height: 1.5; }}",
    f".wm-stub {{ flex: 1; border-left: 1px dashed {HAIRLINE}; padding-left: 1.2rem; "
    "min-width: 170px; flex-shrink: 0; }",
    ".wm-bet { font-weight: 700; font-size: 0.95rem; }",
    f".wm-stake {{ font-size: 0.8rem; color: {GREY}; margin-top: 0.1rem; }}",
    ".wm-odds { display: flex; gap: 0.6rem; margin-top: 0.55rem; "
    "font-variant-numeric: tabular-nums; font-size: 0.82rem; }",
    ".wm-odds div { text-align: center; }",
    f".wm-odds .k {{ display: block; color: {GREY}; font-size: 0.68rem; }}",
    f".wm-odds .v {{ display: block; font-weight: 600; color: {NAVY}; }}",
    ".wm-box { padding: 0.85rem 1rem; font-size: 0.88rem; margin: 1.3rem 0; line-height: 1.5; }",
    f".wm-avoid {{ border-left: 3px solid {RED}; background: {RED_SOFT}; color: {INK}; }}",
    f".wm-exposure {{ border-top: 1px solid {HAIRLINE}; border-bottom: 1px solid {HAIRLINE}; "
    f"color: {INK}; display: flex; gap: 1.8rem; flex-wrap: wrap; font-variant-numeric: tabular-nums; }}",
    f".wm-exposure b {{ color: {NAVY}; }}",
    f".wm-footer {{ background: {NAVY}; color: {PARCHMENT}; font-size: 0.75rem; "
    "padding: 0.9rem 1.1rem; margin-top: 1.4rem; line-height: 1.5; }",
    f".wm-footer b {{ color: {GOLD_SOFT}; }}",
    ".wm-result { margin-top: 0.6rem; padding-top: 0.5rem; border-top: 1px dashed "
    f"{HAIRLINE}; font-size: 0.8rem; font-variant-numeric: tabular-nums; }}",
    f".wm-result .fs {{ color: {GREY}; }}",
    ".wm-result .pnl { font-weight: 700; }",
    f".wm-tracker {{ display: flex; gap: 2rem; flex-wrap: wrap; padding: 0.9rem 1.1rem; "
    f"background: {NAVY}; color: {PARCHMENT}; margin: 0.9rem 0 1.3rem 0; "
    "font-variant-numeric: tabular-nums; }",
    f".wm-tracker .num {{ font-family: 'Fraunces', serif; font-weight: 700; font-size: 1.3rem; color: {GOLD_SOFT}; }}",
    f".wm-tracker .lbl {{ font-size: 0.72rem; color: {PARCHMENT_DARK}; margin-top: 0.1rem; }}",
])

html(
    "<link rel='preconnect' href='https://fonts.googleapis.com'>"
    "<link href='https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700"
    "&family=Inter:wght@400;500;600;700&display=swap' rel='stylesheet'>"
    f"<style>{_CSS}</style>"
)

cards = load_cards()

if not cards:
    st.error(
        "No cards found in the data/ folder yet. Add a JSON file named "
        "YYYY-MM-DD.json to publish the first card."
    )
    st.stop()

dates = list(cards.keys())

with st.sidebar:
    st.markdown("### WinningMore")
    selected_date = st.selectbox("Card date", dates, index=0)
    all_leagues = sorted({m["league"] for m in cards[selected_date]["matches"]})
    league_filter = st.multiselect("Filter by league", all_leagues, default=[])
    html(
        f"<div style='margin-top:1.5rem; font-size:0.78rem; color:{PARCHMENT_DARK};'>"
        f"{len(dates)} card{'s' if len(dates) != 1 else ''} published"
        f"</div>"
    )

card = cards[selected_date]
pretty_date = datetime.strptime(card["date"], "%Y-%m-%d").strftime("%A %-d %B %Y")

html(
    f"""
    <div class="wm-wordmark">WINNINGMORE · DAILY PREDICTION CARD</div>
    <p class="wm-date">{pretty_date}</p>
    <div class="wm-sub">Card #{card['card_number']} of the {card['season_label']} &nbsp;—&nbsp; {' · '.join(card['leagues_covered'])}</div>
    """
)

all_settled = [
    m
    for c in cards.values()
    for m in c["matches"]
    if m.get("status") == "primary" and m.get("result")
]
season_wins = sum(1 for m in all_settled if m["result"]["outcome"] == "won")
season_losses = sum(1 for m in all_settled if m["result"]["outcome"] == "lost")
season_pnl = sum(m["result"].get("pnl", 0) for m in all_settled)
season_staked = 0
for m in all_settled:
    for token in m["stake"].replace("$", " $").split():
        if token.startswith("$"):
            try:
                season_staked += float(token[1:])
            except ValueError:
                pass
            break
season_bankroll = STARTING_BANKROLL + season_pnl
season_roi = (season_pnl / season_staked * 100) if season_staked else 0

if all_settled:
    html(
        f"""
        <div class="wm-tracker">
          <div><div class="num">{season_wins}W\u2013{season_losses}L</div><div class="lbl">Season record</div></div>
          <div><div class="num">{'+' if season_pnl >= 0 else ''}{money(season_pnl)}</div><div class="lbl">Net profit</div></div>
          <div><div class="num">{money(season_bankroll)}</div><div class="lbl">Bankroll (from $500)</div></div>
          <div><div class="num">{'+' if season_roi >= 0 else ''}{season_roi:.1f}%</div><div class="lbl">ROI on staked</div></div>
        </div>
        """
    )

if card.get("lesson"):
    st.markdown(
        f'<div class="wm-lesson"><b>Lesson from yesterday.</b> {card["lesson"]}</div>',
        unsafe_allow_html=True,
    )

if card.get("no_fixture_today"):
    st.markdown(
        f'<div class="wm-box" style="border-left:3px solid {GREY}; background:{PARCHMENT_DARK}; color:{INK};">'
        f'<b>No fixture today.</b> {card["no_fixture_today"]}</div>',
        unsafe_allow_html=True,
    )

matches = card["matches"]
if league_filter:
    matches = [m for m in matches if m["league"] in league_filter]

for m in matches:
    status = STATUS_STYLE.get(m["status"], STATUS_STYLE["skip"])
    row_class = "wm-match"
    if m.get("featured"):
        row_class += " featured"
    if m["status"] == "danger":
        row_class += " danger"

    if m.get("odds"):
        odds_html = "".join(
            f'<div><span class="k">{k.upper()}</span><span class="v">{v}</span></div>'
            for k, v in m["odds"].items()
        )
    else:
        odds_html = f'<div style="font-size:0.78rem; color:{GREY}; font-style:italic;">Awaiting live odds</div>'

    result_html = ""
    if m.get("result"):
        r = m["result"]
        outcome_color = {"won": GREEN, "lost": RED}.get(r["outcome"], GREY)
        outcome_label = {"won": "WON", "lost": "LOST", "void": "VOID"}.get(r["outcome"], "")
        pnl = r.get("pnl", 0)
        pnl_str = f"{'+' if pnl >= 0 else ''}{money(pnl)}" if m["status"] == "primary" else ""
        result_html = (
            '<div class="wm-result">'
            f'<span class="fs">FT {r["score"]}</span> &nbsp; '
            f'<span style="color:{outcome_color};">{outcome_label}</span>'
            + (f' <span class="pnl" style="color:{outcome_color};">{pnl_str}</span>' if pnl_str else "")
            + "</div>"
        )

    html(
        f"""
        <div class="{row_class}">
          <div class="wm-mnum">{m['number']}</div>
          <div class="wm-minfo">
            <div class="wm-league">{m['league']}</div>
            <div class="wm-teams">{m['match']}</div>
            <div class="wm-time">Kick-off {m['time']} UK</div>
          </div>
          <div class="wm-analysis">{m['analysis']}</div>
          <div class="wm-stub">
            <div class="wm-bet" style="color:{status['color']};">{m['bet_headline']}</div>
            <div class="wm-stake">{m['stake']}</div>
            <div class="wm-odds">{odds_html}</div>
            {result_html}
          </div>
        </div>
        """
    )

if card.get("avoid"):
    st.markdown(
        f'<div class="wm-box wm-avoid"><b>Avoid today.</b> {card["avoid"]}</div>',
        unsafe_allow_html=True,
    )

primaries = [m for m in card["matches"] if m["status"] == "primary"]
skips = [m for m in card["matches"] if m["status"] == "skip"]
dangers = [m for m in card["matches"] if m["status"] == "danger"]
pendings = [m for m in card["matches"] if m["status"] == "pending"]

total_staked = 0
for m in primaries:
    for token in m["stake"].replace("$", " $").split():
        if token.startswith("$"):
            try:
                total_staked += float(token[1:])
            except ValueError:
                pass
            break

html(
    f"""
    <div class="wm-box wm-exposure">
      <div>{len(primaries)} primary bet{'s' if len(primaries) != 1 else ''} &nbsp;=&nbsp; <b>{money(total_staked)}</b> staked</div>
      <div>{len(skips)} disciplined skip{'s' if len(skips) != 1 else ''}</div>
      <div>{len(dangers)} danger match{'es' if len(dangers) != 1 else ''} avoided</div>
      <div>{len(pendings)} pending live odds</div>
    </div>
    """
)

st.markdown(
    f'<div class="wm-footer"><b>Please note.</b> {card.get("footer", "")}</div>',
    unsafe_allow_html=True,
)
