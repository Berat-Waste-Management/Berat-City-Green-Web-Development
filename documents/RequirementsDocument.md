# Software Requirements and Use Cases

## Laundry Service Website
--------
Prepared by:

* Nick Kruse, Worcester Polytechnic Institute
* Mel Morin, Worcester Polytechnic Institute
* Edward Ruzicka, Worcester Polytechnic Institute

---

**Course** : CS 3733 - Software Engineering

**Instructor**: Sakire Arslan Ay

---

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Requirements Specification](#2-requirements-specification)
  - [2.1 Customer, Users, and Stakeholders](#21-customer-users-and-stakeholders)
  - [2.2 User Stories](#22-user-stories)
  - [2.3 Use Cases](#23-use-cases)
- [3. User Interface](#3-user-interface)
- [4. Product Backlog](#4-product-backlog)
- [4. References](#4-references)
- [Appendix: Grading Rubric](#appendix-grading-rubric)

<a name="revision-history"> </a>

## Document Revision History

|    Name   |   Date   |    Changes   |  Version  |
| --------- | -------- | ------------ | --------- |
|Revision 1 |2026-1-05 |Initial draft |    1.0    |
|           |          |              |           |
|           |          |              |           |

----
# 1. Introduction

This software is a laundry service website that allows users to reserve washers and dryers for specific time slots. Users can also find nearby laundromat locations and view washer and dryer availability. In addition, customers may order bulk laundry services that include pickup, washing, drying, folding, ironing, and delivery. Users can customize their orders by selecting services and specifying detergent preferences. The system also allows users to track their laundry and view its current status.

On the admin side, drivers can view available routes on a map, select pickup locations, and update the status of laundry orders.

----
# 2. Requirements Specification

## 2.1 Customer, Users, and Stakeholders

The customers of this software are largely focused on the owners of laundromats who want an app to manage machine usage, scheduling, and other general laundry services. The main users of the app include laundry customers, laundromat administrators, and drivers for the laundromats.

Laundry customers use the system to view machine availability, reserve washers and dryers, schedule laundry times, request bulk laundry services, and track the status of their laundry. 

Administrators use the app to manage machines, view reviews, handle reports of broken machines, and update machine availability. 

Drivers use the app to view pickup and delivery routes, select locations, and update the status of laundry orders during transit.

Our stakeholders include the laundromat's employees who are responsible for maintenance and customer support, as well as developers who make sure the software continues to operate correctly.

----
## 2.2 User Stories

1. As a Laundry User, I want to see the availability  of machines so that I know which machines are open to use.

2. As a Laundry User, I want to register an account and log in so that I can save my location and other information for future use.

3. As a Laundry User, I want to leave reviews for locations so that I can help keep other customers informed.

4. As a Laundry User, I want to schedule laundry time slots so that I can reserve a spot to do my laundry.

5. As a Laundry User, I want to view the laundry schedule so that I can see when other users are scheduled and plan accordingly.

6. As a Laundry User, I want to see how much time is left on machines so that I know when machines will become available.

7. As a Laundry User, I want to report broken machines so that employees know to fix them.

8. As a Laundry User, I want to track my bulk laundry orders so that I know the current status and when my laundry will be completed.

9. As a Laundry User, I want to request bulk laundry services so that my laundry can be picked up, washed, dried, and delivered.

10. As an Admin, I want to view machines that have been reported as broken so that I know which machines need to be fixed.

11. As an Admin, I want to mark machines as inactive so that broken machines are not available for users to reserve.

12. As an Admin, I want to mark machines as active once they are fixed so that users can reserve them again.

13. As an Admin, I want to mark machines as in use so that customers without home computer devices don't go unnoticed to online users who resevere machines virtually.

14. As a Driver, I want to view laundry routes on an interactive map so that I can choose pickup locations closest to me.

15. As a Driver, I want to update the status of laundry in transportation so that users can track their laundry status.


----
## 2.3 Use Cases

___________________________________________________
| Use case # 1       |                            |
| ------------------ |----------------------------|
| Name               | View Machine Availability  |
| Participating actor| Laundry User               |
| Entry condition(s) | The user is logged into the|
|                    | app and a location is      |
|                    | selected                   |
| Exit condition(s)  | Based on general user      |
|                    | reservations, the app shows|
|                    | the current status of      |
|                    | eashers and dryers         |
|                    | (availability, remaining   |
|                    | time)                      |
| Flow of events     | 1. User selects location   |
|                    | 2. App display's location's|
|                    |    machines & availability |
|                    | 3. App shows remaining time|
| Alt flow of events | In step 2: Machine status  |
|                    | doesn't show up, app       |
|                    | displays error message     |
| Iteration #        | Iteration 1                |
|____________________|____________________________|

___________________________________________________
| Use case # 2       |                            |
| ------------------ |----------------------------|
| Name               | Schedule Laundry Time      |
| Participating actor| Laundry User               |
| Entry condition(s) | The user is logged into the|
|                    | app and clicks on schedule |
|                    | button to view the shared  |
|                    | schedule                   |
| Exit condition(s)  | A time is booked for the   |
|                    | user and marked on the     |
|                    | shared schedule for others |
|                    | to see                     |
| Flow of events     | 1. User views schedule     |
|                    | 2. User selects times and  |
|                    |    reserves a spot         |
|                    | 3. App confirms user's     |
|                    |    reserved time and update|
|                    |    the public schedule     |
| Alt flow of events | In step 2: User reservation|
|                    | time is too long and system|
|                    | displays error message     |
|                    | asking user to change times|
| Iteration #        | Iteration 1                |
|____________________|____________________________|

___________________________________________________
| Use case # 3       |                            |
| ------------------ |----------------------------|
| Name               | Report Broken Machine      |
| Participating actor| Laundry User               |
| Entry condition(s) | The user is logged into the|
|                    | app and views machines     |
| Exit condition(s)  | The machine is marked as   |
|                    | broken, which is visible to|
|                    | admin who can then change  |
|                    | its status to inactive     |
| Flow of events     | 1. User selects machine    |
|                    | 2. User reports machine as |
|                    |    broken                  |
|                    | 3. App notifies admin and  |
|                    |    admin can change machine|
|                    |    as inactive             |
| Alt flow of events | In step 2: Machine has     |
|                    | already been reported, and |
|                    | notifies user with message |
| Iteration #        | Iteration 2                |
|____________________|____________________________|

___________________________________________________
| Use case # 4       |                            |
| ------------------ |----------------------------|
| Name               | Admin Updates Machine      |
|                    | Status                     |
| Participating actor| Admin                      |
| Entry condition(s) | Admin is logged into the ap|
|                    | and can see customer has   |
|                    | reported machine as broken |
| Exit condition(s)  | The machine's status is    |
|                    | updated as inactive or     |
|                    | active                     |
| Flow of events     | 1. Admin views list of     |
|                    |    reported machines       |
|                    | 2. Admin selects machine   |
|                    | 3. Admin updates status    |
|                    |    as active or inactive   |
|                    | 4. App displays status to  |
|                    |    users                   |
| Alt flow of events | In step 3: Update fails    |
|                    | and error message is       |
|                    | displayed to admin         |
| Iteration #        | Iteration 3                |
|____________________|____________________________|

___________________________________________________
| Use case # 5       |                            |
| ------------------ |----------------------------|
| Name               | Request Bulk Laundry       |
|                    | Service                    |
| Participating actor| Laundry User               |
| Entry condition(s) | User is logged into the app|
|                    | and bulk laundry services  |
|                    | are available              |
| Exit condition(s)  | A bulk laundry order is    |
|                    | submitted and visible to   |
|                    | driver                     |
| Flow of events     | 1. User selects bulk order |
|                    |    service                 |
|                    | 2. User selects service    |
|                    |    options(wash, dry, iron,|
|                    |    soap, etc.)             |
|                    | 3. System confirms order   |
|                    |    and brings user to track|
|                    |    -ing page               |
| Alt flow of events | In step 3: Requsest fails  |
|                    | if service is down for the |
|                    | day                        |
| Iteration #        | Iteration 3                |
|____________________|____________________________|

___________________________________________________
| Use case # 6       |                            |
| ------------------ |----------------------------|
| Name               | Setting Machine as In-Use  |
| Participating actor| Admin                      |
| Entry condition(s) | Admin is logged in and has |
|                    | access to view machines in |
|                    | use                        |
| Exit condition(s)  | Admin alters in-use status |
|                    | of machines for in-person  |
|                    | customers who use machines |
| Flow of events     | 1. Admin selects machine   |
|                    | 2. Admin alters its in-use |
|                    |    status                  |
|                    | 3. System updates status   |
| Alt flow of events | In step 2: Requsest fails  |
|                    | if machine is already shown|
|                    | to be in use               |
| Iteration #        | Iteration 3                |
|____________________|____________________________|

----
# 3. User Interface

This was AI generated through Figma. As learning college students, we don't expect our final result to be this polished, but these generated images show our general goal.
  <kbd>
      <img src="images/figma.jpg"  border="2">
  </kbd>

  <kbd>
      <img src="images/figma.jpg"  border="2">
  </kbd>


  
----
# 4. Product Backlog

TODO:
Here you should include a link to your GitHub repo issues page, i.e., your product backlog. Make sure to create an issue for each user story.  

----
# 5. References

Cite your references here.

For the papers you cite give the authors, the title of the article, the journal name, journal volume number, date of publication and inclusive page numbers. Giving only the URL for the journal is not appropriate.

For the websites, give the title, author (if applicable) and the website URL.

