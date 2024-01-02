import streamlit as st
import pandas as pd
import template as t
import itertools
import random

st.set_page_config(layout="wide")

st.subheader('Group Members of This Project')
group_members_data = {
    'Name': ['Kaleb Alebachew', 'Natnael Malike', 'Kalkidan Tadesse', 'Mikiyas Mesfin', 'Tewodros Million']
}
group_members_table = st.table(group_members_data)

# load the dataset with the books
df_books = pd.read_csv('data/BX-Books.csv', sep=';', encoding='latin-1')
df_books_ratings = pd.read_csv('data/BX-Book-Ratings-Subset.csv', sep=';', encoding='latin-1')
df_users = pd.read_csv('data/BX-Users.csv', sep=';', encoding='latin-1')

# Initialize session_state if not present
if 'ISBN' not in st.session_state:
    st.session_state['ISBN'] = '0385486804'

# select a user to kickstart
if 'User-ID' not in st.session_state:
  st.session_state['User-ID'] = 98783	

# fill the friends list to start the recommendations
if 'Friends' not in st.session_state:
  st.session_state['Friends'] = [277427, 278026, 277523, 276680]


# initializations
friends_list = [277427, 278026, 277523, 276680]
df_book = df_books[df_books['ISBN'] == st.session_state['ISBN']]
dict_isbn_groups = df_books_ratings.groupby(['ISBN'])['User-ID'].aggregate(lambda x: list(x))

def jaccard_distance(user_ids_isbn_a, user_ids_isbn_b):
                
    set_isbn_a = set(user_ids_isbn_a)
    set_isbn_b = set(user_ids_isbn_b)
    
    union = set_isbn_a.union(set_isbn_b)
    intersection = set_isbn_a.intersection(set_isbn_b)
        
    return len(intersection) / float(len(union))

# create a cover and info column to display the selected book
cover, info = st.columns([2, 3])

with cover:
  # display the image
  st.image(df_book['Image-URL-L'].iloc[0])

with info:
  # display the book information
  st.title(df_book['Book-Title'].iloc[0])
  st.markdown(df_book['Book-Author'].iloc[0])
  st.caption(str(df_book['Year-Of-Publication'].iloc[0]) + ' | ' + df_book['Publisher'].iloc[0])

st.subheader('Keep digging your favorite authors')
userid = st.session_state['User-ID']
df = df_books_ratings[df_books_ratings['User-ID'] == userid]
df = df.merge(df_books, on='ISBN')
authors = df['Book-Author'].unique()
titles = df['Book-Title']
rs = df_books[df_books['Book-Author'].isin(authors) & ~df_books['Book-Title'].isin(titles)]
rs = rs.sample(10)
print(rs)
t.recommendations(rs)

st.subheader('Trending among your friends')
friends = st.session_state['Friends']
df = df_books_ratings[df_books_ratings['User-ID'].isin(friends)]
df = df.merge(df_books, on='ISBN')
rs = df.drop_duplicates(subset=['Book-Title'])
rs = rs.sample(10)
print(rs)
t.recommendations(rs)

st.subheader('People with common interests read' , st.session_state['ISBN'])
isbn = st.session_state['ISBN'] 
dict_isbn_groups = df_books_ratings.groupby(['ISBN'])['User-ID'].aggregate(lambda x: list(x)) # create the dictionary
title = df_books[df_books['ISBN']==isbn]['Book-Title'].values
diff_editions = df_books[((df_books['Book-Title'].isin(title)) & (df_books['ISBN']!=isbn))]['ISBN'].values  # find for different editions of the same book
flag = False
if isbn in(dict_isbn_groups.keys()): # if our isbn is in our dict continue
  pass
else:   # if not try the other editions
  for i in range(len(diff_editions)):
      if diff_editions[i] in(dict_isbn_groups.keys()):
          isbn = diff_editions[i]
          flag  = True
  if flag == False:  # if there aren't any other editions, choose a random 
      isbn = random.choice(list(dict_isbn_groups.keys()))

lst = []
for book, users in dict_isbn_groups.items():
    d = jaccard_distance(dict_isbn_groups[isbn], users)
    if book != isbn and d > 0.0 and d < 0.8:
        d = jaccard_distance(dict_isbn_groups[isbn], users)
        lst.append([book, d])

jaccard = pd.DataFrame(lst, columns=['ISBN', 'Jaccard Distance'])
jaccard = jaccard.sort_values(by="Jaccard Distance", ascending=False).head(10)
rs = df_books[df_books['ISBN'].isin(jaccard['ISBN'])]
df = rs.head(10)
print(df)
t.recommendations(df)



# Define the sidebar buttons / text inputs
userid = st.sidebar.text_input("User-ID", placeholder="Currently logged in as user: 98783")
log_in_clicked = st.sidebar.button("Log In")
if log_in_clicked:
  if userid.isdigit() and int(userid) in df_books_ratings['User-ID'].unique():
    t.select_user(int(userid))
  elif userid.isdigit() and int(userid) in df_users['User-ID'].unique():
    t.welcome_user()
  else:
    t.wrong_credentials()

friendid = st.sidebar.text_input("Let's find your friends!", placeholder="[277427, 278026, 277523, 276680]")
add_clicked = st.sidebar.button("Add")
if add_clicked:
  if friendid.isdigit() and int(friendid) in friends_list:
    t.already_added()
  elif friendid.isdigit() and int(friendid) in df_books_ratings['User-ID'].unique():
    friends_list.append(friendid)
    t.add_friend(int(friends_list))
  else:
    t.friend_not_found()