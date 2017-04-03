from distributions import get_triangular_distribution
from process import Process

if __name__ == "__main__":
    distr = get_triangular_distribution(2)

    process = Process(2, distr, 10000, 'triangular_distr.csv')
    process.process_evolve()