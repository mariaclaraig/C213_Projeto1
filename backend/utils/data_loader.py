import numpy as np
from scipy.io import loadmat

CHAVES_TEMPO   = ['t', 'time', 'tempo', 'tiempo', 'T']
CHAVES_SAIDA   = ['y', 'output', 'saida', 'salida', 'Y', 'out']
CHAVES_ENTRADA = ['u', 'input', 'entrada', 'U', 'in_']

def carregar_mat(caminho_arquivo):
    """
    Carrega arquivo .mat e retorna dicionário padronizado com os dados do processo.

    Parâmetros:
        caminho_arquivo (str): caminho completo para o arquivo .mat

    Retorna:
        dict com chaves: t, y, u, unidade_t, unidade_y, grandeza_y

    Lança:
        ValueError se o arquivo não contiver as variáveis esperadas
        FileNotFoundError se o arquivo não existir
    """
    try:
        dados = loadmat(caminho_arquivo)
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")
    except Exception as e:
        raise ValueError(f"Erro ao ler o arquivo .mat: {str(e)}")

    chaves_validas = {k: v for k, v in dados.items() if not k.startswith('_')}

    t = _encontrar_vetor(chaves_validas, CHAVES_TEMPO, 'tempo')
    y = _encontrar_vetor(chaves_validas, CHAVES_SAIDA, 'saída')
    u = _encontrar_vetor(chaves_validas, CHAVES_ENTRADA, 'entrada')

    unidade_t  = _extrair_metadata(chaves_validas, ['unidade_t', 'unit_t'], 's')
    unidade_y  = _extrair_metadata(chaves_validas, ['unidade_y', 'unit_y'], '-')
    grandeza_y = _extrair_metadata(chaves_validas, ['grandeza_y', 'variable_y'], 'Saída')

    return {
        't': t,
        'y': y,
        'u': u,
        'unidade_t': unidade_t,
        'unidade_y': unidade_y,
        'grandeza_y': grandeza_y
    }


def _encontrar_vetor(dados, candidatos, nome_legivel):
    """Procura um vetor no dict de dados usando lista de nomes candidatos."""
    for chave in candidatos:
        if chave in dados:
            vetor = np.array(dados[chave]).flatten()
            return vetor
    chaves_disponiveis = list(dados.keys())
    raise ValueError(
        f"Variável de '{nome_legivel}' não encontrada no arquivo.\n"
        f"Chaves disponíveis: {chaves_disponiveis}\n"
        f"Esperava uma dessas: {candidatos}"
    )


def _extrair_metadata(dados, candidatos, padrao):
    """Extrai string de metadado ou retorna valor padrão."""
    for chave in candidatos:
        if chave in dados:
            val = dados[chave]
            if hasattr(val, 'flat'):
                return str(list(val.flat)[0]).strip()
            return str(val).strip()
    return padrao
