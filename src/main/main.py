from Baguette import Baguette

import argparse

parser = argparse.ArgumentParser(description='Do you want a hot baguette ?')
parser.add_argument('--path', type=str, help='The PDF path')
parser.add_argument('-k', type=int, default=25, help='Number of tokens')
parser.add_argument("--tf-idf", default=False, action="store_true", help="Use the TF-IDF algorithm")
args = parser.parse_args()

b = Baguette()

if args.tf_idf == False:
    occurences = b.process(args.path, k=args.k)
else:
    occurences = b.tfIdfFromDir(args.path, k=args.k)

print(occurences)