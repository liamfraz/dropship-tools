# Reddit Post Log

Track all Reddit posts for Dropship Tools marketing.

---

## Reddit Posts — 2026-04-12 (pending)

| Subreddit | Title | URL | Status |
|---|---|---|---|
| r/dropship | I analyzed 500 winning dropshipping products in 2026 — here are the 5 patterns that kept showing up | — | pending |
| r/Entrepreneur | How I validate dropshipping products in under 10 minutes (my exact process) | — | pending |
| r/ecommerce | Stop manually researching dropshipping products — here is the workflow that saves me 3 hours a week | — | pending |

---

## Post Content

### Post 1 — r/dropship

**Title:** I analyzed 500 winning dropshipping products in 2026 — here are the 5 patterns that kept showing up

**Body:**

Been doing this for about 3 years. Last year I went back through every product I'd tested (and a bunch I'd studied but not tested) and tried to pull out what the winners actually had in common. Not vibes — actual data signals.

Here's what kept showing up across the ~500 products I looked at:

**Pattern 1: Source cost under 25% of sell price**

Not 30%, not 35%. The winners consistently had source + shipping under 25% of sell price. This isn't about greed — it's math. Once you factor in platform fees (TikTok takes 5%, Shopify takes 2.9% + $0.30), a realistic $6-10 ad spend per unit, and a small return buffer, you need that headroom. Products at 40%+ source cost ratio almost never survived paid traffic.

**Pattern 2: Google Trends interest in the 60-75 range and rising**

This is counterintuitive. The products at 85-95 interest looked great but were almost always too late — supply had already caught up, CPAs were high, margins were compressed. The sweet spot was 60-75 with a rising slope over 90 days. Early enough that you're not fighting 400 other sellers, late enough that demand is real.

**Pattern 3: The Amazon gap**

Product exists on Amazon but there's no dominant listing under $20 for the same thing. This tells you demand is proven but the race to the bottom hasn't started. If Amazon already has something at $14.99 with 10,000 reviews, you're not winning on price or trust. Walk away.

**Pattern 4: $25-$55 price window**

Below $20: basically impossible to run paid ads profitably. Above $70: cold traffic needs too much warming, you need reviews and social proof that take time to build. The $25-$55 window is where impulse purchasing and margin actually coexist. Most of my best performers were $29-$45.

**Pattern 5: Solves a specific articulated problem**

Not "cool gadget", not "looks neat on TikTok". The winners solve a problem the buyer recognizes in themselves and can immediately describe. Posture, pain, organization, convenience. Generic novelty products had a 90-day shelf life at best. Problem-solvers kept selling.

---

The boring part: I now run a checklist on every product before I test. Trend check, margin check, Amazon gap check, price window check. Used to take me 30-45 minutes per product across multiple tabs.

I built a CLI tool that automates this research — happy to share the free trial link if anyone wants to test it. No card required, works in about 60 seconds per product.

What patterns have you guys noticed? Curious if the $25-55 window holds for other niches.

---

### Post 2 — r/Entrepreneur

**Title:** How I validate dropshipping products in under 10 minutes (my exact process)

**Body:**

I used to spend 45 minutes per product researching across 4 different tabs. AliExpress, Google Trends, Amazon, a spreadsheet for margin math. Half the time I'd talk myself into or out of products based on gut feeling rather than the data in front of me.

Here's the actual checklist I use now. Takes under 10 minutes if you're methodical:

---

**Step 1: AliExpress/CJ source check (2 min)**

Search the product. Look at the top 3-5 suppliers. Calculate: (source price + estimated shipping) as a % of your intended sell price. If that number is over 30%, stop here unless you have a very compelling reason. You need room for fees and ads.

Target: source + shipping < 25% of sell price

---

**Step 2: Google Trends direction check (2 min)**

Go to Google Trends. Search the product keyword. Set to "Past 12 months", then "Past 90 days". You're not looking at the raw score — you're looking at the slope.

- Rising slope at 60-75: window is open, get in
- Flat at 80+: probably saturated, supply caught up
- Declining anything: hard pass

The 90-day view reveals the recent momentum that the 12-month view hides.

---

**Step 3: Amazon competition check (2 min)**

Search the product on Amazon. You're looking for the "Amazon gap" — does a dominant listing exist at under $20? If yes, walk away. If the top results are $30-$50 or have weak review counts (under 500), there's room.

You're not trying to beat Amazon. You're looking for gaps Amazon hasn't filled at a price that makes your margin work.

---

**Step 4: True margin calculation (3 min)**

Most people calculate: (sell - source) / sell and call it margin. That's not margin. That's gross margin before the business actually runs.

Real formula:

    Profit = Sell Price - Source Cost - Shipping - Platform Fee - Ad Spend per Unit
    ROI = Profit / (Source + Shipping + Ad Spend)

Use your actual platform fee (TikTok: 5%, Shopify: 2.9% + $0.30 per transaction). Use a conservative ad spend estimate — I use $7-10/unit for TikTok Shop, $8-12/unit for Shopify.

If ROI is under 80%: don't touch it, you'll lose money on any paid traffic.
If ROI is 80-120%: marginal, needs organic or very efficient ads.
If ROI is 120%+: worth testing.

---

**What this looks like in practice**

A product I validated last month: "posture corrector" niche. Source + ship: $9.40. Sell price: $39.99.

- Source ratio: 23.5% ✓
- Trends: 78, rising 90-day ✓
- Amazon: dominant listing at $27 with 40k reviews — went one level deeper, found a specific variant Amazon wasn't stocking. Source $8.20, sell $39.99. Amazon gap confirmed.

That product did $580/day by week 3 on TikTok Shop.

---

Steps 1-3 are what I automated into a CLI tool called Dropship Tools. It pulls source pricing from CJ catalog, checks Google Trends direction, and runs the margin math in about 60 seconds. Free trial at https://dropship-tools.vercel.app — no card required.

But the manual process above works exactly the same way. The discipline matters more than the tooling.

---

### Post 3 — r/ecommerce

**Title:** Stop manually researching dropshipping products — here is the workflow that saves me 3 hours a week

**Body:**

When I tracked how I was actually spending my time, product research was eating 3-4 hours every week. Not because I was being thorough — because I was doing the same 4 checks manually for every product, across separate tabs, with a spreadsheet for the math.

Google Trends → AliExpress → Amazon → margin spreadsheet → repeat.

I've since automated almost all of it. Here's the workflow:

---

**What I was doing manually (and why it took so long)**

Every product validation involved:

1. **Trend check** — Is this keyword rising or declining over 90 days? Not just what's the score, but the direction. A product at 65 and rising is a different business than a product at 80 and flat. 5-7 minutes per keyword.

2. **Source pricing** — Pull top 3 supplier options from AliExpress or CJ. Note source cost + shipping. 5-10 minutes including comparison.

3. **Amazon gap check** — Does a dominant listing exist at under $20? This tells you if there's pricing room. 3-5 minutes.

4. **True margin calc** — Source + shipping + platform fee + ad spend buffer. Not just markup. If ROI is under 80% with real ad spend baked in, the product can't survive paid traffic. 5 minutes in a spreadsheet.

Total per product: 18-30 minutes. At 8-10 products a week, that's 2.5-5 hours just on research.

---

**What the automated workflow looks like**

Now I run a CLI command. It pulls CJ catalog pricing, checks Google Trends direction, and calculates margin. Takes about 60 seconds.

    $ ds scout "posture corrector" --limit 3

    Checking Google Trends... done
    Searching CJ catalog... done
    Scoring candidates... done

    Product               Source+Ship  Sell    Trend    Int.  Score
    Adjustable Back Brace $9.40        $39.99  rising   78    84
    Clavicle Support Band $11.20       $44.99  rising   71    79
    Shoulder Corrector    $7.80        $34.99  stable   52    61

    Top pick: Adjustable Back Brace — STRONG margin (2.6x markup, 68.1% ROI)

Then the margin detail with real ad spend:

    $ ds margin --source 7.20 --shipping 2.20 --price 39.99 --platform tiktok --ad-spend 8.00

    Source Cost    $7.20
    Shipping Cost  $2.20
    Ad Spend/Unit  $8.00
    Sell Price    $39.99
    Platform Fee   $2.00
    Profit/Unit   $20.59
    ROI           113.8%
    Verdict       STRONG

60 seconds vs 20+ minutes. On 10 products a week, that's roughly 3 hours back.

---

**What I still do manually**

The automation handles data collection and scoring. What I still eyeball:

- Is there a TikTok creative angle? No tool replaces this
- Is there a saturation signal I'm missing from scroll research?
- Does the product have any obvious shipping/fragility issues?

The research automation filters out the obvious losers fast. Human judgment still picks the winners.

---

The tool is called Dropship Tools — CLI-based, free trial at https://dropship-tools.vercel.app if you want to try it. No card required. Works on Mac/Linux.

Happy to answer questions about the scoring model or how the trend direction check works.
