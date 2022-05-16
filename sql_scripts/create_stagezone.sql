-- Stage_Games
create table Stage_Games(
    GamesID serial primary key,
    Name text null,
    Release_date date null,
    Developer varchar(100) null,
    Platforms varchar(100) null,
    Required_age int null,
    Categories text null,
    Genres text null,
    Achievements int null,
    Positive_ratings int null,
    Negative_ratings int null,
    Average_playtime int null,
    Median_playtime int null,
    Owners  varchar(100) null,
    Price float null
);

-- Stage_Developer
create table Stage_Developer(
    DeveloperID serial primary key,
    Name varchar(100) null ,
    City varchar(50) null,
    AdministrativeDivision varchar(50) null,
    Country varchar(50) null,
    Founding_Year varchar(4) null
);

-- Stage_Sales
create table Stage_Sales(
    SalesID serial primary key,
    GameName text null ,
    Platform varchar(10) null,
    Year_of_Release int  null,
    Genre varchar(20) null,
    Developer varchar(50) null,
    NA_Sales float null,
    EU_Sales float null,
    JP_Sales float null,
    Other_Sales float null,
    Global_Sales float null,
    SalesYear int null
);
