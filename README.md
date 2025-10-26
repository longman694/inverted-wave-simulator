# Wave Interference Simulation

This is an interactive web application built with Streamlit to simulate and visualize the principle of wave interference. It demonstrates how two waves can combine, either constructively or destructively, based on their phase shift.

This tool is perfect for students, educators, or anyone interested in understanding how wave properties like frequency, phase shift, and path length difference create interference patterns.

## Features

  * **Interactive Chart:** Uses Altair for a zoomable, pannable plot of all three waves.
  * **Real-time Controls:** Adjust wave parameters in the sidebar and see the interference pattern update instantly.
  * **Physics-Based Inputs:**
      * **Frequency ($f$):** Set the frequency of the original wave in Hz.
      * **Speed of Sound ($v$):** Define the medium by setting the wave's speed (e.g., 343 m/s for air).
      * **Path Length Difference ($L$):** Set the extra distance (in meters) the second wave travels, which is used to calculate the time delay.
  * **Calculated Feedback:** The app displays the resulting time delay ($\tau$) in milliseconds, calculated from your inputs.
  * **Data Explorer:** An expandable section to view the raw Pandas DataFrame behind the plot.

## The Science

The simulation is based on the **superposition principle**, which states that the net amplitude of two or more overlapping waves is the sum of their individual amplitudes.

The app models three waves:

1.  **Wave 1 (Original):** A standard sine wave.

      * $\text{Wave}_1(t) = A \sin(\omega t)$

2.  **Wave 2 (Inverted & Delayed):** An inverted copy (180° phase shift) of the first wave, which is also delayed in time ($\tau$).

      * $\text{Wave}_2(t) = -A \sin(\omega(t - \tau))$

3.  **Wave 3 (Sum):** The resulting interference pattern from the superposition of the first two waves.

      * $\text{Wave}_3(t) = \text{Wave}_1(t) + \text{Wave}_2(t)$

-----

### Key Variables:

  * **Amplitude ($A$):** Set to `1` in this simulation.
  * **Angular Frequency ($\omega$):** Calculated from your **Frequency ($f$)** input as $\omega = 2 \pi f$.
  * **Time Delay ($\tau$):** This is the crucial component. It's calculated from your sidebar inputs using the physical relationship:
      * $\tau = L / v$
      * *(Time Delay = Path Length Difference / Speed of Sound)*

By adjusting the inputs, you can create scenarios:

  * **Perfect Destructive Interference:** If the **Path Length Difference ($L$)** is 0, the time delay ($\tau$) is 0. The simulation becomes $ \\sin(\\omega t) + (-\\sin(\\omega t)) $, which equals **0**. This is a classic model for active noise cancellation.
  * **Constructive / Other Interference:** As you increase the **Path Length Difference**, the time delay ($\tau$) increases, shifting Wave 2 along the time axis. This phase shift causes the waves to add up in different ways, changing the amplitude of the resulting Wave 3.

## How to Run

To run this project locally, follow these steps.

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Install uv**

    ```bash
    pip install uv
    ```

3.  **Run app with uv**

    ```bash
    uv run streamlit run app.py
    ```

## Built With

  * [Streamlit](https://streamlit.io/) - For the web app UI and interactivity.
  * [Pandas](https://pandas.pydata.org/) - For data structure management.
  * [NumPy](https://numpy.org/) - For numerical calculations and wave generation.
  * [Altair](https://altair-viz.github.io/) - For declarative and interactive data visualization.

## License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).