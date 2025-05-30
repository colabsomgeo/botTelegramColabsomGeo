

import numpy as np
from scipy.signal import bilinear, lfilter
import librosa 

from speechbrain.pretrained import EncoderClassifier
model = EncoderClassifier.from_hparams(
  "speechbrain/urbansound8k_ecapa"
)

def aplicar_a_weighting(sr, y):
   
    # Frequências e constantes para A-Weighting
    f1, f2, f3, f4 = 20.598997, 107.65265, 737.86223, 12194.217

    A1000 = (f4**2) * (f3**2) / (((f1**2) + (1000**2)) * np.sqrt((f2**2) + (1000**2)) * ((f4**2) + (1000**2)))

    # Coeficientes do filtro
    NUMs = [(2 * np.pi * f4)**2 * (10 ** (A1000 / 20.0)), 0, 0, 0, 0]
    DENs = np.convolve(
        [1, 4 * np.pi * f4, (2 * np.pi * f4)**2],
        np.convolve(
            [1, 4 * np.pi * f1, (2 * np.pi * f1)**2],
            [1, 2 * np.pi * f3]
        )
    )

    # Transformação bilinear para filtro digital
    b, a = bilinear(NUMs, DENs, sr)
    
    # Aplica o filtro ao sinal de áudio
    y_weighted = lfilter(b, a, y)
    
    return y_weighted
def extrair_informacoes_audio(caminho_arquivo):
    """
    Extrai informações de áudio, incluindo RMS, dB, e A-Weighting.
    :param caminho_arquivo: Caminho para o arquivo de áudio
    :return: Dicionário com informações extraídas
    """
    # Carregar o arquivo de áudio
    y, sr = librosa.load(caminho_arquivo)

    # Calcular RMS (Root Mean Square) - média quadrática de ruído
    rms = librosa.feature.rms(y=y)[0]

    # Nível mínimo e máximo de decibéis
    min_db = np.min(librosa.amplitude_to_db(y))
    max_db = np.max(librosa.amplitude_to_db(y))

    # RMS médio
    rms_media = np.mean(rms)

    # Aplicar o filtro A-Weighting
    y_weighted = aplicar_a_weighting(sr, y)

    # Calcular decibéis mínimos e máximos com A-Weighting
    min_dBA = np.min(librosa.amplitude_to_db(y_weighted))
    max_dBA = np.max(librosa.amplitude_to_db(y_weighted))

    return {
        "min_db": float(min_db),
        "max_db": float(max_db),
        "min_dBA": float(min_dBA),
        "max_dBA": float(max_dBA),
        "rms_loudness": float(rms_media)
    }

def classificar_audio(caminho_arquivo):
    # Executa a inferência com o classificador
    output = model.classify_file(caminho_arquivo)
    
    # Retorna a classe predita e a pontuação (opcional)
    predicted_class = output[3]  # index 3 contém o nome da classe
    score = output[2].item()     # index 2 contém o score de confiança (tensor)
    
    return predicted_class[0]

