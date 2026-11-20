# BUILD-LOG — news-image-20261120

Entry: **"The World Today" — a newspaper front page summing up Friday,
20 November 2026.** Competition `news-image-20261120`, account @rfq404
(make.fun), GitHub rifki500 (verified linked). Built 20–21 November 2026
(WIB) in a session started after the competition opened
(20 Nov 2026 00:00 UTC). BUILD ONLY — parent submits.

## The image

1024×1024 PNG, drawn entirely in code (`build_image.py`, PIL — no
external photos, no network). Masthead names the day prominently
("FRIDAY, 20 NOVEMBER 2026", also restated in the footer), seven stories
with headlines, one-to-two-line summaries and small drawn visuals (bridge
under fire, interceptor burst, game controller, EU and UK flags, grounded
plane, warming globe, falling chart). The entrypoint `main.py` (stdlib
only) copies the pre-built `entry.png` to `/output/entry.png` (or
`$MAKEFUN_OUTPUT_DIR/entry.png`).

## Stories used (all of Friday 20 November 2026)

1. **Russia strikes Kyiv's bridges** (lead) — Russian ballistic missiles
   hit three crossings over the Dnipro (Podilsko-Voskresenskyi, Darnytskyi,
   Pivdennyi); 3 killed, 15 hurt; power and water cut across the capital.
   Sources: Reuters, 20 Nov 2026 ("Three killed in missile strikes on
   Kyiv, mayor says, in biggest attack on bridges"); Fox News / SRN News,
   20 Nov 2026 (400+ drones, 110+ missiles; three bridges struck).
2. **Asia's markets plunge** — Nikkei falls 5.1% to a seven-month low;
   SoftBank slides 14.5% as the AI sell-off spreads across Asia (KOSPI
   -5.2%, Taiex -6.4%). Sources: CoinEdition Asia market recap, 20 Nov
   2026; europe says (Japan), 20 Nov 2026; finance.biggo.com, 20 Nov 2026.
3. **Saudi shoots down Houthi missile** — Saudi air defences intercept a
   ballistic missile and drones aimed at the southern region; alerts in
   Jazan, Abha and Khamis Mushait. Sources: Reuters, 20 Nov 2026
   ("Saudi-led coalition says it intercepted Houthi missile targeting
   southern region"); AP via reflector.com, 20 Nov 2026 (five drones and
   one ballistic missile intercepted Friday morning).
4. **GTA 6's record first day** — An estimated $2.36bn from 24.6m copies,
   the biggest entertainment launch ever. Sources: Sensor Tower estimate
   via VGC, first reported 20 Nov 2026; GamesBeat, 20 Nov 2026
   (published 13:30 UTC); Polygon, 20 Nov 2026.
5. **UK and EU agree reset deal** — The Brussels summit agrees food trade,
   youth mobility and linked carbon markets. Sources: Reuters, 20 Nov 2026
   ("What EU and UK have agreed to at summit"; "UK-EU reset deal agreed,
   Downing Street says"); GOV.UK, summit key documents, 20 Nov 2026.
6. **US air travel halted** — The FAA orders a nationwide ground stop;
   1.5m passengers hit and 9,000 flights cancelled. Sources: Al Jazeera,
   20 Nov 2026 (1.5m passengers; stop lifted 8:15pm ET Friday); AP via
   jingletree.com, 20 Nov 2026 (~25,000 flights delayed, 9,000+ cancelled
   Friday, per FlightAware; telecoms outage).
7. **COP31 ends in deadlock** — Talks close with no fossil-fuel deal;
   campaigners call it the worst COP ever. Host Turkey leaves with $26bn
   in green deals. Sources: Reuters, 20 Nov 2026 ("COP31 delivers deals
   for host Turkey as climate diplomacy stalls"); Climate Action Network,
   20 Nov 2026 ("the worst COP ever").

## Stories checked and NOT used

- **Houthi strike on Riyadh's PIF Tower** — happened Thursday 19 Nov
  (Reuters, 19 Nov), not 20 Nov. The page instead reports the distinct
  Friday interception (story 3).
- **Kenya's last Ebola patient** — discharged and announced Wednesday
  11 Nov (Health Minister Aden Duale); 20 Nov items are only reposts.
- **US Senate energy permitting bill (62–33)** — passed Thursday 19 Nov
  (Reuters; USA Today, 19 Nov), not 20 Nov.
- **IMF warning on global public debt** — delivered by Kristalina Georgieva
  Thursday 19 Nov at the APEC summit in Shenzhen, not 20 Nov.
- **Italy fines Meta €805m** — announced Saturday 14 Nov, not 20 Nov.
- **Voyager 1 one light-day** — crossed the mark 18 Nov, NASA confirmed
  19 Nov, not 20 Nov. **BepiColombo Mercury orbit** — insertion is
  21 Nov, not 20 Nov.

## Verification (run 21 Nov 2026, ~00:05 WIB)

- `main.py` run twice with `MAKEFUN_OUTPUT_DIR` set to two scratch
  dirs; both outputs byte-identical and matching the repo `entry.png`:
  sha256 `92036b2e660a7ffa1215d68b19d0b2e4a3993014291615d81afb2079b7b180f2`
  (run 1, run 2, and repo file — all three identical).
- Dimensions: 1024×1024 px (limit 1024×1024). Format: PNG.
- File size: 121,922 bytes (limit 1,048,576 bytes).
- Visual inspection: all seven headlines and summaries legible at
  1024 px; date prominent in the masthead and restated in the footer;
  no garbled text, no text-on-text overlap. Two small fixes were made
  after the first render (explosion bursts got outlines and sparks so
  they do not read as suns; stray green dots removed from the flags
  icon); the final render was re-inspected.
- `main.py` imports only `os` and `shutil` (stdlib); no network access
  in the entrypoint or the generator. `build_image.py` uses PIL locally
  only; the entrypoint never imports it.

## Commit

- Repository: https://github.com/rifki500/news-image-20261120-entry
- Commit sha: (filled at commit time)

## Honest caveats

- Kyiv casualty counts varied through the day: the mayor's early Friday
  report (3 killed, 15 hurt) is what the page uses, as reported by
  Reuters on 20 Nov; later reports put the Kyiv toll at 6 and 8 across
  Ukraine.
- Nikkei and SoftBank: the page uses closing figures (Nikkei -5.06%,
  SoftBank -14.48%); intraday lows were about -4.85% and -16%.
- GTA 6 launched on 19 Nov; the $2.36bn day-one estimate was first
  reported on 20 Nov (Sensor Tower via VGC), which is the event the
  page reports.
- The Houthi story is the Friday interception, not the Thursday 19 Nov
  PIF Tower strike — a different, earlier event. The page says
  "intercepts", not "tower hit".
- COP31: the 19 Nov edition of this series covered the draft dropping
  fossil fuels; this page covers the final-day outcome (stall, Turkey's
  deals, "worst COP ever"), a distinct 20 Nov development.
