# WeatherAI Frontend

A modern React TypeScript frontend for the WeatherAI application, featuring a clean and intuitive user interface for weather forecasting.

## Features

- Real-time weather data display
- Interactive weather charts using Plotly.js
- Detailed weather information tables
- Responsive design for all devices
- TypeScript for type safety
- React 18 with modern features

## Prerequisites

- Node.js (v16 or higher)
- npm (v6 or higher)
- Backend API running (see main project README)

## Installation

1. Clone the repository and navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file in the frontend directory:
```bash
REACT_APP_API_URL=http://localhost:8000
```

## Development

To start the development server:

```bash
npm start
```

The application will be available at `http://localhost:3000`.

## Building for Production

To create a production build:

```bash
npm run build
```

The build artifacts will be stored in the `build/` directory.

## Testing

To run the test suite:

```bash
npm test
```

## Project Structure

```
frontend/
├── src/
│   ├── components/        # React components
│   ├── services/         # API services
│   ├── types/           # TypeScript interfaces
│   ├── App.tsx          # Main application component
│   ├── App.css          # Main application styles
│   ├── App.test.tsx     # Application tests
│   ├── index.tsx        # Application entry point
│   ├── index.css        # Global styles
│   ├── reportWebVitals.ts # Performance monitoring
│   └── setupTests.ts    # Test configuration
├── public/              # Static files
├── package.json         # Dependencies and scripts
├── tsconfig.json       # TypeScript configuration
├── tailwind.config.js  # Tailwind CSS configuration
└── postcss.config.js   # PostCSS configuration
```

## Key Dependencies

- React 18
- TypeScript
- Plotly.js for interactive charts
- React Testing Library
- Web Vitals for performance monitoring

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from Create React App

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
