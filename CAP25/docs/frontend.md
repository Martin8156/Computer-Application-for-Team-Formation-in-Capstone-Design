# Frontend Documentation

## Overview
The frontend is built using React and provides a user interface for uploading CSV files and displaying project matching results. The application communicates with a backend server running on port 8888.

## Components

### App Component
The main component of the application that handles file uploads and displays matching results.

#### State Variables
- `matchingData`: Stores the matching results from the backend
- `uploadStatus`: Tracks the status of file uploads

#### Key Functions

##### `fetchMatchingData()`
- Fetches current matching data from the backend
- Endpoint: `POST http://localhost:8888/matching`
- Called on component mount and after successful file uploads

##### `handleFileUpload(event)`
- Handles CSV file uploads
- Endpoint: `POST http://localhost:8888/file/upload`
- Takes a CSV file and file type (Student/Company)
- Updates upload status based on server response

## UI Structure

### Header Section
- Displays the title "Project Matching System"

### Upload Section
- File upload form with:
  - File input (accepts .csv files)
  - Upload button
  - Status message display

### Matching Data Display
Displays four main sections:
1. Skills List
2. Students List
   - Shows student names and EIDs
   - Lists skills for each student
3. Projects List
   - Shows project names
   - Lists required skills
4. Matching Results
   - Shows project-student assignments
   - Groups students under their assigned projects

## Styling

### App.css
- Centered layout with max-width container
- Consistent padding and margins
- Card-like sections with background colors
- Responsive design elements

### Key CSS Classes
- `.App`: Main container styling
- `.App-header`: Header styling with dark background
- `.upload-section`: Styling for file upload area
- `.matching-data`: Styling for results display
- `.status-message`: Styling for upload status messages

## Usage

1. Start the application (`npm start`)
2. Upload student CSV file
3. Upload company CSV file
4. Wait for matching results to display
5. View the assignments in the matching section

## Dependencies
- React 18.2.0
- react-dom 18.2.0
- axios (for HTTP requests)
- react-scripts 5.0.1

## Development
- Run `npm start` for development server
- Run `npm build` for production build
- Default port: 3000
