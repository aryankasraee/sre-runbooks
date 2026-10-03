# Runbook: pod in CrashLoopBackOff

> Owner: platform · Last verified: not yet (standard kubectl; verify against your cluster)

## Symptoms

`kubectl get pods` shows `CrashLoopBackOff` or a climbing `RESTARTS` count.

## Impact

The workload has fewer healthy replicas than intended. Check the Deployment's
`READY` count to see whether users are affected.

## Diagnose

1. What happened last time it died:

   ```bash
   kubectl -n NS describe pod POD | sed -n '/Last State/,/Ready:/p'
   kubectl -n NS logs POD --previous --tail=100
   ```

2. Read the exit code in `Last State`:
   - `137` / `OOMKilled`: memory limit too low or a leak; see `kubectl top pod`.
   - `1` or `2`: the application failed on start; the previous logs say why.
   - `Error` right after a deploy: a bad config, secret, or image.
3. Did it start with the last rollout? `kubectl -n NS rollout history deploy/NAME`.
4. Failing probes also restart a healthy app: check `Liveness probe failed` events
   in `describe`.

## Mitigate

- Started at a deploy: `kubectl -n NS rollout undo deploy/NAME`, then investigate.
- OOMKilled: raise the memory limit through a reviewed change, not `kubectl edit`.
- Bad liveness probe: loosen `initialDelaySeconds` / `timeoutSeconds` through git.

## Verify

`kubectl -n NS get pods` shows `Running` with a stable `RESTARTS` count for several
minutes, and the Deployment's `READY` matches `DESIRED`.

## Escalate

If the previous logs show a dependency failure (database, queue), escalate to that
dependency's owner with the log excerpt.

## Do not

- `kubectl delete pod` in a loop: you destroy the evidence in `--previous`.
- Edit live objects that GitOps manages: they are reverted, and you teach nobody
  anything.
