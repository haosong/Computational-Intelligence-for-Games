#include <iostream>
#include <sstream>
#include <cstring>
#include <algorithm>
#include <vector>
#include <unordered_set>

// Mex Operation
int mex(std::unordered_set<int> &nimbers) {
    int mex = 0;
    while (nimbers.find(mex) != nimbers.end()) mex++;
    return mex;
}

// Check if one is P-Position
bool isPPos(std::vector<int> &pos, std::vector<int> &grundy) {
    int nimber = 0;
    for (int i : pos) nimber ^= grundy[i];
    return nimber == 0;
}

// Analyze position from string to vector of int
std::vector<int> readPosition(std::string &pos) {
    unsigned long lo = 0, hi = 0;
    std::vector<int> res;
    if (pos.length() == 0) pos == "xx";
    while (hi < pos.length()) {
        if (pos.at(hi) != '.' && pos.at(hi) != 'x') throw -1;
        if (pos.at(hi) == '.') {
            if (hi > lo) res.push_back((int) (hi - lo));
            while (hi < pos.length() && pos.at(hi) == '.') hi++;
            lo = hi;
        }
        hi++;
    }
    if (pos.at(pos.length() - 1) == 'x') res.push_back((int) (pos.length() - lo));
    return res;
}

// Get n-th Grundy Number
int getGrundyNumber(int n, std::vector<int> &grundy) {
    if (grundy[n] != -1) return grundy[n];
    if (n <= 2) {
        grundy[n] = n % 2;
        return n % 2;
    }
    std::unordered_set<int> reachable;
    for (int i = 0; i <= n - 2; i++)
        reachable.insert(getGrundyNumber(i, grundy) ^ getGrundyNumber(n - 2 - i, grundy));
    grundy[n] = mex(reachable);
    return grundy[n];
}

// Get [0, n] Grundy Number
std::vector<int> generateGrundyNumberList(int n) {
    std::vector<int> grundy(n + 1, -1);
    for (int i = n; i >= 0; i--) getGrundyNumber(i, grundy);
    return grundy;
}

// Make a move to win
void makeMove(std::string &pos, std::vector<int> &grundy) {
    int minGroups = (int) readPosition(pos).size() + 2;
    std::string ans;
    for (unsigned long i = 0; i < pos.length(); i++) {
        if (pos.at(i) == '.') continue;
        auto *next = new char[pos.length()];
        strcpy(next, pos.c_str());
        if (i < pos.length() - 1 && pos.at(i + 1) == 'x') {
            next[i] = '.';
            next[i + 1] = '.';
        } else if ((i == 0 || pos.at(i - 1) == '.') && (i == pos.length() - 1 || pos.at(i + 1) == '.'))
            next[i] = '.';
        std::string next_str(next);
        delete[] next;
        std::vector<int> newPos = readPosition(next_str);
        if ((int) newPos.size() < minGroups && isPPos(newPos, grundy)) {
            minGroups = (int) newPos.size();
            ans = next_str;
        }
    }
    if (ans.length() > 0) std::cout << ans << std::endl;
}

// Main Function
int main(int argc, char **argv) {
    try {
        if (argc == 3 && strcmp(argv[1], "grundy") == 0) {
            std::istringstream iss(argv[2]);
            int n;
            iss >> n;
            if (!iss || n < 0) throw -1;
            std::vector<int> grundy = generateGrundyNumberList(n);
            std::cout << "[";
            for (int i = 0; i <= n; i++)
                std::cout << grundy[i] << (i != n ? ", " : "]\n");
        } else if (argc == 2) {
            std::string position(argv[1]);
            std::vector<int> pins = readPosition(position);
            std::vector<int> grundy = generateGrundyNumberList(position.length());
            if (isPPos(pins, grundy)) std::cout << "LOSS" << std::endl;
            else makeMove(position, grundy);
        }
    } catch (...) {
        std::cout << "Illegal Argument" << std::endl;
        return -1;
    }
    return 0;
}
