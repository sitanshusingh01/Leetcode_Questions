class Solution {
    static final long LIMIT = 1_000_000L;
    long[][] C = new long[5001][27];

    public String smallestPalindrome(String s, int k) {
        int[] cnt = new int[26];
        for (char c : s.toCharArray()) cnt[c - 'a']++;

        int[] half = new int[26];
        int len = 0;
        char mid = 0;

        for (int i = 0; i < 26; i++) {
            half[i] = cnt[i] / 2;
            len += half[i];
            if ((cnt[i] & 1) == 1) mid = (char) ('a' + i);
        }

        buildComb(len);

        if (count(half, len) < k) return "";

        StringBuilder left = new StringBuilder();

        while (len > 0) {
            for (int i = 0; i < 26; i++) {
                if (half[i] == 0) continue;

                half[i]--;
                long ways = count(half, len - 1);

                if (ways >= k) {
                    left.append((char) ('a' + i));
                    len--;
                    break;
                } else {
                    k -= ways;
                    half[i]++;
                }
            }
        }

        StringBuilder ans = new StringBuilder(left);
        if (mid != 0) ans.append(mid);
        ans.append(new StringBuilder(left).reverse());

        return ans.toString();
    }

    private void buildComb(int n) {
        for (int i = 0; i <= n; i++) {
            C[i][0] = 1;
            for (int j = 1; j <= Math.min(i, 26); j++) {
                if (j == i)
                    C[i][j] = 1;
                else
                    C[i][j] = Math.min(LIMIT, C[i - 1][j - 1] + C[i - 1][j]);
            }
        }
    }

    private long count(int[] half, int total) {
        long res = 1;
        int remain = total;

        for (int x : half) {
            if (x == 0) continue;
            res = Math.min(LIMIT, res * comb(remain, x));
            remain -= x;
            if (res >= LIMIT) return LIMIT;
        }

        return res;
    }

    private long comb(int n, int r) {
        if (r == 0 || r == n) return 1;
        r = Math.min(r, n - r);

        long ans = 1;
        for (int i = 1; i <= r; i++) {
            ans = ans * (n - r + i) / i;
            if (ans >= LIMIT) return LIMIT;
        }
        return ans;
    }
}