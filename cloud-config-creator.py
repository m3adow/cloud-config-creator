#!/usr/bin/env python3
import os
import yaml
import jinja2


from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-t", "--templatefile", help="Path to template file", metavar="TEMPLATEFILE", required=True)
    parser.add_argument("-f", "--valuesfile", help="Path to values files", metavar="VALUEFILE", required=True)
    parser.add_argument("-o", "--outpath", help="Directory for created files (default: ./)", metavar="OUTPATH",
                        required=False)
    parser.add_argument("-i", "--includepath", help="Directory for includes", metavar="INCLUDEPATH")

    return parser.parse_args()


def parse_valuesfile(f):
    f_content = yaml.load(f)
    global_values = f_content.get('global', {})
    print(global_values)
    nodes = f_content.get('nodes', {})

    for node in nodes:
        if 'override' in global_values:
            node.update(global_values['override'])

    return nodes


def main():
    args = parse_args()

    if args.outpath:
        outpath = args.outpath
    else:
        outpath = os.getcwd()

    with open(args.valuesfile, 'r') as f:
        nodes = parse_valuesfile(f)

    if args.includepath:
        templateLoader = jinja2.FileSystemLoader(searchpath=[os.getcwd(), os.path.dirname(args.templatefile),
                                                             args.includepath], followlinks=True)
    else:
        templateLoader = jinja2.FileSystemLoader(searchpath=[os.getcwd(), os.path.dirname(args.templatefile)],
                                                 followlinks=True)
    templateEnv = jinja2.Environment(loader=templateLoader)
    print(nodes)
    for node in nodes:
        remaining_nodes = list(nodes)
        remaining_nodes.remove(node)

        template = templateEnv.get_template(args.templatefile)

        with open(outpath + "/" + node['hostname'] + '.yml', "w") as f:
            f.write(template.render({
                "my": node,
                "remaining_nodes": remaining_nodes,
                "nodes": nodes
                }))


if __name__ == "__main__":
    # execute only if run as a script
    main()
