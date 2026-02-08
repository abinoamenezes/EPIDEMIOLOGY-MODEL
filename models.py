from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class SLITRParams:
    beta: float    # transmissao
    eta: float     # reducao de transmissao em tratamento (0..1)
    sigma: float   # reativacao L -> I
    delta: float   # deteccao/inicio tratamento I -> T
    tau: float     # cura do tratamento T -> R
    gamma: float   # recuperacao sem tratamento I -> R (geralmente baixa)
    theta: float   # reinfeccao de R (0..1, imunidade parcial)
    mu: float      # natalidade/mortalidade natural


def _nn(x: np.ndarray) -> np.ndarray:
    # evita negativos por erro numerico
    return np.maximum(x, 0.0)


def slitr_rhs(t: float, y: np.ndarray, p: SLITRParams) -> np.ndarray:
    """
    Modelo SLITR (TB):
      S: suscetiveis
      L: latentes (nao transmitem)
      I: ativos (transmitem)
      T: em tratamento (transmissao reduzida)
      R: recuperados (imunidade parcial)
    Com nascimentos/mortes naturais (mu) mantendo N ~ constante.
    """
    S, L, I, T, R = _nn(y)
    N = S + L + I + T + R
    if N <= 0:
        return np.zeros_like(y)

    # Forca de infeccao: I + eta*T
    lam = p.beta * (I + p.eta * T) / N

    dS = p.mu * N - lam * S - p.mu * S
    dL = lam * S + p.theta * lam * R - (p.sigma + p.mu) * L
    dI = p.sigma * L - (p.delta + p.gamma + p.mu) * I
    dT = p.delta * I - (p.tau + p.mu) * T
    dR = p.tau * T + p.gamma * I - p.theta * lam * R - p.mu * R

    return np.array([dS, dL, dI, dT, dR], dtype=float)
