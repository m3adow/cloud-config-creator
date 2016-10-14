#!/usr/bin/env python3
import os
import yaml
import jinja2


from argparse import ArgumentParser
from pprint import pprint


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-t", "--templatefile", help="Path to template file", metavar="TEMPLATEFILE", required=True)
    parser.add_argument("-f", "--valuesfile", help="Path to values files", metavar="VALUEFILE", required=True)
    parser.add_argument("-o", "--outpath", help="Directory for created files (default: ./)", metavar="OUTPATH",
                        required=False)
    parser.add_argument("-i", "--includepath", help="Directory for includes", metavar="INCLUDEPATH")

    return parser.parse_args()


def main():
    args = parse_args()

    if args.outpath:
        outpath = args.outpath
    else:
        outpath = os.getcwd()

    with open(args.valuesfile) as f:
        nodes = yaml.load(f)

    # pprint(nodes)
    if args.includepath:
        templateLoader = jinja2.FileSystemLoader(searchpath=[os.getcwd(), args.includepath], followlinks=True)
    else:
        templateLoader = jinja2.FileSystemLoader(searchpath=os.getcwd(), followlinks=True)
    templateEnv = jinja2.Environment(loader=templateLoader)

    for node in nodes:
        remaining_nodes = list(nodes)
        remaining_nodes.remove(node)

        template = templateEnv.get_template(args.templatefile)

        '''
        print(template.render({
            "my": node,
            "remaining_nodes": remaining_nodes
        }))
        '''
        with open(outpath + "/" + node['hostname'] + '.yml', "w") as f:
            f.write(template.render({
                "my": node,
                "remaining_nodes": remaining_nodes,
                "nodes": nodes
                }))


if __name__ == "__main__":
    # execute only if run as a script
    main()
