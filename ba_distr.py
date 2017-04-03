from distributions import get_ba_distribution
from process import Process

if __name__ == "__main__":
    distr = get_ba_distribution(2)

    process = Process(2, distr, 10000, 'ba_distr.csv')
    process.process_evolve()