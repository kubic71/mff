create function TotalPrice(@pID integer) returns numeric
as 
declare @ret numeric;


select sum(UnitPrice * Quantity)
    from Item where IID = @pIID;

return @ret;