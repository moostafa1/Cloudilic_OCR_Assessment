import matplotlib.pyplot as plt
import json
from config import CONFIG



# Define the event handler
def onclick(event):
    """
    Handles mouse click events on a matplotlib plot.

    Parameters
    ----------
    event : matplotlib.backend_bases.MouseEvent
        The event object containing information about the mouse click, including
        the location of the click in data coordinates.

    Notes
    -----
    This function appends the (x, y) coordinates of the click to the global
    `coordinates_data` list if the click is within the axes of the plot.
    """
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




if __name__ == "__main__":
    img = plt.imread(CONFIG["invoice_image_path"])

    # List to store coordinates data
    coordinates_data = []

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
    with open(CONFIG["rois_json"], "w") as json_file:
        json.dump(start_end_coordinates, json_file, indent=4)

    print("Coordinates data saved to coordinates_data.json")