DECLARE @temp_table_count int

SELECT @temp_table_count = COUNT(*) FROM tempdb..sysobjects WHERE name = '##tomove%'

 

  IF @temp_table_count <>0
  Begin
    declare @sql nvarchar(max)
    select @sql = isnull(@sql+';', '') + 'drop table ' + quotename(name)
    FROM tempdb..sysobjects
    where name = '##tomove'
    exec (@sql)
  END

;WITH Data
     AS (SELECT supplierid, 
                FileHistoryID, feedid,
                SamevendorCounter = ROW_NUMBER() OVER(PARTITION BY supplierID, feedid
                ORDER BY createddate DESC)
   FROM Control_RM.[dbo].[FeedHistory] where ErrorFeed is null)
   SELECT d.*, s.DBName into ##tomove
   FROM Data d
	 inner join Control_RM.dbo.Supplier s
	 on d.SupplierID = s.SupplierID
   WHERE SamevendorCounter not in (1,2) and dbname in (select dbname from Control_RM.[dbo].[ArchiveDBList])

alter table ##tomove
add processed varchar(1),
ColumnNames varchar(max)

delete from ##tomove where FileHistoryID in (Select FileHistoryID from Control_RM.[dbo].[EhArchiveLog])

update ##tomove set processed = 'P'

update ##tomove set ColumnNames = a.columnnames from ##tomove inner join Control_RM.[dbo].[ArchiveDBList] a on ##tomove.dbname = a.dbname


declare @dbname varchar(100)
declare @FileHistoryID int
declare @count int
declare @counttotal int
declare @aa varchar(max)
declare @feedid int
declare @supplierid int

set @count = 1

select @counttotal = count(*) from ##tomove


-- While/For LOOP start

while @count <= @counttotal

begin



select top 1 @dbname = dbname,@FileHistoryID = FileHistoryID, @aa = columnnames, @feedid = FeedID, @supplierid = SupplierID from ##tomove where processed = 'P'

-- EH counts for Log
INSERT into Control_RM.[dbo].[EhArchiveLog](FileHistoryID,Supplierid)
values(@FileHistoryID,@supplierid)


EXEC('Select count(*) as counts into ##temp from '+@dbname+'.dbo.EntityHistory where FileHistoryID = '+@FileHistoryID)

update Control_RM.[dbo].[EhArchiveLog]
SET CountEH = (Select top 1 Counts from ##temp)
where FileHistoryID = @FileHistoryID

drop table ##temp
-- EH count end



exec('insert into ' + @dbname + '.dbo.EntityHistoryArchive(' + @aa + ')
select ' + @aa + ' from ' + @dbname + '.dbo.EntityHistory
where FileHistoryID =' + @FileHistoryID)

exec('delete from ' + @dbname + '.dbo.EntityHistory where FileHistoryID = ' + @FileHistoryID)


-- EHArchive counts for Log

EXEC('Select count(*) as counts into ##temp from '+@dbname+'.dbo.EntityHistoryArchive where FileHistoryID = '+@FileHistoryID)

update Control_RM.[dbo].[EhArchiveLog]
SET CountEHA = (Select top 1 Counts from ##temp)
where FileHistoryID = @FileHistoryID


drop table ##temp
-- EHArchive count end



set @count = @count + 1

update ##tomove set Processed = 'Y' where FileHistoryID = @FileHistoryID


end
