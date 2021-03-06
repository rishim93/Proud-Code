UPDATE _stage_ADDRESS
SET city = ltrim(rtrim(city)),
    FullAddress = ltrim(rtrim(fulladdress))
WHERE city IS NOT NULL
  UPDATE _stage_ADDRESS
  SET FullAddress3 = CASE
                         WHEN charindex('(', reverse(fulladdress2)) <> 0 THEN left(fulladdress2, len(fulladdress2)-charindex('(', reverse(fulladdress2))+1)
                         ELSE FullAddress2
                     END
  UPDATE _stage_ADDRESS
  SET FullAddress3 = RTRIM(LTRIM(FullAddress3))
  UPDATE _stage_ADDRESS
  SET FullAddress3 = Left(Fulladdress3, len(fulladdress3)-1) WHERE fulladdress3 LIKE '%.'
  UPDATE _stage_ADDRESS
  SET FullAddress3 = left(FullAddress3, len(FullAddress3)-charindex(' ', reverse(FullAddress3))) WHERE fulladdress3 LIKE ('% AB')
  OR FullAddress3 LIKE ('% BC')
  OR FullAddress3 LIKE ('% MB')
  OR FullAddress3 LIKE ('% MB')
  OR FullAddress3 LIKE ('% NB')
  OR FullAddress3 LIKE ('% NL')
  OR FullAddress3 LIKE ('% NS')
  OR FullAddress3 LIKE ('% NT')
  OR FullAddress3 LIKE ('% NU')
  OR FullAddress3 LIKE ('% ON')
  OR FullAddress3 LIKE ('% PE')
  OR FullAddress3 LIKE ('% QC')
  OR FullAddress3 LIKE ('% SK')
  OR FullAddress3 LIKE ('% YT')
  
  UPDATE _stage_ADDRESS
  SET FullAddress4 = CASE
                         WHEN patindex('%'+city+'%', fulladdress3)<>0 THEN replace(Fulladdress3, Substring(Fulladdress3, patindex('%'+city+'%', fulladdress3), len(CITY)), '')
                         ELSE FullAddress3
                     END 
                     
-- Get all cities for Corresponding postal codes (first 3 digits in a temp table), postal code not like  '_0%'

  SELECT distinct(city) AS city,
         left(postcode, 3) AS post3 INTO ##cities
FROM PostCodeCity --  Refernce Table 
WHERE left(Postcode, 3) IN
    (SELECT left(Postalcode, 3)
     FROM _stage_ADDRESS
     WHERE Province IS NULL
       AND PostalCode NOT LIKE '_0%')
       
       

-- Replace not found Cities from Fulladdress3 by filling cities using 1st 3 digits of postal code

  UPDATE _stage_ADDRESS
  SET City = c.city
  FROM _stage_ADDRESS a
  INNER JOIN ##cities c ON left(A.postalcode, 3) = c.post3 WHERE a.Province IS NULL
  AND a.City IS NULL
  UPDATE _stage_ADDRESS
  SET City = ltrim(rtrim(city)) WHERE Province IS NULL
  UPDATE _stage_ADDRESS
  SET FullAddress4 = CASE
                         WHEN patindex('%'+city+'%', fulladdress3)<>0
                              AND Province IS NULL THEN replace(Fulladdress3, Substring(Fulladdress3, patindex('%'+city+'%', fulladdress3), len(CITY)), '')
                         ELSE FULLADDRESS4
                     END
  UPDATE _stage_ADDRESS
  SET City = NULL WHERE Province IS NULL 
  
  
  -- get Parsed Addresses back into _stage

  UPDATE _stage
  SET Fulladdress4 = sa.Fulladdress4,
      PostalCode = sa.PostalCode,
      city = sa.city,
      Province = sa.Province
  FROM _stage_address sa
  LEFT JOIN _stage s ON sa.NEQ = s.NEQ TRUNCATE TABLE _stage_address
