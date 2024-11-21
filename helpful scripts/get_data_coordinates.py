import matplotlib.pyplot as plt
import json


img = plt.imread("E:\Cloudilic assessment\Invoice arabic.jpeg")

# List to store coordinates data
coordinates_data = []

# Define the event handler
def onclick(event):
    if event.inaxes is not None:  # Check if the click is inside the image axes
        x, y = int(event.xdata), int(event.ydata)
        coordinates_data.append((x, y))
        print(f"Coordinates: ({x}, {y})")


# Define the event handler for key presses
def onkey(event):
    if event.key == 'n':
        if coordinates_data:  # Check if the list is not empty
            removed = coordinates_data.pop()  # Remove the last element
            print(f"Removed last coordinates: {removed}")
            print(f"Number of selected coordinates: {len(coordinates_data)}")
        else:
            print("No coordinates to remove.")


# Connect the event to the handler
fig, ax = plt.subplots()
ax.imshow(img)
cid = fig.canvas.mpl_connect('button_press_event', onclick)
cid_key = fig.canvas.mpl_connect('key_press_event', onkey)


plt.show()


print(coordinates_data)

# Create a separate counter to keep keys in sequence
start_end_coordinates = {
    idx + 1: [coordinates_data[i], coordinates_data[i + 1]]
    for idx, i in enumerate(range(0, len(coordinates_data) - 1, 2))
}

# Save to JSON file after closing the plot
# saving: invoice number, date, total amount, second product cost
with open("coordinates_data.json", "w") as json_file:
    json.dump(start_end_coordinates, json_file, indent=4)

print("Coordinates data saved to coordinates_data.json")