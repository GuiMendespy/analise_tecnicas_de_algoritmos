"""Bonus: compara a versao original e a de inicializacao sob demanda. Uso: PYTHONPATH=<repo> python bonus.py <rotulo>"""
import gc, time, csv, random, sys, statistics as st, tracemalloc
import networkx as nx

SEED, REPS = 42, 5

def medir(f, reps=REPS):
    f(); ts = []
    for _ in range(reps):
        gc.collect(); gc.disable()
        t0 = time.perf_counter(); f(); ts.append(time.perf_counter() - t0); gc.enable()
    return ts

def componentes(n, c, grau=6, pesos=False):
    """n vertices em n/c componentes de tamanho c, cada uma G(c, p) com grau medio ~min(grau, c-1)."""
    partes = [nx.gnp_random_graph(c, min(1.0, grau / (c - 1)), seed=SEED + i) for i in range(n // c)]
    G = nx.disjoint_union_all(partes)
    if pesos:
        rng = random.Random(SEED)
        for u, v in G.edges: G[u][v]["weight"] = rng.randint(1, 9)
    return G

def cenarios():
    for c in [10, 50, 250, 1000]:                       # n=1000 fixo, varia o tamanho das componentes
        yield f"n1000_comp{c}", componentes(1000, c), {}
    yield "conexo_n500_g10", nx.gnp_random_graph(500, 10 / 499, seed=SEED), {}
    G = nx.gnp_random_graph(2000, 10 / 1999, seed=SEED)
    for k in [10, 50]:
        yield f"conexo_n2000_k{k}", G, dict(k=k, seed=SEED)
    yield "peso_n1000_comp10", componentes(1000, 10, pesos=True), dict(weight="weight")
    yield "peso_conexo_n500", componentes(500, 500, pesos=True), dict(weight="weight")

if __name__ == "__main__":
    rot = sys.argv[1]; linhas = []
    print(rot, nx.__file__, flush=True)
    for nome, G, kw in cenarios():
        ts = medir(lambda: nx.betweenness_centrality(G, **kw))
        tracemalloc.start(); nx.betweenness_centrality(G, **{**kw, "k": 1, "seed": SEED}); pico = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        ref = nx.betweenness_centrality(G, **kw)
        linhas.append(dict(versao=rot, cenario=nome, n=G.number_of_nodes(), m=G.number_of_edges(),
                           componentes=nx.number_connected_components(G), mediana=st.median(ts), desvio=st.stdev(ts),
                           minimo=min(ts), maximo=max(ts), pico_kib_1origem=pico / 1024,
                           checksum=round(sum(ref.values()), 9)))
        print(linhas[-1], flush=True)
    with open(f"dados/bonus_{rot}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0])); w.writeheader(); w.writerows(linhas)
