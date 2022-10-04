#!/usr/bin/env python
# coding: utf-8

# Hacker News Comment Comparison
# 
# Here we will run a program that compares the different scores of posts on Hacker News.

# In[1]:


#Import File, Print First 5 Rows
from csv import reader

opened_file = open('hacker_news.csv', encoding = 'UTF-8')
read_file = reader(opened_file)
hn = list(read_file)

print(hn[:5])


# In[2]:


#Extract Headers
header = hn[:1]
data_set = hn[1:]

# Simple exploratory data query
print("Headers:")
print(header)
print('\n')
print("Sample Data:")
for row in hn[1:6]:
    print(row)
    print('\n')
    
print('Number of rows:', len(hn))


# In[3]:


# Lists that will store our three categories of posts
ask_posts = []
show_posts = []
other_posts = []

#Seperating the data into 3 lists
for row in hn:
    title = row[1]
    title = title.lower()
    if title.startswith('ask hn') is True:
        ask_posts.append(row)
    if title.startswith('show hn') is True:
        show_posts.append(row)
    else:
        other_posts.append(row)
        
print("Number of Ask Posts = ",len( ask_posts))
print(ask_posts[:5])
print('\n')

print("Number of Show Posts = ",len( show_posts))
print(show_posts[:5])
print('\n')

print("Number of Other Posts = ",len( other_posts))
print(other_posts[:5])
print('\n')


# In[4]:


#Calculating the average number of comments for each post list
#Ask posts
total_ask_comments = 0

for row in ask_posts:
    num_comments = row[4]
    num_comments = int(num_comments)
    total_ask_comments += num_comments

avg_ask_comments = total_ask_comments / len(ask_posts)

print('Total Number of comments in ask posts = ',total_ask_comments)
print('Number of ask posts = ', len(ask_posts))
print('The average number of comments in ask posts is', avg_ask_comments)
print('\n')

#Show posts
total_show_comments = 0

for row in show_posts:
    num_comments = row[4]
    num_comments = int(num_comments)
    total_show_comments += num_comments

avg_show_comments = total_show_comments / len(show_posts)

print('Total Number of show comments = ',total_show_comments)
print('Number of show posts = ', len(show_posts))
print('The average number of comments in show posts is', avg_show_comments)
print('\n')


# It appears that the average number of comments in the ask posts is greater than and the show post.

# In[5]:


import datetime as dt

# Creates counts for post/hr and comments OR points per hr with any dataset
def count_posts_hour(dataset, post_type, metric, show=False):
    # Allows user to select metric of success as comments or points
    if metric == "comments":
        index = 4
    elif metric == "points":
        index = 3
        
    # isolating the columns we need (time created and comments/posts)
    result_list = []
    for row in dataset:
        created_at = row[6]
        num_metric = int(row[index])
        result_list.append([created_at, num_metric])
    
    # populate metrics by hour in dictionaries via iterating through results_list
    counts_by_hour = {}
    metric_by_hour = {}    

    date_format = '%m/%d/%Y %H:%M' # example format for str: '11/22/2015 13:43'
    
    for row in result_list:
        temp_metric = row[1]
        created_at_str = row[0]
        created_at_dt = dt.datetime.strptime(created_at_str, date_format)
        hour = created_at_dt.strftime('%H')
        if hour not in counts_by_hour:
            counts_by_hour[hour] = 1
            metric_by_hour[hour] = temp_metric
        else:
            counts_by_hour[hour] += 1
            metric_by_hour[hour] += temp_metric
    
    # print summaries for posts/hr and points/comments per hr only if 'show'=True
    # 'show' = False by default. This is primarily for demonstration.
    if show == True:
        print('For {} Posts:'.format(post_type))
        print('Frequency table of posts per hour')
        print(counts_by_hour)
        print('\n')
        print('Number of {} asks posts created at each hour received:'.format(metric))
        print(metric_by_hour)
    return counts_by_hour, metric_by_hour


# In[6]:


ask_counts_by_hour, ask_comments_by_hour = count_posts_hour(ask_posts, 'Ask HN', 'comments', show=True)


# In[7]:


# calculates average comments or posts per hour. Not ordered.
def average_metric_by_hour(counts_by_hour, metric_by_hour, show=False):
    avg_by_hour = []
    for key in counts_by_hour:
        avg = (metric_by_hour[key]/counts_by_hour[key])
        avg_by_hour.append([key, avg])
    
    if show == True:    # default, we do not need to show this, but display lines for demo
        for row in avg_by_hour:    #using a for loop for easier readability
            print(row)

    return avg_by_hour


# In[8]:


# 'show' argument = True for the sake of demonstration
ask_avg_by_hour = average_metric_by_hour(ask_counts_by_hour, ask_comments_by_hour, show=True)


# In[9]:


# Builds on average_metric_by_hour by sorting to find top 5 and bottom 5 hours for success metric
def sort_avg_by_hour(avg_by_hour, post_type, metric):
    
    swap_avg_by_hour = []
    for row in avg_by_hour:
        swap_avg_by_hour.append([row[1],row[0]])
    
    # Sort in highest to lowest to find best hours
    sorted_swap = sorted(swap_avg_by_hour, reverse=True)
    print('Top 5 Hours for {} Posts {}'.format(post_type, metric))
    show_sorted(sorted_swap, metric)
    
    # Sort in lowest to highest to find worst hours
    sorted_swap_bottom = sorted(swap_avg_by_hour, reverse=False)
    print('\n')
    print('Bottom 5 Hours for {} Posts {}'.format(post_type, metric))
    show_sorted(sorted_swap_bottom, metric)

# Sub function to display first 5 rows in specified format
def show_sorted(sorted_swap, metric):
    str_format = "{hr}: {avg:.2f} average {m} per post"
    
    for row in sorted_swap[:5]:
        hour = dt.datetime.strptime(row[1], '%H')
        hour_str = hour.strftime("%H:%M")
        average = row[0]
        print(str_format.format(hr=hour_str, avg=average, m=metric))


# In[10]:


sort_avg_by_hour(ask_avg_by_hour, 'Ask HN', 'comments')

