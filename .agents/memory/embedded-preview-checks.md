---
name: Embedded preview checks
description: Distinguish a healthy server from a browser-blocked embedded preview.
---

When the user reports a blank embedded preview despite successful HTTP requests,
inspect frame-related response headers and the selected canvas frame before
restarting the server again.

**Why:** Repeated server restarts and direct screenshots showed a working site
while the embedded preview was blocked by Django's frame protection.

**How to apply:** A direct screenshot bypasses the iframe's ancestor checks.
Check X-Frame-Options and CSP frame-ancestors separately, and preserve private
page protections when changing preview behavior.
