import streamlit as st
import pdfplumber

st.title("Vehicle Mileage Calculator and Text Search")

# Add a sidebar button to calculate mileage
calculate_mileage = st.sidebar.button("Check Mileage")

# Define vehicle options and their respective mileage values
vehicle_options = {
    "Bus": 3.5,  # Default mileage for Bus
    "Car": 12.0,  # Example mileage for Car
    "Truck": 2.5,  # Example mileage for Truck
    "Moter Cycle": 40.0,
}

# Vehicle selection dropdown
selected_vehicle = st.sidebar.selectbox("Select Vehicle", list(vehicle_options.keys()))

# Get the selected vehicle's mileage value
mileage = vehicle_options.get(selected_vehicle, 3.5)  # Default to Bus mileage if not found

# Add a checkbox to enable custom mileage
enable_custom_mileage = st.sidebar.checkbox("Enable Custom Mileage")

# Add an input field to manually set the mileage (conditionally rendered)
if enable_custom_mileage:
    custom_mileage = st.sidebar.text_input("Custom Mileage (km/L)", mileage)

# Validate and update the mileage value
try:
    if enable_custom_mileage:
        mileage = float(custom_mileage)
except ValueError:
    st.write("Please enter a valid custom mileage value.")

# Calculate fuel consumption in liters per kilometer
fuel_consumption = 1 / mileage

# Add a sidebar button for calculating fuel consumption
calculate_fuel_consumption = st.sidebar.button("Calculate Fuel Consumption")

# Add a sidebar input for entering the total distance
total_distance = st.sidebar.text_input("Total Distance (km)", "")

# Add a sidebar input for entering the fuel price
fuel_price = st.sidebar.text_input("Fuel Price (per liter)", "")

# Add a sidebar input for entering additional expenses
additional_expenses = st.sidebar.text_input("Additional Expenses (Rs.)", "")

# Add a file uploader to upload a PDF file
uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])

# Add a text input for search queries
search_query = st.sidebar.text_input("Search Query in PDF", "")

# Add a search button to initiate the search
search_button = st.sidebar.button("Search in PDF")

if calculate_mileage:
    st.subheader("Mileage and Fuel Consumption:")
    st.write(f"Selected Vehicle: {selected_vehicle}")
    if enable_custom_mileage:
        st.write(f"Custom Mileage: {mileage:.2f} km/L")
    else:
        st.write(f"Default Mileage: {mileage:.2f} km/L")
    

if uploaded_file is not None:
    pdf_text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            pdf_text += page.extract_text()

    if calculate_fuel_consumption:
        if total_distance and fuel_price:
            try:
                distance = float(total_distance)
                fuel_needed = distance / mileage
                fuel_cost = fuel_needed * float(fuel_price)

                if additional_expenses and additional_expenses.replace(".", "", 1).isdigit():
                    total_cost = fuel_cost + float(additional_expenses)
                    st.subheader(f"Fuel Consumption for {distance} km:")
                    st.write(f"Total Distance: {distance} km")
                    st.write(f"Fuel Needed: {fuel_needed:.2f} liters")
                    st.write(f"Fuel Price: Rs.{fuel_price} per liter")
                    st.write(f"Additional Expenses: Rs.{additional_expenses}")
                    st.write(f"Total Fuel Cost: Rs.{total_cost:.2f}")
                else:
                    st.subheader(f"Fuel Consumption for {distance} km:")
                    st.write(f"Total Distance: {distance} km")
                    st.write(f"Fuel Needed: {fuel_needed:.2f} liters")
                    st.write(f"Fuel Price: Rs.{fuel_price} per liter")
                    st.write("Additional Expenses: Not specified")
                    st.write(f"Total Fuel Cost: Rs.{fuel_cost:.2f}")
            except (ValueError, ZeroDivisionError):
                st.write("Please enter valid values for total distance, fuel price, and mileage.")

    if search_button and search_query:
        search_results = [line for line in pdf_text.split("\n") if search_query.lower() in line.lower()]
        st.subheader(f"Search Results for '{search_query}' in PDF:")
        if search_results:
            for result in search_results:
                st.write(result)
        else:
            st.write(f"No matching results found for '{search_query}' in the PDF.")
