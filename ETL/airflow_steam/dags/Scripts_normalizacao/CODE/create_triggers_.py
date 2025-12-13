import psycopg2
from DML.config import DB_CONFIG
 
def create_triggers():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SET search_path TO public;")
    conn.commit()
    # Aqui foi alterado a lógica da trigger fn_limit_tags_per_game devido ter jogos que quebram a regra de negócio.
    # Retorno alterado para NULL
    # Outra alteração foi o WHEN em update_user_score_before para evitar execuções desnecessárias
    cur.execute("""
        CREATE OR REPLACE FUNCTION update_user_score_before()
        RETURNS TRIGGER AS $$
        DECLARE
            pos INTEGER := COALESCE(NEW.positive, 0);
            neg INTEGER := COALESCE(NEW.negative, 0);
            total INTEGER;
        BEGIN
            IF TG_OP = 'UPDATE' THEN
                IF (OLD.positive IS NOT DISTINCT FROM NEW.positive) AND
                (OLD.negative IS NOT DISTINCT FROM NEW.negative) THEN
                    RETURN NEW;
                END IF;
            END IF;

            total := pos + neg;
  
            NEW.user_score := ROUND((pos::numeric * 100) / total)::INTEGER;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_update_user_score
        BEFORE INSERT OR UPDATE ON detalhes
        FOR EACH ROW
        WHEN (NEW.positive != 0 AND NEW.negative != 0)
        EXECUTE FUNCTION update_user_score_before();

        CREATE OR REPLACE FUNCTION trg_add_mature_tag_improved()
        RETURNS trigger AS $$
        BEGIN
        
            IF NEW.required_age >= 18 THEN
                CALL pr_safe_link_tag(NEW.appid, 'mature'); --PROCEDURE QUE CRIAMOS
            END IF;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_games_add_mature
        AFTER INSERT ON games
        FOR EACH ROW
        WHEN (NEW.required_age IS NOT NULL AND NEW.required_age >= 18)
        EXECUTE FUNCTION trg_add_mature_tag_improved();
        
        CREATE OR REPLACE FUNCTION fn_limit_tags_per_game()
        RETURNS TRIGGER AS $$
        DECLARE
            qtd_tags_atuais INT;
            LIMITE_TAGS CONSTANT INT := 20;
        BEGIN
            SELECT COUNT(*) INTO qtd_tags_atuais
            FROM tags_game
            WHERE id_game = NEW.id_game;
            
            IF qtd_tags_atuais >= LIMITE_TAGS THEN
                RETURN NULL; 
            END IF;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        
        CREATE TRIGGER tg_check_tag_limit
        BEFORE INSERT ON tags_game
        FOR EACH ROW
        EXECUTE FUNCTION fn_limit_tags_per_game();
        """
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Triggers criadas com sucesso.")
 
 