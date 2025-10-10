<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
  <span style="display: inline-flex; align-items: center;">
    <img src="web/public/icon-small.png" alt="icon" style=" margin-right: 10px;">
    <h1 style="margin: 0;">Simple Attendance</h1>
  </span>

##

  <div>
    <img src="https://github.com/muscodev/simple_attendance/actions/workflows/ci.yml/badge.svg" alt="CI Status">
    <img src="https://muscodev.github.io/simple_attendance/coverage-badge.svg" alt="Coverage">
  </div>
</div>

# Simple Attendance

A location-based attendance tracking system designed for small businesses with mobile employees in field operations like support, maintenance, and service teams.

## Overview

Simple Attendance is a SaaS-based Progressive Web App (PWA) that enables companies to track employee attendance using geolocation. Built with multi-tenancy in mind, it allows multiple companies to operate independently within a single deployment.

## Key Features

- **Progressive Web App (PWA)**: Works seamlessly across Android, iOS, and Windows devices with PWA-capable browsers
- **Geolocation-based Check-in/Check-out**: Automatic location capture during attendance marking
- **Multi-tenant SaaS Model**: Multiple companies can use the same deployment with isolated data
- **Location Management**: Admins can define multiple work locations for their company
- **Distance Calculation**: Automatically records the nearest location and distance from marked points
- **Simple Onboarding**: Share a setup link with employees for one-time mobile app configuration
- **Attendance Reports**: View daily, monthly, and custom date range reports per employee
- **Cross-platform Support**: Accessible via web and mobile through a unified portal

## How It Works

1. **Company Admin Setup**: Login to the web/mobile portal and add work locations
2. **Employee Registration**: Admin adds employees and shares setup link
3. **One-time Configuration**: Employees configure their mobile app using the shared link
4. **Daily Attendance**: Employees mark in/out; system captures location and calculates distance from nearest marked location
5. **Reporting**: Admins view attendance records with date filters and employee-wise breakdowns

## Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Frontend**: Vue.js + Vite
- **Deployment**: Cloud-ready (containerized)

## Roadmap

### Upcoming Features

- **Geofencing**: Set allowed radius for each employee based on marked locations
- **Automated Processing**: Convert raw attendance marks into processed daily and monthly reports
- **Enhanced Analytics**: More detailed insights and attendance patterns


## Deployment

The application is designed for cloud deployment and can be containerized using Docker. Refer to deployment documentation for platform-specific instructions.

## Use Cases

- Field service companies
- Maintenance teams
- Support staff
- Mobile sales teams
- Any business with employees working at multiple locations

## Browser Compatibility

Works on any modern browser with PWA support:
- Chrome/Edge (Android, iOS, Windows, macOS)
- Safari (iOS, macOS)



## Support

For issues and questions, please use the GitHub issue tracker.
