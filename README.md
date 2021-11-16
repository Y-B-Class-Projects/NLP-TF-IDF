In this project we went through hundreds of articles in Hebrew from the news site [walla.co.il](http://walla.co.il "walla.co.il") and through NLP we searched for articles that matched the query we defined in advance.
We used the **TF-IDF** method to find distances between the articles and the query.
The distances between the Marmots were calculated using three different distance functions:
- Cosine distance
- Euclidean distance
- Jaccard distance

The query used in the run is "קרונה COVID חיסונים מחלימים חיסון שלישי בוסטר מתחסנים הקורונה מחלה בדיקות סגר חולים"

Top results of the three distance functions:

│ file                        │cosine distances│
│ data\2934404.txt │           0.671822 │<br />
│ data\2919869.txt │           0.729147 │<br />
│ data\2795571.txt │           0.729724 │<br />
│ data\2788711.txt │           0.730278 │<br />
│ data\2672932.txt │           0.732511 │<br />
│ data\2930070.txt │           0.744248 │<br />
│ data\2920501.txt │           0.745138 │<br />
│ data\2752677.txt │           0.749246 │<br />
│ data\3025567.txt │           0.756526 │<br />
│ data\2686327.txt │           0.763186 │<br />

------------


│ file             │   euclidean distances │<br />
│ data\2612943.txt │               60.7065 │<br />
│ data\2617199.txt │               60.7065 │<br />
│ data\2617945.txt │               60.7065 │<br />
│ data\2624898.txt │               60.7065 │<br />
│ data\2674495.txt │               60.7065 │<br />
│ data\2674793.txt │               60.7065 │<br />
│ data\2676337.txt │               60.7065 │<br />
│ data\2677887.txt │               60.7065 │<br />
│ data\2682157.txt │               60.7065 │<br />
│ data\2682875.txt │               60.7065 │<br />

------------


│ file             │   jaccard distances │<br />
│ data\2628358.txt │           0.00047619  │<br />
│ data\2695054.txt │           0.0004914   │<br />
│ data\2953739.txt │           0.0005      │<br />
│ data\2841717.txt │           0.000530223 │<br />
│ data\2743524.txt │           0.000536769 │<br />
│ data\3004443.txt │           0.000547345 │<br />
│ data\2834335.txt │           0.000548246 │<br />
│ data\2843278.txt │           0.000548246 │<br />
│ data\2731211.txt │           0.000553403 │<br />
│ data\2897353.txt │           0.000560852 │<br />
