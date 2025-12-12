# Bloodborne Text Adventure
By Anupreet Singh, Khushika Shah & Michael Marti


This project is a text adventure inspired by *Bloodborne*. We built a custom JSON dataset to describe the world (locations, characters, items, dialogues) and a parser that lets you play entirely through typed commands in a Colab notebook.

## World Data (JSON layout)
- `Data/Locations/*.json` — `id`, `name`, `description`, `previous`/`next` links, optional `key_item_for_travel`, `characters` (`id`, `count`), `items` (`id`, `count`).
- `Data/Characters/*.json` — `id`, `name`, `alias`, `description`, `health`, `damage`, `friendly`/`vulnerable`, optional `stun_item_id`, `drop_items` (`id`, `quantity`).
- `Data/Items/*.json` — `id`, `name`, `description`, `category`, `gettable` flag, and item-specific stats (e.g., `healing`, `damage`, `gate_unlocked`).
- `Data/Dialogues/*.json` — dialogue trees keyed by character.

The parser loads these JSON files into memory and uses them to drive room descriptions, combat, travel, inventory, and dialogue.

## Contributors
- Anupreet Singh — designed and implemented the JSON-based world database; developed core parts of the action set and game-state update logic; and collaborated on debugging and integration.

- Khushika Shah — implemented LLM-based input-to-action mapping using few-shot prompting with Mistral-7B; built major portions of the action set and state-update logic; and collaborated on debugging and integration.

- Michael Marti — contributed to overall design direction and project documentation.

## Actions
This is a list of the possible actions you can take in the game

- ATTACK — Fight a hostile character using a weapon in your inventory. Example Prompt: `attack father gascoigne with the hunter Axe` or `attack silver beast using the whirligigsaw`
- TALK — Start a conversation with someone present in the room(They only respond if they are friendly at the moment). Prompt: `talk to the plain doll`, or `talk to gilbert`.
- USE — Consume or activate an item in your inventory. Prompt: `use a blood vial` replenishes health `use lamp` opens up a list of fast travel locations available.  
- Upgrade weapon — Improve a weapon at the proper station. Prompt: `upgrade_weapon hunter axe`.
- TRAVEL — Move to an adjacent location via its exits. Prompt: `travel to plaza` or `Go to the entry balcony`
- TELEPORT — Warp to a location with a lit lamp. Prompt: `use lamp` enables this as well whenever you are in a room that has the lamp.
- GET — Pick up all copies of an item from the room. Prompt: `get blood vial` picks up all the blood vials in the room.
- INSPECT — Examine an item or character in the room or inventory. Prompt: `inspect lamp`.
- HEAL — Restore health using one blood vial. Prompt: `heal` or `heal using a blood vial` or `use blood vial`
- INCREASE HEALTH — Increase the players maximum health when in the hunter lawn by consuming blood echoes. Prompt: `Increase Health`.
- INVENTORY STATS — Lists out what you are carrying. Prompt: `Inventory` or `check Inventory`
- PLAYER STATS — Shows your core stats (health, insight, echoes, etc.). Prompt: `player stats`
- DESRIBE ROOM — Reprint the current room description, items, characters, exits. Prompt: `describe this room`.

## How to play:
1) Open `parser.ipynb` in Colab(by uploading it to your google drive).  
2) Run all the cells in the notebook sequentially, The notebook pulls all the Game data from the repository automatically.
3) You just need to scroll down to the last cell to see a CLI open up. 
4) Use custom input in CLI to execute the above mentioned actions.

## TIPS
- You are supposed to play by typing in custom commands in the the CLI
- Each area of the game has a boss that is invulnerable unless you a stun item found in that area to make him vulnerable to damage, so do explore. The stun items are specific to bosses and maybe dropped by either an enemy, a friendly NPC or just found in the environment. 
- Beat gehrman to win the game. Spoiler Alert- It take a while
- Enjoy the Hunt
