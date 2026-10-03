# Runbook: TLS certificate expired or about to

> Owner: platform · Last verified: 2026-10-03 · Verified how: commands run against a live public site

## Symptoms

Browsers show `NET::ERR_CERT_DATE_INVALID`; clients fail with `certificate has
expired`; an expiry alert fires.

## Impact

Every client that validates certificates fails for that hostname: effectively an
outage for that service.

## Diagnose

1. What certificate is actually being served (not what you think is deployed):

   ```bash
   echo | openssl s_client -connect HOST:443 -servername HOST 2>/dev/null \
     | openssl x509 -noout -subject -issuer -enddate
   ```

2. Will it last? Exit code 0 means valid for at least another 30 days:

   ```bash
   echo | openssl s_client -connect HOST:443 -servername HOST 2>/dev/null \
     | openssl x509 -noout -checkend $((30*86400))
   ```

3. Does it cover the name, and does the chain verify?

   ```bash
   echo | openssl s_client -connect HOST:443 -servername HOST 2>/dev/null \
     | openssl x509 -noout -ext subjectAltName
   echo | openssl s_client -connect HOST:443 -servername HOST -verify_return_error 2>&1 \
     | grep 'Verify return'
   ```

4. Is every instance serving the same certificate? Check each backend and each
   load-balancer node, not just one: a stale instance is a common cause.

## Mitigate

1. Find out why renewal did not happen (expired ACME account, DNS validation
   broken, rate limit, a renewal job that never ran) before re-issuing. Re-issuing
   without that just fails the same way.
2. Issue or renew, deploy to every instance, and reload (many servers need an
   explicit reload to pick up a new file).

## Verify

Run Diagnose step 1 against **every** instance and confirm the new `notAfter`.

## Escalate

If a certificate authority rate limit is the cause, escalate before retrying:
retrying burns the remaining quota.

## Do not

- Disable certificate verification in clients to "fix" it.
- Bulk-replace certificates for many domains at once: stagger them, so one bad
  renewal path cannot take everything down together.
