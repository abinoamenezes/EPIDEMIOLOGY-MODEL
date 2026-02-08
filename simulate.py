from __future__ import annotations

import argparse
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

from models import SLITRParams, slitr_rhs


def simulate(y0, days: int, step: float, params: SLITRParams):
    t_eval = np.arange(0.0, float(days) + step, step)
    sol = solve_ivp(
        fun=lambda t, y: slitr_rhs(t, y, params),
        t_span=(0.0, float(days)),
        y0=np.array(y0, dtype=float),
        t_eval=t_eval,
        method="RK45",
        rtol=1e-6,
        atol=1e-9,
    )
    if not sol.success:
        raise RuntimeError(f"Falha na integracao: {sol.message}")
    return sol.t, sol.y


def main():
    ap = argparse.ArgumentParser(description="Simulacao SLITR (Tuberculose)")
    ap.add_argument("--days", type=int, default=365 * 5)
    ap.add_argument("--step", type=float, default=1.0)

    # Populacao inicial
    ap.add_argument("--N", type=int, default=1_000_000)
    ap.add_argument("--I0", type=int, default=200)
    ap.add_argument("--L0", type=int, default=50_000)
    ap.add_argument("--T0", type=int, default=50)
    ap.add_argument("--R0", type=int, default=0)

    # Parametros (valores default plausiveis para estudo, nao "verdade oficial")
    ap.add_argument("--beta", type=float, default=8.0)         # ajuste p/ ter endemia
    ap.add_argument("--eta", type=float, default=0.1)          # tratamento transmite pouco
    ap.add_argument("--sigma", type=float, default=1/365)      # reativacao ~ 1 ano (exemplo)
    ap.add_argument("--delta", type=float, default=1/90)       # diagnostico em ~90 dias
    ap.add_argument("--tau", type=float, default=1/180)        # cura em ~180 dias
    ap.add_argument("--gamma", type=float, default=0.0)        # sem cura espontanea (simplifica)
    ap.add_argument("--theta", type=float, default=0.3)        # reinfeccao parcial
    ap.add_argument("--mu", type=float, default=1/(75*365))    # vida media ~75 anos

    args = ap.parse_args()

    S0 = args.N - args.L0 - args.I0 - args.T0 - args.R0
    if S0 < 0:
        raise ValueError("Populacao inicial invalida: ajuste N/L0/I0/T0/R0.")

    y0 = [S0, args.L0, args.I0, args.T0, args.R0]

    params = SLITRParams(
        beta=args.beta,
        eta=min(max(args.eta, 0.0), 1.0),
        sigma=args.sigma,
        delta=args.delta,
        tau=args.tau,
        gamma=args.gamma,
        theta=min(max(args.theta, 0.0), 1.0),
        mu=args.mu,
    )

    t, y = simulate(y0=y0, days=args.days, step=args.step, params=params)
    S, L, I, T, R = y

    # Metricas simples
    peak_I = float(np.max(I))
    peak_T = float(np.max(T))
    end_I = float(I[-1])
    end_L = float(L[-1])

    print("=== SLITR (TB) ===")
    print(f"Pico I (ativos): {peak_I:,.0f}")
    print(f"Pico T (tratamento): {peak_T:,.0f}")
    print(f"I no final: {end_I:,.0f}")
    print(f"L no final: {end_L:,.0f}")

    plt.figure()
    plt.plot(t, S, label="S")
    plt.plot(t, L, label="L (latente)")
    plt.plot(t, I, label="I (ativo)")
    plt.plot(t, T, label="T (tratamento)")
    plt.plot(t, R, label="R")
    plt.xlabel("Dias")
    plt.ylabel("Pessoas")
    plt.title("Modelo SLITR – Tuberculose (latencia + tratamento)")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
