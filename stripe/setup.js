#!/usr/bin/env node
/**
 * Creates the Dropship Tools Pro product and price in Stripe (test mode).
 * Run once: STRIPE_SECRET_KEY=sk_test_... node stripe/setup.js
 */

const stripe = require("stripe")(process.env.STRIPE_SECRET_KEY);
const fs = require("fs");
const path = require("path");

async function main() {
  if (!process.env.STRIPE_SECRET_KEY) {
    console.error("Error: STRIPE_SECRET_KEY environment variable is required");
    console.error("Usage: STRIPE_SECRET_KEY=sk_test_... node stripe/setup.js");
    process.exit(1);
  }

  if (!process.env.STRIPE_SECRET_KEY.startsWith("sk_test_")) {
    console.error("Error: Use a TEST mode key (sk_test_...) for initial setup");
    process.exit(1);
  }

  console.log("Creating Dropship Tools Pro product in Stripe test mode...");

  const product = await stripe.products.create({
    name: "Dropship Tools Pro",
    description:
      "Full access to Dropship Tools CLI — product scouting, margin analysis, AI listings, video scripts, and performance dashboard.",
  });

  console.log(`Product created: ${product.id}`);

  const price = await stripe.prices.create({
    product: product.id,
    unit_amount: 2900,
    currency: "usd",
    recurring: {
      interval: "month",
      trial_period_days: 7,
    },
    nickname: "Pro Monthly",
  });

  console.log(`Price created: ${price.id}`);

  const configPath = path.join(__dirname, "products.json");
  const config = JSON.parse(fs.readFileSync(configPath, "utf8"));
  config.products[0].price_id = price.id;
  config.products[0].product_id = product.id;
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));

  console.log("\n✓ stripe/products.json updated with IDs");
  console.log("\nNext step — add to Vercel environment:");
  console.log(`  vercel env add STRIPE_PRICE_ID`);
  console.log(`  Value: ${price.id}`);
  console.log("\nOr set directly:");
  console.log(
    `  vercel env add STRIPE_PRICE_ID production <<< "${price.id}"`
  );
}

main().catch((err) => {
  console.error("Setup failed:", err.message);
  process.exit(1);
});
