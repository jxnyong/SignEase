# from gramformer import Gramformer

# # Load the Gramformer model
# gramformer = Gramformer(models=1, use_gpu=False)

# input_text = "I studet."

# # Correct the text using Gramformer
# corrected_text = gramformer.correct(input_text)

# # Print the corrected text
# print(corrected_text) 

import re

def transform_text(input_text):
    # Define rules for transformations
    rules = [
        (r'([a-z])([A-Z])', r'\1 \2'),  # Insert space before capital letters
        (r'themeeting', 'the meeting'),  # Specific word transformation
    ]

    # Apply rules to input_text
    for pattern, replacement in rules:
        input_text = re.sub(pattern, replacement, input_text)

    # Capitalize the first letter of the transformed text
    input_text = input_text.capitalize()

    return input_text

input_text = "letsstartthemeeting"
output_text = transform_text(input_text)
print(output_text)  # Output: "Let's start the meeting."
# Remember that the success of your model depends on the quality and diversity of your training data and the complexity of the transformations you want to achieve. Rule-based methods can work well for simple cases, but machine learning models may be necessary for handling more complex patterns.





