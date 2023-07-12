from sdp import *
from time import time
import argparse


def get_data(args):
    if args.cluster or args.polygon:
        centers = [parse_point(f'Center #{i}: ', args.dimension)
                   for i in range(args.num_clusters)]
        if args.cluster:
            data = gen_clusters(args.num_clusters, args.pts_per_cluster,
                                args.dimension, args.radius, centers)
        else:
            # TODO: add support for multiple polygons with different centers
            data = gen_polygon(args.num_points, args.radius, centers[0][0], centers[0][1])
    else:
        data = np.array([parse_point(f'Data point #{i + 1}: ', args.dimension)
                         for i in range(args.num_points)])
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cluster', action='store_true')
    parser.add_argument('-p', '--polygon', action='store_true')
    parser.add_argument('-nc', '--num_clusters', type=int, default=1)
    parser.add_argument('-ppc', '--pts_per_cluster', type=int, default=10)
    parser.add_argument('-d', '--dimension', type=int, default=2)
    parser.add_argument('-r', '--radius', type=float, default=1.0)
    parser.add_argument('-np', '--num_points', type=int, default=3)
    parser.add_argument('-k', type=int, default=2)
    parser.add_argument('-ng', '--no_gurobi', action='store_true')

    args = parser.parse_args()
    data = get_data(args)
    k = args.k
    print('Input data:\n', np.around(data, 3))

    start_t = time()
    m, cost = sdp_k_means(data, k)
    sdp_t = time()
    if not args.no_gurobi:
        opt = optimal_k_means(data, k)
        opt_t = time()
        print('Optimal objective function value:', round(opt, 3))
        print(f'Gurobi running time: {opt_t - sdp_t} seconds')
    print('SDP objective function value:', round(cost, 3))
    print('SDP solver returned matrix:\n', np.around(m, 3))
    print('Trace:\n', np.round(np.trace(m), 3))
    print(f'SDP running time: {sdp_t - start_t} seconds')
