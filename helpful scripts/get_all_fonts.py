import os
import pickle

# Replace with your font directory path
font_dir = 'C:\\Windows\\Fonts'

# List all .ttf and .otf fonts
available_fonts = [f for f in os.listdir(font_dir) if f.endswith(('.ttf', '.otf'))]

print(available_fonts)

# Save the list to a pickle file
save_path = 'E:\Cloudilic assessment\helpful scripts/available_fonts.pkl'
with open(save_path, 'wb') as f:
    pickle.dump(available_fonts, f)
