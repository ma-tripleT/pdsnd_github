"""
Udacity python project for Programming for Data Science with Python Nanodegree Program
By Matthew Thomson https://github.com/ma-tripleT
"""

import time
import pandas as pd
import numpy as np
from typing import List

from pandas.core.frame import DataFrame

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities: List[str] = ['chicago','new york city','washington']
months: List[str] = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days_of_week: List[str]= ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
numbered_days: List[range] = list(range(7))

EARLEST_DOB: int = 1940

def input_selector(what_you_want: str) -> str:
    """ Loops through asking the user what they want until they provide a valid answer

    Args: 
        (str) what_you_want: a choice of city, month, day or yes/no

    Returns:
        (str) selection: the valid choice from the user
    """

    if what_you_want == 'city':
        options = cities
    elif what_you_want == 'month':
        options = months
    elif what_you_want == 'day':
        options = days_of_week

    valid_input = False
    while valid_input != True:

        print(f"Your options are for {what_you_want} are:\n {options}")
        print('-  '*2)
        print(f"Please enter your {what_you_want} of choice:")
        selection = input().casefold()
        if selection in options:
            print(f"Thanks for choosing the {what_you_want} as: {selection}")
            print('- '*10)
            valid_input = True
            return selection
        else:
            print('-+/'*10)
            print(f"\nThat {what_you_want} '{selection}' isn't on the list of options!\nPlease try again\n")
            print('-+/'*10)
    
def get_filters() -> List[str]:
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for all required inputs
    [city, month, day] = [input_selector(choice) for choice in ['city','month','day']]

    print('-'*40)
    return [city, month, day]


def load_data(city: str, month: str, day: str) -> DataFrame:
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    # df['day_of_week'] = df['Start Time'].dt.weekday
    df['day_of_week'] = df['Start Time'].dt.day_name()

    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        
        month = months.index(month)
   
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df

def see_some_raw_data() -> bool:
    """Asks the user for a yes/no answer and returns True/False"""
    print("Would you like to see 5 (more) rows of raw data?\n Yes/No answers only")
    yayornay: str = input().casefold()
    if yayornay in ['yes','no']:
        if yayornay == 'yes':
            return True
        else:
            return False
    else:
        print("That's not a legitimate option, please try again.")


def raw_data_show(df: DataFrame):
    """Asks the user if they would like to see some raw data, 5 rows at a time, then displays it"""

    first_row_to_show: int = 0
    num_rows_to_show: int = 5
    last_row_to_show: int = first_row_to_show + num_rows_to_show
    num_iterations: int = 0
    num_rows_total: int = df.shape[0]

    while last_row_to_show <= num_rows_total + num_rows_to_show:
    # TODO: What about when you've hit yes a million times and have less than 5 rows remaining? 
    # Will the [a:f] formatting work if c is the last row...
        if see_some_raw_data():
            print(df.iloc[first_row_to_show:last_row_to_show])
            first_row_to_show += num_rows_to_show
            last_row_to_show += num_rows_to_show
            num_iterations += 1
        else:
            break

def dob_trim(df: DataFrame) -> DataFrame:
    """If the 'Birth Year' column exists then drop all values older than 1940"""
    
    # Drop the oldest riders who are unlikely to be valid given they're at least 81yo

    print(f"Let's look at the 'Birth Year'")
    print(f"We see there's {df[df['Birth Year'] < EARLEST_DOB].shape[0]} of riders born earlier than {EARLEST_DOB}, good on them for keeping fit!")
    print(f"However I somewhat doubt that there's actually a rider born in {int(df['Birth Year'].min())}")
    print(f"At risk of discriminating by age, we'll drop all riders born before {EARLEST_DOB}, even if their birth date was a data entry error")
    df = df[df['Birth Year'] >= EARLEST_DOB]
    print("This also happens to remove the NaN values")
    print('-'*40)
    return df
    # # Find
    # nan_mask = df['Birth Year'].isna()
    # how_many_nans = nan_mask.sum()
    # if how_many_nans > 0:
    #     print(f"There's {how_many_nans} 'NaN' values in the 'Birth Year', let's look at the stats")
    #     mu_dob = np.mean(df['Birth Year'])
    #     sigma_dob = np.std(df['Birth Year'])
    #     df['Birth Year'].mask(
    #         nan_mask, 
    #         int(np.rint(np.random.normal(loc=mu_dob, scale=sigma_dob))),
    #         inplace=True)


def data_cleaning(df: DataFrame) -> DataFrame:
    """A function to clean up the data by removing problems such as 'NaN' entries
    and other strange entries such as someone renting a bike after being born in 1885!"""
    print("Cleaning the data to remove problems\n ")

    nulls = df.isnull().sum()
    nulls = nulls[nulls != 0]

    if not nulls.empty:
        print(f"The columns below some 'NaN' values:\n{nulls}")

    # for index_with_nan in enumerate(nulls.keys()[:]):
        # print(f"Column: {index_with_nan} \n ")

    if 'Birth Year' in df.columns.values.tolist():
        df = dob_trim(df)

    time.sleep(2)

    no_user_type: float = format(df['User Type'].isna().sum()/df.shape[0]*100, '.2g')
    print(f"A few rows don't have any information for 'User Type' but it is only {no_user_type}% so we'll just drop them")
    df = df.dropna(axis = 0, subset=['User Type'])

    if 'Gender' in df.columns.values.tolist():
        gender_neutral: float = format(df['Gender'].isna().sum()/df.shape[0]*100, '.2g')
        print(f"{gender_neutral}% of trips don't have any information for 'Gender' so we'll forward-fill.")
        df.fillna(method="ffill")
        # gender_neutral: float = format(nulls['Gender']/df.shape[0]*100, '.2g')
        # print(f"A few rows don't have any information for 'Gender' but it is only {gender_neutral}% so we'll just drop them")
        # df = df.dropna(axis = 0, subset=['Gender'], inplace=True)
        
    return df

def time_stats(df: DataFrame, month: str, day: str):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # popular_month = df['month'].mode().iloc[0]
    popular_month: str = df['month'].mode()[0]
    
    print(f"Most Common Month: {months[popular_month]}")
    if month != 'all':
        print(f"------ Which isn't surprising given you chose {month}")


    # display the most common day of week
    # popular_day = df['day_of_week'].mode().iloc[0]
    popular_day: str = df['day_of_week'].mode()[0]
    
    print(f"Most Common Day of the week: {popular_day}")
    if day != 'all':
        print(f"------ Which isn't surprising given you chose {day}")

    # display the most common start hour
    # popular_hour = df['hour'].mode().iloc[0]
    popular_hour: int = df['hour'].mode()[0]
    
    print(f"Most Common hour: {popular_hour}")

    print("\nThis took %s seconds." % round(time.time() - start_time,2))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(f"Most commonly used Start Station: {df['Start Station'].mode()[0]}")


    # display most commonly used end station
    print(f"Most commonly used End Station: {df['End Station'].mode()[0]}")

    # display most frequent combination of start station and end station trip
    print(f"The most frequent combination of start station and end station trip is:\n{df[['Start Station','End Station']].value_counts().index[0]}")

    print("\nThis took %s seconds." % round(time.time() - start_time,2))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print(f"Total Travel Time: {df['Trip Duration'].sum()}")

    # display mean travel time
    average_seconds = round(df['Trip Duration'].mean())
    average_minutes = round(average_seconds / 60,1)
    print(f"Mean 'Trip Duration': {average_seconds} seconds or {average_minutes} minutes")


    print("\nThis took %s seconds." % round(time.time() - start_time,2))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    df.value_counts(subset='User Type')

    # Display counts of gender
    if 'Gender' in df.columns.values.tolist():
        df.value_counts(subset='Gender')
    else:
        print("No Gender stats to show for your selection of City, Month & Day")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns.values.tolist():
        print(f"The earliest birth year was limited to {EARLEST_DOB} because anyone older seems unrealistic!")
        print(f"The youngest rider was born in {int(df['Birth Year'].max())}")
        print(f"More riders were born in {int(df['Birth Year'].mode()[0])} than any other year")
    else:
        print("For your selections we don't have any User Type stats")


    print("\nThis took %s seconds." % round(time.time() - start_time,2))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        raw_data_show(df)
        df = data_cleaning(df)
        time_stats(df, month, day)
        time.sleep(2)
        station_stats(df)
        time.sleep(2)
        trip_duration_stats(df)
        time.sleep(2)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
