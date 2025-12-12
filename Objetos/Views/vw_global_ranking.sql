CREATE OR REPLACE VIEW vw_global_ranking AS
SELECT
    g.appid,
    g.name,
    d.metacritic_score,
    d.recommendations,
    d.owners_min,
    d.owners_max,
    d.average_playtime_forever,
    
    CASE
        WHEN (d.positive + d.negative) > 0 
        THEN d.positive::numeric / (d.positive + d.negative)
        ELSE NULL
    END AS positive_ratio,

    (

        COALESCE(d.score_rank, 0) * 3 +
        COALESCE(d.metacritic_score, 0) * 2 +
        COALESCE(d.user_score, 0) * 2 +
        COALESCE(d.recommendations, 0) * 0.5 +
        COALESCE(d.average_playtime_forever, 0) / 20 +
        COALESCE(d.owners_max, 0) / 2000 +
        COALESCE(d.positive - d.negative, 0)
    ) AS global_score

FROM games g
JOIN detalhes d ON d.id_game = g.appid
ORDER BY global_score DESC
LIMIT 100;