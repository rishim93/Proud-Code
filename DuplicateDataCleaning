USE [DBRishi]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		Rishi Madan
-- Create date: 2020-03-06
-- Description:	Duplicate Detection Procedure
-- =============================================
ALTER PROCEDURE [dbo].[prDuplicateDetection](
		@RecordSource as Varchar(100),
		@LDM as int)



AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;
	


	DECLARE @temp_table_count INT
	DECLARE @Input_Table varchar(100) 


	SET @Input_Table = '_DuplicateRecords'
	

	EXEC('Truncate Table '+ @Input_Table);




	
	-- Get Records based on the Parameter
	IF @RecordSource = 'Unmatched'
	-- SourceID = 1
	BEGIN
		EXEC('INSERT INTO ' +@Input_Table+ ' (City, IDmask1, Address1, Address2, Postcode, SupplierID, CC, StateCode,  CountryISO, IDmask2, FeedHistoryID)
			SELECT     CleanCity, IDmask1, CleanAddress1, CleanAddress2, CleanPostCode, SupplierID, CC, StateCode,  CountryISO, CASE WHEN LEN(IDmask2)<=20 THEN IDmask2 END, FeedHistoryID
			FROM         CClean.dbo.vwElementDD
			WHERE     Matchstatusflag = 2')
			--AND Supplierid IN (SELECT SupplierID FROM Control_strings.dbo.Supplier WHERE IE = ''Y'')')

		-- add businessname
		EXEC('UPDATE        ' +@Input_Table+ '  SET BusinessName = CE.ElementData, NameElementID = 1
			FROM             ' +@Input_Table+ '  INNER JOIN CClean.dbo.vwElementDD CE ON  ' +@Input_Table+ '.IDmask1 = CE.IDmask1
			WHERE        ElementID = 1')

		-- add tradestyle to businessname record
		EXEC('UPDATE        ' +@Input_Table+ '  SET Tradestyle = CE.ElementData
			FROM             ' +@Input_Table+ '  INNER JOIN CClean.dbo.vwElementDD CE ON  ' +@Input_Table+ '.IDmask1 = CE.IDmask1
			WHERE        ElementID = 2')
		
		-- Concat Address1 and Address2 
		EXEC('UPDATE        ' +@Input_Table+ '  SET Addressfull = replace(Ltrim(rtrim(concat(Address1,'' '',Address2))),'' '','''')')


		-- SourceID = 1 for unmatched	
		EXEC('UPDATE        ' +@Input_Table+ '  SET SourceID = 1')
	
	
	END   -- END OF IF for UnMatched
	IF @LDM = 1
	-- LDM data to be included with Unmatched based on Potalcode from Unmatched
	BEGIN
		EXEC('INSERT INTO ' +@Input_Table+ ' (City, IDmask1, Address1, Postcode, SupplierID, StateCode,BusinessName,TradeStyle,Tel)
			  SELECT    City, IDmask1, Address1, Postcode, SupplierID, StateCode,BusinessName,TradeStyle,Tel
			FROM         Analysis.dbo.LDM
			WHERE  REPLACE(Postcode,'' '','''') in (Select distinct(REPLACE(Postcode,'' '','''')) from _DuplicateRecords)')

		-- SourceID = 1 for unmatched	
		EXEC('UPDATE        ' +@Input_Table+ '  SET SourceID = 1 WHERE Supplierid = 1')
	END
		
		--## Processing ##--
		
		
		-- Where PostCode is NULL
		EXEC('UPDATE        ' +@Input_Table+ '  SET ExcludeReasonID = -1 WHERE Postcode is NULL')

		-- Where there is only 1 postcode 
		EXEC('UPDATE         ' +@Input_Table+ '   SET ExcludeReasonID = -2 WHERE PostCode in 
		(Select Postcode FROM       ' +@Input_Table+ '  group by Postcode having count(*) = 1)
		and ExcludeReasonID is NULL')

		-- Exclude Records where BusinessName is NULL
		EXEC('UPDATE        ' +@Input_Table+ '   SET ExcludeReasonID = -4 WHERE BusinessName is NULL')


		-- Add AddressKey,PostcodeKey and BusinessNameKey
		EXEC('UPDATE         ' +@Input_Table+ '   SET PostCodeKey = Postcode')
		EXEC('UPDATE         ' +@Input_Table+ '   SET BusinessNameKey = BusinessName')
		EXEC('UPDATE         ' +@Input_Table+ '   SET TradeStyleKey = TradeStyle')
		EXEC('UPDATE         ' +@Input_Table+ '   SET AddressKey = CONCAT(Address1,Address2)')

		--- Processing businessName, Tradestyle and Address for Finding Exact Duplicates

		--- BusinessName
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'LTD','') WHERE CHARINDEX('LTD',BusinessNameKey,0)>0 
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'LIMITED','') WHERE CHARINDEX('LIMITED',BusinessNameKey,0)>0 
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'CO','') WHERE CHARINDEX('CO',BusinessNameKey,0)>0  
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'COMPANY','') WHERE CHARINDEX('COMPANY',BusinessNameKey,0)>0  
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'CORP','') WHERE CHARINDEX('CORP',BusinessNameKey,0)>0  
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'CORPORATION','') WHERE CHARINDEX('CORPORATION',BusinessNameKey,0)>0  
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'PLC','') WHERE CHARINDEX('PLC',BusinessNameKey,0)>0   
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'PUBLIC LIMITED COMPANY','') WHERE CHARINDEX('PUBLIC LIMITED COMPANY',BusinessNameKey,0)>0   
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'INC','') WHERE CHARINDEX('INC',BusinessNameKey,0)>0   
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'INCORPORATED','') WHERE CHARINDEX('INCORPORATED',BusinessNameKey,0)>0   
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'LLP','') WHERE CHARINDEX('LLP',BusinessNameKey,0)>0  
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'LIMITED LIABILITY PARTNERSHIP','') WHERE CHARINDEX('LIMITED LIABILITY PARTNERSHIP',BusinessNameKey,0)>0  
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'LLC','') WHERE CHARINDEX('LLC',BusinessNameKey,0)>0  
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'LIMITED LIABILITY COMPANY','') WHERE CHARINDEX('LIMITED LIABILITY COMPANY',BusinessNameKey,0)>0  

		--replace common abbreviations _ BusinessName
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'SVC','') WHERE CHARINDEX('SVC',BusinessNameKey,0)>0  
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'CTR','') WHERE CHARINDEX('CTR',BusinessNameKey,0)>0   
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'MFG','') WHERE CHARINDEX('MFG',BusinessNameKey,0)>0   
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'ASSOC','') WHERE CHARINDEX('ASSOC',BusinessNameKey,0)>0   
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'INTL','') WHERE CHARINDEX('INTL',BusinessNameKey,0)>0   
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'SUPLS','') WHERE CHARINDEX('SUPLS',BusinessNameKey,0)>0   
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'ENR','') WHERE CHARINDEX('ENR',BusinessNameKey,0)>0   
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'Assn','') WHERE CHARINDEX('Assn',BusinessNameKey,0)>0
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'SERVICE','') WHERE CHARINDEX('SVC',BusinessNameKey,0)>0  
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'CENTRE','') WHERE CHARINDEX('CTR',BusinessNameKey,0)>0   
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'MANUFACTURING','') WHERE CHARINDEX('MFG',BusinessNameKey,0)>0   
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'ASSOCIATION','') WHERE CHARINDEX('ASSOC',BusinessNameKey,0)>0   
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'INTERNATIONAL','') WHERE CHARINDEX('INTL',BusinessNameKey,0)>0   
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'SUPPLIES','') WHERE CHARINDEX('SUPLS',BusinessNameKey,0)>0   
		update _DuplicateRecords set BusinessNameKey = Control_strings.dbo.subReplaceAbbreviation(BusinessNameKey, 'ENREGISTRE','') WHERE CHARINDEX('ENR',BusinessNameKey,0)>0 

		--remove punctuation from BusinessName and address
		update _DuplicateRecords set BusinessNamekey = replace(businessnamekey,'.',''), Addresskey = replace(Addresskey,'.','')
		update _DuplicateRecords set BusinessNamekey = replace(businessnamekey,'&','AND'), Addresskey = replace(addresskey,'&','AND')
		update _DuplicateRecords set BusinessNamekey = replace(businessnamekey,'-',''), Addresskey = replace(addresskey,'-','')
		update _DuplicateRecords set BusinessNamekey = replace(businessnamekey,',',''), Addresskey = replace(addresskey,',','')
		update _DuplicateRecords set BusinessNamekey = replace(businessnamekey,char(39),''), Addresskey = replace(addresskey,char(39),'') -- this is ' so easier to do with ascii
		update _DuplicateRecords set BusinessNamekey = replace(businessnamekey,'(',''), Addresskey = replace(Addresskey,'(','')
		update _DuplicateRecords set BusinessNamekey = replace(businessnamekey,')',''), Addresskey = replace(Addresskey,')','')
		update _DuplicateRecords set BusinessNamekey = replace(businessnamekey,'/',''), Addresskey = replace(Addresskey,'/','')
		update _DuplicateRecords set BusinessNamekey = replace(businessnamekey,' ',''), Addresskey = replace(addresskey,' ',''), postcodekey = replace(postcodekey,' ','')

		--NAIDE-2045 remove legal forms from business key used for deduplication
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'LTD','') WHERE CHARINDEX('LTD',TradestyleKey,0)>0 
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'LIMITED','') WHERE CHARINDEX('LIMITED',TradestyleKey,0)>0 
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'CO','') WHERE CHARINDEX('CO',TradestyleKey,0)>0  
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'COMPANY','') WHERE CHARINDEX('COMPANY',TradestyleKey,0)>0  
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'CORP','') WHERE CHARINDEX('CORP',TradestyleKey,0)>0  
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'CORPORATION','') WHERE CHARINDEX('CORPORATION',TradestyleKey,0)>0  
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'PLC','') WHERE CHARINDEX('PLC',TradestyleKey,0)>0   
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'PUBLIC LIMITED COMPANY','') WHERE CHARINDEX('PUBLIC LIMITED COMPANY',TradestyleKey,0)>0   
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'INC','') WHERE CHARINDEX('INC',TradestyleKey,0)>0   
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'INCORPORATED','') WHERE CHARINDEX('INCORPORATED',TradestyleKey,0)>0   
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'LLP','') WHERE CHARINDEX('LLP',TradestyleKey,0)>0  
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'LIMITED LIABILITY PARTNERSHIP','') WHERE CHARINDEX('LIMITED LIABILITY PARTNERSHIP',TradestyleKey,0)>0  
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'LLC','') WHERE CHARINDEX('LLC',TradestyleKey,0)>0  
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'LIMITED LIABILITY COMPANY','') WHERE CHARINDEX('LIMITED LIABILITY COMPANY',TradestyleKey,0)>0  

		--replace common abbreviations- Tradestyle
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'SVC','') WHERE CHARINDEX('SVC',TradestyleKey,0)>0  
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'CTR','') WHERE CHARINDEX('CTR',TradestyleKey,0)>0   
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'MFG','') WHERE CHARINDEX('MFG',TradestyleKey,0)>0   
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'ASSOC','') WHERE CHARINDEX('ASSOC',TradestyleKey,0)>0   
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'INTL','') WHERE CHARINDEX('INTL',TradestyleKey,0)>0   
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'SUPLS','') WHERE CHARINDEX('SUPLS',TradestyleKey,0)>0   
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'ENR','') WHERE CHARINDEX('ENR',TradestyleKey,0)>0   
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'Assn','') WHERE CHARINDEX('Assn',TradestyleKey,0)>0
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'SERVICE','') WHERE CHARINDEX('SVC',TradestyleKey,0)>0  
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'CENTRE','') WHERE CHARINDEX('CTR',TradestyleKey,0)>0   
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'MANUFACTURING','') WHERE CHARINDEX('MFG',TradestyleKey,0)>0   
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'ASSOCIATION','') WHERE CHARINDEX('ASSOC',TradestyleKey,0)>0   
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'INTERNATIONAL','') WHERE CHARINDEX('INTL',TradestyleKey,0)>0   
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'SUPPLIES','') WHERE CHARINDEX('SUPLS',TradestyleKey,0)>0   
		update _DuplicateRecords set TradestyleKey = Control_strings.dbo.subReplaceAbbreviation(TradestyleKey, 'ENREGISTRE','') WHERE CHARINDEX('ENR',TradestyleKey,0)>0 

		--remove punctuation Tradestyle
		update _DuplicateRecords set TradestyleKey = replace(TradestyleKey,'.','')
		update _DuplicateRecords set TradestyleKey = replace(TradestyleKey,'&','AND')
		update _DuplicateRecords set TradestyleKey = replace(TradestyleKey,'-','')
		update _DuplicateRecords set TradestyleKey = replace(TradestyleKey,',','')
		update _DuplicateRecords set TradestyleKey = replace(TradestyleKey,char(39),'')
		update _DuplicateRecords set TradestyleKey = replace(TradestyleKey,'(','')
		update _DuplicateRecords set TradestyleKey = replace(TradestyleKey,')','')
		update _DuplicateRecords set TradestyleKey = replace(TradestyleKey,'/','')
		update _DuplicateRecords set TradestyleKey = replace(TradestyleKey,' ','')

		--remove common terms from address eg suite, unit, unite
		update _DuplicateRecords set addresskey = Control_strings.dbo.subReplaceAbbreviation(AddressKey, 'suite','') WHERE Addresskey like '% suite%'
		update _DuplicateRecords set addresskey = Control_strings.dbo.subReplaceAbbreviation(AddressKey, 'unit','') WHERE Addresskey like '% unit%'
		update _DuplicateRecords set addresskey = Control_strings.dbo.subReplaceAbbreviation(AddressKey, 'unite','') WHERE Addresskey like '% unite%'
		update _DuplicateRecords set addresskey = Control_strings.dbo.subReplaceAbbreviation(AddressKey, 'unité','') WHERE Addresskey like '% unité%'
		update _DuplicateRecords set addresskey = Control_strings.dbo.subReplaceAbbreviation(AddressKey, 'bureau','') WHERE Addresskey like '% bureau%'
		update _DuplicateRecords set addresskey = Control_strings.dbo.subReplaceAbbreviation(AddressKey, 'no','') WHERE Addresskey like '% no%'  



		 UPDATE _DuplicateRecords set Address1 = REPLACE(Address1,'|',';') Where charindex('|',Address1)>0
		 UPDATE _DuplicateRecords set Address2 = REPLACE(Address2,'|',';') Where charindex('|',Address2)>0
		 UPDATE _DuplicateRecords set AddressFull = REPLACE(AddressFull,'|',';') Where charindex('|',AddressFull)>0
		 UPDATE _DuplicateRecords set AddressKey = REPLACE(AddressKey,'|',';') Where charindex('|',AddressKey)>0
		 UPDATE _DuplicateRecords set BusinessName = REPLACE(BusinessName,'|',';') Where charindex('|',BusinessName)>0
		 UPDATE _DuplicateRecords set BusinessNameKey = REPLACE(BusinessNameKey,'|',';') Where charindex('|',BusinessNameKey)>0
		 UPDATE _DuplicateRecords set CC = REPLACE(CC,'|',';') Where charindex('|',CC)>0
		 UPDATE _DuplicateRecords set City = REPLACE(City,'|',';') Where charindex('|',City)>0
		 UPDATE _DuplicateRecords set CountryISO = REPLACE(CountryISO,'|',';') Where charindex('|',CountryISO)>0
		 UPDATE _DuplicateRecords set CreatedDate = REPLACE(CreatedDate,'|',';') Where charindex('|',CreatedDate)>0
		 UPDATE _DuplicateRecords set ExcludeReasonID = REPLACE(ExcludeReasonID,'|',';') Where charindex('|',ExcludeReasonID)>0
		 UPDATE _DuplicateRecords set FeedHistoryID = REPLACE(FeedHistoryID,'|',';') Where charindex('|',FeedHistoryID)>0
		 UPDATE _DuplicateRecords set IsDup = REPLACE(IsDup,'|',';') Where charindex('|',IsDup)>0
		 UPDATE _DuplicateRecords set NameElementID = REPLACE(NameElementID,'|',';') Where charindex('|',NameElementID)>0
		 UPDATE _DuplicateRecords set Postcode = REPLACE(Postcode,'|',';') Where charindex('|',Postcode)>0
		 UPDATE _DuplicateRecords set PostCodeKey = REPLACE(PostCodeKey,'|',';') Where charindex('|',PostCodeKey)>0
		 UPDATE _DuplicateRecords set Processed = REPLACE(Processed,'|',';') Where charindex('|',Processed)>0
		 UPDATE _DuplicateRecords set SIC = REPLACE(SIC,'|',';') Where charindex('|',SIC)>0
		 UPDATE _DuplicateRecords set SourceID = REPLACE(SourceID,'|',';') Where charindex('|',SourceID)>0
		 UPDATE _DuplicateRecords set StateCode = REPLACE(StateCode,'|',';') Where charindex('|',StateCode)>0
		 UPDATE _DuplicateRecords set SupplierID = REPLACE(SupplierID,'|',';') Where charindex('|',SupplierID)>0
		 UPDATE _DuplicateRecords set Tel = REPLACE(Tel,'|',';') Where charindex('|',Tel)>0
		 UPDATE _DuplicateRecords set TradeStyle = REPLACE(TradeStyle,'|',';') Where charindex('|',TradeStyle)>0
		 UPDATE _DuplicateRecords set TradestyleKey = REPLACE(TradestyleKey,'|',';') Where charindex('|',TradestyleKey)>0
		 UPDATE _DuplicateRecords set IDmask2 = REPLACE(IDmask2,'|',';') Where charindex('|',IDmask2)>0
		 UPDATE _DuplicateRecords set IDmask1 = REPLACE(IDmask1,'|',';') Where charindex('|',IDmask1)>0
		 UPDATE _DuplicateRecords set YearStarted = REPLACE(YearStarted,'|',';') Where charindex('|',YearStarted)>0

END

