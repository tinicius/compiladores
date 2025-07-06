program TestContinue;
var i: integer;
begin
i := 1;
while i <= 5 do
begin
  if i = 3 then 
  begin
    i := i + 1;
    continue;
  end;
  writeln(i);
  i := i + 1;
end;
end.