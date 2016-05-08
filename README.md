<h1 align="center">Recommender-System-using-Item-Based-Collaborative-Filtering</h1>
The main aim of this project was to implement an item-based collaborative filtering recommender system for a given user using Pearson Correlation and Prediction equations.

The input file ratings-dataset.tsv contains UserId, Mover rating and Movie title. Based on the information of all users, the ratings for movies that a given user has not rated is calculated and based on this information, the movies are recommended that the user would most probably like. 

###Item Based Collaborative Filtering
<strong>Format of data file for item</strong>

The input data file is in the form of Tab separated value - <em>ratings-dataset.tsv</em>. The file consists of one rating event per line. Each rating event is of the form:

<em>User_id\tRating\tMovie_title</em>

The User_id is a string that contains only alphanumeric characters with hyphens or spaces (no tabs). The rating is one of the float values 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, and 5.0 The Movie_title is a string . The three fields -- User_id, rating, and the Movie_title -- are separated by a single tab character (\t).

<strong>Running the code: 

<em>python nayak_nandan_collabFilter.py (ratings-dataset.tsv) (user) (n) (k)</em></strong>

The program takes 4 arguments:

1. <em>ratings-dataset.tsv</em>: The name of the ratings file.
 
2. <em>user</em>: The id of the user (string) for whom you should make recommendations.
 
3. <em>n</em>: The size of the neighborhood N to be used in the prediction equation.

4. <em>k</em>: The number of recommendations that should be made for the specified user.

<strong>Output of the program</strong>

The program outputs ‘k’ recommended movies for the user specified in the input parameter and the predicted rating (rounded up to 5 decimal places) for each of those movies. The output is sorted in descending order of the predicted ratings. In case the ratings are same for two movies, they are sorted ascendingly by name. 

<strong>To test the code, you can run:</strong>

<strong><em> nayak_nandan_collabFilter.py ratings-dataset.tsv Kluver 20 5</em></strong>

<strong>Sample Output:</strong>

<em>
Eternal Sunshine of the Spotless Mind 4.19946

Kill Bill: Vol. 2 4.19182

Kill Bill: Vol. 1 4.17114

Erin Brockovich 4.16667

Sin City 4.16667
</em>


<strong>Program Description</strong>
<ol>
<strong><li>Finding Item Similarity</li></strong>

The ratings file is read and the similarity between all pairs of items is computed using the Pearson correlation equation as mentioned below:
<p align="center">
<img src="https://github.com/NandanNayak/Recommender-System-using-Item-Based-Collaborative-Filtering/blob/edits/Pic1.png" />
</p>
•	Sum over set of users U who rated both items i, j.

•	ru,i is rating of user u on item i

•	ri is average rating of i-th item by those users.

Sometimes there is not enough data to compute the similarity between two items. In the worst case -- for example, if only one user rated both items -- the denominator in the formula will be zero. In such cases, the similarity function just returns 0.0.


<strong><li>Ratings Prediction</li></strong>

Using the prediction equation, the rating of a user ‘U’ on an item ‘i’ that the user has not already rated is predicted:

<p align="center">
<img src="https://github.com/NandanNayak/Recommender-System-using-Item-Based-Collaborative-Filtering/blob/edits/Pic2.png" />
</p>
 
 If there are fewer than N items with nonzero similarity to item i, then the similarity function returns a prediction of 0.0.
 
<p align="center">
<img src="https://github.com/NandanNayak/Recommender-System-using-Item-Based-Collaborative-Filtering/blob/edits/Pic3.png" />
</p>
 
The program outputs a list of ‘k’ items to recommend to the user specified as an input argument. The k items with the highest predicted rating for this user is identified. 
</ol>
