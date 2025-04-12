from gpiozero import LED, Button
from time import sleep, time
from random import uniform

# Set up the LED on GPIO pin 4
led = LED(4)

# Set up buttons on GPIO pins 15 (right) and 14 (left)
right_button = Button(15)
left_button = Button(14)

# Get player names
left_name = input('Left player name is: ')
right_name = input('Right player name is: ')

# Initialize scores
left_score = 0
right_score = 0

# Flag to ensure only one button press is processed per round
button_pressed = False

# Number of rounds
max_rounds = 5
rounds = 0

# Function to handle button presses
def pressed(button):
    global reaction_start_time, left_score, right_score, button_pressed
    if reaction_start_time is not None and not button_pressed:
        reaction_time = time() - reaction_start_time
        if button.pin.number == 14:
            print(f"{left_name} pressed the button in {reaction_time:.2f} seconds")
            left_score += 1
        else:
            print(f"{right_name} pressed the button in {reaction_time:.2f} seconds")
            right_score += 1
        reaction_start_time = None
        button_pressed = True

while rounds < max_rounds:
    # Reset button_pressed flag at the start of each round
    button_pressed = False

    # Turn the LED on
    led.on()
    print("LED is ON")

    # Wait for a random time between 5 and 10 seconds
    sleep(uniform(5, 10))

    # Turn the LED off and record the start time
    led.off()
    reaction_start_time = time()
    print(f"LED turned OFF at: {reaction_start_time}")

    # Assign the function to button press events
    right_button.when_pressed = pressed
    left_button.when_pressed = pressed

    # Wait for 2 seconds to allow players to press the button
    end_time = time() + 2
    while time() < end_time:
        pass  # Busy-wait instead of blocking the main thread

    # Reset button press handlers after each round
    right_button.when_pressed = None
    left_button.when_pressed = None

    # Print current scores only if a button was pressed
    if button_pressed:
        print(f"Current Scores: {left_name} - {left_score}, {right_name} - {right_score}")
    else:
        print("No button was pressed this round.")

    rounds += 1

print("Game Over")
print(f"Final Scores: {left_name} - {left_score}, {right_name} - {right_score}")
