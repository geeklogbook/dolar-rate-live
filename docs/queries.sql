SELECT key AS exchange,
       value->>'ask'       AS ask,
       value->>'bid'       AS bid,
       value->>'time'      AS ts_unix,
       value->>'totalAsk'  AS total_ask,
       value->>'totalBid'  AS total_bid,
       b.data->>'time'     AS global_time,
       b.created_at
FROM bitcoin b,
     jsonb_each(b.data) 
WHERE key <> 'time';