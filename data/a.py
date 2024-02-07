import data

nodes = data.nodes['summer']

print(nodes)
#8611 ... nodes['node27'].pos[1]
#5400 ... nodes['node0'].pos[1]

max_pix_dif = nodes['node0']['pos'][1] - nodes['node27']['pos'][1]
print(max_pix_dif)

for nodename, node in nodes.items():
    pix_dif = node['pos'][1] - nodes['node27']['pos'][1]
    alt_dif = pix_dif / max_pix_dif * (nodes['node27']['altitude'] - nodes['node0']['altitude'])
    alt = nodes['node27']['altitude'] - alt_dif
    print(f"{nodename}: {alt}")
