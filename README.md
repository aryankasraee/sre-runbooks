# sre-runbooks

Runbooks and a postmortem template written to be used at 3 a.m. by someone who did
not write them.

## Runbooks

| Situation | Verified |
|---|---|
| [PostgreSQL replica lag or failure (Patroni)](runbooks/postgres-replica-lag.md) | drill, see [patroni-ha-lab](https://github.com/aryankasraee/patroni-ha-lab) |
| [Valkey master failover (Sentinel)](runbooks/valkey-sentinel-failover.md) | tried on a real instance |
| [TLS certificate expired or expiring](runbooks/tls-certificate-expiry.md) | commands run against a live site |
| [Pod in CrashLoopBackOff](runbooks/kubernetes-crashloopbackoff.md) | not yet (standard kubectl) |
| [Disk full](runbooks/disk-full.md) | not yet (standard Linux tools) |

The **Verified** column is honest on purpose. A runbook nobody has tried is a
draft; each file states how it was checked at the top.

## Templates

- [`templates/runbook.md`](templates/runbook.md): Symptoms, Impact, Diagnose, Mitigate, Verify, Escalate, Do not.
- [`templates/postmortem.md`](templates/postmortem.md): blameless, with a timeline and owned action items.

## What makes a runbook usable

- **Starts from what the on-call sees** (the alert, the error), not from the architecture.
- **Says how bad it is** (Impact) before saying what to do, so the on-call can decide to escalate.
- **Cheapest checks first**, each with a decision attached.
- **Reversible actions first**, with irreversible ones named.
- **Ends with Verify**: the exact command and the expected result.
- **A "Do not" section.** The tempting mistake is usually the real incident.

## Checked in CI

`scripts/check_runbooks.py` fails the build if a runbook is missing a required
section, has no `Last verified` line, or links to a file that does not exist.
Run it locally with `python3 scripts/check_runbooks.py`.

## License

MIT
