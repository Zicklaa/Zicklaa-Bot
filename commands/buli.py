import logging
import discord
from datetime import datetime, timedelta, timezone
import requests
from zoneinfo import ZoneInfo
from discord.ext import commands

logger = logging.getLogger("ZicklaaBot.Buli")

# ---------- Konfiguration / Konstanten ----------
BERLIN_TZ = ZoneInfo("Europe/Berlin")
WEEKDAYS = ("Mo", "Di", "Mi", "Do", "Fr", "Sa", "So")
BASE = "https://api.football-data.org/v4"

# Eine Session hält Keep-Alive-Verbindungen offen
_SESSION: requests.Session | None = None


class Buli(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def buli(self, ctx):
        try:
            '''allowed_channel_id = 123456789012345678  
            if ctx.channel.id != allowed_channel_id:
                await ctx.reply("Dieser Command ist nur im BuLi Channel erlaubt lol")
                return'''

            api_token = getattr(self.bot, "FOOTBALL_DATA_API_TOKEN", None)
            if not api_token:
                raise RuntimeError("FOOTBALL_DATA_API_TOKEN nicht gesetzt.")

            session = get_session(api_token)

            matchday, fixtures, date_range = fetch_next_matchday_with_scores(
                session)

            embed = discord.Embed(
                title=f"Bundesliga – Spieltag {matchday}",
                description="\n".join(format_line(m) for m in fixtures),
                color=discord.Color.red()
            )
            embed.set_footer(
                text=f"Zeiten: Europa/Berlin  •  Zeitraum: {date_range}")

            await ctx.reply(embed=embed)

        except Exception as e:
            # Dein Spruch, aber entschärft
            await ctx.reply("Klappt nit lol 🤷")
            logger.error(f"Buli from {ctx.author.name}: {e}")


def get_session(api_token: str) -> requests.Session:
    # Gibt eine vorbereitete requests.Session mit Auth-Header zurück (singleton).
    global _SESSION
    if _SESSION is None:
        s = requests.Session()
        s.headers.update({"X-Auth-Token": api_token})
        _SESSION = s
    else:
        # Falls sich der Token am Bot ändert:
        _SESSION.headers.update({"X-Auth-Token": api_token})
    return _SESSION


def fd_get(session: requests.Session, path: str, params: dict | None = None) -> dict:
    # Wrapper für Football-Data GET mit Error-Handling.
    url = f"{BASE}{path}"
    resp = session.get(url, params=params, timeout=15)
    if resp.status_code == 429:
        raise RuntimeError("Rate Limit erreicht (HTTP 429).")
    if not resp.ok:
        raise RuntimeError(f"API Fehler {resp.status_code}: {resp.text}")
    return resp.json()


def to_dt(utc_iso: str) -> datetime:
    # Wandelt ISO8601 mit 'Z' in aware datetime (UTC) um.
    return datetime.fromisoformat(utc_iso.replace("Z", "+00:00"))


def team_name(team: dict) -> str:
    # Bevorzugt kurze Teamnamen.
    return team.get("shortName") or team.get("tla") or team.get("name") or "?"


def score_str(match: dict) -> str:
    """
    Liefert z.B.:
      ' — 2:1', ' — 0:0 (LIVE)', '' (kein Score verfügbar)
    Plus Elfer-Hinweis bei FINISHED: ' (n.E. x:y)'
    """
    status = match.get("status")
    s = match.get("score") or {}
    # Reihenfolge der Quellen
    candidates = [
        s.get("fullTime") or {},
        s.get("regularTime") or {},
        s.get("extraTime") or {},
        s.get("halfTime") or {},
    ]
    home = away = None
    for c in candidates:
        h, a = c.get("home"), c.get("away")
        if h is not None and a is not None:
            home, away = h, a
            break

    pen = s.get("penalties") or {}
    pen_home, pen_away = pen.get("home"), pen.get("away")
    pen_suffix = f" (n.E. {pen_home}:{pen_away})" if (
        pen_home is not None and pen_away is not None and status == "FINISHED"
    ) else ""

    if home is not None and away is not None:
        if status == "IN_PLAY":
            return f" — {home}:{away} (LIVE)"
        elif status == "FINISHED":
            return f" — {home}:{away}{pen_suffix}"
        else:
            return f" — {home}:{away}"
    if status == "IN_PLAY":
        return " — LIVE"
    return ""


def format_line(match: dict) -> str:
    # Formatiert eine Zeile für das Embed (Zeit, Teams, Venue, Score).
    home = team_name(match["homeTeam"])
    away = team_name(match["awayTeam"])
    dt_local = to_dt(match["utcDate"]).astimezone(BERLIN_TZ)
    when = dt_local.strftime(f"{WEEKDAYS[dt_local.weekday()]}, %d.%m. %H:%M")
    venue = (match.get("venue") or "").strip()
    venue_str = f"  —  {venue}" if venue else ""
    return f"`{when}`  **{home}** vs **{away}**{venue_str}{score_str(match)}"


def determine_next_matchday_from_scheduled(scheduled_matches: list[dict]) -> tuple[int, list[dict]]:
    # Ermittelt den nächsten Spieltag aus SCHEDULED-Matches und gibt (MD, fixtures_sorted) zurück.
    md_to_matches: dict[int, list[dict]] = {}
    for m in scheduled_matches:
        md = m.get("matchday")
        if md is not None:
            md_to_matches.setdefault(md, []).append(m)
    if not md_to_matches:
        raise RuntimeError("Konnte den nächsten Spieltag nicht bestimmen.")

    next_md = min(
        md_to_matches.keys(),
        key=lambda md: min(to_dt(x["utcDate"]) for x in md_to_matches[md])
    )
    fixtures_sorted = sorted(
        md_to_matches[next_md], key=lambda m: to_dt(m["utcDate"]))
    return next_md, fixtures_sorted


def fetch_next_matchday_with_scores(session: requests.Session) -> tuple[int, list[dict], str]:
    """
    1) Holt SCHEDULED (21 Tage) -> ermittelt nächsten Spieltag
    2) Holt Fenster (±1 Tag um Spieltagsbeginn/-ende) ohne Statusfilter -> Scores/LIVE inkludiert
    3) Gibt (spieltag, fixtures_sorted, date_range_text) zurück
    """
    # 1) scheduled holen
    today_utc = datetime.now(timezone.utc).date()
    scheduled = fd_get(
        session, "/competitions/BL1/matches",
        params={
            "status": "SCHEDULED",
            "dateFrom": today_utc.isoformat(),
            "dateTo": (today_utc + timedelta(days=21)).isoformat(),
        },
    ).get("matches", [])

    if not scheduled:
        scheduled = fd_get(session, "/competitions/BL1/matches",
                           params={"status": "SCHEDULED"}).get("matches", [])

    if not scheduled:
        raise RuntimeError("Keine anstehenden Bundesliga-Spiele gefunden.")

    # nächsten Spieltag aus scheduled bestimmen
    next_md, fixtures_sched = determine_next_matchday_from_scheduled(scheduled)

    # Zeitfenster bestimmen (grob) und erweitern
    first_kick = to_dt(fixtures_sched[0]["utcDate"])
    last_kick = to_dt(fixtures_sched[-1]["utcDate"])
    date_from = (first_kick - timedelta(days=1)).date().isoformat()
    date_to = (last_kick + timedelta(days=1)).date().isoformat()

    # 2) Fenster ohne Statusfilter laden, dann auf matchday filtern
    window_matches = fd_get(
        session, "/competitions/BL1/matches",
        params={"dateFrom": date_from, "dateTo": date_to},
    ).get("matches", [])

    fixtures = [m for m in window_matches if m.get(
        "matchday") == next_md] or fixtures_sched
    fixtures.sort(key=lambda m: to_dt(m["utcDate"]))

    # 3) Zeitraum-Text (lokal)
    first_local = to_dt(fixtures[0]["utcDate"]).astimezone(BERLIN_TZ)
    last_local = to_dt(fixtures[-1]["utcDate"]).astimezone(BERLIN_TZ)
    date_range = (
        first_local.strftime("%d.%m.%Y")
        if first_local.date() == last_local.date()
        else f'{first_local.strftime("%d.%m.%Y")} – {last_local.strftime("%d.%m.%Y")}'
    )
    return next_md, fixtures, date_range


def setup(bot):
    bot.add_cog(Buli(bot))
