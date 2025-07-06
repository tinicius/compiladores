program TestBreak;
var i: integer;
begin
i := 1;
while i <= 10 do
begin
  if i = 5 then break;
  writeln(i);
  i := i + 1;
end;
writeln("Saiu do loop");
end.