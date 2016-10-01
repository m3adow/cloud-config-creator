# cloud-config-creator
A small Python script to ease the creation of extensive cloud config files for clusters.

---

A basic CoreOS cluster configuration has about 95% identical configuration in a cloud config file.
Still, you need to change every configuration change in every file. That's why I wrote this script.
Enabled by [Jinja2](http://jinja.pocoo.org/docs/dev/templates/) templating you'll only need one master
template and one values file.

**Basic usage:**

```bash
./cloud-config-creator master-example.tmpl values-example.yml
```

This will create files named like the hostname for each cluster node in the values file located in the current working
directory.

You can use `--outpath` to alter the output directory for created files.

Furthermore you can add includes to every node, see the master-example.tmpl to see how. If you want, you can stash your includes
in a different path, this path can be added via `--includepath`.

For more information see [my blog post](https://adminswerk.de/easy-cluster-cloud-config-creation/) about cloud-config-creator.
