program TestIf2;
var x, y: integer;
begin
x := 2;
if x > 10 then
writeln("Maior que 10");
else
readln(x);
if x>5 then
  writeln("Entre 6 e 10");
else
  writeln("Menor ou igual a 5");
end.