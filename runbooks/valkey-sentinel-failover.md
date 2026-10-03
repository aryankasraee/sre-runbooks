# Runbook: Valkey master failover (Sentinel)

> Owner: platform · Last verified: 2026-10-03 · Verified how: tried against a one-master, one-replica, one-sentinel instance

## Symptoms

Clients get `READONLY` errors or connection resets; Sentinel logs a `+switch-master`;
a master host is down; or you need to move the master on purpose.

## Impact

Writes fail from the moment the old master goes away until clients learn the new
address (seconds, if clients are Sentinel-aware). Data written to the old master
and not yet replicated is lost: Valkey replication is asynchronous.

## Diagnose

All commands run against a Sentinel (port 26379):

1. Who is master now? `valkey-cli -p 26379 SENTINEL get-master-addr-by-name <name>`
2. Replicas and their link state: `valkey-cli -p 26379 SENTINEL replicas <name>`
   (look for `flags: slave` and `master-link-status: ok`).
3. Can a failover be authorized? `valkey-cli -p 26379 SENTINEL ckquorum <name>`
   (expected: `OK <n> usable Sentinels`).

## Mitigate

Planned move of the master:

`valkey-cli -p 26379 SENTINEL failover <name>` replies `OK`, and the new master
address is visible within a few seconds.

Unplanned: Sentinel fails over by itself once the master has been down for
`down-after-milliseconds`. Do not start a second failover on top of it.

## Verify

1. `SENTINEL get-master-addr-by-name <name>` returns the new address.
2. On the new master, `INFO replication` shows `role:master`.
3. **The old master rejoins as a replica by itself**, but not instantly: in the
   test it took about 25 seconds. Confirm with `ROLE` on the old node
   (`slave`) and `connected_slaves` on the new master.

## Escalate

If `ckquorum` fails (not enough Sentinels), no failover can happen: fix the
Sentinels first and escalate to the platform owner.

## Do not

- Promote a replica with `REPLICAOF NO ONE` while Sentinel is managing the set;
  Sentinel will reconfigure it back.
- Assume zero data loss after a failover. Check what the application can tolerate.
