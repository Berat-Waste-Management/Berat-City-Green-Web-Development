# Project Design Document

## Laundry Service Website
--------
Prepared by:

* Nick Kruse, Worcester Polytechnic Institute
* Mel Morin, Worcester Polytechnic Institute
* Edward Ruzicka, Worcester Polytechnic Institute
* Archer Petter, Worcester Polytechnic Institute
---

**Course** : CS 3733 - Software Engineering 

**Instructor**: Sakire Arslan Ay

---

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Software Design](#2-software-design)
    - [2.1 Database Model](#21-model)
    - [2.2 Modules and Interfaces](#22-modules-and-interfaces)
    - [2.2.1 Overview](#221-overview)
    - [2.2.2 Interfaces](#222-interfaces)
    - [2.3 User Interface Design](#23-view-and-user-interface-design)
- [3. References](#3-references)

<a name="revision-history"> </a>

### Document Revision History

|    Name   |   Date   |    Changes   |  Version  |
| --------- | -------- | ------------ | --------- |
|Revision 1 |2026-2-05 |Initial draft |    1.0    |
|Revision 2 |2026-2-10 |Project Design|    1.1    |
|Revision 3  |2026-2-12 |Draft Submison|   1.2    |
|Revision 4  |2026-2-18 |Pre-meeting changes|   1.3    |
|Revision 5  |2026-2-19 |Post-meeting changes|   1.4    |
|Revision 6  |2026-2-20 |Final changes|   1.5    |


# 1. Introduction

This document was created to provide an overview for the design of our Laundry App. Using UML diagrams it shows the relationships between class components. 

# 2. Software Design

## 2.1 Database Model

Machine
- The Machine table stores all registered machines at various locations. It's stored in the database and contains machine ID, type, and location.  
Role: Represents each individual machine
      Links to reservation path
      Organizes by location

Booking
- The Booking table stores all submitted registrations by users. It records machine ID, user ID, start time, and end time.
Role: Tracks scheduled time blocks for each machine
      Allows multiple reservations per machine
      Uses a calendar style scheduling system
      Associates reservations made by specific users

Location
- The Location table stores all available laundromats on the app (dorms on campus). It records ID and name of each location.
Role: Groups machines by dorm
      Allows map page to link to different dorm laundromat pages with their respective machines

Report 
- The Report table stores all reports sent out by a user on a problem from a machine. 
It stores the machine and a short description of the problem.
Role: Shows problems to an admin

Member
- The member table we have stores all registered users of the app. It contains login and role (Admin, User, Driver), and records other general information (username, email, password)
Role: Authenticate users
      Records name of user who creates reservation
      Determines Roles (admin, driver, user)

Admin
- The Admin is a type of user who has higher permissions like disabling machines. 
The admin has extra data like the locations it serves and the reports they've been sent. 
Role: Maintain website and machine

Driver
- The Driver is a type of user who can pick up people's laundry and wash it for them. They have a car saved in their data. 
Role: Ship people's laundry 

User 
- The User type is the base kind of user that any normal person who enters the website will register as. The only special property they have is an address. 

![alt text](<Images/UML_Diagram.png>)

## 2.2 Modules and Interfaces

### 2.2.1 Overview

Our software architecture is pretty similar to the other software that we have created in class. We have the authorization component for the User, Driver, and Admin to register and login to their respective accounts. Each account will look different based on the user-type, for example, the Driver will be able to change the status of the orders that they receive and Admin will be able to view reports from the location input that they registered with. In terms of models, we will have viewable machines for users and drivers to reserve on the home page, and each user will have different accessible pages. Such as, the User will have an added feature to report machines, while the admin will have a separate page on their profile that will allow them to view the machines that have been reported for their location. The driver will also have an added page that will allow them to register their vehicle to the database. 

![alt text](<Images/FP UML - System.jpg>)

### 2.2.2 Interfaces

#### 2.2.2.1 \ Main Routes

|   | Methods           | URL Path   | Description  |
|:--|:------------------|:-----------|:-------------|
|1. | index                  | / or /index           |  displays the main page            |
|2. | profile                  |  /user/<int:user_id>/profile          |  displays the current users profile page            |
|3. |  reserve                 |  /machine/<int:machine_id>/reserve          |  reserves a timeslot for the user for a machine            |
|4. | cancel_reservation                  |  /machine/<int:machine_id>/cancel          |  cancels a reservation            |
|5. |  reserve_time                 | /machine/<int:machine_id>/reserve_time           | reserves a time for the user to use a machine             
|6. |  reviews                     | /location/<int:location_id>/reviews         | Leaves a review based on the laundromat location            
|7. |  view_reports    | /user/<int:user_id>/profile/reports         | allows admin to review reports based on a location            
|8. |  reserve_bulk           | /machine/<int:machine_id>/reserve_bulk    | reserves a bulk booking for laundry pickup and drop-off             
|9. |  report_machine          | /machine/<int:machine_id>/report_machine       | reports a broken machine to be later viewed by admin            |
|10. |  routes_map    | /user/<int:user_id>/profile/orders/routes_map     | an interactive routes map; drivers select a location of the route           |
|11. |  status_update   | /user/<int:user_id>/profile/orders/status_update   | shows the status update for where the laundry is in the process; drivers can update the status       |
|12. |  machine_update     | /user/<int:user_id>/profile/reports/<int:machine_id>/machine_update  | admin can update the machine status depending on if it is broken or fixed          |


#### 2.2.2.2 \ Auth Routes

|   | Methods           | URL Path   | Description  |
|:--|:------------------|:-----------|:-------------|
|1. | register                  | /user/register           | registers a new user / displays register page            |
|2. | login                  |  /user/login          | logs in a user / displays login page             |
|3. |  logout                 | /user/logout           |  logs out a user and takes them back to the login            |
|4. | admin register            |/user/admin_register            |registers an admin with dropdown locations/displays register page              |


#### 2.2.2.3 \ Errors Routes
|   | Methods           | URL Path   | Description  |
|:--|:------------------|:-----------|:-------------|
|1. | internal error     | 500           | if there is an internal error it is an error 500   |
|2. | not found error    | 404         |  if the page is not found it will produce a 404 error    |

### 2.3 User Interface Design 

The UI design mockups here are for the Admin, Driver, and User profile pages which will display the bookings, reports, and bulk laundry orders

![alt text](<Images/AdminProfileLaundryService.webp>)

![alt text](<Images/DriverProfileLaundryService.png>)

![alt text](<Images/UserProfileLaundryService.png>)


Here is what is presented on our current website:

Register Page:
![alt text](<Images/Screenshot 2026-02-20 005940.png>)

Login Page:
![alt text](<Images/Screenshot 2026-02-20 005924.png>)

Locations Page:
![alt text](<Images/Screenshot 2026-02-20 005755.png>)

Specific Location's Machines Page:
![alt text](<Images/Screenshot 2026-02-20 005824.png>)

Profile Page:
![alt text](<Images/Screenshot 2026-02-20 005810.png>)

Reserve Machine Page:
![alt text](<Images/Screenshot 2026-02-20 005852.png>)

Machines Page with Reservation:
![alt text](<Images/Screenshot 2026-02-20 005907.png>)


# 3. References

[drawio.com](drawio.com) - Creation of the database UML diagram 
