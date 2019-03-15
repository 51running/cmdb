#encoding:utf-8

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-H","--host",type=str,default="127.0.0.1",help="Server Addr")
    parser.add_argument("-P","--port",type=int,default=8888,help="Server port")
    parser.add_argument("-V","--verbose",action="store_true",help="DEBUG INFO")

    args = parser.parse_args()
    print(args.host)
    print(args.port)
    print(args.verbose)

