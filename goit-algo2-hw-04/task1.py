from collections import defaultdict, deque


def bfs(graph, source, sink, parent):
    visited = {source}
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if v not in visited and graph[u][v] > 0:
                visited.add(v)
                parent[v] = u
                if v == sink:
                    return True
                queue.append(v)
    return False


def edmonds_karp(graph, source, sink):
    max_flow = 0
    while True:
        parent = {}
        if not bfs(graph, source, sink, parent):
            break
        path_flow = float("inf")
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, graph[u][v])
            v = u
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = u
        max_flow += path_flow
    return max_flow


EDGES = [
    ("T1", "W1", 25), ("T1", "W2", 20), ("T1", "W3", 15),
    ("T2", "W3", 15), ("T2", "W4", 30), ("T2", "W2", 10),
    ("W1", "S1", 15), ("W1", "S2", 10), ("W1", "S3", 20),
    ("W2", "S4", 15), ("W2", "S5", 10), ("W2", "S6", 25),
    ("W3", "S7", 20), ("W3", "S8", 15), ("W3", "S9", 10),
    ("W4", "S10", 20), ("W4", "S11", 10), ("W4", "S12", 15),
    ("W4", "S13", 5), ("W4", "S14", 10),
]

WAREHOUSE_SHOPS = {
    "W1": ["S1", "S2", "S3"],
    "W2": ["S4", "S5", "S6"],
    "W3": ["S7", "S8", "S9"],
    "W4": ["S10", "S11", "S12", "S13", "S14"],
}


def build_graph():
    g = defaultdict(lambda: defaultdict(int))
    for u, v, cap in EDGES:
        g[u][v] += cap
        g[v][u] += 0  # initialize reverse edge
    INF = 10 ** 9
    g["SRC"]["T1"] = INF;  g["T1"]["SRC"] = 0
    g["SRC"]["T2"] = INF;  g["T2"]["SRC"] = 0
    for i in range(1, 15):
        g[f"S{i}"]["SNK"] = INF; g["SNK"][f"S{i}"] = 0
    return g


def main():
    orig = {(u, v): cap for u, v, cap in EDGES}
    g = build_graph()
    total_flow = edmonds_karp(g, "SRC", "SNK")

    def flow(u, v):
        return orig.get((u, v), 0) - g[u][v]

    # Terminal → warehouse actual flows
    t1_in = {w: flow("T1", w) for w in ["W1", "W2", "W3"]}
    t2_in = {w: flow("T2", w) for w in ["W2", "W3", "W4"]}

    # Proportionally attribute shared-warehouse shop flows to each terminal
    def split(warehouse, shop_flow):
        a = t1_in.get(warehouse, 0)
        b = t2_in.get(warehouse, 0)
        total = a + b
        if total == 0:
            return 0.0, 0.0
        return shop_flow * a / total, shop_flow * b / total

    t1_shops = {s: flow("W1", s) for s in WAREHOUSE_SHOPS["W1"]}
    t2_shops = {s: flow("W4", s) for s in WAREHOUSE_SHOPS["W4"]}

    for w in ["W2", "W3"]:
        for s in WAREHOUSE_SHOPS[w]:
            t1_share, t2_share = split(w, flow(w, s))
            t1_shops[s] = t1_share
            t2_shops[s] = t2_share

    # ── Report ──────────────────────────────────────────────────────────────
    print("=" * 50)
    print("  Logistics Network Maximum Flow Report")
    print("=" * 50)
    print(f"\nAlgorithm : Edmonds-Karp (BFS-based Ford-Fulkerson)")
    print(f"Total maximum flow: {total_flow} units\n")

    print("Warehouse-level flows:")
    for w, shops in WAREHOUSE_SHOPS.items():
        in_t1 = t1_in.get(w, 0)
        in_t2 = t2_in.get(w, 0)
        outs = {s: flow(w, s) for s in shops}
        print(f"  {w}: total_in={in_t1 + in_t2}  (T1={in_t1}, T2={in_t2})  shop_flows={outs}")

    print()
    print(f"{'Terminal':<13} {'Shop':<10} {'Flow (units)'}")
    print("-" * 38)
    for s_num in range(1, 10):
        s = f"S{s_num}"
        print(f"{'Terminal 1':<13} {'Shop ' + str(s_num):<10} {t1_shops.get(s, 0):.1f}")
    print()
    for s_num in range(4, 15):
        s = f"S{s_num}"
        print(f"{'Terminal 2':<13} {'Shop ' + str(s_num):<10} {t2_shops.get(s, 0):.1f}")

    t1_total = sum(t1_shops.values())
    t2_total = sum(t2_shops.values())
    print(f"\nTerminal 1 total: {t1_total:.1f} units")
    print(f"Terminal 2 total: {t2_total:.1f} units")

    # Actual flow per shop (for analysis)
    shop_flow = {}
    for w, shops in WAREHOUSE_SHOPS.items():
        for s in shops:
            shop_flow[s] = flow(w, s)

    print("\n" + "=" * 50)
    print("  Analysis")
    print("=" * 50)

    print("\n1. Which terminal provides the most flow?")
    winner = "Terminal 1" if t1_total >= t2_total else "Terminal 2"
    print(f"   {winner} leads: T1={t1_total:.1f} units, T2={t2_total:.1f} units.")
    print("   T1 connects to W1 (exclusive) plus shared W2 and W3.")
    print("   T2 connects to W4 (exclusive) plus shared W2 and W3.")

    print("\n2. Routes with the lowest capacity and their impact:")
    low = sorted(EDGES, key=lambda e: e[2])[:5]
    for u, v, cap in low:
        print(f"   {u}→{v}: capacity={cap}, actual flow={flow(u, v)}")
    print("   W4→S13 (5 units) is the tightest edge and hard-caps Shop 13 supply.")

    print("\n3. Shops with least goods and how to improve them:")
    zeros = [s for s, f in sorted(shop_flow.items(), key=lambda x: int(x[0][1:])) if f == 0]
    if zeros:
        print(f"   Shops receiving 0 units: {zeros}")
        print("   Shop 3 (S3): W1→S3 has capacity 20 but W1 is already fully used by S1+S2.")
        print("   Increasing T1→W1 from 25 to 45 would let S3 receive goods too.")
        print("   Shops 12–14 (S12–S14): W4→these edges have remaining capacity,")
        print("   but T2→W4 is saturated at 30. Increasing T2→W4 beyond 30 would help.")
    else:
        print("   All shops receive some goods.")

    print("\n4. Bottlenecks (saturated edges):")
    saturated = [(u, v, cap) for u, v, cap in EDGES if flow(u, v) == cap]
    for u, v, cap in saturated:
        print(f"   {u}→{v} saturated at {cap} units")
    print("   All terminal→warehouse edges are fully saturated.")
    print("   These are the primary bottlenecks: any increase in their capacity")
    print("   would directly translate into higher total flow through the network.")


if __name__ == "__main__":
    main()
