
<img src="https://github.com/lilliemadali/soccerstreets/blob/master/Trip-Goalie-Logo-with-tag.png" height="150">
######
[Live Project](http://#)   |  [Overview](https://github.com/SoccerStreets/soccerstreets#overview)   |   [Team Members](https://github.com/SoccerStreets/soccerstreets#team-members)   |   [What We Used](https://github.com/SoccerStreets/soccerstreets#what-we-used)   |   [MVP](https://github.com/SoccerStreets/soccerstreets#mvp-minimum-viable-product)   |   [Challenges](https://github.com/SoccerStreets/soccerstreets#challenges--solutions)   |   [Code](https://github.com/SoccerStreets/soccerstreets#code-snippets)   | [Screenshots](https://github.com/SoccerStreets/soccerstreets#screenshots)   |   [Contributing](https://github.com/SoccerStreets/soccerstreets#contribute-to-trip-goalie)

> How can we create a safe, worry-free riding experience for youth and parents?

##Overview:
TRIP GOALIE seeks to connect youth, parents/guardians, and chaperones via a web app that notifies and verifies youth arrival and departure. Youth, parents/guardians, and chaperones will register and create a profile which contains their name, contact information, photo, their associated youth (if it is a parent profile), and a username and password. Parents/guardians identify the pick up point (rail station) where they will drop off their youth. The chaperone assigned to the rail station will receive a list of youth to escort on the train. Once the youth arrive at the pick up point, the chaperone verifies that they are en route. The chaperone sends another notification of the youth's arrival at the destination site. The notification process begins again as the youth head back home.

####User Story
Shelly is a mother who would like to ensure the safe departure and arrival of her child. Her child is very active, loves soccer and is aged 6 to 16 years old. She would like to have a chaperone ride with her child and their friends. She would like to know that they met their chaperone and arrived at their location safely.

####Our Core Outcomes:
* Increased user experience of parents who are concerned with youth safety
* Increased ridership of youth ages 9 to 17


##Github Link:
https://github.com/SoccerStreets/soccerstreets

##Team Members:
* Lillie Madali, project manager
* Candace Bazemore, marketing and graphic design
* Lisa Copeland, user experience design
* Kaushik Visvanathan, front-end web developer
* Keyur Patel, back-end web developer
* Andrew Hill, back-end web developer
* Jesslyn Landgren, full-stack developer

##What We Used:
####Languages:
* Python
* HTML5
* CSS
* JavaScript

####Frameworks:
* Flask
* Jinja
* Bootstrap

####Other:

##Minimum Viable Product ("MVP"):
After mapping out the process, the team decided on an MVP. One challenge we faced was prioritizing our MVP and stretch goals within the time constraint of a 24-hour hackathon.  

####Initial MVP
* User authentication
* Profiles (youth, parents, chaperones)
* Photo upload 
* QR code for checking-in
* Send notifications of arrival, successful drop-off, and alerts


####Stretch Goals
* Real-time tracking of youth with travelling icons


##Challenges & Solutions:
####Some of the biggest challenges we faced with this project build included:
* Challenge: Implementing the QR scanner was challenging as the QR scanner codes that were available did not actually do what we wanted to do.
* Solution: The team implemented a work-around for the QR scanner by creating an ID for the parent and the child.

##Code Snippets
####Parent Registration
```
    <div class="container-fluid">
      <form action="/submit_register" method="POST">

        <label><b>I am a: </b></label>

        <label class="radio-inline">
          <input type="radio" id="ChaperoneRadio" name="optradio" value="chaperone">Chaperone
        </label>

        <label class="radio-inline">
          <input id="ParentRadio" type="radio" name="optradio" value="parent">Parent
        </label>

        <label class="radio-inline">
          <input type="radio" name="optradio" value="kid">Kid
        </label>

        <div class="container">
          <!-- <label><b>First Name</b></label> -->
          <input type="text" placeholder="First Name" name="fname" required>

          <!-- <label><b>Last Name</b></label> -->
          <input type="text" placeholder="Last Name" name="lname" required>

          <!-- <label><b>Phone Number</b></label> -->
          <input type="text" placeholder="Phone Number" name="phone" required>

          <!-- <label><b>Marta Station</b></label> -->
          <input class ="Station" type="text" placeholder="Nearest Marta Station" name="station" required>
```

##Screenshots
<img src="#">

##Future State
<img src="#">
