from typing import List

class Solution:
    def stoneGameII(self, piles: List[int]) -> int:
        n = len(piles)

        # suffix[i] = total stones from i to n-1
        suffix = [0] * (n + 1)

        for i in range(n - 1, -1, -1):
            suffix[i] = suffix[i + 1] + piles[i]

        # dp(i, M) = maximum stones current player can get
        # starting from index i with current M
        memo = {}

        def dp(i, M):
            if i >= n:
                return 0

            key = (i, M)
            if key in memo:
                return memo[key]

            # If we can take all remaining piles
            if i + 2 * M >= n:
                memo[key] = suffix[i]
                return suffix[i]

            best = 0

            # Take X piles, where 1 <= X <= 2*M
            for X in range(1, 2 * M + 1):
                # Stones left for Bob after Alice takes X
                opponent = dp(i + X, max(M, X))

                # Total remaining stones - Bob's maximum
                current = suffix[i] - opponent

                best = max(best, current)

            memo[key] = best
            return best

        return dp(0, 1)