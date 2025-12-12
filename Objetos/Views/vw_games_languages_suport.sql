CREATE OR REPLACE VIEW vw_games_languages_suport AS
SELECT 
    g.appid,
    g.name,

    COUNT(DISTINCT lg.id_language) AS total_languages,

    STRING_AGG(DISTINCT l.language_name, ', ') AS interface_languages,
    CASE 
        WHEN COUNT(DISTINCT lg.id_language) >= 10 THEN 'Excellent support'
        WHEN COUNT(DISTINCT lg.id_language) >= 5 THEN 'Good support'
        ELSE 'Limited support'
    END AS support_rating

FROM games g
LEFT JOIN languages_game lg
    ON g.appid = lg.id_game
LEFT JOIN languages l 
    ON l.id = lg.id_language

GROUP BY g.appid, g.name
ORDER BY total_languages DESC;