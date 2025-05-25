Project Plan Group 1

Currency Conversion Application

UMGC CMSC 495 Section 6380

Elizabeth Bloss

Jackson Perry

Carl Blocker

Jonah Kiplimo

Table of Contents

Overview..................................................................................................................2

Project
Deliverables...................................................................................................\...2

Project
Scope..............................................................................................................2

Resource
List..............................................................................................................2

Team Member
Roles.....................................................................................................3

Requirements.............................................................................................................3

Case
Scenario.............................................................................................................4

Schedule
Summary.......................................................................................................4

Detailed
Schedule........................................................................................................5

Schedule Update &
Tracking........................................................................\....................6

Communication
Plan....................................................................................................6

Risk
Management........................................................................................................7

OVERVIEW

This project plan will provide a description of group one's currency
conversion web application. It will contain detailed aspects of the
project including deliverables, project scope, team member roles,
requirements, case scenarios, and a project schedule. A communication
plan will also be included to identify the methods in which information
would be shared with stakeholders in a timely manner.

PROJECT DELIVERABLES

The currency conversion web application uses a GUI for users to convert
a monetary amount. Users will input a numeric value, select a base
currency, and select a conversion currency. After the desired values are
input, a 'convert' button may be pressed and the converted numeric value
will be displayed as output. The project will be delivered through a web
application in a container.

.

PROJECT SCOPE

**Project Scope Statement**

Develop a currency conversion web application where the user will enter
information (initial value, base currency, desired conversion currency)
and the converted monetary value will be displayed.

**Project Meeting**

The project meetings are scheduled for each {DAY} at {TIME} from 5/21 to
7/8. During the first meeting, topics such as project design, team
roles, and project goals were discussed.

RESOURCE LIST

Several resources will be utilized by the team to accomplish the task of
creating the website:

1)  Personal computers for programming linux/mac or Windows with
    Docker/WSL

2)  IDE: Vscode

3)  Python 3.12 and venv

4)  Version-controlled software (GitHub repository)

5)  Open source API for conversion rates ( openexchangerates.org)

6)  Internet access (LAN/Wi-Fi is needed)

7)  libraries outlined in requirements.txt

    a.  blinker==1.9.0

    b.  certifi==2025.4.26

    c.  charset-normalizer==3.4.2

    d.  click==8.2.1

    e.  Flask==3.1.1

    f.  idna==3.10

    g.  itsdangerous==2.2.0

    h.  Jinja2==3.1.6

    i.  MarkupSafe==3.0.2

    j.  python-dotenv==1.1.0

    k.  requests==2.32.3

    l.  urllib3==2.4.0

    m.  Werkzeug==3.1.3

TEAM MEMBER ROLES

**Project Manager**

This person is responsible for managing the team and organizing
meetings. They are responsible for contacting the client about any
updates or issues that occur throughout the project. They ensure that
all deadlines are met and requirements are completed. The project
manager for group one is {......\....}

**Programmer**

All team members can work together to ensure the function and logic of
the tools algorithms as well as ensuring performance and safety of the
application. This is to ensure that integration testing is performed as
development happens and acceptance testing is thoroughly completed prior
to delivery with a focus on security and accuracy.

**User Interface Designer**

These individuals are responsible for designing and layout of the
graphical user interface for the project. The frontend of the program
will be developed with HTML/CSS/tailwinds The team members that will
focus on this are {..........}

**Tester**

All team members will serve as testers and complete a rigorous test plan
as outlines by the Project manager. Sufficient assertion within the
codebase is also desired. We will test for functionality and correctness
but also for appropriate error handling and graceful failure

REQUIREMENTS

**Business Requirements**

1.  Allow users to convert one currency to another in near real-time.

-   Support popular global currencies (USD, EUR, GBP, INR, JPY, etc.).

```{=html}
<!-- -->
```
-   Display accurate and up-to-date exchange rates.

```{=html}
<!-- -->
```
-   Ensure easy usability on both desktop and mobile devices.

```{=html}
<!-- -->
```
-   Provide a secure and fast user experience to retain users.

**Functional Requirements**

-   **Currency Selection**: User selects source and target currencies
    > from dropdowns.

```{=html}
<!-- -->
```
-   **Input Field**: User inputs the amount to convert.

```{=html}
<!-- -->
```
-   **Conversion Calculation**: App retrieves current exchange rates and
    > calculates the converted value.

```{=html}
<!-- -->
```
-   **Display Result**: Show converted amount clearly to the user.

```{=html}
<!-- -->
```
-   **Exchange Rate Source**: Integration with a reliable external API
    > (e.g., [OpenExchangeRates](https://openexchangerates.org/)).

```{=html}
<!-- -->
```
-   **Auto-Refresh Rates**: Periodically update exchange rates (e.g.,
    > every 10 mins or on demand).

```{=html}
<!-- -->
```
-   **Currency Symbol and Code Display**: Show symbols (\$, €, ₹) and
    > ISO codes (USD, EUR, INR).

```{=html}
<!-- -->
```
-   **Mobile Responsiveness**: Ensure UI adapts well to various screen
    > sizes.

```{=html}
<!-- -->
```
-   **Error Handling**: Display error messages for invalid inputs or
    > failed API calls.

```{=html}
<!-- -->
```
-   **History (Optional)**: Maintain a list of recent conversions.

```{=html}
<!-- -->
```
-   **Localization (Optional)**: Support multiple languages or regional
    > formats.

**Technical Requirements**

-   **Frontend**:

    -   Language: HTML, CSS

    -   /Tailwind

-   **Backend** (if applicable):

    -   Language: Python (Flask)

    -   Use server-side code to call external currency exchange API

-   **API Integration**:

    -   Must fetch exchange rates from a real-time API.

    -   Handle rate limits and API key security

-   **Performance**:

    -   Fast load times (\<2s on average internet)

    -   Minimized API calls (cache responses where possible)

-   **Security**:

    -   Secure API keys (never expose them in frontend)

    -   HTTPS for all data transmission

    -   Input validation to prevent injection or malicious input

-   **Hosting/Deployment**:

    -   Use GitHub for version control

-   **Browser Compatibility**:

    -   Should work across major browsers (Chrome, Firefox, Safari,
        > Edge)

CASE SCENARIO

**User Journey:**

**1. Launching the Application**

-   The user opens the app and lands on the Welcome Screen.

-   The screen displays a main menu with the following options:

```{=html}
<!-- -->
```
-   Currency Converter

-   Conversion History

-   Exit

    **2. Currency Conversion**

-   The user selects the \"Currency Converter\" button.

-   The Currency Converter screen opens.

-   They are presented with a clean Tailwind-styled form that includes:

-   Input field to enter the amount (e.g., 100)

-   Dropdown to select source currency (e.g., USD)

-   Dropdown to select target currency (e.g., EUR)

-   A "Convert" button

-   The user enters the value 100, selects USD as the source and EUR as
    the target, and clicks \"Convert\".

-   The converted amount appears below the form:

-   100 USD = 92.34 EUR (check via Api for correct rate at test time)

-   The conversion is saved in the backend session as history.

-   The user clicks \"Exit\" to return to the main menu.

    **3. Conversion History**

-   From the main menu, the user selects \"Conversion History\".

-   A panel opens showing the last three conversions made in the current
    session:

    -   100 USD → 92.34 EUR

    -   50 GBP → 63.12 USD

    -   200 JPY → 1.30 EUR

-   The user can click \"Print History\" to export the session log to
    PDF or print using a local printer.

-   The user returns to the main menu and selects \"Exit\" to close the
    app.

**4. Error Handling Scenarios:**

-   Invalid Input -- Amount

-   User enters a non-numeric amount (e.g., \"ten\")

-   The system shows a Tailwind-styled error banner:

-   Please enter a valid numeric amount.

-   Invalid Currency Selection

-   User enters a manually typed currency code not in the dropdown
    (e.g., XYZ).

-   Error message appears:

-   XYZ\' is not a supported currency code.

-   Empty Field Submission

-   User clicks \"Convert\" without filling all fields.

-   Red outlines appear on missing fields with a message:

-   All fields are required to perform the conversion.

-   API Failure / No Internet

-   If the exchange rate API is down or there's no internet:

-   Unable to retrieve exchange rates. Please try again later.

**Success Criteria:**

-   User can complete at least 3 conversions in one session.

-   Conversions are saved temporarily in session memory.

-   Tailwind ensures responsive layout on all devices.

-   User receives clear error messages for all input errors.

SCHEDULE SUMMARY

**Currency Conversion Application -- Development Schedule with
Milestones**

**(CMSC 495: Group 1 Project, Summer 2025)**

  ------------------------------------------------------------------------
  **Phase**       **May**       **June**                     **July**
  --------------- ------------- ---------------------------- -------------

  ------------------------------------------------------------------------

Detail Target End

W T F S S M T W T F S S M T W T F S S M T W T F S S M T W T F S S M T W
T F S S M T W T F S S M T W T F S S M T

  --------------------------------------------------------------------------------
  **Meet      5/21/25                                                       
  Team**                                                                    
  ----------- --------- ------- ------ ------- ------- ------ ------ ------ ------
  **Project   5/27/25                                                       
  Plan**                                                                    

  **Project   6/3/25                                                        
  Design**                                                                  

  **Phase I   6/10/25                                                       
  Build**                                                                   

  **Test      6/17/25                                                       
  Plan**                                                                    

  **Phase II  6/24/25                                                       
  Build**                                                                   

  **User      7/1/25                                                        
  Guide**                                                                   

  **Final     7/8/25                                                        
  Report**                                                                  
  --------------------------------------------------------------------------------

DETAILED SCHEDULE

**Target Start Target End**

**Meet Team:** 05/14/25 05/21/25

Discuss Roles 05/21/25

Communication Plans 05/21/25

Discuss Project Options 05/21/25

**Project Plan:** 05/21/25 05/27/25

Allocate Roles 05/27/25

Discuss Requirements 05/24/25

**Project Design:** 05/27/25 06/03/25

Config File Load 06/03/25

Backend coding 06/02/25

Frontend coding 06/02/25

**Phase I Build:** 05/30/25 06/10/25

Config File Load 06/09/25

Backend development 06/09/25

**Test Plan:** 06/10/25 06/17/25

Indiv Test Plans 06/15/25

First Draft (Test Plans) 06/12/25

Final Draft (Test Plans) 06/16/25

**Phase II Build:** 06/03/25 06/24/25

User UI 06/23/25

**User Guide:** 06/25/25 07/01/25

Indiv User Guides 06/30/25

First Draft (User Guide) 06/27/25

Final Draft (User Guide) 06/30/25

**Final Report:** 06/17/25 07/08/25

Compile Report 07/07/25

Presentation 07/07/25

SCHEDULE UPDATE & TRACKING

**Currency Conversion Application -- Development Schedule with
Milestones**

**(CMSC 495: Group 1 Project, Summer 2025)**

  ------------------------------------------------------------------------
  **Phase**       **May**       **June**                     **July**
  --------------- ------------- ---------------------------- -------------

  ------------------------------------------------------------------------

Detail Target End

W T F S S M T W T F S S M T W T F S S M T W T F S S M T W T F S S M T W
T F S S M T W T F S S M T W T F S S M T

  -----------------------------------------------------------------------------------
  **Meet      5/21/25   COMPLETE                                               
  Team**                                                                       
  ----------- --------- ---------- ------ ------- ------- ------ ------ ------ ------
  **Project   5/27/25                                                          
  Plan**                                                                       

  **Project   6/3/25                                                           
  Design**                                                                     

  **Phase I   6/10/25                                                          
  Build**                                                                      

  **Test      6/17/25                                                          
  Plan**                                                                       

  **Phase II  6/24/25                                                          
  Build**                                                                      

  **User      7/1/25                                                           
  Guide**                                                                      

  **Final     7/8/25                                                           
  Report**                                                                     
  -----------------------------------------------------------------------------------

COMMUNICATION PLAN

Team members will communicate via the LEO "Group 1 Members Only"
discussion group and daily through Discord. Group members will also
manage version control via a GitHub repository "CMSC495" created by
Jackson Perry.

+--------------+------------+-------------+-------------+-------------+
|              |            | **CONTACT   |             |             |
|              |            | LIST**      |             |             |
+==============+============+=============+=============+=============+
| **Name**     | **Org**    | **Role**    | **Discord** | **GitHub**  |
+--------------+------------+-------------+-------------+-------------+
| Elizabeth    | UMGC       | XXX         | E_Bloss     | erbloss     |
| Bloss        |            |             |             |             |
|              | CMSC 495   |             |             |             |
+--------------+------------+-------------+-------------+-------------+
| Jackson      | UMGC       | XXX         | ja          | ja          |
| Perry        |            |             | ckson1982\_ | ckson-perry |
|              | CMSC 495   |             |             |             |
+--------------+------------+-------------+-------------+-------------+
| Carl Blocker | UMGC       | XXX         | Cblock11    |             |
|              |            |             |             |             |
|              | CMSC 495   |             |             |             |
+--------------+------------+-------------+-------------+-------------+
| Jonah        | UMGC       | XXX         | lymore_afk  | lymore-afk  |
| Kiplimo      |            |             |             |             |
|              | CMSC 495   |             |             |             |
+--------------+------------+-------------+-------------+-------------+
| Hung Dao     | UMGC       | Instructor  | N/A         | N/A         |
|              |            |             |             |             |
|              | CMSC 495   |             |             |             |
+--------------+------------+-------------+-------------+-------------+

RISK MANAGEMENT

There can be several risk factors that may result in project delays or
that could affect the overall efficiency of the program. Some of the
risks that can be anticipated are:

-   Team Availability

    -   We may fall behind due to scheduling conflicts if we are unable
        to consistently meet and discuss the development of the project

    -   To resolve this issue, we will predetermine a set time for
        weekly communication where we will discuss what we have
        accomplished and what needs to be done. There will also be an
        ongoing chat forum via Discord

-   Teamwork

    -   Team collaboration in computer science is a new territory for
        some in the group. Members will learn to work together in a
        virtually remote setting and use version control software
        (GitHub) to submit a cohesive program.

-   Unfamiliarity with specific programming languages

    -   There are some members that may be more familiar with the
        languages chosen to create the program. Each of us is expected
        to familiarize ourselves with the languages that we will be
        using so that we are better prepared to contribute to the group.
        Open and respectful communication among members will enable us
        all to grow as programmers.
