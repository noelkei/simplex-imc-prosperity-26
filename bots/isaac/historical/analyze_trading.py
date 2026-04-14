"""
EDA de microestructura de mercado
==================================
Explora en detalle los CSV de prices y trades para entender
qué señales son útiles antes de construir una estrategia.

Uso:
    python eda_trading.py
    python eda_trading.py --data ./data --output ./eda_output
"""

import argparse, os, glob, re
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import FuncFormatter

DATA_DIR   = "./data"
OUTPUT_DIR = "./eda_output"
SEP = "─" * 70

# ════════════════════════════════════════════════════════
#  CARGA
# ════════════════════════════════════════════════════════

def parse_day(f): 
    m = re.search(r"day_(-?\d+)", f)
    return int(m.group(1)) if m else 0

def load_all(data_dir):
    pf = sorted(glob.glob(f"{data_dir}/prices_*.csv"), key=parse_day)
    tf = sorted(glob.glob(f"{data_dir}/trades_*.csv"),  key=parse_day)
    if not pf:
        raise FileNotFoundError(f"No hay prices_*.csv en {data_dir!r}")

    def read(files):
        dfs = []
        for f in files:
            df = pd.read_csv(f, sep=";")
            df.columns = df.columns.str.strip().str.lower()
            df["day"] = parse_day(f)
            df["global_ts"] = df["day"] * 1_000_000 + df["timestamp"]
            dfs.append(df)
        return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

    return read(pf), read(tf)


# ════════════════════════════════════════════════════════
#  SECCIÓN 1 — ESTRUCTURA BRUTA
# ════════════════════════════════════════════════════════

def section_structure(prices, trades):
    print(f"\n{'═'*70}")
    print("  SECCIÓN 1 · ESTRUCTURA DE LOS DATOS")
    print(f"{'═'*70}")

    print(f"\n{'── PRICES ──':}")
    print(f"  Filas       : {len(prices):,}")
    print(f"  Columnas    : {list(prices.columns)}")
    print(f"  Productos   : {sorted(prices['product'].unique())}")
    print(f"  Días        : {sorted(prices['day'].unique())}")
    print(f"  Ticks/prod  : {prices.groupby(['product','day']).size().to_dict()}")
    print(f"\n  Primeras filas:")
    print(prices.head(3).to_string())

    if not trades.empty:
        print(f"\n{'── TRADES ──':}")
        print(f"  Filas       : {len(trades):,}")
        print(f"  Columnas    : {list(trades.columns)}")
        print(f"  Símbolos    : {sorted(trades['symbol'].unique())}")
        print(f"\n  Primeras filas:")
        print(trades.head(3).to_string())

    # Nulos
    print(f"\n{'── NULOS EN PRICES ──':}")
    null_pct = (prices.isnull().sum() / len(prices) * 100).round(2)
    print(null_pct[null_pct > 0].to_string() if null_pct.any() else "  Ninguno")

    if not trades.empty:
        print(f"\n{'── NULOS EN TRADES ──':}")
        null_t = (trades.isnull().sum() / len(trades) * 100).round(2)
        print(null_t[null_t > 0].to_string() if null_t.any() else "  Ninguno")


# ════════════════════════════════════════════════════════
#  SECCIÓN 2 — LIBRO DE ÓRDENES
# ════════════════════════════════════════════════════════

def section_orderbook(prices):
    print(f"\n{'═'*70}")
    print("  SECCIÓN 2 · LIBRO DE ÓRDENES")
    print(f"{'═'*70}")

    bid_p = sorted([c for c in prices.columns if re.match(r"bid_price_\d", c)])
    ask_p = sorted([c for c in prices.columns if re.match(r"ask_price_\d", c)])
    bid_v = sorted([c for c in prices.columns if re.match(r"bid_volume_\d", c)])
    ask_v = sorted([c for c in prices.columns if re.match(r"ask_volume_\d", c)])

    print(f"\n  Niveles detectados : {len(bid_p)} bid / {len(ask_p)} ask")

    for product in sorted(prices["product"].unique()):
        sub = prices[prices["product"] == product].copy()
        # Ticks con libro vacío
        if bid_p:
            empty_bid = (sub[bid_p[0]].isna() | (sub[bid_p[0]] == 0)).sum()
            empty_ask = (sub[ask_p[0]].isna() | (sub[ask_p[0]] == 0)).sum()
            print(f"\n  [{product}]")
            print(f"    Ticks sin bid L1 : {empty_bid:,}  ({empty_bid/len(sub)*100:.1f}%)")
            print(f"    Ticks sin ask L1 : {empty_ask:,}  ({empty_ask/len(sub)*100:.1f}%)")

            valid = sub[sub[bid_p[0]] > 0]
            if len(valid) and ask_p:
                spread = valid[ask_p[0]] - valid[bid_p[0]]
                print(f"    Spread L1 (válido): mean={spread.mean():.2f}  std={spread.std():.2f}  min={spread.min():.0f}  max={spread.max():.0f}")
            
            # ¿El mid_price es consistente con bid/ask?
            if "mid_price" in sub.columns and ask_p:
                calc_mid = (valid[bid_p[0]] + valid[ask_p[0]]) / 2
                diff = (valid["mid_price"] - calc_mid).abs()
                print(f"    Desviación mid_price vs (bid+ask)/2: max={diff.max():.4f}")

            # Volumen medio por nivel
            if bid_v:
                print(f"    Volumen medio bid por nivel: " +
                      " | ".join(f"L{i+1}={sub[c].mean():.1f}" for i,c in enumerate(bid_v)))
            if ask_v:
                print(f"    Volumen medio ask por nivel: " +
                      " | ".join(f"L{i+1}={sub[c].mean():.1f}" for i,c in enumerate(ask_v)))


# ════════════════════════════════════════════════════════
#  SECCIÓN 3 — PRECIO: DRIFT, VOLATILIDAD, AUTOCORRELACIÓN
# ════════════════════════════════════════════════════════

def section_price_dynamics(prices):
    print(f"\n{'═'*70}")
    print("  SECCIÓN 3 · DINÁMICA DE PRECIOS")
    print(f"{'═'*70}")

    for product in sorted(prices["product"].unique()):
        sub = prices[prices["product"] == product].sort_values("global_ts").copy()
        mid = sub["mid_price"] if "mid_price" in sub.columns else None
        if mid is None:
            continue

        # Filtrar ticks con mid = 0
        mid_valid = mid[mid > 0]
        pct_valid = len(mid_valid) / len(mid) * 100

        print(f"\n  [{product}]")
        print(f"    Ticks con mid_price > 0 : {len(mid_valid):,} ({pct_valid:.1f}%)")

        if len(mid_valid) < 10:
            print("    Insuficientes datos válidos.")
            continue

        # Returns tick a tick
        ret = mid_valid.pct_change().dropna()
        print(f"    Return medio/tick  : {ret.mean()*1e4:.4f} bps")
        print(f"    Volatilidad/tick   : {ret.std()*1e4:.4f} bps")
        print(f"    Skewness           : {ret.skew():.4f}")
        print(f"    Kurtosis           : {ret.kurtosis():.4f}")

        # Drift lineal intra-día
        for day in sorted(sub["day"].unique()):
            s_day = sub[sub["day"] == day]
            m_day = s_day["mid_price"][s_day["mid_price"] > 0]
            if len(m_day) < 10:
                continue
            x = np.arange(len(m_day))
            slope, intercept = np.polyfit(x, m_day.values, 1)
            r2 = np.corrcoef(x, m_day.values)[0,1]**2
            print(f"    Día {day:>3}  slope={slope:+.4f}/tick  R²={r2:.4f}  "
                  f"(+{slope*len(m_day):.1f} total en el día)")

        # Autocorrelación de returns (¿hay momentum o mean-reversion?)
        if len(ret) > 20:
            ac1 = ret.autocorr(1)
            ac2 = ret.autocorr(2)
            ac5 = ret.autocorr(5)
            print(f"    Autocorr returns  : lag1={ac1:+.4f}  lag2={ac2:+.4f}  lag5={ac5:+.4f}")
            if ac1 < -0.1:
                print(f"    → Señal mean-reversion (neg. en lag1)")
            elif ac1 > 0.1:
                print(f"    → Señal momentum (pos. en lag1)")
            else:
                print(f"    → Sin autocorrelación clara en returns")


# ════════════════════════════════════════════════════════
#  SECCIÓN 4 — TRADES: MICROESTRUCTURA
# ════════════════════════════════════════════════════════

def section_trades(trades, prices):
    if trades.empty:
        return

    print(f"\n{'═'*70}")
    print("  SECCIÓN 4 · MICROESTRUCTURA DE TRADES")
    print(f"{'═'*70}")

    for symbol in sorted(trades["symbol"].unique()):
        t = trades[trades["symbol"] == symbol].sort_values("global_ts").copy()
        print(f"\n  [{symbol}]")

        # ── Frecuencia ─────────────────────────────────────
        for day in sorted(t["day"].unique()):
            td = t[t["day"] == day]

            ts_range = td["timestamp"].max() - td["timestamp"].min()
            freq = len(td) / ts_range if ts_range > 0 else np.nan

            vwap = (
                td["price"].mul(td["quantity"]).sum() / td["quantity"].sum()
                if td["quantity"].sum() > 0 else np.nan
            )

            print(
                f"    Día {day:>3}  trades={len(td)}  vol={td['quantity'].sum()}  "
                f"VWAP={vwap:.2f}  "
                f"freq={freq*1e3:.3f} trades/1000ticks"
            )

        # ── Distribución de cantidades ─────────────────────
        q = t["quantity"]
        print(
            f"    Quantity  : min={q.min():.0f}  median={q.median():.0f}  "
            f"mean={q.mean():.2f}  max={q.max():.0f}"
        )
        print(f"    Top qtys  : {q.value_counts().head(5).to_dict()}")

        # ── Participantes ──────────────────────────────────
        if (
            "buyer" in t.columns and
            "seller" in t.columns and
            (t["buyer"].notna().any() or t["seller"].notna().any())
        ):
            buyers  = t["buyer"].dropna().unique()
            sellers = t["seller"].dropna().unique()

            print(f"    Buyers únicos  : {len(buyers)}  {list(buyers[:5])}")
            print(f"    Sellers únicos : {len(sellers)}  {list(sellers[:5])}")

            # Actividad por participante
            all_parts = set(buyers) | set(sellers)
            rows = []

            for p in all_parts:
                bought = t.loc[t["buyer"] == p, "quantity"].sum()
                sold   = t.loc[t["seller"] == p, "quantity"].sum()

                rows.append({
                    "participant": p,
                    "bought": bought,
                    "sold": sold,
                    "net": bought - sold,
                })

            df_p = pd.DataFrame(rows)

            if not df_p.empty and "net" in df_p.columns:
                df_p = df_p.sort_values("net", ascending=False)

                print(f"\n    Flujo neto por participante:")
                print(df_p.to_string(index=False))
            else:
                print("    No hay datos suficientes de participantes")

        else:
            print("    No hay información de buyer/seller")

        # ── Impacto de precio ──────────────────────────────
        sub_p = prices[prices["product"] == symbol].sort_values("global_ts")

        if "mid_price" in sub_p.columns and len(sub_p) > 0:
            merged = pd.merge_asof(
                t.sort_values("global_ts"),
                sub_p[["global_ts", "mid_price"]].rename(columns={"mid_price": "mid"}),
                on="global_ts",
                direction="nearest",
            )

            diff = merged["price"] - merged["mid"]

            print(
                f"\n    Desvío trade vs mid  : mean={diff.mean():+.2f}  "
                f"std={diff.std():.2f}  (+ = trade por encima del mid)"
            )
            print(f"    % trades sobre mid   : {(diff > 0).mean()*100:.1f}%")
            print(f"    % trades bajo mid    : {(diff < 0).mean()*100:.1f}%")


# ════════════════════════════════════════════════════════
#  SECCIÓN 5 — SEÑALES POTENCIALES
# ════════════════════════════════════════════════════════

def section_signals(prices, trades):
    print(f"\n{'═'*70}")
    print("  SECCIÓN 5 · SEÑALES POTENCIALES")
    print(f"{'═'*70}")

    for product in sorted(prices["product"].unique()):
        sub = prices[prices["product"] == product].sort_values("global_ts").copy()
        if "mid_price" not in sub.columns:
            continue
        mid = sub["mid_price"].replace(0, np.nan)

        print(f"\n  [{product}]")

        # EMA rápida vs lenta
        sub["ema5"]  = mid.ewm(span=5,  adjust=False).mean()
        sub["ema20"] = mid.ewm(span=20, adjust=False).mean()
        sub["ema_cross"] = (sub["ema5"] > sub["ema20"]).astype(int).diff().abs()
        crosses = sub["ema_cross"].sum()
        print(f"    Cruces EMA(5/20)   : {int(crosses)}")

        # Spread como señal de liquidez
        bid_p = sorted([c for c in prices.columns if re.match(r"bid_price_\d", c)])
        ask_p = sorted([c for c in prices.columns if re.match(r"ask_price_\d", c)])
        if bid_p and ask_p:
            valid = sub[(sub[bid_p[0]] > 0) & (sub[ask_p[0]] > 0)]
            spread = valid[ask_p[0]] - valid[bid_p[0]]
            sub.loc[valid.index, "spread"] = spread
            # ¿El spread predice movimiento?
            sub["mid_ret_1"]  = mid.shift(-1) - mid
            corr_spread_ret = sub["spread"].corr(sub["mid_ret_1"])
            print(f"    Corr(spread, ret+1): {corr_spread_ret:+.4f}")

        # Imbalance L1: (bidvol - askvol) / (bidvol + askvol)
        if "bid_volume_1" in sub.columns and "ask_volume_1" in sub.columns:
            bv = sub["bid_volume_1"].replace(0, np.nan)
            av = sub["ask_volume_1"].replace(0, np.nan)
            imb = (bv - av) / (bv + av)
            sub["imbalance"] = imb
            sub["mid_ret_1"] = mid.shift(-1) - mid
            corr_imb = imb.corr(sub["mid_ret_1"])
            print(f"    Corr(imbalance, ret+1): {corr_imb:+.4f}")
            if abs(corr_imb) > 0.05:
                print(f"    → El imbalance tiene poder predictivo (|corr| > 0.05)")

        # ¿Cuántos ticks hay entre un trade y el siguiente movimiento de precio?
        if not trades.empty and product in trades["symbol"].values:
            t = trades[trades["symbol"] == product].sort_values("global_ts")
            merged = pd.merge_asof(
                t[["global_ts","price"]],
                sub[["global_ts","mid_price"]],
                on="global_ts", direction="forward"
            )
            if len(merged) > 0:
                price_impact = merged["mid_price"] - merged["price"]
                print(f"    Impacto post-trade en mid: mean={price_impact.mean():+.2f}  "
                      f"std={price_impact.std():.2f}")


# ════════════════════════════════════════════════════════
#  SECCIÓN 6 — GRÁFICOS
# ════════════════════════════════════════════════════════

def plot_all(prices, trades, outdir):
    print(f"\n{'═'*70}")
    print("  SECCIÓN 6 · GRÁFICOS")
    print(f"{'═'*70}")

    os.makedirs(outdir, exist_ok=True)
    products = sorted(prices["product"].unique())

    for product in products:
        sub = prices[prices["product"] == product].sort_values("global_ts").copy()
        mid = sub["mid_price"].replace(0, np.nan)
        bid_p = sorted([c for c in prices.columns if re.match(r"bid_price_\d", c)])
        ask_p = sorted([c for c in prices.columns if re.match(r"ask_price_\d", c)])

        fig = plt.figure(figsize=(14, 14))
        fig.suptitle(product, fontsize=13, fontweight="bold")
        gs = gridspec.GridSpec(4, 2, figure=fig, hspace=0.45, wspace=0.3)

        # 1. Mid price + EMA
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(sub["global_ts"], mid, linewidth=0.6, color="#4C72B0", alpha=0.7, label="mid")
        ema5  = mid.ewm(span=5,  adjust=False).mean()
        ema20 = mid.ewm(span=20, adjust=False).mean()
        ax1.plot(sub["global_ts"], ema5,  linewidth=1.2, color="#DD8452", label="EMA5")
        ax1.plot(sub["global_ts"], ema20, linewidth=1.2, color="#C44E52", label="EMA20")
        if not trades.empty and product in trades["symbol"].values:
            t = trades[trades["symbol"] == product]
            ax1.scatter(t["global_ts"], t["price"], s=8, color="black", alpha=0.5,
                        zorder=4, label="trades")
        _day_markers(ax1, sub)
        ax1.set_title("Mid price + EMA5/20 + trades", fontsize=10)
        ax1.legend(fontsize=8); ax1.grid(True, linewidth=0.3)
        ax1.yaxis.set_major_formatter(FuncFormatter(lambda x,_: f"{x:,.0f}"))

        # 2. Spread L1
        ax2 = fig.add_subplot(gs[1, 0])
        if bid_p and ask_p:
            valid = sub[(sub[bid_p[0]] > 0) & (sub[ask_p[0]] > 0)]
            spread = valid[ask_p[0]] - valid[bid_p[0]]
            ax2.plot(valid["global_ts"], spread, linewidth=0.5, color="#55A868")
            ax2.axhline(spread.mean(), color="red", linewidth=0.8, linestyle="--",
                        label=f"mean={spread.mean():.1f}")
            ax2.legend(fontsize=8)
        ax2.set_title("Spread L1 (ask - bid)", fontsize=10)
        ax2.grid(True, linewidth=0.3)

        # 3. Imbalance L1
        ax3 = fig.add_subplot(gs[1, 1])
        if "bid_volume_1" in sub.columns and "ask_volume_1" in sub.columns:
            bv = sub["bid_volume_1"].replace(0, np.nan)
            av = sub["ask_volume_1"].replace(0, np.nan)
            imb = (bv - av) / (bv + av)
            ax3.plot(sub["global_ts"], imb, linewidth=0.5, color="#8172B2", alpha=0.8)
            ax3.axhline(0, color="black", linewidth=0.5)
            ax3.set_ylim(-1.1, 1.1)
        ax3.set_title("Order imbalance L1  (bid-ask)/(bid+ask)", fontsize=10)
        ax3.grid(True, linewidth=0.3)

        # 4. Histograma de returns
        ax4 = fig.add_subplot(gs[2, 0])
        ret = mid.pct_change().dropna() * 1e4
        ax4.hist(ret, bins=60, color="#4C72B0", alpha=0.75, edgecolor="none")
        ax4.axvline(ret.mean(), color="red", linewidth=1, linestyle="--",
                    label=f"mean={ret.mean():.3f} bps")
        ax4.set_title("Distribución de returns (bps/tick)", fontsize=10)
        ax4.legend(fontsize=8); ax4.grid(True, linewidth=0.3)

        # 5. Autocorrelación de returns
        ax5 = fig.add_subplot(gs[2, 1])
        lags = range(1, 21)
        acs = [ret.autocorr(l) for l in lags]
        ax5.bar(list(lags), acs, color="#DD8452", alpha=0.8, width=0.7)
        ax5.axhline(0, color="black", linewidth=0.5)
        conf = 1.96 / np.sqrt(len(ret))
        ax5.axhline( conf, color="red", linewidth=0.7, linestyle="--", label="95% CI")
        ax5.axhline(-conf, color="red", linewidth=0.7, linestyle="--")
        ax5.set_title("Autocorrelación de returns (lags 1–20)", fontsize=10)
        ax5.legend(fontsize=8); ax5.grid(True, linewidth=0.3)

        # 6. Volumen medio por nivel (bid/ask)
        ax6 = fig.add_subplot(gs[3, 0])
        bid_v = sorted([c for c in prices.columns if re.match(r"bid_volume_\d", c)])
        ask_v = sorted([c for c in prices.columns if re.match(r"ask_volume_\d", c)])
        if bid_v and ask_v:
            lvls = [f"L{i+1}" for i in range(len(bid_v))]
            bvol = [sub[c].mean() for c in bid_v]
            avol = [sub[c].mean() for c in ask_v]
            x = np.arange(len(lvls))
            ax6.barh(lvls, [-v for v in bvol], color="#4C72B0", alpha=0.75, label="Bid")
            ax6.barh(lvls, avol, color="#DD8452", alpha=0.75, label="Ask")
            ax6.axvline(0, color="black", linewidth=0.6)
            ax6.legend(fontsize=8)
        ax6.set_title("Profundidad media del libro", fontsize=10)
        ax6.grid(True, linewidth=0.3)

        # 7. PnL
        ax7 = fig.add_subplot(gs[3, 1])
        if "profit_and_loss" in sub.columns:
            ax7.plot(sub["global_ts"], sub["profit_and_loss"],
                     color="#1D9E75", linewidth=0.8)
            ax7.axhline(0, color="black", linewidth=0.5, linestyle="--")
            _day_markers(ax7, sub)
        ax7.set_title("Profit & Loss", fontsize=10)
        ax7.grid(True, linewidth=0.3)

        safe = re.sub(r"[^\w]", "_", product)
        path = os.path.join(outdir, f"eda_{safe}.png")
        fig.savefig(path, dpi=130, bbox_inches="tight")
        plt.close(fig)
        print(f"  → eda_{safe}.png")


def _day_markers(ax, sub):
    if "day" not in sub.columns:
        return
    for day in sub["day"].unique():
        first_ts = sub[sub["day"] == day]["global_ts"].iloc[0]
        ax.axvline(first_ts, color="gray", linewidth=0.5, linestyle=":", alpha=0.6)


# ════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data",   default=DATA_DIR)
    parser.add_argument("--output", default=OUTPUT_DIR)
    args = parser.parse_args()

    print(f"\nCargando datos de {args.data!r} …")
    prices, trades = load_all(args.data)
    print(f"  prices: {len(prices):,} filas  |  trades: {len(trades):,} filas")

    section_structure(prices, trades)
    section_orderbook(prices)
    section_price_dynamics(prices)
    section_trades(trades, prices)
    section_signals(prices, trades)
    plot_all(prices, trades, args.output)

    print(f"\n{'═'*70}")
    print(f"  Resultados guardados en {args.output!r}")
    print(f"{'═'*70}\n")

if __name__ == "__main__":
    main()