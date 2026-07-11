class Solution {
    public int countCompleteComponents(int n, int[][] edges) {
        List<Integer>[] graph = new ArrayList[n];
        for (int i = 0; i < n; i++) {
            graph[i] = new ArrayList<>();
        }

        for (int[] edge : edges) {
            graph[edge[0]].add(edge[1]);
            graph[edge[1]].add(edge[0]);
        }

        boolean[] visited = new boolean[n];
        int ans = 0;

        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                int[] info = new int[2]; // info[0] = nodes, info[1] = degree sum
                dfs(i, graph, visited, info);

                int nodes = info[0];
                int edgeCount = info[1] / 2;

                if (edgeCount == nodes * (nodes - 1) / 2) {
                    ans++;
                }
            }
        }

        return ans;
    }

    private void dfs(int node, List<Integer>[] graph, boolean[] visited, int[] info) {
        visited[node] = true;
        info[0]++;
        info[1] += graph[node].size();

        for (int nei : graph[node]) {
            if (!visited[nei]) {
                dfs(nei, graph, visited, info);
            }
        }
    }
}