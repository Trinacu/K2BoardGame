cards = {
    "move1": {
        "info":"Add 1 movement action",
	    "count": 5,
        "effect": {
            "move": 1
        }
	},
    "move2": {
        "info":"Add 2 movement action",
	    "count": 3,
        "effect": {
            "move": 2
        }
	},
    "move3": {
        "info":"Add 3 movement action",
	    "count": 2,
        "effect": {
            "move": 3
        }
	},
    "move12": {
        "info":"Add 1 movement up or 2 down action",
	    "count": 1,
        "effect": {
            "move": 1,
            "move_down": 2
        }
	},
    "move13": {
        "info":"Add 1 movement up or 3 down action",
	    "count": 1,
        "effect": {
            "move": 1,
            "move_down": 3
        }
	},
    "move23": {
        "info":"Add 2 movement up or 3 down action",
	    "count": 1,
        "effect": {
            "move": 2,
            "move_down": 3
        }
	},
    "accl0": {
        "info":"Add 0 acclimatization",
	    "count": 1,
        "effect": {
            "accl": 0
        }
	},
    "accl1": {
        "info":"Add 1 acclimatization",
	    "count": 2,
        "effect": {
            "accl": 1
        }
	},
    "accl2": {
        "info":"Add 2 acclimatization",
	    "count": 1,
        "effect": {
            "accl": 2
        }
	},
    "accl3": {
        "info":"Add 3 acclimatization",
	    "count": 1,
        "effect": {
            "accl": 3
        }
	},
#other (non playable cards)
    "backside":{
        "info":"Cards back side",
        "count": 0,
        "effect": {
            "none": 0
        }
    }
}

nodes = {
    "summer": {
        "node0": {
            "altitude": 4800,
            "move_cost": 1,
            "accl_cost": -1,
            "start_node": "True",
            "adjacent": ["node2"],
            "pos": (524, 840)
        },
        "node1": {
            "altitude": 4805,
            "move_cost": 1,
            "accl_cost": -1,
            "start_node": False,
            "adjacent": ["node1", "node2"],
            "pos": (422, 839)
        },
        "node2": {
            "altitude": 4784,
            "move_cost": 1,
            "accl_cost": -1,
            "adjacent": ["node3", "node6"],
            "pos": (319, 843)
            },
        "node3": {
            "altitude": 4978,
            "move_cost": 1,
            "accl_cost": -1,
            "adjacent": ["node2", "node4", "node7"],
            "pos": (239, 805)
        },
        "node4": {
            "altitude": 5065,
            "move_cost": 1,
            "accl_cost": -1,
            "adjacent": ["node3", "node5", "node8"],
            "pos": (153, 788)
        },
        "node5": {
            "altitude": 5070,
            "move_cost": 1,
            "accl_cost": -1,
            "adjacent": ["node4", "node9"],
            "pos": (66, 787)
        },
        "node6": {
            "altitude": 5152,
            "move_cost": 1,
            "accl_cost": -1,
            "adjacent": ["node1", "node2", "node7"],
            "pos": (367, 771)
        },
        "node7": {
            "altitude": 5381,
            "move_cost": 1,
            "accl_cost": -1,
            "adjacent": ["node6", "node8"],
            "pos": (293, 726)
        },
        "node8": {
            "altitude": 5432,
            "move_cost": 2,
            "accl_cost": -1,
            "adjacent": ["node4", "node7", "node11"],
            "pos": (204, 716)
        },
        "node9": {
            "altitude": 5498,
            "move_cost": 1,
            "adjacent": ["node5", "node12"],
            "pos": (67, 703)
        },
        "node10": {
            "altitude": 5901,
            "move_cost": 2,
            "adjacent": ["node11", "node13"],
            "pos": (273, 624)
        },
        "node11": {
            "altitude": 5850,
            "move_cost": 1,
            "adjacent": ["node8", "node10", "node14"],
            "pos": (186, 634)
        },
        "node12": {
            "altitude": 5917,
            "move_cost": 1,
            "adjacent": ["node9", "node14", "node15"],
            "pos": (86, 621)
        },
        "node13": {
            "altitude": 6366,
            "move_cost": 2,
            "adjacent": ["node10", "node14", "node16"],
            "VP": 2,
            "pos": (248, 533)
        },
        "node14": {
            "altitude": 6269,
            "move_cost": 2,
            "adjacent": ["node11", "node12", "node13", "node17"],
            "VP": 2,
            "pos": (160, 552)
        },
        "node15": {
            "altitude": 6401,
            "move_cost": 2,
            "adjacent": ["node12", "node17"],
            "VP": 2,
            "pos": (64, 526)
        },
        "node16": {
            "altitude": 6651,
            "move_cost": 1,
            "accl_cost": 1,
            "adjacent": ["node13", "node18", "node19"],
            "VP": 3,
            "pos": (312, 477)
        },
        "node17": {
            "altitude": 6687,
            "move_cost": 1,
            "adjacent": ["node14", "node15", "node20"],
            "VP": 3,
            "pos": (142, 470)
        },
        "node18": {
            "altitude": 6988,
            "move_cost": 2,
            "accl_cost": 1,
            "adjacent": ["node16", "node22"],
            "VP": 4,
            "pos": (361, 411)
        },
        "node19": {
            "altitude": 6963,
            "move_cost": 2,
            "accl_cost": 1,
            "adjacent": ["node16", "node21"],
            "VP": 4,
            "pos": (234, 416)
        },
        "node20": {
            "altitude": 6983,
            "move_cost": 3,
            "accl_cost": 1,
            "adjacent": ["node17", "node21"],
            "VP": 4,
            "pos": (75, 412)
        },
        "node21": {
            "altitude": 7299,
            "move_cost": 2,
            "accl_cost": 1,
            "adjacent": ["node19", "node20", "node23"],
            "VP": 5,
            "pos": (157, 350)
        },
        "node22": {
            "altitude": 7412,
            "move_cost": 2,
            "accl_cost": 1,
            "adjacent": ["node18", "node24"],
            "VP": 5,
            "pos": (382, 328)
        },
        "node23": {
            "altitude": 7539,
            "move_cost": 2,
            "accl_cost": 1,
            "adjacent": ["node21", "node25"],
            "VP": 5,
            "pos": (231, 303)
        },
        "node24": {
            "altitude": 7820,
            "move_cost": 3,
            "accl_cost": 2,
            "adjacent": ["node22", "node26"],
            "VP": 6,
            "pos": (372, 248)
        },
        "node25": {
            "altitude": 7886,
            "move_cost": 2,
            "accl_cost": 1,
            "adjacent": ["node23", "node26"],
            "VP": 6,
            "pos": (268, 235)
        },
        "node26": {
            "altitude": 8238,
            "move_cost": 3,
            "accl_cost": 2,
            "adjacent": ["node24", "node25", "node27"],
            "VP": 7,
            "pos": (327, 166)
        },
        "node27": {
            "altitude": 8611,
            "move_cost": 3,
            "accl_cost": 2,
            "adjacent": ["node26"],
            "VP": 10,
            "pos": (312, 93)
        }
    },
    "winter": {
        "node0": {
            "altitude": 4123,
            "move_cost": 1,
            "accl_cost": -1,
            "start_node": "True",
            "adjacent": ["node2"],
            "pos": (517, 840)
        }
    }
}
weather = {
    "summer": {
        "card1": {
            "day1": {
                "below_6k": {
                    "move": 0,
                    "accl": 0
                },
                "6k_to_7k": {
                    "move": 0,
                    "accl": 0
                },
                "7k_to_8k": {
                    "move": 0,
                    "accl": 0
                },
                "above_8k": {
                    "move": 0,
                    "accl": 0
                }
            },
            "day2": {
                "below_6k": {
                    "move": 0,
                    "accl": 0
                },
                "6k_to_7k": {
                    "move": 0,
                    "accl": 0
                },
                "7k_to_8k": {
                    "move": 0,
                    "accl": 0
                },
                "above_8k": {
                    "move": 0,
                    "accl": 0
                }
            },
            "day3": {
                "below_6k": {
                    "move": 0,
                    "accl": 0
                },
                "6k_to_7k": {
                    "move": 0,
                    "accl": 0
                },
                "7k_to_8k": {
                    "move": 0,
                    "accl": 0
                },
                "above_8k": {
                    "move": 0,
                    "accl": 0
                }
            }
        },
        "card2": {
            "day1": {
                "below_6k": {
                    "move": 0,
                    "accl": 0
                },
                "6k_to_7k": {
                    "move": 0,
                    "accl": 0
                },
                "7k_to_8k": {
                    "move": 0,
                    "accl": 0
                },
                "above_8k": {
                    "move": 0,
                    "accl": 0
                }
            },
            "day2": {
                "below_6k": {
                    "move": 0,
                    "accl": 0
                },
                "6k_to_7k": {
                    "move": 0,
                    "accl": 0
                },
                "7k_to_8k": {
                    "move": 0,
                    "accl": 1
                },
                "above_8k": {
                    "move": 0,
                    "accl": 0
                }
            },
            "day3": {
                "below_6k": {
                    "move": 0,
                    "accl": 0
                },
                "6k_to_7k": {
                    "move": 0,
                    "accl": 0
                },
                "7k_to_8k": {
                    "move": 0,
                    "accl": 2
                },
                "above_8k": {
                    "move": 0,
                    "accl": 0
                }
            }
        },
        "card3": {
            "day1": {
                "below_6k": {
                    "move": 0,
                    "accl": 0
                },
                "6k_to_7k": {
                    "move": 0,
                    "accl": 1
                },
                "7k_to_8k": {
                    "move": 0,
                    "accl": 0
                },
                "above_8k": {
                    "move": 0,
                    "accl": 0
                }
            },
            "day2": {
                "below_6k": {
                    "move": 0,
                    "accl": 0
                },
                "6k_to_7k": {
                    "move": 0,
                    "accl": 0
                },
                "7k_to_8k": {
                    "move": 0,
                    "accl": 0
                },
                "above_8k": {
                    "move": 0,
                    "accl": 0
                }
            },
            "day3": {
                "below_6k": {
                    "move": 0,
                    "accl": 0
                },
                "6k_to_7k": {
                    "move": 0,
                    "accl": 2
                },
                "7k_to_8k": {
                    "move": 0,
                    "accl": 0
                },
                "above_8k": {
                    "move": 0,
                    "accl": 0
                }
            }
        },
        "card4": {
            "day1": {
                "below_6k": {
                    "move": 0,
                    "accl": 0
                },
                "6k_to_7k": {
                    "move": 0,
                    "accl": 0
                },
                "7k_to_8k": {
                    "move": 0,
                    "accl": 0
                },
                "above_8k": {
                    "move": 0,
                    "accl": 0
                }
            },
            "day2": {
                "below_6k": {
                    "move": 0,
                    "accl": 0
                },
                "6k_to_7k": {
                    "move": 0,
                    "accl": 2
                },
                "7k_to_8k": {
                    "move": 0,
                    "accl": 2
                },
                "above_8k": {
                    "move": 0,
                    "accl": 2
                }
            },
            "day3": {
                "below_6k": {
                    "move": 0,
                    "accl": 0
                },
                "6k_to_7k": {
                    "move": 0,
                    "accl": 0
                },
                "7k_to_8k": {
                    "move": 0,
                    "accl": 0
                },
                "above_8k": {
                    "move": 0,
                    "accl": 0
                }
            }
        },
        "card5": {
            "day1": {
                "below_6k": {
                    "move": 0,
                    "accl": 0
                },
                "6k_to_7k": {
                    "move": 0,
                    "accl": 1
                },
                "7k_to_8k": {
                    "move": 0,
                    "accl": 1
                },
                "above_8k": {
                    "move": 0,
                    "accl": 1
                }
            },
            "day2": {
                "below_6k": {
                    "move": 0,
                    "accl": 0
                },
                "6k_to_7k": {
                    "move": 0,
                    "accl": 0
                },
                "7k_to_8k": {
                    "move": 0,
                    "accl": 1
                },
                "above_8k": {
                    "move": 0,
                    "accl": 1
                }
            },
            "day3": {
                "below_6k": {
                    "move": 0,
                    "accl": 0
                },
                "6k_to_7k": {
                    "move": 0,
                    "accl": 0
                },
                "7k_to_8k": {
                    "move": 0,
                    "accl": 0
                },
                "above_8k": {
                    "move": 0,
                    "accl": 1
                }
            }
        },
        "card6": {
            "day1": {
                "below_6k": {
                    "move": 0,
                    "accl": 0
                },
                "6k_to_7k": {
                    "move": 0,
                    "accl": 0
                },
                "7k_to_8k": {
                    "move": 0,
                    "accl": 0
                },
                "above_8k": {
                    "move": 0,
                    "accl": 2
                }
            },
            "day2": {
                "below_6k": {
                    "move": 0,
                    "accl": 0
                },
                "6k_to_7k": {
                    "move": 0,
                    "accl": 0
                },
                "7k_to_8k": {
                    "move": 0,
                    "accl": 2
                },
                "above_8k": {
                    "move": 0,
                    "accl": 2
                }
            },
            "day3": {
                "below_6k": {
                    "move": 0,
                    "accl": 0
                },
                "6k_to_7k": {
                    "move": 0,
                    "accl": 0
                },
                "7k_to_8k": {
                    "move": 0,
                    "accl": 0
                },
                "above_8k": {
                    "move": 0,
                    "accl": 0
                }
            }
        }
    }
}
