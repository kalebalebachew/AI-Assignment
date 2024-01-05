import numpy as np
import pandas as pd

books = pd.read_csv("data/BX_Books.csv", encoding='latin-1', error_bad_lines=False, sep=';')
ratings = pd.read_csv("data/BX-Book-Ratings.csv", encoding='latin-1', error_bad_lines=False, sep=';')


books.columns = ['ISBN', 'bookTitle', 'bookAuthor', 'yearOfPublication', 'publisher', 'imageUrlS', 'imageUrlM', 'imageUrlL']

ratings.columns = ['userID', 'ISBN', 'bookRating']

ratings = ratings.set_index("ISBN")

books = books.set_index("ISBN")

books.head()

ratings.tail()



def array_distance(a,b):
  return np.linalg.norm(a - b)

# Testing function

a=np.array([3, 4, 5, 3, 2, 4])
b = np.array([4, 4, 4, 3, 2, 2])

array_distance(a, b)


def ratings_from_user(userID):
  ratings_from_user = ratings.query("userID==%d" % userID)
  ratings_from_user = ratings_from_user[["bookRating"]]
  return ratings_from_user

#Testing
ratings_from_user(276704)


distance_test = ratings_from_user(276729).join(ratings_from_user(276729), rsuffix="_A", lsuffix="_B")

array_distance(distance_test["bookRating_B"], distance_test['bookRating_A'])



def distance_between_users(user1:int, user2:int): 
  ratings_from_user1 = ratings_from_user(user1)
  ratings_from_user2 = ratings_from_user(user2)


 
  both_ratings = ratings_from_user1.join(ratings_from_user2, lsuffix="_A", rsuffix="_B").dropna()

  
  distance = array_distance(both_ratings["bookRating_A"], both_ratings["bookRating_B"])

  return [user1, user2, distance]


distance_between_users(276729, 276704)



print ("We have %d users" %len(ratings["userID"].unique()))

def distance_from_all(targetID:int):
  all_users = ratings["userID"].unique()[:3000] 

  distances = [distance_between_users(targetID, users) for users in all_users]

  distances = pd.DataFrame(distances, columns = ["targetID", "otherUserID", "distance"])

  return distances.set_index("otherUserID").sort_values("distance").query("distance>0")

distance_from_all(276704)


def suggest_to(userID:int):
  
  similar_users = distance_from_all(userID).head(3)
  similar_users_list = similar_users.index
  
  ratings_from_similar_users = ratings[ratings["userID"].isin(similar_users_list)]

  suggestions = ratings_from_similar_users.groupby("ISBN").mean()[["bookRating"]]
  suggestions = suggestions.sort_values("bookRating", ascending=False)

  

  return suggestions.join(books[["bookTitle", "bookAuthor", "yearOfPublication"]])

suggest_to(276704)




