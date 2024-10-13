import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Form } from 'react-bootstrap';
import ReactApexChart from 'react-apexcharts';
import Papa from 'papaparse';  // Import PapaParse
import csvFile from './hotel_bookings_1000.csv';  // Path to your CSV file

const Dashboard = () => {
    const [rawData, setRawData] = useState([]);  // Separate raw CSV data
    const [filteredData, setFilteredData] = useState([]);
    const [startDate, setStartDate] = useState('2015-01-01');
    const [endDate, setEndDate] = useState('2017-12-31');

    // Load and parse the CSV data on component mount
    useEffect(() => {
        Papa.parse(csvFile, {
            download: true,
            header: true,  // Parse CSV as an array of objects
            complete: (result) => {
                setRawData(result.data);  // Set raw CSV data as array of objects
            },
            error: (error) => {
                console.error("Error parsing CSV: ", error);
            }
        });
    }, []);

    // Function to filter the data based on a date range
    const filterDataByDate = (data, startDate, endDate) => {
        return data.filter(item => {
            // Ensure valid dates, handle cases where some date fields may be undefined or invalid
            if (!item.arrival_date_year || !item.arrival_date_month || !item.arrival_date_day_of_month) return false;
            const itemDate = new Date(`${item.arrival_date_year}-${item.arrival_date_month.padStart(2, '0')}-${item.arrival_date_day_of_month.padStart(2, '0')}`);
            return itemDate >= new Date(startDate) && itemDate <= new Date(endDate);
        });
    };

    // Filter data when the date range changes or raw data is loaded
    useEffect(() => {
        if (rawData.length) {
            const filtered = filterDataByDate(rawData, startDate, endDate);
            setFilteredData(filtered);
        }
    }, [startDate, endDate, rawData]);  // Use rawData as dependency

    return (
        <Container fluid className="dashboard mt-4">
            <DateRangePicker setStartDate={setStartDate} setEndDate={setEndDate} />
            <Row className="mt-4">
                <Col md={6}>
                    <Card>
                        <Card.Body>
                            <VisitorTimeSeries data={filteredData} />
                        </Card.Body>
                    </Card>
                </Col>
                <Col md={6}>
                    <Card>
                        <Card.Body>
                            <VisitorsByCountry data={filteredData} />
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
            <Row className="mt-4">
                <Col md={6}>
                    <Card>
                        <Card.Body>
                            <Sparkline data={filteredData} type="adults" />
                        </Card.Body>
                    </Card>
                </Col>
                <Col md={6}>
                    <Card>
                        <Card.Body>
                            <Sparkline data={filteredData} type="children" />
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </Container>
    );
};

// Date Range Picker Component
const DateRangePicker = ({ setStartDate, setEndDate }) => {
    return (
        <Form className="date-picker">
            <Row>
                <Col md={6}>
                    <Form.Group controlId="startDate">
                        <Form.Label>Start Date:</Form.Label>
                        <Form.Control type="date" onChange={e => setStartDate(e.target.value)} />
                    </Form.Group>
                </Col>
                <Col md={6}>
                    <Form.Group controlId="endDate">
                        <Form.Label>End Date:</Form.Label>
                        <Form.Control type="date" onChange={e => setEndDate(e.target.value)} />
                    </Form.Group>
                </Col>
            </Row>
        </Form>
    );
};

// Time Series Chart: Number of visitors per day
const VisitorTimeSeries = ({ data }) => {
    const seriesData = data.map(item => ({
        x: new Date(`${item.arrival_date_year}-${item.arrival_date_month.padStart(2, '0')}-${item.arrival_date_day_of_month.padStart(2, '0')}`),
        y: parseInt(item.adults) + parseInt(item.children) + parseInt(item.babies)  // Sum of visitors
    }));

    const options = {
        chart: { type: 'line', zoom: { enabled: true } },
        xaxis: { type: 'datetime' },
        title: { text: 'Number of Visitors Per Day' }
    };

    return <ReactApexChart options={options} series={[{ name: 'Visitors', data: seriesData }]} type="line" height={350} />;
};

// Column Chart: Number of visitors per country
const VisitorsByCountry = ({ data }) => {
    const countryMap = data.reduce((acc, item) => {
        acc[item.country] = (acc[item.country] || 0) + (parseInt(item.adults) + parseInt(item.children) + parseInt(item.babies));
        return acc;
    }, {});

    const seriesData = Object.keys(countryMap).map(country => ({
        x: country,
        y: countryMap[country]
    }));

    const options = {
        chart: { type: 'bar' },
        xaxis: { categories: Object.keys(countryMap) },
        title: { text: 'Number of Visitors by Country' }
    };

    return <ReactApexChart options={options} series={[{ name: 'Visitors', data: seriesData }]} type="bar" height={350} />;
};

// Sparkline Charts for Adults and Children Visitors
const Sparkline = ({ data, type }) => {
    const visitorData = data.map(item => parseInt(item[type]));

    const options = {
        chart: { sparkline: { enabled: true } },
        title: { text: `Total ${type === 'adults' ? 'Adult' : 'Children'} Visitors`, align: 'center' }
    };

    const total = visitorData.reduce((acc, curr) => acc + curr, 0);

    return (
        <div className="sparkline">
            <ReactApexChart options={options} series={[{ name: 'Visitors', data: visitorData }]} type="line" height={100} />
            <div className="total-visitors">Total {type}: {total}</div>
        </div>
    );
};

export default Dashboard;
