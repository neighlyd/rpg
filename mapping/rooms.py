"""
ROOM_OPTIONS_FORMAT = {
    "<ZONE_NAME>: [
            {"name": "ROOM_NAME", "description": "ROOM_DESCRIPTION"},
            {"name": "ROOM_NAME", "description": "ROOM_DESCRIPTION"},
        ]
    }
"""

# ROOM_OPTIONS = {
#     "Generic": [
#         {"name": "Dungeon", "description": "A dank dungeon filled with all sorts of nasty implements."},
#         {"name": "Kitchen", "description": "A kitchen where foul and unspeakable cuisines are prepared."},
#         {"name": "Library",
#          "description": "A fiendish library stuffed with decaying books filled with the most eldritch secrets."},
#         {"name": "Hallway", "description": "A hallway. Even dungeon residents need to get around somehow."},
#         {"name": "Armory", "description": "An armory full of rusted and half-broken implements of war."},
#         {"name": "Barracks", "description": "This room of cots and storage chests reeks of mildew and mold."},
#         {"name": "Storeroom", "description": ("This storeroom contains several barrels and boxes filled with rotted "
#                                               "meats.")},
#         {"name": "Laboratory",
#          "description": "Bubbling cauldrons and alembics line the tables of this nefarious workshop."},
#         {"name": "Shrine", "description": "There's blood everywhere. So much blood!"},
#     ],
#     "Lava": [
#         {"name": "Lava Tube", "description": ("A naturally formed corridor stretches out before you caused by a flow of"
#                                               " molten rock that once moved beneath the hardened surface of a lava "
#                                               "flow. The lava is long gone, but the extreme heat of this place is"
#                                               " nevertheless unnerving.")},
#         {"name": "Steam Vent", "description": ("You hear this chamber before you see it. A low hissing fills"
#                                                " the cavern, increasing in volume as you approach. Inside it’s"
#                                                " almost deafening. Steam pours out of cracks in the walls and"
#                                                " floor around which bioluminescent blue lichen has grown.")},
#         {"name": "Thermal Pool", "description": "This chamber is filled with large steaming pools of water."},
#         {"name": "Geode Cathedral", "description": ("An absolutely dazzling array of shimmering geodes line this room,"
#                                                     " covering it from floor to ceiling in a sparkling purple hue.")},
#         {"name": "Chamber of Ash", "description": ("You come upon a vast chamber that stretches upward far beyond your"
#                                                    " feeble torch. The air inside is so still it makes you want to"
#                                                    " scream just to break the pressure on your ears, but when you open"
#                                                    " your mouth the sound dies in your throat. As you step inside your"
#                                                    " feet sink into what feels like snow.")},
#         {"name": "Magma Chamber", "description": "This room glows bright orange with the light of living rock. Rivers"
#                                                  " of molten lava course dangerously through the space. It's best to"
#                                                  " watch your step."},
#         {"name": "Sulfurous Wastes", "description": "This expanse of yellowed and soiled ground is permeated with the"
#                                                     " most obscene stench you have encountered. Deviled eggs? More like"
#                                                     " devil eggs!"},
#         {"name": "Boiling Mud Pits", "description": "Vats of stinking, roiling mud dot the floor of this chamber,"
#                                                     " occasionally lobbing scorching globules at unwary travellers."},
#         {"name": "Lava Tube", "description": ("A naturally formed corridor stretches out before you caused by a flow of"
#                                               " molten rock that once moved beneath the hardened surface of a lava "
#                                               "flow. The lava is long gone, but the extreme heat of this place is"
#                                               " nevertheless unnerving.")},
#     ]
# }

ZONE_OPTIONS = [
    "Dungeon",
    "Lava",
]

ROOM_OPTIONS = [
    {"name": "Dungeon", 
     "zone_types": ["Generic", ],  
     "description": "A dank dungeon filled with all sorts of nasty implements.",
     },
    {"name": "Kitchen", 
     "zone_types": ["Dungeon", ],
     "description": "A kitchen where foul and unspeakable cuisines are prepared.",
     },
    {"name": "Library",
     "zone_types": ["Dungeon", ],
     "description": "A fiendish library stuffed with decaying books filled with the most eldritch secrets.",
     },
    {"name": "Hallway", 
     "zone_types": ["Generic", ],
     "description": "A hallway. Even dungeon residents need to get around somehow.",
     },
    {"name": "Armory", 
     "zone_types": ["Dungeon", ],
     "description": "An armory full of rusted and half-broken implements of war.",
     },
    {"name": "Barracks", 
     "zone_types": ["Dungeon", ],  
     "description": "This room of cots and storage chests reeks of mildew and mold.",
     },
    {"name": "Storeroom", 
     "zone_types": ["Generic", ],
     "description": "This storeroom contains several barrels and boxes filled with rotted meats.",
     },
    {"name": "Laboratory",
     "zone_types": ["Dungeon", ],  
     "description": "Bubbling cauldrons and alembics line the tables of this nefarious workshop.",
     },
    {"name": "Shrine", 
     "zone_types": ["Dungeon", ],
     "description": "There's blood everywhere. So much blood!",
     },
    {"name": "Lava Tube", 
     "zone_types": ["Lava", ],
     "description": ("A naturally formed corridor stretches out before you caused by a flow of molten rock that once "
                     "moved beneath the hardened surface of a lava flow. The lava is long gone, but the extreme heat of"
                     " this place is nevertheless unnerving."),
     },
    {"name": "Steam Vent", 
     "zone_types": ["Lava", ],
     "description": ("You hear this chamber before you see it. A low hissing fills the cavern, increasing in volume as"
                     " you approach. Inside it’s almost deafening. Steam pours out of cracks in the walls and floor"
                     " around which bioluminescent blue lichen has grown."),
     },
    {"name": "Thermal Pool", 
     "zone_types": ["Lava", ],
     "description": "This chamber is filled with large steaming pools of water.",
     },
    {"name": "Geode Cathedral", 
     "zone_types": ["Lava", ],
     "description": ("An absolutely dazzling array of shimmering geodes line this room, covering it from floor to"
                     " ceiling in a sparkling purple hue."),
     },
    {"name": "Chamber of Ash", 
     "zone_types": ["Lava", ],
     "description": ("You come upon a vast chamber that stretches upward far beyond your feeble torch. The air inside"
                     " is so still it makes you want to scream just to break the pressure on your ears, but when you"
                     " open your mouth the sound dies in your throat. As you step inside your feet sink into what feels"
                     " like snow."),
     },
    {"name": "Magma Chamber", 
     "zone_types": ["Lava", ],
     "description": "This room glows bright orange with the light of living rock. Rivers of molten lava course"
                    " dangerously through the space. It's best to"
                    " watch your step.",
     },
    {"name": "Sulfurous Wastes", 
     "zone_types": ["Lava", ],
     "description": ("This expanse of yellowed and soiled ground is permeated with the most obscene stench you have"
                     " encountered. Deviled eggs? More like devil eggs!"),
     },
    {"name": "Boiling Mud Pits", 
     "zone_types": ["Lava", ],
     "description": ("Vats of stinking, roiling mud dot the floor of this chamber, occasionally lobbing scorching"
                     " globules at unwary travellers."),
     },
    {"name": "Lava Tube", 
     "zone_types": ["Lava", ],
     "description": ("A naturally formed corridor stretches out before you caused by a flow of molten rock that once"
                     " moved beneath the hardened surface of a lava flow. The lava is long gone, but the extreme heat"
                     " of this place is nevertheless unnerving."),
     },
    ]
