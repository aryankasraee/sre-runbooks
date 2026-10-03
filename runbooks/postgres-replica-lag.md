# Runbook: PostgreSQL replica is lagging or broken (Patroni)

> Owner: platform · Last verified: 2026-10-03 · Verified how: drill ([patroni-ha-lab](https://github.com/aryankasraee/patroni-ha-lab))

## Symptoms

`patronictl list` shows a member as `stopped`, `start failed`, or with a `Lag` that
keeps growing; replication-lag alert firing; reads from replicas return stale data.

## Impact

Reads on that replica are stale or unavailable. If it was the **synchronous**
standby, **writes can stall** until another standby takes over: treat that as an
outage.

## Diagnose

1. Cluster state: `patronictl -c /etc/patroni/patroni.yml list`
2. Is there a leader and a synchronous standby? No sync standby with
   `synchronous_mode: true` means writes may be blocked: go to Mitigate step 1.
3. Is the member's process up, and is its disk full? A replica that cannot write
   WAL stops replicating.
4. Lag growing with a healthy `streaming` state is usually a long query holding
   back replay on that replica, not a replication fault.

## Mitigate

1. If writes are blocked because no sync standby exists, bring any healthy replica
   back first; Patroni promotes it to synchronous.
2. Broken member: `patronictl -c /etc/patroni/patroni.yml reinit <cluster> <member> --force`.
   **Check the member's role first. Never reinitialize the leader.**
3. Large database: prefer a base backup from another replica over re-cloning from
   the leader, so the leader takes no extra read load.

## Verify

`patronictl list` shows the member `streaming` with `Lag: 0`, and the cluster has
a `Sync Standby` again.

## Escalate

If `reinit` fails twice, or the leader itself is unhealthy, escalate to the
database owner with the output of `patronictl list` and the member's log.

## Do not

- Run `pg_ctl promote` by hand: Patroni will fight you.
- Reinitialize the leader.
- Delete a data directory without confirming which node you are on.
