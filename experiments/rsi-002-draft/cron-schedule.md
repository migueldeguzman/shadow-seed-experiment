# RSI-002 Cron Schedule
Timezone: Asia/Dubai
Sessions per day: 24 (hourly, every hour on the hour)
Subjects per session: 8
Total sessions/day: 192

## Current Schedule (Hourly)

| Job | Cron Expression | Description |
|-----|----------------|-------------|
| `rsi-002-hourly` | `0 * * * *` | Trigger session for all 8 subjects every hour |

## Previous Schedule (Deprecated)

The original schedule used 3 named sessions per day. This was replaced with hourly sessions on 2026-02-20 for faster data collection.

| Session | Trigger | Cron (trigger) | Status |
|---------|---------|----------------|--------|
| ~~morning~~ | ~~10:00~~ | ~~`00 10 * * *`~~ | REMOVED |
| ~~afternoon~~ | ~~16:00~~ | ~~`00 16 * * *`~~ | REMOVED |
| ~~evening~~ | ~~21:00~~ | ~~`00 21 * * *`~~ | REMOVED |
