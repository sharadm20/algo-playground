public class WildcardMatching {
    public boolean isMatch(String s, String p) {
        int sIdx = 0;
        int pIdx = 0;
        int match = -1;
        int starIdx = -1;

        int n = s.length();
        int m = p.length();

        while (sIdx < n) {
            if (pIdx < m && (p.charAt(pIdx) == '?' || s.charAt(sIdx) == p.charAt(pIdx))) {
                sIdx++;
                pIdx++;
            }
            else if (pIdx < m && p.charAt(pIdx) == '*') {
                starIdx = pIdx;
                match = sIdx;
                pIdx++;
            }
            else if (starIdx != -1) {
                pIdx = starIdx + 1;
                sIdx = ++match;
            }
            else {
                return false;
            }
        }

        while (pIdx < m && p.charAt(pIdx) == '*') {
            pIdx++;
        }
        return pIdx == m;
    }
}