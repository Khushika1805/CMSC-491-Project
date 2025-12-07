import json
import os

class DialogueManager:
    def __init__(self, dialogue_json_path):
        # Store the filename (without extension) as the character name
        self.character_name = os.path.splitext(os.path.basename(dialogue_json_path))[0]
        
        # Load the dialogues
        with open(dialogue_json_path, "r") as f:
            self.dialogues = json.load(f)

        # Tracks progression through the dialogue list
        self.current_index = 0

    def get_dialogue(self, insight):
        """
        Return the correct dialogue line based on player insight 
        and the current progression state.
        """

        # If next dialogue exists AND insight is enough → unlock progression
        if self.current_index + 1 < len(self.dialogues):
            next_dialogue = self.dialogues[self.current_index + 1]
            if insight >= next_dialogue["min_insight"]:
                self.current_index += 1

        # Include character name for display or logging
        return {
            "character": self.character_name,
            "dialogue": self.dialogues[self.current_index]["text"]
        }


# Calling the function 
"""
dm = DialogueManager("gilbert.json")

print(dm.get_dialogue(0))
# -> {'character': 'gilbert', 'dialogue': 'Welcome traveler…'}

print(dm.get_dialogue(0))
# -> Next sequential line

"""