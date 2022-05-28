import argparse 
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--conky')
    parser.add_argument('-f')
    parser.add_argument('-t')
    parser.add_argument('--cb', default=False, action='store_true')
    parser.add_argument('--notify', default=False, action='store_true')
    parser.add_argument('--telegram', default=False, action='store_true')
    parser.add_argument('--trade')
    parser.add_argument('--size')
    parser.add_argument('--visible', default=False, action='store_true')
    parser.add_argument('--autotrade', default=False, action='store_true')
    parser.add_argument('--allow_new', default=False, action='store_true')
    args = parser.parse_args()
    if args.trade:
        from trade import Trade
        trade = Trade(profile=args.trade, visible=args.visible, check=int(args.t))
