from typing import List

class Solution:
    def longestRepeating(
        self,
        s: str,
        queryCharacters: str,
        queryIndices: List[int]
    ) -> List[int]:

        n = len(s)

        # Each node:
        # [first_char, last_char, prefix, suffix, best, length]
        tree = [[0] * 6 for _ in range(4 * n)]

        def merge(node):
            L = tree[node * 2]
            R = tree[node * 2 + 1]

            first_char = L[0]
            last_char = R[1]
            length = L[5] + R[5]

            # Prefix
            prefix = L[2]

            if L[2] == L[5] and L[1] == R[0]:
                prefix = L[5] + R[2]

            # Suffix
            suffix = R[3]

            if R[3] == R[5] and L[1] == R[0]:
                suffix = R[5] + L[3]

            # Best answer inside either half
            best = max(L[4], R[4])

            # Best answer crossing the middle
            if L[1] == R[0]:
                best = max(best, L[3] + R[2])

            tree[node] = [
                first_char,
                last_char,
                prefix,
                suffix,
                best,
                length
            ]

        def build(node, left, right):
            if left == right:
                c = ord(s[left]) - ord('a')
                tree[node] = [c, c, 1, 1, 1, 1]
                return

            mid = (left + right) // 2

            build(node * 2, left, mid)
            build(node * 2 + 1, mid + 1, right)

            merge(node)

        def update(node, left, right, idx, c):
            if left == right:
                tree[node] = [c, c, 1, 1, 1, 1]
                return

            mid = (left + right) // 2

            if idx <= mid:
                update(node * 2, left, mid, idx, c)
            else:
                update(node * 2 + 1, mid + 1, right, idx, c)

            merge(node)

        build(1, 0, n - 1)

        ans = []

        for c, idx in zip(queryCharacters, queryIndices):
            update(
                1,
                0,
                n - 1,
                idx,
                ord(c) - ord('a')
            )

            ans.append(tree[1][4])

        return ans