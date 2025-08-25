create table if not exists transit_event (
  id bigserial primary key,
  source text not null,
  line text not null,
  status text not null,
  severity smallint default 0,
  message text,
  started_at timestamptz,
  observed_at timestamptz not null default now()
);

create index if not exists ix_transit_event_line_time
  on transit_event(line, observed_at desc);
