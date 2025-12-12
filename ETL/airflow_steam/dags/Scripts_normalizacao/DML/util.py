import re
import html
from datetime import datetime

PATTERN_CLEAN_PREFIX = re.compile(
    r'^('
    # Palavras Técnicas
    r'(?:Verdict|Review|Score|Rated|Rating|Grade|Rank|Award|Winner|Nominee|Recc?omm?ended|No\s+Score)'
    r'|'
    # Notas e Números (comuns e complexos)
    r'(?:N/?A|Out\s+of\s+\w+|Total\s+Score|\+1)' # Removi o [A-F] daqui
    r'|'
    # --- CORREÇÃO AQUI ---
    # Notas Escolares (A-F) AGORA EXIGEM FRONTEIRA (\b)
    # Isso impede que o "D" de "Dualshockers" seja pego, mas pega "D - IGN"
    r'(?:\b[A-F][+-]?(?=\s|[-–:]|$))' 
    r'|'
    # Padrões Numéricos (8.5, 9/10, 85%)
    r'(?:\d+(?:[.,]\d+)?(?:\s*/\s*\d+)?(?:\s*%)?)'
    
    # Limpa sufixos e separadores
    r')\s*(?:stars?|estrelas?|pts)?\s*[-–:]?\s*', 
    re.IGNORECASE | re.UNICODE
)

# Regex para detectar URLs (Segurança)
PATTERN_IS_URL = re.compile(r'(?:www\.|http|\.com|\.net|\.org|review|index\.php|[a-z0-9]+-[a-z0-9]+-[a-z0-9]+)', re.IGNORECASE)

# ==============================================================================
# 2. LISTA DE SEPARADORES (Fase 2)
# ==============================================================================
SEPARATORS = [" – ", " - ", " : ", ": "] 

def clean_author_hybrid(raw_name):
    if not raw_name:
        return None
    
    # 1. Decodificação e Normalização
    # Transforma &ndash; em –, remove espaços extras
    name = html.unescape(raw_name).strip()
    
    # ------------------------------------------------------------------
    # FASE 1: Limpeza baseada em Regras (Regex)
    # Isso ajuda nos casos onde NÃO TEM traço separador.
    # ------------------------------------------------------------------
    name = PATTERN_CLEAN_PREFIX.sub('', name)
    
    # ------------------------------------------------------------------
    # FASE 2: Limpeza baseada em Estrutura (Separadores)
    # Procura o ÚLTIMO separador e pega o que está à direita.
    # ------------------------------------------------------------------
    for sep in SEPARATORS:
        if sep in name:
            # rsplit divide da direita para esquerda. Limit=1 garante apenas 1 corte.
            # Ex: "Review: Best Game – IGN" -> ['Review: Best Game', 'IGN']
            parts = name.rsplit(sep, 1)
            candidate = parts[-1].strip()
            
            # Só aceita a troca se o lado direito tiver conteúdo
            if len(candidate) > 1:
                name = candidate
                break # Achou um separador válido, para de procurar.

    # 3. Limpeza Final
    name = name.strip(' -–,:"\'/\\|[]()')


    #Tamanho (Elimina erros de parse e iniciais soltas)
    if len(name) < 2 or len(name) > 50:
        return None

    # Detecção de URL/Slug/Caminho
    if PATTERN_IS_URL.search(name) or '/' in name:
        return None

    #Caracteres de Código
    if any(char in name for char in ['{', '}', '”', '“']):
        return None

    #Tem que ter letra (Mata o "☢️💤", "+1" ou só numeros)
    if not re.search(r'[a-zA-Z\u00C0-\u00FF\u4e00-\u9fa5]', name):
        return None

    return name

# ==============================================================================
# PARSEAMENTO DO ARQUIVO
# ==============================================================================
PATTERN_EXTRACT = re.compile(r'“([^”]+)”\s*([^“]*)')

def parse_reviews(string):
    if string == "":
        return ""
    
    extracted = []

    matches = PATTERN_EXTRACT.findall(string)
    for review, raw_author in matches:
        if not review.strip(): continue

        cleaned = clean_author_hybrid(raw_author)
        
        if cleaned:
            # Regra extra para evitar que a palavra "reviews" vire autor
            if cleaned.lower() in ['reviews', 'review']: continue

            extracted.append({
                'author': cleaned,
                'review': review.strip()
            })

    return extracted

def string_to_postgres_date(date_str):
    """
    Converte datas da Steam para formato PostgreSQL 'YYYY-MM-DD'.
    Suporta:
    1. 'May 8, 2020' -> '2020-05-08'
    2. 'May 2020'    -> '2020-05-01' (assume dia 1)
    3. '2020'        -> '2020-01-01' (assume 1 de Jan)
    """
    if not date_str:
        return None
        
    clean_date = date_str.strip()
    
    # Lista de tentativas de formatos, do mais específico para o mais genérico
    formats = [
        "%b %d, %Y", # Padrão: "Oct 21, 2015"
        "%b %Y",     # Sem dia: "Sep 2014" -> Vira 2014-09-01
        "%Y"         # Apenas ano (raro mas acontece): "2018" -> Vira 2018-01-01
    ]
    
    for fmt in formats:
        try:
            date_obj = datetime.strptime(clean_date, fmt).date()
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            continue # Tenta o próximo formato da lista
    
    return None


def safe_int(value, default=0):
    # Converte para int, retornando 0 se falhar ou for vazio
    if not value:
        return default
    try:
        return int(float(value)) # float resolve casos como "0.0" vindo como string
    except (ValueError, TypeError):
        return default

def safe_float(value, default=0.0):
    # Converte para float, lidando com valores estranhos
    if not value:
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def parse_owners(owners_str):
    """
    Transforma '20000 - 50000' em dois inteiros: (20000, 50000)
    se falhar, retorna (0, 0).
    """
    if not owners_str or not isinstance(owners_str, str):
        return 0, 0
    
    parts = owners_str.split(" - ")
    if len(parts) == 2:
        return safe_int(parts[0]), safe_int(parts[1])
    return 0, 0