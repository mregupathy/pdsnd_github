import time
import os
import sys
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO:
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please enter the city name (chicago, new york city, washington): ").strip().lower()
        # check whether received input is there in CITY_DATA, Yes - Break, Else - Loop
        if city in CITY_DATA:
            break
        else:
            print("Invalid city name, please enter one of the following cities mentioned in prompt")

    # TO DO: get user input for month (all, january, february, ... , june)
    MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input("Please enter all or following month names (january,february,march,april,may,june):  ").strip().lower()
        if month in MONTHS:
            break
        elif month == "all":
            break
        else:
            print("Invalid month name, please enter correct month name as mentioned in prompt")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("Please enter all or following days (monday..sunday) : ").strip().lower()
        if day in DAYS:
            break
        elif day == "all":
            break
        else:
            print("Invalid day name, please enter correct day name")
    print('-' * 40)
    return city, month, day


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
    # Load file
    df = get_df_for_city(city)
    # Filter by month
    if month != "all":
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        # add 1 because the index starts from 0 but dt.month returns 1 for jan
        month = months.index(month) + 1
        # create a modified df with month as filter
        df = df[df['month'] == month]
    # Filter by day
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        df = df[df['day_of_week'] == day]
    # return df
    return df


def get_df_for_city(city):
    # Creating a check whether the file exists before reading the csv file.
    # Uses 2 new imports os and sys modules for this check
    if os.path.exists(CITY_DATA[city]) == False:
        sys.exit("ERROR:file doesn't exists ")

    df = pd.read_csv(CITY_DATA[city])
    # convert to time format the Start Time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # create new column called month which will have index
    # from 1 to 12
    df['month'] = df['Start Time'].dt.month
    # create new column called day of week
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    months = ['none', 'january', 'february', 'march', 'april', 'may', 'june']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    print("{} is the most common month".format(months[most_common_month].title()))
    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print("{} is the most common day of week".format(days[most_common_day].title()))
    # TO DO: display the most common start hour
    most_common_start_hour = df['Start Time'].dt.hour.mode()[0]
    most_common_start_hour = f"{most_common_start_hour:02d} HRS"

    print("{} is the most common start hour".format(most_common_start_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_cmon_st_sn = df['Start Station'].mode()[0]
    print("{} is the most commonly used start station".format(most_cmon_st_sn))
    #Alternate Method
    #temp = df['Start Station'].value_counts().idxmax()
    #print("temp {} is the most commonly used start station".format(temp))

    # TO DO: display most commonly used end station
    most_cmon_end_sn = df['End Station'].mode()[0]
    print("{} is the most commonly used end station".format(most_cmon_end_sn))
    # Alternate method
    # temp = df['End Station'].value_counts().idxmax()
    #print("temp {} is the most commonly used end station".format(temp))

    # TO DO: display most frequent combination of start station and end station trip
    combined_station_size = df.groupby(['Start Station', 'End Station']).size()
    mst_freq_comb = combined_station_size.idxmax()
    print("Most freq combination of Start and End Station :  {}".format(mst_freq_comb))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    # Logic -
    # compute sum of trip duration
    # compute mean of trip duration
    # use divmod to break down into HRS and MS

    # TO DO: display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    tot_hrs, tot_mts = divmod(total_trip_duration, 60)
    print("Total Travel Time is : {} HRS and {} MS".format(int(tot_hrs), int(tot_mts)))

    # TO DO: display mean travel time
    mean_trip_duration = df['Trip Duration'].mean()
    mean_hrs, mean_mts = divmod(mean_trip_duration, 60)
    print("Mean Travel Time is : {} HRS and {} MS".format(int(mean_hrs), int(mean_mts)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    # Error Handling for User Type, Gender and Birth Year as these data is not there for
    # washington.csv

    if 'User Type' in df.columns:
        user_types = df['User Type'].value_counts()
        print("Counts of User Types")
        print(user_types)
    else:
        print("No user types available for this dataframe")
    print()
    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_types = df['Gender'].value_counts()
        print("Counts of Gender")
        print(gender_types)
    else:
        print("No gender data available for this dataframe")
    print()
    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:

        old_byear = int(df['Birth Year'].min())
        young_byear = int(df['Birth Year'].max())
        mod_byear = int(df['Birth Year'].mode()[0])
        print("Earliest {} Most Recent {} and Most Common year of birth(s) {}".format(old_byear, young_byear, mod_byear))
    else:
        print("No birth year data available in this dataframe")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def display_raw_data(df):
    """Displays raw data of selected csv file  """
    # takes user input (yes/no) and prints 5 records until user inputs no
    index = 0
    print()
    print('-' * 40)
    print("Displaying df describe :\n")
    print(df.describe())
    print('-' * 40)
    print("Displaying df info :\n")
    print(df.info())
    print('-' * 40)
    while index < len(df):
        user_input = input("Do you want to see 5 lines of raw data ? (yes/no) : ").strip().lower()
        if user_input == 'yes':
            print(df.iloc[index:index + 5])
            index += 5
        elif user_input == 'no':
            print("Stopping the display of raw data.")
            return
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def main():
    while True:
        # Get City, Month, Day
        city, month, day = get_filters()
        print("City {}, Month {}, Day {}".format(city, month, day))
        # Create Data Frame
        df = load_data(city, month, day)
        # Display Raw data of Data frame
        display_raw_data(df)
        # Publish time statistics
        time_stats(df)
        # Publish station statistics
        station_stats(df)
        # Publish trip duration statistics
        trip_duration_stats(df)
        # Publish user statistics
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').strip()
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
