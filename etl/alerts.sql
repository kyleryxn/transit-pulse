-- etl/alerts.sql

create table if not exists alerts (
  alert_id text primary key,
  line text not null,
  category text not null,         -- DELAY | PLANNED_WORK | SERVICE_CHANGE | ...
  severity smallint not null,     -- 0..3 (derived ordering)
  title text,
  description text,
  start_at timestamptz,
  end_at timestamptz,
  updated_at timestamptz not null,
  status text not null default 'active'  -- active | expired
);

create index if not exists ix_alerts_line_active
  on alerts(line)
  where status = 'active';
