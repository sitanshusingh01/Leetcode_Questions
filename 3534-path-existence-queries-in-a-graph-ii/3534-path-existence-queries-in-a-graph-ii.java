import java.util.*;

class Solution {
    public int[] pathExistenceQueries(int n, int[] nums, int maxDiff, int[][] queries) {
        // Sort indices by value
        Integer[] order = new Integer[n];
        for (int i = 0; i < n; i++) order[i] = i;
        Arrays.sort(order, (a, b) -> nums[a] - nums[b]);

        int[] sortedVal = new int[n];
        int[] pos = new int[n]; // pos[originalIndex] -> position in sorted order
        for (int p = 0; p < n; p++) {
            sortedVal[p] = nums[order[p]];
            pos[order[p]] = p;
        }

        // Two-pointer: farthest reachable sorted-position within maxDiff
        int[] right = new int[n];
        int j = 0;
        for (int p = 0; p < n; p++) {
            if (j < p) j = p;
            while (j + 1 < n && sortedVal[j + 1] - sortedVal[p] <= maxDiff) j++;
            right[p] = j;
        }

        // Binary lifting on "farthest reachable in 2^k hops"
        int LOG = 1;
        while ((1 << LOG) < n) LOG++;
        LOG++;

        int[][] up = new int[LOG][n];
        up[0] = right;
        for (int k = 1; k < LOG; k++)
            for (int p = 0; p < n; p++)
                up[k][p] = up[k - 1][up[k - 1][p]];

        int[] ans = new int[queries.length];
        for (int q = 0; q < queries.length; q++) {
            int a = pos[queries[q][0]];
            int b = pos[queries[q][1]];
            if (a == b) { ans[q] = 0; continue; }

            int lo = Math.min(a, b), hi = Math.max(a, b);
            int cur = lo, hops = 0;

            for (int k = LOG - 1; k >= 0; k--) {
                if (up[k][cur] < hi) {
                    cur = up[k][cur];
                    hops += (1 << k);
                }
            }

            ans[q] = (right[cur] >= hi) ? hops + 1 : -1;
        }
        return ans;
    }
}