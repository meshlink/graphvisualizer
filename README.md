Mehslink Graph Visualization Tool
=================================

Visualize graphs generated by meshlink.

# Usage

```python visualize_network_graph.py input_file output_file [position_file]```

Input file must be in expected JSON format (see below).

Output file name extension determines file type.

Position file is optional. Used to cache node locations between runs of the
tool, so that nodes don't jump around.

## Batches

To run a batch of JSON files, you might do this:

```ls *.json | sed s/\.[^\.]*$// | xargs -n 1 -P 1 -I{} python visualize_network_graph.py {}.json {}.png positions```

# Input Data
Input data must be in JSON format. The expected structure is, by example, as
follows:


```
{
	"nodes": {
		"machine1node0": {
			"name": "machine1node0",
			"options": 50331652,
			"devclass": 0
		},
		"machine1node1": {
			"name": "machine1node1",
			"options": 0,
			"devclass": 1
		},
		"machine1node2": {
			"name": "machine1node2",
			"options": 50331652,
			"devclass": 2
		},
		"machine1node3": {
			"name": "machine1node3",
			"options": 50331652,
			"devclass": 0
		},
		"machine1node4": {
			"name": "machine1node4",
			"options": 0,
			"devclass": 1
		},
		"machine1node5": {
			"name": "machine1node5",
			"options": 0,
			"devclass": 2
		},
		"machine1node6": {
			"name": "machine1node6",
			"options": 0,
			"devclass": 0
		},
		"machine1node7": {
			"name": "machine1node7",
			"options": 0,
			"devclass": 1
		},
		"machine1node8": {
			"name": "machine1node8",
			"options": 0,
			"devclass": 2
		},
		"machine1node9": {
			"name": "machine1node9",
			"options": 0,
			"devclass": 0
		}
	},
	"edges": {
		"machine1node0_to_machine1node2": {
			"from": "machine1node0",
			"to": "machine1node2",
			"address": { "host": "127.0.0.1", "port": 10345 },
			"options": 50331652,
			"weight": 6
		},
		"machine1node0_to_machine1node3": {
			"from": "machine1node0",
			"to": "machine1node3",
			"address": { "host": "127.0.0.1", "port": 22643 },
			"options": 50331652,
			"weight": 1
		},
		"machine1node2_to_machine1node0": {
			"from": "machine1node2",
			"to": "machine1node0",
			"address": { "host": "127.0.0.1", "port": 21863 },
			"options": 50331652,
			"weight": 1
		},
		"machine1node3_to_machine1node0": {
			"from": "machine1node3",
			"to": "machine1node0",
			"address": { "host": "127.0.0.1", "port": 21863 },
			"options": 50331652,
			"weight": 1
		}
	}
}
```


