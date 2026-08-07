from functools import lru_cache
from math import inf

class Solution:
    def smallestNumber(self, num: str, t: int) -> str:
        # 1. Factorize t into prime factors 2, 3, 5, 7
        need = [0, 0, 0, 0]  # Counts of required factors: [2, 3, 5, 7]
        x = t
        for i, p in enumerate((2, 3, 5, 7)):
            while x % p == 0:
                need[i] += 1
                x //= p
        
        # If t has prime factors other than 2, 3, 5, 7, it's impossible.
        if x != 1:
            return "-1"

        # Contribution of each digit to the prime factors (2, 3, 5, 7)
        contrib = {
            1: (0, 0, 0, 0),
            2: (1, 0, 0, 0),
            3: (0, 1, 0, 0),
            4: (2, 0, 0, 0),
            5: (0, 0, 1, 0),
            6: (1, 1, 0, 0),
            7: (0, 0, 0, 1),
            8: (3, 0, 0, 0),
            9: (0, 2, 0, 0),
        }

        # 2. DP to find minimum slots to fulfill requirements for 2s and 3s
        @lru_cache(None)
        def min23(a, b):
            if a <= 0 and b <= 0:
                return 0
            best = inf
            for d in (2, 3, 4, 6, 8, 9):
                c2, c3, _, _ = contrib[d]
                na = max(0, a - c2)
                nb = max(0, b - c3)
                
                # Skip if this digit doesn't reduce our needs
                if na == a and nb == b:
                    continue
                
                best = min(best, 1 + min23(na, nb))
            return best

        # Helper to get the absolute minimum digits needed for a given state
        def min_slots(r2, r3, r5, r7):
            return r5 + r7 + min23(r2, r3)

        # 3. Greedy builder to create the smallest valid suffix
        def build(slots, r2, r3, r5, r7):
            ans = []
            for pos in range(slots):
                for d in range(1, 10):
                    c2, c3, c5, c7 = contrib[d]
                    nr2 = max(0, r2 - c2)
                    nr3 = max(0, r3 - c3)
                    nr5 = max(0, r5 - c5)
                    nr7 = max(0, r7 - c7)
                    
                    # If picking digit 'd' leaves enough slots for the remaining requirements
                    if min_slots(nr2, nr3, nr5, nr7) <= slots - pos - 1:
                        ans.append(str(d))
                        r2, r3, r5, r7 = nr2, nr3, nr5, nr7
                        break
            return "".join(ans)

        n = len(num)

        # 4. Attempt to find an answer of the exact same length as `num`
        def solve_length(L):
            if min_slots(*need) > L:
                return None
            
            # For lengths > len(num), we don't care about prefix matching
            if L > n:
                return build(L, *need)

            # Build prefix requirements step by step
            pref = [list(need)]
            for ch in num:
                if ch == "0":
                    break
                cur = pref[-1][:]
                c = contrib[int(ch)]
                for i in range(4):
                    cur[i] = max(0, cur[i] - c[i])
                pref.append(cur)

            # --- THE FIX ---
            # Check if the unmodified string itself is completely valid
            if len(pref) == n + 1 and pref[-1] == [0, 0, 0, 0]:
                return num

            # Try to increment a digit starting from the rightmost available spot
            max_i = min(n - 1, len(pref) - 1)
            for i in range(max_i, -1, -1):
                req = pref[i]
                start = int(num[i]) + 1
                
                for d in range(start, 10):
                    c = contrib[d]
                    nr = [
                        max(0, req[0] - c[0]),
                        max(0, req[1] - c[1]),
                        max(0, req[2] - c[2]),
                        max(0, req[3] - c[3]),
                    ]
                    rem = n - i - 1
                    
                    # Check if the remainder string can accommodate our remaining requirements
                    if min_slots(*nr) <= rem:
                        return num[:i] + str(d) + build(rem, *nr)
            
            return None

        # 5. Core Execution Logic
        # First, try to match the length exactly
        ans = solve_length(n)
        if ans is not None:
            return ans

        # If impossible at length `n`, we build an entirely new string of length `L > n`
        L = max(n + 1, min_slots(*need))
        return build(L, *need)