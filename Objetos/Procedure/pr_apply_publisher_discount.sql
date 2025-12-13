CREATE OR REPLACE PROCEDURE pr_apply_publisher_discount(p_publisher_name TEXT, p_percentual_desconto NUMERIC)
AS $$
DECLARE
    var_publisher_id INT;
    var_count INT;
BEGIN
    --desconto deve ser entre 1% e 90%
    IF p_percentual_desconto <= 0 OR p_percentual_desconto > 90 THEN
        RAISE EXCEPTION 'Erro: O desconto deve ser entre 1%% e 90%%. Valor fornecido: %', p_percentual_desconto;
    END IF;

    --Encontrar o ID do publisher
    SELECT id INTO var_publisher_id
    FROM publishers
    WHERE lower(publisher_name) = lower(p_publisher_name);

    IF var_publisher_id IS NULL THEN
        RAISE EXCEPTION 'Publisher "%" não encontrado.', p_publisher_name;
    END IF;

    --Executar o Update
    UPDATE games g
    SET price = price - (price * (p_percentual_desconto / 100.0))
    FROM publishers_game pg
    WHERE g.appid = pg.id_game AND pg.id_publisher = var_publisher_id
      AND g.price > 0; -- Não aplicar desconto em jogos grátis

    GET DIAGNOSTICS var_count = ROW_COUNT;
    
    RAISE NOTICE 'Promoção aplicada! % jogos da % receberam %%% de desconto.', var_count, p_publisher_name, p_percentual_desconto;
END;
$$
LANGUAGE plpgsql;