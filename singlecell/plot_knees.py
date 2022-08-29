#!/usr/bin/env python3
# Roger Volden

'''
Usage:
    python3 plot_knees.py \
            -s bcstats.tsv \
            -o plots/skera
'''

import argparse
import matplotlib.pyplot as plt

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--tsv', '-t', type=str, required=True,
        help='Output tsv file from bcstats (can be gzipped)'
    )
    parser.add_argument(
        '--output', '-o', type=str, required=True, help='Output png prefix'
    )
    parser.add_argument(
        '--max_cells', '-m', default=-1, type=int,
        help='Force an x axis maximum instead of the mpl default'
    )
    return parser.parse_args()

def read_tsv(tsv, max_cells):
    zipped, first = False, True
    if tsv.endswith('.gz'):
        import gzip
        fh = gzip.open(tsv, 'rb')
        zipped = True
    else:
        fh = open(tsv, 'r')

    counts, last_real = [], -1
    for line in fh:
        if first:
            first = False
            continue
        if zipped:
            line = line.decode()
        _, nreads, rank, numis, real, _ = line.rstrip().split('\t')
        nreads, rank, numis = int(nreads), int(rank), int(numis)
        if rank >= max_cells and max_cells > 0:
            break
        if real == 'cell':
            last_real = rank
        counts.append(numis)

    fh.close()
    counts.sort(reverse=True)
    return counts, last_real

def plot_from_tsv(counts, ncells, args):
    max_cells, output = args.max_cells, args.output

    plt.figure(figsize=(5, 3.5))
    c = plt.axes([0.125, 0.125, 0.8, 0.8])

    pink = (223/255, 25/255, 149/255)

    c.plot(range(len(counts)), counts, lw=1, color='grey', zorder=10)
    c.plot(range(ncells), counts[:ncells], lw=1.5, color=pink, zorder=11)

    c.set_xlabel(r'Cell # (log$_{10}$)')
    c.set_xscale('log')
    c.set_yscale('log')
    c.set_ylabel(r'log$_{10}$(# of UMIs)')
    c.set_title('UMIs per cell')

    output += '.knee.png'
    plt.savefig(output, dpi=600)

def main(args):
    counts, ncells = read_tsv(args.tsv, args.max_cells)
    plot_from_tsv(counts, ncells, args)

if __name__ == '__main__':
    args = parse_args()
    main(args)
