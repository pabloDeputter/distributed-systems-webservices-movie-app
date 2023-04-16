# Movies API Manual
#### By Pablo Deputter - s0205440

## Manual
The API and webpage can be launched using the bash script ```run.sh```. This will prompt you to either input 'prod' or 'dev'. Enter 'dev'.
This script will launch the API and the webpage on the following ports:`5000` and `5177`.
The API can be accessed at `http://localhost:5000/` and the webpage at `http://localhost:5177/`. The script will
also create a virtual environment and install all the required packages for the API and webpage. The API documentation 
can be accessed at `http://localhost:5000/docs/`. All the endpoints are prefixed with `/api`.

## Design Considerations of the Movies API

I used the package Flask-Restx since it came with Swagger UI which was easy to use and I could easily add the documentation to the API.
Some API endpoints such as the `movie/similar-runtime`, ... can also be provided with a `page`and `per_page` query parameter to paginate the results, but this isn't 
completely implemented since you specified in the mail that this wasn't necessary.
The webpage was built using Vue since I find it very easy to use and it is a framework that I am familiar with. As I said earlier the API can be accessed at `http://localhost:5000/docs`.

The API has been designed to follow the principles of the REST architecture:
* Uses standard HTTP method to interact with resources such as GET, POST and DELETE. For example, GET is used to retrieve information about a movie, POST is used to add a movie to a user's favorites list, and DELETE is used to remove a movie from the system.
* Each request to the API is independent and contains all the information necessary to complete the request. This makes the API scalable and stateless.

* Resource-based URLs are used to identify and access resources. For example, `/movie/{movie_id}` is used to retrieve details about a specific movie.

* All data returned from the API is in JSON format, which is widely used and easy to parse. For endpoints that return multiple results such as `/movie/similar-runtime` the results are encapsulated withing a `data` property.

* The API provides standard error messages in case of failed requests, such as "404 Resource not found" and "401 Authentication failed". This makes it easy to quickly determine errors and resolve issues.

* The API uses query parameters for optional parameters.

* The API provides a consistent response structure for all endpoints, which includes a "data" property that contains the requested data and a "status" property that contains the HTTP status code and any relevant messages.


So we can conclude that the API has been design with the REST principles in mind to provide a scalable and consistent API.