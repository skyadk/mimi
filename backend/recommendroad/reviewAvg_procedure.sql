DELIMITER $$
	DROP PROCEDURE IF EXISTS loopInsert$$
	CREATE PROCEDURE loopInsert() 
 
 BEGIN
  DECLARE i int DEFAULT 1;
  DECLARE avg double DEFAULT 0;
 
  WHILE i <= 460000 DO  /* count(sid) */
     
	SELECT avg(total_score) INTO avg FROM reviews  where sid = i group by sid;
     IF(avg) THEN
		UPDATE  stores SET  review_avg = avg WHERE sid = i ;
	 END IF;
     set i = i + 1;
     
     END WHILE;
 END$$
 DELIMITER ;
 
 call loopInsert();
 
 select * from stores;