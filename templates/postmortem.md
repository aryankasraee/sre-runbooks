# Postmortem: <title>

**Date:** <YYYY-MM-DD> · **Severity:** <SEV> · **Authors:** <names> · **Status:** draft | final

Blameless: this document describes what the system and the process allowed, not who
failed.

## Summary

Two or three sentences a stranger could read.

## Impact

What users saw, for how long, how many. Include the error budget spent if there is an SLO.

## Timeline (UTC)

| Time | Event |
|---|---|
| hh:mm | First sign (alert, report, deploy) |
| hh:mm | Detected |
| hh:mm | Mitigation started |
| hh:mm | Resolved |

Detection time and time-to-mitigate are the two numbers worth tracking over time.

## Root cause

The chain of causes, not one cause. Ask "why" until the answer is about a missing
guardrail, not a person.

## What went well / what went badly / where we were lucky

Luck is a finding: write down what would have made it worse.

## Action items

| Action | Owner | Due | Prevents / detects / mitigates |
|---|---|---|---|

An action item without an owner and a date is a wish.
