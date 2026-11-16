"""Experimentos A-D do relatorio (NetworkX, commit e59d718). Uso: PYTHONPATH=<repo> python benchmark.py"""
import gc, time, csv, random, statistics as st, sys
from collections import deque
import numpy as np
import networkx as nx

SEED, REPS = 42, 5
OUT = "dados/"

def medir(f, reps=REPS):
    f()                                   # aquecimento
    ts = []
    for _ in range(reps):
        gc.collect(); gc.disable()
        t0 = time.perf_counter(); f(); ts.append(time.perf_counter() - t0)
        gc.enable()
    return ts

def resumo(ts):
    return dict(mediana=st.median(ts), desvio=st.stdev(ts), minimo=min(ts), maximo=max(ts))

def grafo(n, grau, exigir_conexo=True):
    G = nx.gnp_random_graph(n, grau / (n - 1), seed=SEED)
    if exigir_conexo: assert nx.is_connected(G), (n, grau)
    return G

def escrever(nome, linhas):
    with open(OUT + nome, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0])); w.writeheader(); w.writerows(linhas)

def exp_A():
    L = []
    for n in [125, 250, 500, 1000, 2000]:
        G = grafo(n, 10); V, E = G.number_of_nodes(), G.number_of_edges()
        r = resumo(medir(lambda: nx.betweenness_centrality(G)))
        L.append(dict(n=n, m=E, **r, ns_por_VE=r["mediana"] / (V * E) * 1e9)); print("A", L[-1], flush=True)
    x, y = np.log([l["n"] for l in L]), np.log([l["mediana"] for l in L])
    print("A inclinacao log-log:", np.polyfit(x, y, 1)[0])
    escrever("A_tempo_n.csv", L)

def exp_B():
    L = []; n = 500
    for g in [5, 10, 20, 40, 80]:
        G = grafo(n, g, False); E = G.number_of_edges(); comp = nx.number_connected_components(G)
        r = resumo(medir(lambda: nx.betweenness_centrality(G)))
        L.append(dict(grau=g, m=E, componentes=comp, **r)); print("B", L[-1], flush=True)
    E_ = np.array([l["m"] for l in L]); T = np.array([l["mediana"] for l in L])
    a, b = np.polyfit(E_, T, 1); r2 = np.corrcoef(E_, T)[0, 1] ** 2
    print("B R2:", r2, "intercepto", b)
    escrever("B_tempo_densidade.csv", L)

def exp_C():
    n = 1000; G = grafo(n, 10)
    exato = nx.betweenness_centrality(G); L = []
    t_exato = None
    for k in [25, 50, 100, 250, 500, 1000]:
        ts = medir(lambda: nx.betweenness_centrality(G, k=k, seed=SEED))
        ap = nx.betweenness_centrality(G, k=k, seed=SEED)
        err = np.array([abs(ap[v] - exato[v]) for v in G])
        r = resumo(ts)
        if k == 1000: t_exato = r["mediana"]
        L.append(dict(k=k, **r, erro_medio=err.mean(), erro_max=err.max())); print("C", L[-1], flush=True)
    for l in L: l["aceleracao"] = t_exato / l["mediana"]
    escrever("C_aproximacao.csv", L)

# ---- Experimento D: copia instrumentada das funcoes -----------------------------
def contar(G):
    c = dict(desenfileirados=0, arestas=0, upd_sigma=0, upd_delta=0)
    bc = dict.fromkeys(G, 0.0)
    for s in G:
        S = []; P = {v: [] for v in G}; sigma = dict.fromkeys(G, 0.0); D = {}
        sigma[s] = 1.0; D[s] = 0; Q = deque([s])
        while Q:
            v = Q.popleft(); c["desenfileirados"] += 1; S.append(v)
            for w in G[v]:
                c["arestas"] += 1
                if w not in D: Q.append(w); D[w] = D[v] + 1
                if D[w] == D[v] + 1: sigma[w] += sigma[v]; P[w].append(v); c["upd_sigma"] += 1
        delta = dict.fromkeys(S, 0)
        while S:
            w = S.pop(); coeff = (1 + delta[w]) / sigma[w]
            for v in P[w]: delta[v] += sigma[v] * coeff; c["upd_delta"] += 1
            if w != s: bc[w] += delta[w]
    scale = 1 / ((len(G) - 1) * (len(G) - 2))   # normalized=True, nao direcionado: 2/((n-1)(n-2)) * 1/2
    return {v: b * scale for v, b in bc.items()}, c

def exp_D():
    L = []
    for n in [125, 250, 500, 1000]:
        G = grafo(n, 10); V, E = G.number_of_nodes(), G.number_of_edges()
        bc, c = contar(G); ref = nx.betweenness_centrality(G)
        assert all(abs(bc[v] - ref[v]) < 1e-9 for v in G), "copia instrumentada difere do NetworkX"
        L.append(dict(n=n, m=E, **c, dois_V_E=2 * V * E, razao=c["arestas"] / (2 * V * E))); print("D", L[-1], flush=True)
    escrever("D_contadores.csv", L)

if __name__ == "__main__":
    print(nx.__file__, nx.__version__, flush=True)
    for e in sys.argv[1:] or "DBCA": globals()["exp_" + e]()
