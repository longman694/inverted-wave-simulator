import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# --- App Title and Description ---
st.set_page_config(layout="wide")
st.title("Wave Interference Simulation")
st.markdown("""
This app simulates wave interference using three waves:
1.  **Wave 1:** The original sine wave.
2.  **Wave 2:** An inverted version of the original, with an adjustable time delay.
3.  **Wave 3:** The sum of Wave 1 and Wave 2 (destructive or constructive interference).

Use the sliders in the sidebar to see how frequency and time delay affect the resulting wave.
""")

# --- Sidebar Inputs ---
st.sidebar.header("Wave Controls")

# Input for Frequency
frequency = st.sidebar.number_input(
    "Frequency (Hz)",
    min_value=20.0,
    max_value=200.0,
    value=40.0,
    step=5.0,
    help="Frequency (f) of the original wave (Wave 1)."
)

# NEW: Input for Speed of Sound
speed_of_sound = st.sidebar.number_input(
    "Speed of Sound (v)",
    min_value=300.0,
    max_value=1000.0,
    value=343.0,  # Default speed of sound in air
    step=1.0,
    help="Speed of the wave (e.g., speed of sound in air, v) in m/s."
)

# NEW: Input for Length (Path Difference)
length = st.sidebar.number_input(
    "Path Length Difference (m)",
    min_value=0.0,
    max_value=5.0,
    value=0.0,
    step=0.1,
    help="The extra distance in meter that Wave 2 must travel, in meters. This creates the time delay."
)

# Input for Time Delay
time_delay_sec = length / (speed_of_sound + 1e-9)

# --- Wave Calculations ---

# Convert time delay from milliseconds to seconds
time_delay_ms = time_delay_sec * 1000.0

# Create a time array (e.g., for 100 milliseconds of simulation)
# 1000 points for a smooth curve
t = np.linspace(0, 0.050, 1000) 

# Calculate angular frequency
omega = 2 * np.pi * frequency

# 1. Wave 1 (Original): A * sin(ω*t)
wave1 = 1 * np.sin(omega * t)

# 2. Wave 2 (Inverted & Delayed): -A * sin(ω*(t - τ))
# The "-1 *" inverts the wave (180° phase shift)
# The "(t - time_delay_sec)" applies the time delay
wave2 = -1 * np.sin(omega * (t - time_delay_sec))

# 3. Wave 3 (Sum): Wave 1 + Wave 2
wave3 = wave1 + wave2

# --- Data Preparation with Pandas ---

# Create a "wide" DataFrame first
df_wide = pd.DataFrame({
    'Time (s)': t,
    'Wave 1 (Original)': wave1,
    'Wave 2 (Inverted & Delayed)': wave2,
    'Wave 3 (Sum)': wave3
})

# "Melt" the DataFrame into a "long" format
# This format is ideal for plotting with Altair
df_long = df_wide.melt(
    'Time (s)',
    var_name='Wave',
    value_name='Amplitude'
)

# --- Plotting with Altair ---

# Create the base chart
chart = alt.Chart(df_long).mark_line().encode(
    # Set X-axis to Time
    x=alt.X('Time (s)', axis=alt.Axis(title='Time (s)')),
    
    # Set Y-axis to Amplitude
    y=alt.Y('Amplitude', axis=alt.Axis(title='Amplitude'), scale=alt.Scale(domain=[-2.2, 2.2])),
    
    # Color the lines based on the 'Wave' column
    color=alt.Color('Wave', title='Wave Type'),
    
    # Add tooltips for interactivity
    tooltip=['Time (s)', 'Wave', 'Amplitude']
).properties(
    title=f"Interference (Frequency: {frequency} Hz, Length: {length:.2f} m, Delay: {time_delay_ms:.2f} ms)"
).interactive() # Make the chart zoomable and pannable

# Display the chart in the Streamlit app
st.altair_chart(chart, use_container_width=True)

# --- Optional: Show Raw Data ---
with st.expander("View Raw Data"):
    st.dataframe(df_wide)
