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
    "Speed of Sound (m/s)",
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

# ==========================================================
# --- 2. Frequency Response Plot (NEW SECTION) ---
# ==========================================================
st.header("Frequency Response Plot (20 Hz to 500 Hz)")
st.markdown(f"""
This plot shows the resulting amplitude (SPL) of **Wave 3 (the sum)** across a *range* of frequencies.
This simulation shows the "comb filtering" effect caused by the fixed time delay of **{time_delay_sec*1000:.2f} ms**.
""")

# --- Frequency Response Calculation ---

@st.cache_data
def calculate_frequency_response(delay, speed, path_length):
    """
    Calculates the SPL of Wave 3 for frequencies from 20 to 500 Hz.
    We use @st.cache_data so this only re-runs when inputs change.
    """
    
    # Define the frequency range to scan
    freq_range = np.linspace(20, 500, 481) # 20 Hz to 500 Hz, 1 Hz steps
    
    # We need a time array for the RMS calculation.
    # 100ms (0.1s) is a good, safe duration to get a stable RMS.
    t_sweep = np.linspace(0, 0.1, 1000) 
    
    # Calculate the reference RMS (RMS of Wave 1, which has amplitude 1)
    # RMS for a sine wave of amplitude 1 is 1/sqrt(2)
    rms_ref = 1 / np.sqrt(2)
    
    spl_results = []

    # Loop through each frequency to calculate the resulting SPL
    for f in freq_range:
        omega_sweep = 2 * np.pi * f
        
        # 1. Wave 1
        wave1_sweep = 1 * np.sin(omega_sweep * t_sweep)
        
        # 2. Wave 2 (using the fixed time_delay_sec)
        wave2_sweep = -1 * np.sin(omega_sweep * (t_sweep - delay))
        
        # 3. Wave 3 (Sum)
        wave3_sweep = wave1_sweep + wave2_sweep
        
        # Calculate the RMS of the resulting wave
        rms_wave3 = np.sqrt(np.mean(np.square(wave3_sweep)))
        
        # Calculate SPL in dB relative to Wave 1's RMS (the 0 dB baseline)
        # Add a small epsilon (1e-9) to prevent log(0) error
        spl = 20 * np.log10((rms_wave3 + 1e-9) / rms_ref)
        
        spl_results.append({'Frequency (Hz)': f, 'SPL (dB)': spl})

    # Create a DataFrame for the frequency response plot
    return pd.DataFrame(spl_results)

# Run the calculation
df_freq = calculate_frequency_response(time_delay_sec, speed_of_sound, length)

# --- Plotting with Altair ---
chart_freq = alt.Chart(df_freq).mark_line(color="#2ca02c").encode(
    x=alt.X('Frequency (Hz)', axis=alt.Axis(title='Frequency (Hz)'), scale=alt.Scale(domain=[20, 500])),
    y=alt.Y('SPL (dB)', axis=alt.Axis(title='Sound Pressure Level (dB)')),
    tooltip=[
        alt.Tooltip('Frequency (Hz)', format='.1f'), 
        alt.Tooltip('SPL (dB)', format='.2f')
    ]
).properties(
    title=f"Frequency Response for {length:.2f} m Path Difference (τ = {time_delay_sec*1000:.2f} ms)"
).interactive()

st.altair_chart(chart_freq, use_container_width=True)


# --- Optional: Show Raw Data ---
with st.expander("View Time Domain Raw Data"):
    st.dataframe(df_wide)
    
with st.expander("View Frequency Response Raw Data"):
    st.dataframe(df_freq)