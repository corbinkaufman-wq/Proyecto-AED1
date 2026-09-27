#include <iostream>
#include <vector>

using namespace std;

class Fenwick {
public:
    int n;
    vector<int> bit;

    explicit Fenwick(int size) : n(size), bit(size >= 0 ? size + 1 : 0, 0) {
        if (size < 0) throw "Tamano invalido";
    }

    static int lowbit(int i) {
        return i & -i;
    }

    void add(int i, int delta, bool trace = false) {
        if (i < 1 || i > n) throw "Indice de actualizacion invalido";
        bool first = true;
        for (; i <= n; i += lowbit(i)) {
            int before = bit[i];
            bit[i] += delta;
            if (trace) {
                cout << (first ? "" : ",")
                     << "{\"i\":" << i
                     << ",\"before\":" << before
                     << ",\"after\":" << bit[i]
                     << ",\"next\":" << i + lowbit(i) << "}";
                first = false;
            }
        }
    }

    int prefix(int i, bool trace = false) const {
        if (i < 0 || i > n) throw "Indice de consulta invalido";
        int sum = 0;
        bool first = true;
        for (; i > 0; i -= lowbit(i)) {
            sum += bit[i];
            if (trace) {
                cout << (first ? "" : ",")
                     << "{\"i\":" << i
                     << ",\"value\":" << bit[i]
                     << ",\"sum\":" << sum
                     << ",\"next\":" << i - lowbit(i) << "}";
                first = false;
            }
        }
        return sum;
    }

    int range(int l, int r) const {
        if (l < 1 || l > r || r > n) throw "Rango invalido";
        return prefix(r) - prefix(l - 1);
    }
};

bool test() {
    Fenwick empty(0);
    if (empty.prefix(0) != 0) return false;
    for (int n = 1; n <= 64; n++) {
        Fenwick f(n);
        vector<int> a(n + 1, 0);
        for (int k = 0; k < 100; k++) {
            int i = (k * 17) % n + 1;
            int delta = k % 13 - 6;
            a[i] += delta;
            f.add(i, delta);
            int sum = 0;
            for (int j = 1; j <= n; j++) {
                sum += a[j];
                if (f.prefix(j) != sum) return false;
            }
            for (int l = 1; l <= n; l++) {
                int expected = 0;
                for (int r = l; r <= n; r++) {
                    expected += a[r];
                    if (f.range(l, r) != expected) return false;
                }
            }
        }
    }
    return true;
}

int main() {
    try {
        if (!test()) {
            cerr << "Error en las pruebas de Fenwick\n";
            return 1;
        }

        vector<int> a = {0, 3, 2, 5, 1, 4, 7, 2, 6};
        Fenwick f(8);
        for (int i = 1; i <= 8; i++) f.add(i, a[i]);

        cout << "{\"values\":[";
        for (int i = 1; i <= 8; i++) {
            cout << (i == 1 ? "" : ",") << a[i];
        }
        cout << "],\"nodes\":[";
        for (int i = 1; i <= 8; i++) {
            cout << (i == 1 ? "" : ",")
                 << "{\"i\":" << i
                 << ",\"lowbit\":" << Fenwick::lowbit(i)
                 << ",\"start\":" << i - Fenwick::lowbit(i) + 1
                 << ",\"value\":" << f.bit[i]
                 << ",\"parent\":" << i + Fenwick::lowbit(i) << "}";
        }
        cout << "],\"query\":[";
        int q = f.prefix(7, true);
        cout << "],\"query_result\":" << q << ",\"left_query\":[";
        int left = f.prefix(2, true);
        cout << "],\"range_result\":" << q - left << ",\"update\":[";
        f.add(3, 4, true);
        cout << "],\"updated_query\":[";
        int updated = f.prefix(7, true);
        Fenwick single(1);
        single.add(1, 9);
        cout << "],\"updated_result\":" << updated
             << ",\"zero\":" << f.prefix(0)
             << ",\"single\":" << single.prefix(1) << "}\n";
    } catch (const char* message) {
        cerr << message << '\n';
        return 1;
    }
    return 0;
}
