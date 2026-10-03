# Runbook: disk is full on a host

> Owner: platform · Last verified: not yet (standard Linux tools; verify on your hosts)

## Symptoms

`No space left on device`; services crash or stop writing; a disk-usage alert.

## Impact

Anything that writes (databases, logs, temp files) fails. A database on a full disk
can corrupt or stop: treat as urgent.

## Diagnose

1. Which filesystem? `df -h` (and `df -i`: it can be inodes, not bytes).
2. Biggest directories on that filesystem, without crossing mount points:

   ```bash
   sudo du -xh --max-depth=2 /PATH | sort -rh | head -20
   ```

3. Deleted files still held open by a process (space not freed until it exits):

   ```bash
   sudo lsof +L1 | head
   ```

4. Containers: `docker system df` shows images, containers, volumes and build cache.

## Mitigate

Free space in the safest order:

1. Old rotated logs and caches you can regenerate.
2. `docker system prune` only after reading what it will remove. Never add
   `--volumes` without checking: volumes hold data.
3. If a process holds a deleted file open (step 3), restart that process.
4. If the data is legitimately growing, extend the volume and open a ticket for the cause.

## Verify

`df -h` shows headroom, and the service that failed is writing again.

## Escalate

If the disk is a database volume and the database stopped, escalate to the database
owner before restarting it.

## Do not

- `rm` inside a database data directory to "make space".
- Truncate a log file a service is still writing to without knowing whether the
  service tolerates it (`truncate -s 0` is safe for append-only logs, not for
  everything).
