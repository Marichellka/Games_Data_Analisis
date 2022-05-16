create table Genres(
    GenreID serial primary key,
    Name varchar(30) null
);

create table Categories(
    CategoryID serial primary key,
    Name varchar(50) null
);

create table Platforms(
    PlatformID serial primary key,
    Code varchar(10) null,
    Name varchar(20) null
);

create table Regions(
    RegionID serial primary key,
    Code varchar(5) null,
    Name varchar(20) null
);

create table Dates(
    DateID serial primary key,
    Day int null,
    Month int null,
    Year int null,
    DayOfWeek int null,
    DayOfYear int null
);

create table Developers(
    DeveloperID serial primary key,
    Name varchar(100) null,
    City varchar(20) null,
    AdministrativeDivision varchar(20) null,
    Country varchar(20) null,
    Founding_Year int null
);

create table Games(
    GameID serial primary key,
    Name varchar(100) null,
    RequiredAge int null,
    Price float null
);

create table GenresList(
    ListID serial primary key,
    GenreID int references Genres(GenreID),
    GameID int references Games(GameID)
);

create table CategoriesList(
    ListID serial primary key,
    CategoryID  int references Categories(CategoryID),
    GameID int references Games(GameID)
);

create table GameAnalysis(
    GameAnalysisID serial primary key ,
    GameID int references Games (GameID) null,
    DeveloperID int references Developers (DeveloperID) null,
    PlatformID int references Platforms (PlatformID) null,
    ReleaseID int references Dates (DateID) null,
    DateID int references Dates (DateID) null,
    RegionId int references Regions (RegionID) null,
    Achievements int null,
    PositiveRatings int null,
    NegativeRatings int null,
    MedianPlaytime int null,
    AveragePlaytime int null,
    UserCount int null,
    RegionSales float null,
    GlobalSales float null
);
