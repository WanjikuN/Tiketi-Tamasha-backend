# Tiketi-Tamasha-backend
## ERD Diagram
![Relational Diagram](./images/erdiagram.png)

# 1. TIKETI TAMASHA BACKEND 
# 1.1 Project Overview

"Tiketi Tamasha" is an event ticketing and management platform designed to address the challenges associated with discovering, booking, and attending events. The project's goal is to provide a user-friendly experience for both event organizers and attendees.

# 1.2 Problem Statement
Existing event ticketing platforms often lack essential features, such as a simple user interface, secure payment processing, and real-time ticket availability updates. Tiketi Tamasha aims to overcome these challenges and provide a seamless experience.

# 1.3 Solution
The solution involves a Full Stack development approach with React for the frontend and Python Flask for the backend. The system emphasizes security through JWT Bearer authentication, user-defined roles, and secure payment processing with MPESA STK.

# 1.4 Team
The project is developed by a Full Stack team with expertise in React for the frontend and Python Flask for the backend.

# 2. Architecture Overview
# 2.1 Technology Stack
Backend: Python Flask
Database: PostgreSQL
Frontend: ReactJs & Redux Toolkit (state management)
Wireframes: Figma (Mobile-friendly)
Testing Frameworks: Jest & Minitests

# 2.2 System Components
Backend Server: Handles authentication, user and event management, ticketing, and payment processing.
Database: Stores user data, event information, and transaction details.
Frontend Client: Provides a user interface for interacting with the system.
Testing Frameworks: Jest for frontend testing and Minitests for backend testing.

# 3. API Documentation
# 3.1 Authentication
Endpoint: /auth
Description: Manages user authentication using JWT Bearer tokens.

# 3.2 User Management
Endpoint: /users
Description: Allows user registration, role assignment, and profile management.

# 3.3 Event Management
Endpoint: /events
Description: Enables organizers to create events, set ticket availability, and define pricing.

# 3.4 Ticket Management
Endpoint: /tickets
Description: Manages the purchase and viewing of tickets by customers.

# 3.5 Payment Processing
Endpoint: /payments
Description: Facilitates secure payment processing using MPESA STK.

# 3.6 Search and Discovery
Endpoint: /search
Description: Allows users to search for events based on location, tags, or categories.

# 4. Database Schema
# 4.1 Tables
Users
Events
Tickets
Payments

# 4.2 Relationships
Users to Events (Organizer relationship)
Users to Tickets (Customer relationship)
Events to Tickets (Ticket availability relationship)

# 5. Security Measures
# 5.1 JWT Bearer
Ensures secure authentication using JWT Bearer tokens.

# 5.2 User Roles and Permissions
Defines user roles with preset permissions to ensure proper access control.

# 5.3 Secure Payment Processing
Implements secure payment processing through MPESA STK.

# 6. Testing Strategy
# 6.1 Jest
Utilizes Jest for frontend testing to ensure UI components function as expected.

# 6.2 Minitests
Implements Minitests for backend testing to verify the correctness of server-side functionalities.

# 6.3 Test Coverage
Regularly assesses test coverage to maintain the reliability of the system