import time
import pandas as pd
import numpy as np

#Creating a dictionary containing the data sources for the three cities
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#Function to figure out the filtering requirements of the user
global day, month
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello!\n')
    print("I'm Temidayo!!!\n")
    #Initializing an empty city variable to store city choice from user
    #You will see this repeat throughout the program
    print('Let\'s explore some US bikeshare data together!\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_list = ['chicago', 'new york city', 'washington']
    city = input('Would you like to see data for Chicago, New York City or Washington?\n').lower()

    while city not in  city_list:
        print('Invalid city')
        city = input('would you like to see data for Chicago, New York City, or Washington?\n').lower()

    # get user input for month (all, january, february, ... , june)
    filter_rsp = input('Would you like to filter the data by month, day or both?\n').lower()
    
    if filter_rsp == 'month':
        month = input('Which month? January, February, March, May or June\n').lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        
        while month not in months:

            month = input('Which month\? January, February, march, April, May or June\n').lower()

        day = 'all'

    # get user input for day of week (all, monday, tuesday, ... sunday) 
    elif filter_rsp == "day":
        day = int(input('which day?: Please type your response as an integer (e.g. 0 = monday, 6 = sunday)\n'))
        while day < 0 or day > 6 or type(day) == str:
            print("Invalid day")
            day = int(input("which day? Please type your response as an integer(e.g., 0 = monday, 6 = sunday)\n"))
        month = 'all'

    elif filter_rsp == "both":
        month = input("which month ? January, February, March, May or June?\n").lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june']

        while month not in months:
            month = input("which month ? January, February, March, May or June?\n").lower()

        day = int(input("which day? Please type your response as an integer(e.g., 0 = monday, 6 = sunday)\n"))

        while day < 0 or day > 6 or type(day) == str:
            print("Invalid day")
            day = int(input("which day? Please type your response as an integer(e.g., 0 = monday, 6 = sunday)\n"))
            
   

    return city, month, day

#Function to load data from .csv files
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
    print('===============Please wait while loading data===============')

    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])     


    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get th corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]


    return df

#Function to calculate all the time-related statistics for the chosen data
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most Common Month:', common_month)

    # display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print('Most Common Day of week:', common_day_of_week)

    #Extract hour from the start time column to create an hour
    df['hour'] = df['Start Time'].dt.hour
    # display the most common start hour
    common_start_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Function to calculate station related statistics
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most Commonly Used Start station', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most Commonly Used End Station', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['Freq Start and End Trip'] = df['Start Station'] + ':' + df['End Station']
    print('\nMost Frequent Start Station and End Station Trip', df['Freq Start and End Trip'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Function for trip duration related statistics
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\nTotal Travel Time:', df['Trip Duration'].sum())

    # display mean travel time
    print('\nAverage travel time:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Function to calculate user statistics
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nUser Type:\n', df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df.columns:
        print('\nGender Counts:\n', df.Gender.value_counts())

    else:
        print('\nNo Gender data to share.')

    
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
       print('\nEarliest Year of Birth:', int(df['Birth Year'].min()))

       print('\nMost Recent Year of Birth:', int(df['Birth Year'].max()))

       print('\nMost Common Year of Birth:', int(df['Birth Year'].mode()[0]))
    else: 
       print('\nNo birth year data to share.')

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)

#Function to display the data frame itself as per user request
pd.set_option('display.max_columns', 200)
def display_data(df):
    """Displays 5 rows of data from the csv file for the selected city.

    Args:
        param1 (df): The data frame you wish to work with.

    Returns:
        None.
    """
    #counter variable is initialized as a tag to ensure only details from
    #a particular point is displayed
    loc = 0
    print("\n would you like to view 5 rows of raw data? Enter yes or no")
    while True:
        rdata = input('  (yes or no):  ').lower()
        if  rdata == 'yes':
            print(df.iloc[loc:loc + 5])
            loc += 5

            #If user opts for it, this displays next 5 rows of data
        
            print("\n would you like to view the next 5 rows of raw data?")
            continue
        else:
            break    

#Main function to call all the previous functions
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
