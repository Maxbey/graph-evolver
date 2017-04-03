from distributions import get_uniform_distribution
from process import Process

if __name__ == "__main__":
    distr = get_uniform_distribution(2)

    process = Process(2, distr, 10000, 'uniform_distr.csv')
    process.process_evolve()