import adsk.core, adsk.fusion, adsk.cam, traceback
import re  # Import the regular expression module

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = app.activeProduct

        # Check if there is an active design
        if not design:
            ui.messageBox('No active Fusion 360 design', 'No Design')
            return

        # Get the root component of the active design
        rootComp = design.rootComponent

        # Input box for user to enter the search regex pattern
        result = ui.inputBox('Enter the regex pattern to search for in component names:', 'Component Search Regex', '.*part.*')
        inputValue = result[0]  # User's input regex pattern
        inputOk = result[1]  # Boolean indicating if the user clicked 'OK'

        # Check the user response and proceed if OK was clicked
        if inputOk:
            message = 'Operation canceled by the user.'
            ui.messageBox(message)
            return
        
        pattern = re.compile(inputValue)  # Compile the regex pattern

        # List to hold components to delete (to avoid modifying the collection while iterating)
        components_to_delete = []

        # Function to recursively find components to delete
        def find_components(component):
            for comp in component.occurrences:
                # Use regex search to match the pattern
                if pattern.search(comp.component.name):
                    components_to_delete.append(comp)
                # Recursively search in sub-components
                find_components(comp.component)

        # Start the recursive component search
        find_components(rootComp)

        # Delete found components and count them
        number_deleted = len(components_to_delete)
        for comp in components_to_delete:
            comp.deleteMe()

        # Reporting the results
        if number_deleted > 0:
            message = 'Deleted {} components matching pattern "{}"'.format(number_deleted, inputValue)
        else:
            message = 'No components found matching pattern "{}"'.format(inputValue)

        ui.messageBox(message)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

if __name__ == "__main__":
    run(adsk.fusion.Design.cast(None))
