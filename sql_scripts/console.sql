-- Facts
-- Games that only in Stage_sales
WITH TempAnalysis(GameID, DeveloperID, PlatformID, ReleaseID, DateID, RegionID, Global_Sales)
AS (
    SELECT DISTINCT GameID, DeveloperID, PlatformID, d.DateID as ReleaseID,
                    dates.DateID, RegionID, Global_Sales
    FROM games
    join stage_sales as sales
    on lower(games.name)=lower(sales.gamename)
    join developers
    on developers.name = sales.developer
    join dates
    on dates.year=sales.year_of_release and dates.day is null
    join dates as d
    on d.year=sales.salesyear and d.day is null
    join platforms
    on  platforms.code = sales.platform
    cross join regions
    where lower(sales.gamename) not in (select lower(name) from stage_games)
)
INSERT INTO gameanalysis(GameID, DeveloperID, PlatformID, ReleaseID, DateID, RegionID, GlobalSales)
SELECT DISTINCT GameID, DeveloperID, PlatformID, ReleaseID, DateID, RegionID, Global_Sales
FROM TempAnalysis;

-- Fill fact of sales of games that only in Stage_sales
create or replace procedure InsertSales()
as
$$
declare
    sales_row record;
    curs cursor for select * from gameanalysis;
BEGIN
    for row in curs loop
        select * into sales_row from stage_sales
        where lower(gamename) = (select lower(name) from games where gameid = row.gameid)
        and platform = (select code from platforms where platformid = row.platformid)
        and lower(developer) = (select lower(name) from developers where developerid = row.developerid)
        and salesyear = (select year from dates where dateid = row.dateid);
        if row.regionid = 1 then
            update gameanalysis
            set regionsales = sales_row.na_sales
            where current of curs;
        elsif row.regionid = 2 then
            update gameanalysis
            set regionsales = sales_row.eu_sales
            where current of curs;
        elsif row.regionid = 3 then
            update gameanalysis
            set regionsales = sales_row.jp_sales
            where current of curs;
        else
            update gameanalysis
            set regionsales = sales_row.other_sales
            where current of curs;
        end if;
    end loop;
end
$$
language plpgsql;
call InsertSales();

-- Games that only in Stage_games
WITH TempAnalysis(GameID, DeveloperID, PlatformID, ReleaseID, achievements,
    usercount, positiveratings, negativeratings, medianplaytime, GlobalSales)
AS (
    SELECT DISTINCT GameID, DeveloperID, PlatformID, dates.dateid,
                    achievements, (string_to_array(owners, '-'))[1]::int,
                    positive_ratings, negative_ratings, median_playtime,
                    owners*sgames.price
    FROM games
    join stage_games as sgames
    on games.name=sgames.name
    join developers
    on developers.name = sgames.developer
    join dates
    on make_date(dates.year, dates.month, dates.day)=sgames.release_date
    join platforms
    on  platforms.name in (select unnest(string_to_array(sgames.platforms, ';')))
    where lower(games.name) not in (select lower(gamename) from stage_sales)
)
INSERT INTO gameanalysis(GameID, DeveloperID, PlatformID, ReleaseID, achievements,
                         usercount, positiveratings, negativeratings, medianplaytime,
                         GlobalSales)
SELECT DISTINCT GameID, DeveloperID, PlatformID, ReleaseID,achievements, usercount,
                positiveratings, negativeratings, medianplaytime, GlobalSales
FROM TempAnalysis
where GameID not in (select gameid from gameanalysis);

-- Other games (that in Stage_games and Stage_sales)
WITH TempAnalysis(GameID, DeveloperID, PlatformID, ReleaseID, DateID, RegionID,
    achievements, usercount, positiveratings, negativeratings, medianplaytime,
     average_playtime, Global_Sales)
AS (
    SELECT DISTINCT GameID, DeveloperID, PlatformID, dates.dateid as ReleaseID,
                    d.dateid, RegionID, achievements, positive_ratings,
                    (string_to_array(owners, '-'))[1]::int as usercount,
                    negative_ratings, median_playtime, average_playtime, global_sales
    FROM games
    join stage_games as sgames
    on lower(games.name) = lower(sgames.name)
    join stage_sales as sales
    on lower(sales.gamename) = lower(sgames.name)
    join developers
    on developers.name = sgames.developer
    join dates
    on make_date(dates.year, dates.month, dates.day)=sgames.release_date
    join platforms
    on  platforms.name in (select unnest(string_to_array(sgames.platforms, ';')))
    join dates as d
    on sales.salesyear=d.year and d.day is null
    cross join regions
)
INSERT INTO gameanalysis(GameID, DeveloperID, PlatformID, ReleaseID, DateID, RegionID,
    achievements, usercount, positiveratings, negativeratings, averageplaytime,
    medianplaytime, GlobalSales)
SELECT DISTINCT GameID, DeveloperID, PlatformID, ReleaseID, DateID, RegionID,
    achievements, usercount, positiveratings, negativeratings, average_playtime,
    medianplaytime, Global_Sales
FROM TempAnalysis
where GameID not in (select gameid from gameanalysis);

-- Fill fact of sales of games that in Stage_sales and Stage_games
create or replace procedure InsertSales2()
as
$$
declare
    sales_row record;
    curs cursor for select * from gameanalysis where regionid is not null
                                                 and achievements is not null;
BEGIN
    for row in curs loop
        select * into sales_row from stage_sales
        where lower(gamename) = (select lower(name) from games where gameid = row.gameid)
        and lower(developer) = (select lower(name) from developers where developerid = row.developerid)
        and year_of_release = (select year from dates where dateid = row.releaseid)
        and salesyear = (select year from dates where dateid = row.dateid);
        if row.regionid = 1 then
                update gameanalysis
                set regionsales = sales_row.na_sales
                where current of curs;
        elsif row.regionid = 2 then
                update gameanalysis
                set regionsales = sales_row.eu_sales
                where current of curs;
        elsif row.regionid = 3 then
                update gameanalysis
                set regionsales = sales_row.jp_sales
                where current of curs;
        elsif row.regionid = 4 then
                update gameanalysis
                set regionsales = sales_row.other_sales
                where current of curs;
        end if;
    end loop;
end
$$
language plpgsql;
call InsertSales2();
