-- Dates
WITH TempDates(Day, Month, Year, DayOfWeek, DayOfYear)
AS (
    SELECT DISTINCT extract(day from release_date), extract(month from release_date),
                    extract(year from release_date), extract(dow from release_date),
                    extract(doy from release_date)
    FROM stage_games
    UNION
    SELECT DISTINCT NULL::numeric, NULL::numeric, year_of_release,
                    NULL::numeric, NULL::numeric
    FROM stage_sales
    UNION
    SELECT DISTINCT NULL::numeric, NULL::numeric, salesyear,
                    NULL::numeric, NULL::numeric
    FROM stage_sales
)
INSERT INTO Dates(Day, Month, Year, DayOfWeek, DayOfYear)
SELECT DISTINCT Day, Month, Year, DayOfWeek, DayOfYear
FROM TempDates
WHERE CONCAT(Day, Month, Year) NOT IN
(SELECT CONCAT(Day, Month, Year) FROM Dates)
AND Year is not null;

-- Developers
WITH TempDevelopers(Name, City, AdministrativeDivision, Country, founding_year)
AS (
    SELECT DISTINCT name, city::varchar(20), administrativedivision::varchar(20),
                country::varchar(20), founding_year::integer
    FROM stage_developer
    UNION
    SELECT DISTINCT developer, null::varchar(20), null::varchar(20), null::varchar(20),
                    null::integer
    FROM stage_sales
    where lower(developer) not in (select lower(name) from stage_developer)
    UNION
    SELECT DISTINCT developer, null::varchar(20), null::varchar(20), null::varchar(20),
                    null::integer
    FROM stage_games
    where lower(developer) not in (select lower(name) from stage_developer)
)
INSERT INTO Developers(Name, City, AdministrativeDivision, Country, founding_year)
SELECT DISTINCT name, city, administrativedivision, country, founding_year::integer
FROM TempDevelopers
where lower(name) not in (select lower(name) from developers);

-- Games
WITH TempGames(Name,requiredAge, price)
AS (
    SELECT DISTINCT name::varchar(100), required_age, price
    FROM stage_games
    union
    SELECT DISTINCT gamename::varchar(100), null::int, null::float
    FROM stage_sales
    where lower(gamename) not in (select lower(name) from stage_games)
)
INSERT INTO Games(Name, requiredage, price)
SELECT DISTINCT Name, requiredage, price
FROM TempGames
where lower(name) not in (select lower(name) from games);

-- Genres
create or replace procedure InsertIntoGenres()
as
$$
declare
    row text;
    curr_genre varchar(30);
BEGIN
    for row in
        select genres from stage_games
    loop
        foreach curr_genre in array string_to_array(row, ';') loop
            if lower(curr_genre) not in (select lower(name) from genres) then
                insert into genres(name) values(curr_genre);
            end if;
        end loop;
    end loop;
end;
$$
language plpgsql;
call InsertIntoGenres();

INSERT INTO genres(Name)
SELECT DISTINCT genre
    FROM stage_sales
where lower(genre) not in (select lower(name) from genres);

-- Categories
create or replace procedure InsertIntoCategories()
as
$$
declare
    row text;
    curr_category varchar(50);
BEGIN
    for row in
        select categories from stage_games
    loop
        foreach curr_category in array string_to_array(row, ';') loop
            if lower(curr_category) not in (select lower(name) from categories) then
                insert into categories(name) values(curr_category);
            end if;
        end loop;
    end loop;
end;
$$
language plpgsql;
call InsertIntoCategories();

-- Regions
insert into regions(code, name) values ('NA', 'North America');
insert into regions(code, name) values ('EU', 'Europe');
insert into regions(code, name) values ('JP', 'Japan');
insert into regions(code, name) values ('OTH', 'Other');

-- Platforms
create or replace procedure InsertIntoPlatforms()
as
$$
declare
    row text;
    curr_platform varchar(20);
BEGIN
    for row in
        select platforms from stage_games
    loop
        foreach curr_platform in array string_to_array(row, ';') loop
            if lower(curr_platform) not in (select lower(name) from platforms) then
                insert into platforms(name) values(curr_platform);
            end if;
        end loop;
    end loop;
end
$$
language plpgsql;
call InsertIntoPlatforms();

insert into platforms(code)
select distinct platform from stage_sales
where lower(platform) not in (select lower(code) from platforms);

--CategoryList
create or replace procedure InsertIntoCategoryList()
as
$$
declare
    row record;
    curr_category varchar(50);
    id_category int;
    id_game int;
BEGIN
    for row in
        select name, categories from stage_games
    loop
        foreach curr_category in array string_to_array(row.categories, ';') loop
            select gameid into id_game from games where lower(name)=lower(row.name);
            select categoryid into id_category from categories
            where name=curr_category;
            insert into categorieslist(categoryid, gameid) values(id_category, id_game);
        end loop;
    end loop;
end
$$
language plpgsql;
call InsertIntoCategoryList();

--GenresList
create or replace procedure InsertIntoGenresList()
as
$$
declare
    row record;
    curr_genre varchar(30);
    id_genre int;
    id_game int;
BEGIN
    for row in
        select name, genres from stage_games
    loop
        foreach curr_genre in array string_to_array(row.genres, ';') loop
            select gameid into id_game from games where lower(name)=lower(row.name);
            select genreid into id_genre from genres
            where name=curr_genre;
            insert into genreslist(genreid, gameid) values(id_genre, id_game);
        end loop;
    end loop;
end
$$
language plpgsql;
call InsertIntoGenresList();

create or replace procedure InsertIntoGenresList2()
as
$$
declare
    row record;
    curr_genre varchar(30);
    id_genre int;
    id_game int;
BEGIN
    for row in
        select gamename, genre from stage_sales
        where gamename not in (select name from stage_games)
    loop
        select gameid into id_game from games where lower(name)=lower(row.gamename);
        select genreid into id_genre from genres
        where name=curr_genre;
        insert into genreslist(genreid, gameid) values(id_genre, id_game);
    end loop;
end
$$
language plpgsql;
call InsertIntoGenresList2();

