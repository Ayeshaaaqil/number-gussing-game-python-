import streamlit as st
import random

# Set page configuration
st.set_page_config(
    page_title="Number Guessing Game",
    page_icon="🎮",
    layout="centered"
)

# Initialize game state
if 'random_number' not in st.session_state:
    st.session_state.random_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.messages = []

# Function to restart the game
def restart_game():
    st.session_state.random_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.messages = []

# Title and instructions
st.title("🎮 Number Guessing Game")
st.markdown("""
Try to guess the number between 1 and 100!
I'll tell you if your guess is too high or too low.
""")

# Game interface
col1, col2 = st.columns([3, 1])

with col1:
    guess = st.number_input("Enter your guess:", min_value=1, max_value=100, step=1, key="guess_input")

with col2:
    submit = st.button("Submit Guess")
    
# Handle guess submission
if submit and not st.session_state.game_over:
    st.session_state.attempts += 1
    
    if guess < st.session_state.random_number:
        st.session_state.messages.append(f"Guess #{st.session_state.attempts}: {guess} is too low!")
    elif guess > st.session_state.random_number:
        st.session_state.messages.append(f"Guess #{st.session_state.attempts}: {guess} is too high!")
    else:
        st.session_state.messages.append(f"🎉 Congratulations! You guessed the number {st.session_state.random_number} in {st.session_state.attempts} attempts!")
        st.session_state.game_over = True

# Display game messages
st.subheader("Game Progress:")
message_container = st.container()

with message_container:
    for message in st.session_state.messages:
        if "Congratulations" in message:
            st.success(message)
        elif "too low" in message:
            st.warning(message)
        elif "too high" in message:
            st.error(message)

# Show restart button if game is over
if st.session_state.game_over:
    if st.button("Play Again"):
        restart_game()

# Display game statistics
st.sidebar.header("Game Statistics")
st.sidebar.metric("Attempts", st.session_state.attempts)
st.sidebar.metric("Target Number", "???" if not st.session_state.game_over else st.session_state.random_number)

# Add some fun facts about the current number
if st.session_state.game_over:
    number = st.session_state.random_number
    st.sidebar.subheader(f"Fun Facts about {number}")
    
    facts = []
    if number % 2 == 0:
        facts.append(f"{number} is an even number.")
    else:
        facts.append(f"{number} is an odd number.")
        
    if number > 1 and all(number % i != 0 for i in range(2, int(number**0.5) + 1)):
        facts.append(f"{number} is a prime number!")
        
    if int(number**0.5)**2 == number:
        facts.append(f"{number} is a perfect square! ({int(number**0.5)}²)")
    
    for fact in facts:
        st.sidebar.info(fact)