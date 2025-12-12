As of now, the structure of the data is as follows, I think it is scalable as the development of the game progresses. 

## 🧍 Characters

Stores core **gameplay-relevant information** for NPCs:

- Stats (health, damage, difficulty, etc.)
- Flags (hostile/friendly, quest state)
- Inventory and droppable items
- Progression or interaction rules

Dialogue is intentionally **not stored here** — instead, each character references a matching JSON file inside `/Dialogues/`.


## 💬 Dialogues

Contains full dialogue scripts for each NPC in **separate JSON files**.

Each file generally includes:

- Dialogue organized by states/triggers
- Optional responses or branching choices
- One root object per character

Example format:

{
  "intro": [
    "Oh, you must be a Hunter...",
    "This town is cursed..."
  ],
  "quest_active": [
    "Have you found the cure?"
  ]
}

Keeping dialogue separate allowed easier writing, editing, and localization in the future.


## 🎒 Items

Defines all interactable objects:

- Consumables (e.g., Blood Vials)
- Weapons and upgrades
- Quest/key items
- Special artifacts

Each item JSON includes:

- Item description
- Gameplay effects or stat changes
- Initial location or way to obtain it




## 🌍 Locations

Defines the layout and structure of the game world:

- Name + detailed room description
- Connected/exits to other areas
- Items that spawn in this location
- NPCs present initially
- Special triggers (e.g., lamps, boss gates)

Example fields:

{
  "name": "Central Yharnam",
  "description": "A dark and grim district filled with hostile townsfolk.",
  "exits": ["Great Bridge", "Sewer Entrance"],
  "items": ["Pebble"],
  "npcs": ["Gilbert"]
}
