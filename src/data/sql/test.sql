 select 
                             horse.id,
                             coalesce(count(ticket.horse_id), 0) as horse_count 
                             
                             from horse 
                             left join ticket on ticket.horse_id = horse.id 
                             where horse.race_id = 1
                             group by horse.id
                             order by horse_count asc