#include <iostream>
#include <sstream>
#include <iomanip>

#define LIMIT 99

double ***prob;
int **move;
double **roll;

void get_all_roll_prob(int goal, int x, int y) {
    for (int target = 2; target <= std::max(2, goal - std::min(x, y)); target++) {
        auto **prob = new double *[goal + 1];
        for (int i = 0; i <= goal; i++)
            prob[i] = new double[7];
        auto *prob_target = new double[target + 1];
        prob_target[0] = 1.0;
        for (int i = 2; i <= target; i++)
            prob_target[i] = 0.0;
        for (int i = 2; i <= target; i++) {
            for (int j = 2; j <= 6; j++)
                if (i - j >= 0)
                    prob_target[i] += prob_target[i - j] / 6.0;
            prob[i][0] = prob_target[i];
            prob[i][6] = 1.0 - prob[i][0];
            for (int j = 1; j < 6; j++) {
                int r = std::min(6, i + j);
                while (r >= 2 && i > i + j - r && i + j - r >= 0) {
                    prob[i][j] += prob_target[i + j - r] / 6.0;
                    r--;
                }
                prob[i][6] -= prob[i][j];
            }
        }
        roll[target] = prob[target];
    }
}

void win_prob_non_recursive(int goal, int x, int y) {
    for (int n = 1; n < LIMIT; n++) {
        for (int i = goal - 1; i >= x; i--) {
            for (int j = goal - 1; j >= y; j--) {
                double opt_prob = 2.0 * (n % 2 == 0 ? -1 : 1);
                int opt_move = 0;
                if (n % 2 == 0) {
                    for (int s = 2; s <= std::max(2, goal - i); s++) {
                        double one_prob = prob[n - 1][i][j] * roll[s][6];
                        for (int k = s; k < s + 6; k++)
                            one_prob += (i + k >= goal ? 1.0 : prob[n - 1][i + k][j]) * roll[s][k - s];
                        opt_prob = std::max(one_prob, opt_prob);
                        opt_move = one_prob == opt_prob ? s : opt_move;
                    }
                } else {
                    for (int s = 2; s <= std::max(2, goal - j); s++) {
                        double p = prob[n - 1][i][j] * roll[s][6];
                        for (int k = s; k < s + 6; k++)
                            p += (j + k >= goal ? 0.0 : prob[n - 1][i][j + k]) * roll[s][k - s];
                        opt_prob = std::min(p, opt_prob);
                        opt_move = p == opt_prob ? s : opt_move;
                    }
                }
                prob[n][i][j] = opt_prob;
                move[i][j] = opt_move;
            }
        }
    }
}

int main(int argc, char **argv) {
    try {
        if (argc == 4) {
            int x, y, goal;
            std::string str = std::string(argv[1]) + " " + std::string(argv[2]) + " " + std::string(argv[3]);
            std::istringstream iss(str);
            iss >> goal >> x >> y;
            if (!iss || goal < 0 || x < 0 || y < 0) throw -1;
            prob = new double **[LIMIT];
            for (int i = 0; i < LIMIT; i++) {
                prob[i] = new double *[goal];
                for (int j = 0; j < goal; j++) {
                    prob[i][j] = new double[goal];
                    for (int k = 0; k < goal; k++)
                        prob[i][j][k] = 0.5;
                }
            }
            move = new int *[goal];
            for (int i = 0; i < goal; i++)
                move[i] = new int[goal];
            roll = new double *[std::max(2, goal - std::min(x, y)) + 1];
            get_all_roll_prob(goal, x, y);
            win_prob_non_recursive(goal, x, y);
            std::cout << std::setprecision(6) << prob[LIMIT - 1][x][y] << " " << move[x][y] << std::endl;
        }
    } catch (...) {
        return -1;
    }
    return 0;
}

