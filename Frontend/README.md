
## Waterdip AI Front End Assignment

## Overview
A React-based single-page dashboard that visualizes hotel booking data with the following features:
- *Time Series Chart*: Displays the number of visitors (adults + children + babies) per day.
- *Column Chart*: Shows the number of visitors from each country.
- *Sparkline Charts*: Separate charts for the total number of adult and children visitors.
- *Date Range Selector*: Allows users to filter data based on the selected date range, updating all charts accordingly.

## Data
The dataset consists of 1,000 hotel booking records with the following columns:
- arrival_date_year
- arrival_date_month
- arrival_date_day_of_month
- adults: Number of adults for the booking.
- children: Number of children for the booking.
- babies: Number of babies for the booking.
- country: Country of origin of the travelers.

## Setup

1. Clone the repository:
   bash
   git clone https://github.com/Sravanis23/Waterdip-labs.git
   

2. Install dependencies:
   bash
   npm install
   

3. Run the app:
   bash
   npm start
   

## Tools & Libraries
- *React*: Used for building the dashboard UI.
- *ApexCharts*: For rendering the charts.
- *Bootstrap*: Used for styling the layout.
- *PapaParse*: CSV parser to handle the hotel booking data.

## Features

- *Date Range Picker*: Allows selecting a custom date range to filter booking data.
- *Time Series Chart*: A line chart showing the number of visitors per day, where visitors = adults + children + babies.
- *Column Chart*: A bar chart showing the number of visitors per country.
- *Sparkline Charts*: Two small charts showing trends for adult and children visitors over time.
  
## File Structure

- index.js: The entry point of the app.
- Dashboard.js: The main component responsible for rendering the charts and date picker.
- hotel_bookings_1000.csv: The dataset used for charting.
