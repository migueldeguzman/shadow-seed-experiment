# RSI-002 Cron Schedule
Timezone: Asia/Dubai
Sessions per day: 5
Subjects per session: 12
Total sessions/day: 60

| Session | Trigger | Analysis | Cron (trigger) | Cron (analysis) |
|---------|---------|----------|----------------|------------------|
| morning | 10:00 | 11:00 | `00 10 * * *` | `00 11 * * *` |
| afternoon | 16:00 | 17:00 | `00 16 * * *` | `00 17 * * *` |
| evening | 21:00 | 22:00 | `00 21 * * *` | `00 22 * * *` |
| midnight | 00:00 | 01:00 | `00 00 * * *` | `00 01 * * *` |
| latenight | 03:00 | 04:00 | `00 03 * * *` | `00 04 * * *` |
