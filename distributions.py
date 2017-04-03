def get_ba_distribution(m):
    distribution = []

    for i in range(m):
        distribution.append(0.0)

    distribution.append(1.0)

    return distribution


def get_uniform_distribution(g):
    distribution = []
    M = 3 * g - 1

    distribution.append(0.0)

    for i in range(M):
        distribution.append(1.0 / M)

    return distribution


def get_triangular_distribution(g):
    distribution = []

    Q = (g + 1)**2

    distribution.append(0.0)

    for i in range(g + 1):
        distribution.append(float(i + 1) / Q)

    return distribution + distribution[::-1][1:-1]
