#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import time
import pandas as pd
import operator
import subprocess
import sys

def install(package):
    #install a module 
    #Reference https://www.activestate.com/resources/quick-reads/how-to-install-python-packages-using-a-script/

    subprocess.check_call([sys.executable, "-m", "pip", "install", package])  

try:
    # try to import fuzzywuzzy
    from fuzzywuzzy import fuzz
    
except ModuleNotFoundError:
    #if not installed then install 
    install('fuzzywuzzy')
    from fuzzywuzzy import fuzz
    
    
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#List of data (City, month and WeekName)
list_city=['chicago', 'new york city', 'washington']
list_month=['january', 'february', 'march', 'april', 'may', 'june','all']
list_week_name=['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all'] 


def choice(prompt, choices=('yes', 'no')):
    """Return a valid input from the user given an array of possible answers.
    """

    while True:
        choice = input(prompt).lower()
        if choice in choices:
            break
        prompt = ("\nInvalid Response.Please choise again!\n")
    return choice


def similarity(input_data,data_list):
    #This function checks the similarity ratio between the input  and  our data list
    #Reference https://towardsdatascience.com/fuzzy-string-matching-in-python-68f240d910fe
    input_data=input_data.lower()
    ratio={}
    
    #ratio calculation 
    for i in data_list:
        r=fuzz.ratio(input_data,i.lower())
        ratio[i]=r
    most_r=max(ratio.items(),key=operator.itemgetter(1))[0]
    
    if ratio[most_r] == 100:
        return (input_data,most_r,'exact')
    elif ratio[most_r] < 50:
        return (input_data,most_r,'no found')
    else:
        return (input_data,most_r,'similar')


def check(data):   
    if data[2]=='exact':
        return data[1]
    elif data[2]=='similar':
        i=choice('Do you mean \'{}\' ? Enter yes or no\n'.format(data[1].title()))
        if i=='yes':
            return data[1]
        else:
            print('\nInvalid Response.Please choise again!\n ')
    else:
        print('\nInvalid Response.Please choise again!\n ')
        return None   


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello!Let\'s explore some US bikeshare data!\n')
    city=None
    month=None
    day=None
    while True:
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        while city == None:
            city=input('Please enter a city (chicago, new york city, washington):')
            city_sim=similarity(city,list_city)
            city=check(city_sim)

        # get user input for month (all, january, february, ... , june)
        while month==None:
            month=input('\nwhich month?(january,february,march,april or all(for all months)): ')
            month_sim=similarity(month,list_month)
            month=check(month_sim)
        # get user input for day of week (all, monday, tuesday, ... sunday)
        while day==None:
            day=input('\nwhich day?(monday, tuesday, wednesday, thursday, friday, saturday, sunday or all(for all days)): ')
            day_sim=similarity(day,list_week_name)
            day=check(day_sim) 
        # confirm the user input
        confirm = choice("\nPlease confirm that you would like to apply "
                                  "the following filter to the bikeshare data."
                                  "\n\n City: {}\n Month: {}\n Weekday"
                                  ": {}\n\nEnter yes or no.\n>"
                                  .format(city, month, day ))
        if confirm.lower() == 'yes':
            break
        else:
            city=None
            month=None
            day=None
            print("\nLet's try this again!")
    print('-'*40)
    return city,month,day    


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df=pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Week_day']=df['Start Time'].dt.day_name()
    
    # filter by day of week if applicable
    if day!='all':
         # filter by day of week to create the new dataframe
        df=df[df['Week_day']==day.title()]
    
    # filter by month if applicable
    if month!='all':
        # use the index of the months list to get the corresponding int
        month = list_month.index(month) + 1
        # filter by month to create the new dataframe
        df=df[df['Month']==month]
    
    return df


def time_stats(df,day,month):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month=='all':
        #if month is given then we don't need to display the most common month
        common_month=df['Month'].mode()[0]
        print('The Most Common Month: {}'.format(str(list_month[common_month-1].title())))

    # display the most common day of week
    if day=='all':
        #if day is given then we don't need to display the most common day
        common_day = df['Week_day'].mode()[0]
        print('The Most Common Day Of week: {}'.format(common_day.title()))

    # display the most common start hour
    common_start_hour=df['Start Time'].dt.hour.mode()[0]
    print('The Most Common Start Hour: {}'.format(common_start_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most Commonly used Start Station : {}'.format(df['Start Station'].mode()[0]))
    

    # display most commonly used end station
    print('Most Commonly used End Station : {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df_trip=(df['Start Station']+ ' -> ' +df['End Station'])
    print('Most Commonly Used Station in End and Start Station: {}'.format(df_trip.mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travel Time:')
    total_travel=df['Trip Duration'].sum()
    days=int(total_travel//86400)
    hours=int((total_travel% 86400)//3600)
    minutes=int(((total_travel% 86400) % 3600)//60)
    seconds=int(((total_travel% 86400) % 3600) % 60)
    print('{} days {} hours {} minutes {} seconds , total in second= {}'.format(days,hours,minutes,seconds,total_travel))
    print('_'*40)
    
    # display mean travel time
    print('Average Travel Time:')
    mean_travel=df['Trip Duration'].mean()
    days=int(mean_travel//86400)
    hours=int((mean_travel % 86400)//3600)
    minutes=int(((mean_travel % 86400) % 3600)//60)
    seconds=int(((mean_travel % 86400) % 3600) % 60)
    print('{} days {} hours {} minutes {} seconds , Average in seconds= {}'.format(days,hours,minutes,seconds,mean_travel))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def user_stats(df,city):
    
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Numbers of user by type :')
    print(df['User Type'].value_counts().to_string())
    print('_'*40)

    # Display counts of gender   
    try:
        print('Numbers of user by gender :')
        print(df['Gender'].value_counts().to_string())
        print('_'*50)
    except KeyError:
        print("We're sorry! There is no data of user genders for {}."
              .format(city.title()))

    # Display earliest, most recent, and most common year of birth
    try:
        earliest=df['Birth Year'].min()
        recent=df['Birth Year'].max()
        mode=df['Birth Year'].mode()[0]
        print('The earliest year of birth: {}'.format(int(earliest)))
        print('The most common year of birth: {}'.format(int(mode)))
        print('The most recent year of birth: {}'.format(int(recent)))
    except:
        print("We're sorry! There is no data of birth year for {}."
              .format(city.title()))

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)

    
def display_data(df, ref):
    """Display 5 line of sorted raw data each time."""

    print("\nYou choosed to view raw data.")

    # sort data by column
    ref = 0
    sort_df = choice("\nHow would you like to sort the display of data?\n" 
                        "Press Enter to view unsorted.\n \n "
                         "st: Start Time\n et: End Time\n "
                         "td: Trip Duration\n ss: Start Station\n "
                         "es: End Station\n",
                         ('st', 'et', 'td', 'ss', 'es', ''))

    order = choice("\nWould you like it to be sorted ascending or "
                             "descending? \n asc: Ascending\n desc: Descending"
                             "\n",
                             ('asc', 'desc'))

    if order == 'asc':
        order = True
    elif order == 'desc':
        order = False

    if sort_df == 'st':
        df = df.sort_values(['Start Time'], ascending=order)
    elif sort_df == 'et':
        df = df.sort_values(['End Time'], ascending=order)
    elif sort_df == 'td':
        df = df.sort_values(['Trip Duration'], ascending=order)
    elif sort_df == 'ss':
        df = df.sort_values(['Start Station'], ascending=order)
    elif sort_df == 'es':
        df = df.sort_values(['End Station'], ascending=order)
    elif sort_df == '':
        pass

    # each loop displays 5 lines of raw data
    while True:
        for i in range(ref, len(df.index)):
            print("\n")
            print(df.iloc[ref:ref+5].to_string())
            print("\n")
            ref += 5

            if choice("Do you want to keep printing raw data?"
                      " Enter yes or no.\n") == 'yes':
                continue
            else:
                break
        break

    return ref


def main():
    while True:
        city, month, day = get_filters()
        df=load_data(city,month,day)
        ref = 0
        while True:
            select_data = choice("\nWhat information would you "
                                 "like to obtain?\n\n ts: Time Stats\n ss: "
                                 "Station Stats\n tds: Trip Duration Stats\n "
                                 "us: User Stats\n dd: Display Data\n "
                                 "r: Restart\n",
                                 ('ts', 'ss', 'tds', 'us', 'dd', 'r'))
            if select_data == 'ts':
                time_stats(df,day,month)
            elif select_data == 'ss':
                station_stats(df)
            elif select_data == 'tds':
                trip_duration_stats(df)
            elif select_data == 'us':
                user_stats(df, city)
            elif select_data == 'dd':
                ref = display_data(df, ref)
            elif select_data == 'r':
                break

        restart = choice("\nWould you like to restart?Enter yes or no.\n")
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()


# In[ ]:




